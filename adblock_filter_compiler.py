import re
import requests
import concurrent.futures
from datetime import datetime, timedelta, timezone
import json
import logging
import cProfile
from functools import lru_cache

# Enhanced regex for efficiency (stricter IP, reduced backtracking)
domain_regex = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
    r"|(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"  # Domain
)

def is_valid_domain(domain):
    return bool(domain_regex.fullmatch(domain))

def parse_hosts_file(content):
    # Generator for lazy evaluation
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith(('#', '!')):
            yield line if line.startswith('||') and line.endswith('^') else f'||{line.split()[-1]}^'

def generate_filter(file_contents):
    adblock_rules = set()
    base_domains = set()
    stats = {"duplicates": 0, "compressed": 0}

    for content in file_contents:
        for rule in parse_hosts_file(content):
            domain = rule[2:-1]
            base_domain = '.'.join(domain.rsplit('.', 2)[-2:])
            if rule not in adblock_rules and base_domain not in base_domains:
                adblock_rules.add(rule)
                base_domains.add(base_domain)
            else:
                stats["duplicates" if rule in adblock_rules else "compressed"] += 1

    sorted_rules = sorted(adblock_rules)
    header = generate_header(len(sorted_rules), **stats)
    filter_content = '\n'.join([header, *sorted_rules])

    errors = validate_filter(filter_content)
    if errors:
        logging.warning(f"Filter validation issues found:\n{chr(10).join(errors)}")

    return filter_content, stats

def generate_header(domain_count, duplicates, compressed):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    return f"""# Title: Ghostnetic's Blocklist
# Description: Python script that generates adblock filters.
# Last Modified: {timestamp}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates}
# Domains Compressed: {compressed}
"""

@lru_cache(maxsize=128)
def fetch_blocklist(url, session=None, max_age=timedelta(hours=24)):
    """Fetch blocklist using optional session and caching."""
    now = datetime.now(timezone.utc)
    if url in fetch_blocklist.cache_info().hits:
        last_fetch_time, _ = fetch_blocklist.cache_info().hits[url]
        if now - last_fetch_time < max_age:
            logging.info(f"Using cached result for {url}")
            return fetch_blocklist.cache_get(url)

    session = session or requests.Session()
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        result = response.text
        fetch_blocklist.cache_set(url, result)
        return result
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")

def validate_filter(filter_content):
    """Basic validation for AdBlock filter syntax."""
    errors = []
    for line_num, line in enumerate(filter_content.splitlines(), start=1):
        if not (line.startswith(("||", "@@")) or line == "" or line.startswith("#")):
            errors.append(f"Line {line_num}: Invalid rule syntax: {line}")
    return errors
 
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    profiler = cProfile.Profile()
    profiler.enable()

    with open('config.json') as f:
        config = json.load(f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        with requests.Session() as session:
            results = executor.map(lambda url: fetch_blocklist(url, session), config['blocklist_urls'])

    file_contents = filter(None, results)
    filter_content, stats = generate_filter(file_contents)

    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

    logging.info(f"Blocklist generated: {len(filter_content.splitlines())} lines, {stats['duplicates']} duplicates removed, {stats['compressed']} domains compressed")

    profiler.disable()
    profiler.print_stats(sort="cumulative")

if __name__ == "__main__":
    main()
