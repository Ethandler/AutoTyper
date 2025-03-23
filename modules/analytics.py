"""
modules/analytics.py
Track runs in a CSV, analyze WPM history, etc.
"""

import csv
import os
import time

LOG_DIR = "data/logs"
LOG_FILE = "typing_stats.csv"

def log_run(wpm, mistakes, timestamp=None):
    """
    Log a completed run to CSV with WPM, mistakes, and a timestamp.
    """
    if not timestamp:
        timestamp = time.time()

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_path = os.path.join(LOG_DIR, LOG_FILE)
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "WPM", "Mistakes"])
        writer.writerow([
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
            wpm,
            mistakes
        ])

def load_history():
    """
    Return a list of past runs from the CSV for further analysis or plotting.
    """
    file_path = os.path.join(LOG_DIR, LOG_FILE)
    if not os.path.isfile(file_path):
        return []

    data = []
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
