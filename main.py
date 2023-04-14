import requests
from datetime import datetime

def get_list_from_url(url):
    response = requests.get(url)
    return response.text.splitlines()

def parse_adblock_filter(lines):
    domains = []
    for line in lines:
        if line.startswith('||') and '^' in line:
            domain = line.split('^')[0][2:]
            domains.append(domain)
    return domains

def parse_hosts_file(lines):
    domains = []
    for line in lines:
        if not line.startswith('#'):
            parts = line.split()
            if len(parts) == 2:
                ip, domain = parts
                if ip in ['0.0.0.0', '127.0.0.1']:
                    domains.append(domain)
    return domains

def parse_domain_list(lines):
    domains = []
    for line in lines:
        if not line.startswith('#'):
            domains.append(line)
    return domains

def get_domains_from_url(url):
    lines = get_list_from_url(url)
    if any(line.startswith('||') for line in lines):
        return parse_adblock_filter(lines)
    elif any(line.startswith(('0.0.0.0', '127.0.0.1')) for line in lines):
        return parse_hosts_file(lines)
    else:
        return parse_domain_list(lines)

def generate_filter(blocklist_urls, whitelist_urls):
    blocklist_domains = []
    for url in blocklist_urls:
        blocklist_domains.extend(get_domains_from_url(url))

    whitelist_domains = []
    for url in whitelist_urls:
        whitelist_domains.extend(get_domains_from_url(url))

    blocklist_domains = list(set(blocklist_domains) - set(whitelist_domains))
    blocklist_domains.sort()

    duplicates_removed = len(blocklist_domains) - len(set(blocklist_domains))
    
    with open('blocklist.txt', 'w') as f:
        f.write(f'# Title: AdBlock Filter Generator\n')
        f.write(f'# Description: Chrome Extension to generate adblock syntax filter from multiple host files and blocklists\n')
        f.write(f'# Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'# Domain Count: {len(blocklist_domains)}\n')
        f.write(f'# Duplicates Removed: {duplicates_removed}\n')
        f.write(f'#===============================================================\n')
        for domain in blocklist_domains:
            f.write(f'||{domain}^\n')

    with open('whitelist.txt', 'w') as f:
        for domain in whitelist_domains:
            f.write(f'{domain}\n')

blocklist_urls = [
    https://hblock.molinero.dev/hosts_adblock.txt
    https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
    https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts
    https://blokada.org/blocklists/ddgtrackerradar/standard/hosts.txt
    
]

whitelist_urls = [
    https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist.txt
    https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist-referral.txt
    https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist-urlshortener.txt
]

generate_filter(blocklist_urls, whitelist_urls)