# AdBlock Filter Compiler

This repository contains a Python script designed to compile and optimize various blocklists, host files, and domain lists into a single, efficient AdBlock filter list. The script ensures that the resulting list is free of duplicates and redundant rules, providing a streamlined and effective ad-blocking experience.

## Key Features

- **Integration**: Combines multiple blocklists, host files, and domain lists into one cohesive AdBlock filter.
- **Optimization**: Identifies and removes duplicate entries and redundant rules to enhance filter efficiency.
- **Customization**: Allows users to specify custom blocklist sources through a `config.json` file.
- **Header Generation**: Automatically generates a header with detailed metadata, including the date, time, domain count, and statistics on duplicates and redundant rules removed.

## Default Filter Lists

By default, the script integrates the following filter lists:

- [hagezi/dns-blocklists (pro.txt)](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt)
- [quidsup/notrack-blocklists (trackers.hosts)](https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/trackers.hosts)
- [hBlock/blocklist (hosts_adblock.txt)](https://hblock.molinero.dev/hosts_adblock.txt)

You can customize the sources by modifying the `blocklist_urls` array in the `config.json` file.

## Getting Started

### Prerequisites

- Ensure you have Python 3.x installed on your system.
- Install the required Python package:
  ```bash
  pip install requests
  ```

### Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/adblock-filter-compiler.git
   cd adblock-filter-compiler
   ```
2. Create a `config.json` file and configure your blocklist URLs:
   ```json
   {
     "blocklist_urls": [
       "https://example.com/blocklist1.txt",
       "https://example.com/blocklist2.txt"
     ]
   }
   ```
3. Run the script to generate the filter list:
   ```bash
   python adblock_filter_compiler.py
   ```
   The script will output a `blocklist.txt` file containing the compiled filter list.

## Automated Updates

This repository leverages GitHub Actions to automate the filter compilation process. The workflow is scheduled to run daily, ensuring that the `blocklist.txt` file is updated with the latest changes.

## Contributing

Contributions are welcome! If you have any improvements, suggestions, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using the AdBlock Filter Compiler! If you have any questions or need further assistance, feel free to reach out.
