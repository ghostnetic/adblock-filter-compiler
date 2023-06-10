# AdBlock Filter Compiler

This repository offers a Python script that combines and processes various blocklists, host files, and domain lists to produce an AdBlock filter list. A sorted list of domains in AdBlock syntax format is produced after the script eliminates duplicates and redundant rules.

## Features

- Combines multiple blocklists, host files, and domain lists into a single AdBlock filter list
- Removes duplicate entries
- Removes redundant rules that are covered by existing domain rules
- Generates a header with the date, time, domain count, and the number of duplicates and redundant rules removed
- Allows customization of blocklist sources through a configuration file

## Included Filter Lists

This project combines the following filter lists by default:

- [hagezi/dns-blocklists (multi.txt)](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt)
- [quidsup/notrack-blocklists (trackers.hosts)](https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts)
- [oisd/blocklist-big (big.oisd.nl)](https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt)
- [hBlock/blocklist (hosts_adblock.txt)](https://hblock.molinero.dev/hosts_adblock.txt)

You can easily add your own filter lists by creating a `config.json` file and updating the `blocklist_urls` array with the URLs of your custom filter lists.

## Usage

1. Clone the repository or download the source code.
2. Create a `config.json` file and add or remove blocklist URLs in the `blocklist_urls` array.
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
