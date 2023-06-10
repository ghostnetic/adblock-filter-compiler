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
    """Generates filter content from file_contents by eliminating duplicates and redundant rules."""
    duplicates_removed = 0
    redundant_rules_removed = 0
    adblock_rules_set = set()
    base_domain_set = set()

    for content in file_contents:
        adblock_rules = parse_hosts_file(content)
        for rule in adblock_rules:
            domain = rule[2:-1]  # Remove '||' and '^'
            base_domain = '.'.join(domain.split('.')[-2:])  # Get the base domain (last two parts)
            if rule not in adblock_rules_set:
                # Check for redundant rules
                if base_domain not in base_domain_set:
                    adblock_rules_set.add(rule)
                    base_domain_set.add(base_domain)
                else:
                    redundant_rules_removed += 1
            else:
                duplicates_removed += 1

    sorted_rules = sorted(list(adblock_rules_set))
    header = generate_header(len(sorted_rules), duplicates_removed, redundant_rules_removed)
    filter_content = '\n'.join([header, '', *sorted_rules])  # Add an empty line after the header
    return filter_content, duplicates_removed, redundant_rules_removed

def generate_header(domain_count, duplicates_removed, redundant_rules_removed):
    """Generates header with specific domain count, removed duplicates, and compressed domains information."""
    date = datetime.now().strftime('%Y-%m-%d')
    return f"""# Title: AdBlock Filter Compiler
# Description: A Python script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {date}
# Domain Count: {domain_count}
# Duplicates Removed: {duplicates_removed}
# Domains Compressed: {redundant_rules_removed}
#=================================================================="""

def get_parent_domains(domain):
    """Generates the immediate parent domain of a given domain."""
    parts = domain.split('.')
    if len(parts) > 2:
        return ['.'.join(parts[i:]) for i in range(1, 2)]
    else:
        return []

def main():
    """Main function to fetch blocklists and generate a combined filter."""
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://adguardteam.github.io/HostsRegistry/assets/filter_27.txt',
        'https://hblock.molinero.dev/hosts_adblock.txt',
    ]

    file_contents = []
    for url in blocklist_urls:
        with requests.get(url) as response:
            file_contents.append(response.text)

    filter_content, duplicates_removed, redundant_rules_removed = generate_filter(file_contents)

    # Write the filter content to a file
    with open('blocklist.txt', 'w') as f:
        f.write(filter_content)

if __name__ == "__main__":
    main()

