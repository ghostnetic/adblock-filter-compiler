import re
import requests
import concurrent.futures
from datetime import datetime, timezone
import json
import logging

# Enhanced regex for efficiency (more strict IP pattern, reduced backtracking)
domain_regex = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
    r"|(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"  # Domain
)

def is_valid_domain(domain):
    return bool(domain_regex.fullmatch(domain))  # Use fullmatch for stricter check

def parse_hosts_file(content):
    # Generator for lazy evaluation, potentially saving memory
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
            base_domain = '.'.join(domain.rsplit('.', 2)[-2:])  # Efficient base domain extraction
            if rule not in adblock_rules and base_domain not in base_domains:
                adblock_rules.add(rule)
                base_domains.add(base_domain)
            else:
                stats["duplicates" if rule in adblock_rules else "compressed"] += 1

    sorted_rules = sorted(adblock_rules)
    header = generate_header(len(sorted_rules), **stats)
    return '\n'.join([header, *sorted_rules]), stats  # No need for extra newline

def generate_header(domain_count, duplicates, compressed):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    return f"""# Title: Ghostnetic's Blocklist
# Description: Python script that generates adblock filters.
# Last Modified: {timestamp}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates}
# Domains Compressed: {compressed}
"""

def fetch_blocklist(url, session=None):
    """Fetch blocklist using optional session for potential reuse."""
    session = session or requests.Session()  # Create if not provided
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    with open('config.json') as f:
        config = json.load(f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Reuse session for all requests within the executor
        with requests.Session() as session:
            results = executor.map(lambda url: fetch_blocklist(url, session), config['blocklist_urls'])
    
    file_contents = filter(None, results)  # More concise filtering
    filter_content, stats = generate_filter(file_contents)

    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

    logging.info(f"Blocklist generated: {len(filter_content.splitlines())} lines, {stats['duplicates']} duplicates removed, {stats['compressed']} domains compressed")

if __name__ == "__main__":
    main()
