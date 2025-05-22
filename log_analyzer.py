# ----------------------------------------
# SYSTEM LOG ANALYZER AUTOMATION
# ----------------------------------------
# This script automates fetching, filtering, and saving Windows Event Logs.
# It uses `wevtutil` to fetch the latest system logs, filters based on keywords and
# optionally a date, highlights matches in the console, and appends results to a combined file.

import subprocess
import os
from datetime import datetime
import sys
import re
import argparse

# Try to import colorama for colored console output; if not installed, use dummy no-op colors
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class DummyColor:
        RESET_ALL = ''
        RED = ''
        GREEN = ''
        YELLOW = ''
        BRIGHT = ''
    Fore = DummyColor()
    Style = DummyColor()

# Constants for log file names
LOG_FILE = "system_log.txt"            # raw logs fetched by wevtutil
DEFAULT_KEYWORDS = [                     # default list of keywords to search in logs
    'error', 'fail', 'critical', 'warning',
    'unauthorized', 'denied', 'sudo', 'permission',
    'crash', 'restart', 'start', 'stop', 'reload',
    'timeout', 'unreachable', 'connection',
    'disk', 'cpu', 'memory', 'swap', 'space',
    'not found', 'exception', 'terminated', 'directory'
]
COMBINED_FILE = "filtered_logs_combined.txt"  # file to append filtered results

# ----------------------------------------
# Display tool usage information in the console
# ----------------------------------------
def info():
    width = 60
    heading = "System Log Analyzer & Filter Tool"
             
    # Print a centered, colored heading
    print("\n" + Fore.RED + Style.BRIGHT + heading.center(width) + Style.RESET_ALL + "\n")
    help_text = f"""
Usage:
- If no keywords are provided, the script uses DEFAULT_KEYWORDS.
- Provide --keywords to override (comma-separated list).
- Provide --date to filter logs only from that day (format YYYY-MM-DD).
- Results are appended to {COMBINED_FILE} with timestamps and separators.
"""
    print(Fore.CYAN + help_text + Style.RESET_ALL)

# ----------------------------------------
# Fetch the latest 100 system logs via wevtutil and save to LOG_FILE
# ----------------------------------------
def get_logs():
    print("\n" + "-"*30)
    print("......Fetching system logs......")
    print("\n" + "-"*30)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        subprocess.run(
            ["wevtutil", "qe", "System", "/c:100", "/f:text"],
            stdout=f, text=True
        )
    print(f"Logs saved to - {LOG_FILE}")

# ----------------------------------------
# Read LOG_FILE, optionally filter by date, and collect entries containing any keyword
# Returns a list of log blocks (each block is multiple lines) and total log count
# ----------------------------------------
def filter_logs(keywords, date_filter=None):
    filtered_lines = []
    total_logs = 0

    if not os.path.exists(LOG_FILE):
        print(f"{Fore.RED}Log file not found! Please fetch the logs first.{Style.RESET_ALL}")
        return filtered_lines, total_logs

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        skip_section = False

        for i, line in enumerate(lines):
            # Count non-empty lines for total_logs
            if line.strip():
                total_logs += 1

            # If a date filter is provided, look for 'Date:' lines and parse
            if date_filter and line.lower().startswith("date:"):
                try:
                    log_date_str = line.strip().split("Date:")[1].strip()
                    log_date = datetime.strptime(
                        log_date_str, "%m/%d/%Y %I:%M:%S %p"
                    ).date()
                except ValueError:
                    continue  # skip lines that fail to parse
                skip_section = (log_date != date_filter)

            # Skip lines until next date section if filtering out
            if skip_section:
                continue

            # If any keyword appears in this line, collect the full log entry
            if any(keyword.lower() in line.lower() for keyword in keywords):
                # Backtrack to the start of this log block (empty line delimiter)
                start_index = i
                while start_index > 0 and lines[start_index - 1].strip() != "":
                    start_index -= 1

                # Collect all lines until the next blank line
                log_block = []
                while start_index < len(lines) and lines[start_index].strip() != "":
                    log_block.append(lines[start_index])
                    start_index += 1

                # Add an empty line after each block for readability
                filtered_lines.extend(log_block + ["\n"])

    return filtered_lines, total_logs

# ----------------------------------------
# Highlight occurrences of keywords in a text line using colored output
# ----------------------------------------
def highlight_keywords(text, keywords):
    pattern = re.compile(r'(' + '|'.join(re.escape(k) for k in keywords) + r')', re.IGNORECASE)
    return pattern.sub(lambda m: f"{Fore.RED}{m.group(0)}{Style.RESET_ALL}", text)

# ----------------------------------------
# Append filtered lines to COMBINED_FILE with a timestamp and keyword header
# ----------------------------------------
def append_filtered_logs(filtered, keywords):
    with open(COMBINED_FILE, "a", encoding="utf-8") as f:
        run_header = f" Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
        keywords_line = f" Keywords: {', '.join(keywords)} "
        separator_line = "=" * 80

        # Write header and separators
        f.write("\n" + separator_line + "\n")
        f.write(run_header.center(len(separator_line)) + "\n")
        f.write(keywords_line.center(len(separator_line)) + "\n")
        f.write(separator_line + "\n\n")
        f.write("[ ......NEW LOG ENTRIES...... ]\n\n")

        # Write each filtered block
        for line in filtered:
            f.write(line)

        f.write("\n" + "="*100 + "\n")
        f.write("[ End of log entries — All records processed. ✅ ]\n")
        f.write("="*100 + "\n\n\n")

    print(f"Filtered logs appended to: {COMBINED_FILE}")

# ----------------------------------------
# Main entry point: parse args, run tasks, and output results
# ----------------------------------------
def main():
    parser = argparse.ArgumentParser(description="System Log Analyzer")
    parser.add_argument(
        "--keywords", type=str,
        help="Comma-separated keywords to search for (optional)"
    )
    parser.add_argument(
        "--date", type=str,
        help="Date to filter logs in YYYY-MM-DD format (optional)"
    )

    args = parser.parse_args()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log the run timestamp to the combined file
    print("Script run at:", timestamp)
    with open(COMBINED_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n[Script run at:] {timestamp}\n")

    # Display usage info
    info()

    # Determine keywords: user-specified or defaults
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else DEFAULT_KEYWORDS

    # Determine date filter, if provided
    if args.date:
        try:
            date_filter = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"{Fore.RED}Invalid date format! Expected YYYY-MM-DD.{Style.RESET_ALL}")
            sys.exit(1)
    else:
        date_filter = None

    # Fetch, filter, and display logs
    get_logs()
    filtered, total_logs = filter_logs(keywords, date_filter)

    # Print summary to console
    print("\n" + "="*40)
    print(f"Total logs scanned: {total_logs}")
    print(f"Total matches found: {len(filtered)}")
    print("="*40 + "\n")

    # Display and save filtered results
    if filtered:
        for line in filtered:
            print(highlight_keywords(line, keywords), end='')
    else:
        print(f"{Fore.YELLOW}No matching logs found. Try using more general terms.{Style.RESET_ALL}")

    append_filtered_logs(filtered, keywords)

if __name__ == "__main__":
    main()
