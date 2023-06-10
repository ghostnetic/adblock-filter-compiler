import requests
from datetime import datetime

def parse_hosts_file(content):
    """Parses a host file content into AdBlock rules."""
    lines = content.split('\n')
    adblock_rules = []

    for line in lines:
        line = line.strip()

        # Ignore comments and empty lines
        if line.startswith('#') or line.startswith('!') or line == '':
            continue

        # Check if line follows AdBlock syntax, else create new rule
        if line.startswith('||') and line.endswith('^'):
            adblock_rules.append(line)
        else:
            parts = line.split()
            domain = parts[-1]
            rule = f'||{domain}^'
            adblock_rules.append(rule)

    return adblock_rules

def generate_filter(file_contents):
    """Generates filter content from file_contents by eliminating duplicates."""
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
    filter_content = '\n'.join([header, '', *sorted_rules])  # Add an empty line after the header
    return filter_content, duplicates_removed

def generate_header(domain_count, duplicates_removed):
    """Generates header with specific domain count and removed duplicates information."""
    date = datetime.now().strftime('%Y-%m-%d')
    return f"""# Title: AdBlock Filter Compiler
# Description: A Python script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {date}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
#==============================================================="""

def main():
    """Main function to fetch blocklists and generate a combined filter."""
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt',
        'https://hblock.molinero.dev/hosts_adblock.txt',
    ]

    file_contents = []
    for url in blocklist_urls:
        with requests.get(url) as response:
            file_contents.append(response.text)

    filter_content, duplicates_removed = generate_filter(file_contents)

    # Write the filter content to a file
    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

if __name__ == "__main__":
    main()
