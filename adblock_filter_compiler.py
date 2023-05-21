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

def generate_filter(blocklist_contents, whitelist_urls):
    duplicates_removed = 0
    adblock_rules_set = set()

    for content in blocklist_contents:
        adblock_rules = parse_hosts_file(content)
        for rule in adblock_rules:
            if rule not in adblock_rules_set:
                adblock_rules_set.add(rule)
            else:
                duplicates_removed += 1

    sorted_rules = sorted(list(adblock_rules_set))
    header = generate_header(len(sorted_rules), duplicates_removed)
    filter_content = '\n'.join([header, '', *sorted_rules])  # Added empty line after the header

    whitelist_rules = []
    for url in whitelist_urls:
        with requests.get(url) as response:
            whitelist_content = response.text
            whitelist_rules.extend(whitelist_content.splitlines())

    whitelist_header = generate_whitelist_header(len(whitelist_rules))
    whitelist_content = '\n'.join([whitelist_header, '', *whitelist_rules])

    return filter_content, duplicates_removed, whitelist_content

def generate_header(domain_count, duplicates_removed):
    return f"""# Title: AdBlock Filter Compiler
# Description: Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {datetime.now().strftime('%Y-%m-%d')}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
#==============================================================="""

def generate_whitelist_header(domain_count):
    return f"""# Title: AdBlock Whitelist Compiler
# Description: List of whitelisted domains for AdBlock filters.
# Created: {datetime.now().strftime('%Y-%m-%d')}
# Domain Count: {domain_count}
#==============================================================="""

def main():
    blocklist_urls = [
        # Hagezi Normal
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        # Notrack
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        # AdGuard
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt',
    ]

    whitelist_urls = [
        'https://raw.githubusercontent.com/AhaDNS/Aha.Dns.Domains/master/Domains/whitelist.txt',
        # anudeep Whitelist
        'https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt',
    ]

    blocklist_contents = []
    for url in blocklist_urls:
        with requests.get(url) as response:
            blocklist_contents.append(response.text)

    filter_content, duplicates_removed, whitelist_content = generate_filter(blocklist_contents, whitelist_urls)

    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

    with open('whitelist.txt', 'w') as f:
        f.write(whitelist_content)

if __name__ == "__main__":
    main()
