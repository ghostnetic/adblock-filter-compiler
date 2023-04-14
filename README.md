# AdBlock Filter Compiler

This repository offers a Python script that combines and processes various blocklists, host files, and domain lists to produce an AdBlock filter list. A sorted list of domains in AdBlock syntax format is produced after the script eliminates duplicates.

## Features

- Combines multiple blocklists, host files, and domain lists into a single AdBlock filter list
- Removes duplicate entries
- Generates a header with the date, domain count, and the number of duplicates removed

## Usage

1. Clone the repository or download the source code.
2. Add or remove blocklist URLs in the `blocklist_urls` list in the `adblock_filter_compiler.py` file.
3. Run the `adblock_filter_compiler.py` script. This will generate the `blocklist.txt` file with the combined filter list in AdBlock syntax format.

## Automated Updates

This repository uses GitHub Actions to automate the filter generation process. The workflow runs every day at 9 AM EST (2 PM UTC) and updates the `blocklist.txt` file if there are any changes.

## Dependencies

- Python 3.x
- requests

## Contributing

Feel free to open an issue or submit a pull request if you have any improvements or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
