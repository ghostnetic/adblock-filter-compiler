import requests
from datetime import datetime

def parse_hosts_file(content):
    lines = content.split('\n')
    adblock_rules = []

    for line in lines:
        line = line.strip()

        if line.startswith('#') or line.startswith('!') or line == '':
            continue

        if line.startswith('||') and line.endswith('^'):
            adblock_rules.append(line)
        else:
            parts = line.split()
            domain = parts[-1]
            rule = f'||{domain}^'
            adblock_rules.append(rule)

    return adblock_rules

def remove_redundant_rules(adblock_rules_set):
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
    adblock_rules_set = {rule for content in file_contents for rule in parse_hosts_file(content)}
    if compress:
        adblock_rules_set = remove_redundant_rules(adblock_rules_set)
    duplicates_removed = len(file_contents) * len(adblock_rules_set) - len(adblock_rules_set)

    sorted_rules = sorted(adblock_rules_set)
    header = generate_header(len(sorted_rules), duplicates_removed, len(adblock_rules_set))
    filter_content = '\n'.join([header, '', *sorted_rules])
    return filter_content, duplicates_removed

def check_for_redundant_rules(adblock_rules_set):
    redundant_rules = set()
    for rule in adblock_rules_set:
        if rule.startswith('||'):
            domain = rule[2:-1]
            for subdomain in [f'||{subdomain}^' for subdomain in domain.split('.')[1:]]:
                if subdomain in adblock_rules_set:
                    redundant_rules.add(subdomain)
    return redundant_rules

def generate_header(domain_count, duplicates_removed, compressed_domain_count):
    date = datetime.now().strftime('%Y-%m-%d')
    redundant_rules = check_for_redundant_rules(adblock_rules_set)
    return f"""# Title: AdBlock Filter Compiler
# Description: Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {date}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
# Compressed Domain Count: {compressed_domain_count}
# Redundant Rules: {len(redundant_rules)}
#==============================================================="""

def main():
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt',
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.txt',
    ]

    file_contents = []
    for url in blocklist_urls:
        response = requests.get(url)
        file_contents.append(response.text)

    filter_content, duplicates_removed = generate_filter(file_contents)

    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

if __name__ == "__main__":
    main()
