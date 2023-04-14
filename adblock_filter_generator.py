import requests
import os
from datetime import datetime

def fetch_file(url):
    response = requests.get(url)
    return response.text.splitlines()

def process_list(file_lines, is_whitelist=False):
    processed_list = []
    for line in file_lines:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        if is_whitelist:
            line = '@@||' + line + '^'
        else:
            if line.startswith('127.0.0.1 ') or line.startswith('0.0.0.0 '):
                line = '||' + line[10:] + '^'
            else:
                line = '||' + line + '^'
        processed_list.append(line)
    return processed_list

def main():
    blocklist_urls = [
        'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt',
        'https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts',
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt',
        'https://adguardteam.github.io/HostlistsRegistry/assets/filter_24.txt'
    ]

    whitelist_urls = [
        'https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist.txt',
        'https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist-urlshortener.txt',
        'https://github.com/hagezi/dns-blocklists/raw/main/adblock/whitelist-referral.txt'
    ]

    blocklist = []
    for url in blocklist_urls:
        file_lines = fetch_file(url)
        blocklist.extend(process_list(file_lines))

    whitelist = []
    for url in whitelist_urls:
        file_lines = fetch_file(url)
        whitelist.extend(process_list(file_lines, is_whitelist=True))

    blocklist = sorted(list(set(blocklist) - set(whitelist)))
    whitelist = sorted(list(set(whitelist)))

    duplicates_removed = len(blocklist) - len(set(blocklist))

    header = f"""# Title: AdBlock Filter Generator
# Description: Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists.
# Created: {datetime.now().strftime('%Y-%m-%d')}
# Domain Count: {len(blocklist)}
# Duplicates Removed: {duplicates_removed}
#===============================================================""".strip()

    with open('blocklist.txt', 'w') as f:
        f.write(header + '\n\n')
        for line in blocklist:
            f.write(line + '\n')

    with open('whitelist.txt', 'w') as f:
        f.write(header + '\n\n')
        for line in whitelist:
            f.write(line + '\n')

if __name__ == "__main__":
    main()
