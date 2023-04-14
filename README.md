# AdBlock Filter Generator

AdBlock Filter Generator is a Python-based script that generates AdBlock syntax filters by combining and processing multiple blocklists, host files, and domain lists. The script fetches and parses blocklists and whitelists from provided URLs, removes redundant entries, and creates two output files: `blocklist.txt` and `whitelist.txt`.

## Prerequisites

- Python 3.x
- `requests` library

## Setup

1. Clone the repository:

```

git clone <https://github.com/><your-username>/adblock-filter-generator.git

```

2. Navigate to the repository directory:

```

cd adblock-filter-generator

```

3. Install the required dependencies:

```

pip install -r requirements.txt

````

## Configuration

In the `adblock_filter_generator.py` script, add the URLs for the blocklists and whitelists you want to use to the `blocklist_urls` and `whitelist_urls` lists.

Example:

```python
blocklist_urls = [
 "https://example.com/blocklist.txt",
 "https://anotherexample.com/hosts.txt"
]

whitelist_urls = [
 "https://example.com/whitelist.txt"
]
````

## Usage

Run the script with the following command:

```
python adblock_filter_generator.py
```

The script will fetch and process the lists, remove redundant entries, and save the results to "blocklist.txt" and "whitelist.txt".

## Scheduling

To refresh the lists every 24 hours, you can schedule the script to run daily using a task scheduler or cron job, depending on your operating system.

### Windows:

Use Windows Task Scheduler to create a task that runs the script daily.

### macOS / Linux:

Use `cron` to create a daily job that runs the script. Add an entry similar to the following in your crontab (replace `/path/to/script` with the actual path to the script):

```
0 0 * * * /usr/bin/python /path/to/script/adblock_filter_generator.py
```

This will run the script every day at midnight.
