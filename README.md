# AdBlock Filter Compiler

This repository offers a Python script that combines and processes various blocklists, host files, and domain lists to produce an AdBlock filter list. A sorted list of domains in AdBlock syntax format is produced after the script eliminates duplicates.

## Features

- Combines multiple blocklists, host files, and domain lists into a single AdBlock filter list
- Removes duplicate entries
- Generates a header with the date, domain count, and the number of duplicates removed

## Included Filter Lists

This project combines the following filter lists by default:

- [hagezi/dns-blocklists (multi.txt)](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt)
- [quidsup/notrack-blocklists (trackers.hosts)](https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts)
- [oisd/blocklist-big (big.oisd.nl)](https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt)
- [hBlock/blocklist (hosts_adblock.txt)](https://hblock.molinero.dev/hosts_adblock.txt)

You can easily add your own filter lists by modifying the `adblock_filter_generator.py` script and updating the `blocklist_urls` list with the URLs of your custom filter lists.

## Usage

1. Clone the repository or download the source code.
2. Add or remove blocklist URLs in the `blocklist_urls` list in the `adblock_filter_compiler.py` file.
3. Run the `adblock_filter_compiler.py` script. This will generate the `blocklist.txt` file with the combined filter list in AdBlock syntax format.

## Automated Updates

This repository uses GitHub Actions to automate the filter generation process. The workflow runs every day and updates the `blocklist.txt` file if there are any changes.

## Dependencies

- Python 3.x
- requests

## Contributing

Feel free to open an issue or submit a pull request if you have any improvements or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
