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

def generate_filter(file_contents):
    duplicates_removed = 0
    adblock_rules_set = set()

    for content in file_contents:
        adblock_rules = parse_hosts_file(content)
        for rule in adblock_rules:
            if rule not in adblock_rules_set:
                adblock_rules_set.add(rule)
            else:
                duplicates_removed += 1

    sorted_rules = sorted(list(adblock_rules_set))
    header = generate_header(len(sorted_rules), duplicates_removed)
    filter_content = '\n'.join([header, '', *sorted_rules]) # Added empty line after the header
    return filter_content, duplicates_removed

def generate_header(domain_count, duplicates_removed):
    date = datetime.now().strftime('%Y-%m-%d')
    return f"""# Title: AdBlock Filter Compiler
# Description: Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {date}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
#==============================================================="""

def main():
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://hblock.molinero.dev/hosts_adblock.txt',
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
