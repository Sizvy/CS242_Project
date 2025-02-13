import os
import json
import re
from collections import defaultdict

### define folder path
folder_path = "/home/cs242/group_6"

def normalize_text(text):
    """removes special characters and converts to lowercase for better comparison"""
    return re.sub(r'\W+', '', text.lower()) if text else ""

def count_duplicates(folder_path):
    """reads all json files and counts duplicate entries"""
    all_entries = []
    title_dict = defaultdict(list)  ### to track duplicates

    ### read all json files
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    all_entries.extend(data)
                except json.JSONDecodeError:
                    print(f"❌ error reading {file_name} (invalid json format)")

    total_entries = len(all_entries)
    unique_entries = 0
    duplicate_count = 0

    ### check for duplicates using normalized title
    seen_titles = set()
    for entry in all_entries:
        title = normalize_text(entry.get("title", ""))
        if title in seen_titles:
            duplicate_count += 1
        else:
            seen_titles.add(title)
            unique_entries += 1

    ### calculate percentage of duplicates
    duplicate_percentage = (duplicate_count / total_entries) * 100 if total_entries > 0 else 0
    removable_entries = duplicate_count

    ### print results
    print("\n📊 Duplicate Analysis Results:")
    print(f"🔹 Total Entries: {total_entries}")
    print(f"🔹 Unique Entries: {unique_entries}")
    print(f"🔹 Duplicate Entries: {duplicate_count}")
    print(f"🔹 Duplicate Percentage: {duplicate_percentage:.2f}%")
    print(f"🔹 Entries to be Removed (if deduplication is applied): {removable_entries}\n")

if __name__ == "__main__":
    count_duplicates(folder_path)
