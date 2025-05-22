                                                      ##🔍 System Log Analyzer

Have you ever found yourself buried in system log files, struggling to spot errors, warnings, or unusual activity? I certainly did—and that’s exactly why I created System Log Analyzer.

This project was born out of the need to quickly filter and understand system log files without having to manually scroll through endless lines of data. Whether you're a system administrator, developer, or just someone trying to troubleshoot an issue, this tool can help you get right to the point—clearly and efficiently.

> “Stop drowning in system logs—let the analyzer surface the insights you need!”

A Python & Batch-powered command-line utility that fetches, filters, highlights, and archives Windows System Event Logs for rapid troubleshooting, proactive monitoring, and forensic analysis. Ideal for sysadmins, DevOps engineers, security analysts, and power users who want instant visibility into system health.

---

## 📖 Table of Contents

1. 🚀 Why This Exists  
2. 🛠️ Tech Stack  
3. ✨ Key Features  
4. 📁 Project Structure  
5. 📦 Use Case Scenarios  
6. 🧠 How It Works  
7. 🏃‍♂️ Usage Guide  
8. 📷 Sample Output  
9. ❓ FAQ  
10. 🧪 Basic Test Cases  
11. 🙏 Acknowledgments

---

## 🚀 Why This Exists

- **Speed Up Troubleshooting**  
  Manually poring over Event Viewer entries is tedious. This tool automates the fetch→filter→highlight cycle so you spend seconds, not hours, finding critical events.  

- **Stay Ahead of Issues**  
  Automatically archive each scan’s results with timestamps—build trend reports or audit trails without extra effort.  

- **Shareable Reports**  
  Consolidated text outputs make it easy to hand off findings to teammates or include in incident postmortems.

---

## 🛠️ Tech Stack

Component             | Purpose  
---------------------|------------------------------------------------------------  
🐍 Python 3.x         | Core scripting—text parsing, date handling, file I/O.  
🔧 wevtutil           | Windows native CLI to export Event Viewer logs in text form.  
🎨 colorama           | Color-coded console output on Windows for instant visual cues.  
📝 Batch File (.bat)  | One-click run without typing commands.  
📄 Markdown (.md)     | Rich, readable documentation format.  
⚙️ Git & GitHub        | Version control, collaboration, and hosting.  

---

## ✨ Key Features

- Automated Log Retrieval (`wevtutil /c:100`)
- Keyword-Based Filtering (default: error, warning, failed)
- Color-Coded Highlights (using colorama)
- Date-Specific Scans (`--date YYYY-MM-DD`)
- Persistent Archiving to `filtered_logs_combined.txt`
- Double-click Batch Automation with `run_analyzer.bat`

---

## 📁 Project Structure

system-log-analyzer/  
│  
├── log_analyzer.py              → Python script (fetch, filter, highlight, archive)  
├── run_analyzer.bat             → Windows batch file for one-click execution  
├── requirements.txt             → External dependencies (e.g., colorama)   
├── README.md                    → This documentation  
└── sample_output/               → Example outputs  
    └── filtered_logs_example.txt → Sample filtered log results

---

## 📦 Use Case Scenarios

- 🧰 **System Admins** – Quickly extract recent error/warning events after user complaints.
- 🔐 **Security Analysts** – Identify failed login attempts, service shutdowns, or critical crashes.
- 🧪 **QA/Testers** – Check if application installs triggered any system errors.
- 📊 **Report Builders** – Include filtered log results in automated monitoring dashboards.

---

## 🧠 How It Works

1. Uses `wevtutil` to export system logs.
2. Filters logs based on keywords and/or date.
3. Color-codes matches using `colorama`.
4. Appends results to a consolidated `.txt` log with timestamps.
5. Can be triggered via CLI or batch file.

---

## 🏃‍♂️ Usage Guide

Run with Python:  
```bash
python log_analyzer.py --keywords error,warning --date 2025-05-22
```

Or double-click:  
```bash
run_analyzer.bat
```
---

## 📷 Sample Output

================================================================================  
                   Run at: 2025-05-22 14:30:05                     
                  Keywords: error, warning, critical                 
================================================================================  

Date: 05/22/2025 02:29:45 PM  
Source: Service Control Manager  
Event ID: 7009  
Type: Error  
Message: The service XYZ failed to start due to a timeout...  

================================================================================  
[ End of log entries — All records processed. ✅ ]  
================================================================================  

---

## ❓ FAQ

**Q: Can I scan other logs like Application or Security?**  
A: Yes! Just replace `System` with `Application` or `Security` in the `wevtutil` command inside the script.

**Q: What’s the default number of logs scanned?**  
A: 100 entries by default. Modify `/c:100` in `log_analyzer.py` if needed.

**Q: Will this work on Linux or macOS?**  
A: No. This is designed specifically for Windows using native `wevtutil`.

---

## 🧪 Basic Test Cases

Test                | Expected Result  
-------------------|------------------------  
Run without args    | Uses default keywords  
--date only         | Filters logs from that date  
Invalid date format | Error message shown  
No matches found    | “No matching logs found” message  

---

## 🙏 Acknowledgments

- Built with Python and wevtutil  
- Thanks to colorama for terminal color output  
- Inspired by daily sysadmin struggles!

---

👋 Thanks for checking out System Log Analyzer! Feel free to ⭐ the repo and share your feedback!
