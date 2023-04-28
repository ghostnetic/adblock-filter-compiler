import concurrent.futures
import requests
from datetime import datetime


def parse_hosts_file(content):
    adblock_rules = (line.strip() for line in content.split('\n')
                     if not (line.startswith('#') or line.startswith('!') or line == ''))

    return set(rule for rule in adblock_rules if rule.startswith('||') and rule.endswith('^')
               or (parts := rule.split()) and (domain := parts[-1]) and f'||{domain}^')


def compress_rules(adblock_rules_set):
    compressed_rules = set()
    excluded_domains = set()

    for rule in adblock_rules_set:
        if rule.startswith('||'):
            domain = rule[2:-1]
            if not any(d for d in excluded_domains if domain.endswith(d)):
                compressed_rules.add(rule)
                excluded_domains.add(domain)
        else:
            compressed_rules.add(rule)

    return compressed_rules


def generate_filter(file_contents, compress=True):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        adblock_rules_set = set()
        for adblock_rules in executor.map(parse_hosts_file, file_contents):
            adblock_rules_set.update(adblock_rules)

    if compress:
        adblock_rules_set = compress_rules(adblock_rules_set)

    duplicates_removed = len(file_contents) * len(adblock_rules_set) - len(adblock_rules_set)
    sorted_rules = sorted(adblock_rules_set)

    header = generate_header(len(sorted_rules), duplicates_removed)
    filter_content = '\n'.join([header, '', *sorted_rules])

    return filter_content, duplicates_removed


def generate_header(domain_count, duplicates_removed, compressed_count=None):
    date = datetime.now().strftime('%Y-%m-%d')
    header = f"""# Title: AdBlock Filter Compiler
# Description: Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {date}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
#"""
    if compressed_count is not None:
        header += f"Domains Compressed: {compressed_count}\n#"

    header += "===============================================================\n"

    return header


def main():
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt',
    ]

    file_contents = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for url in blocklist_urls]
        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            file_contents.append(response.text)

    filter_content, duplicates_removed = generate_filter(file_contents)

    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)


if __name__ == "__main__":
    main()
