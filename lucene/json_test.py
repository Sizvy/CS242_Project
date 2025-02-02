import os
import json

# Define the folder path
folder_path = "/home/cs242/group_6"

# List all JSON files in the folder
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Initialize a flag to track validity
all_valid = True

# Check each JSON file
for file in json_files:
    file_path = os.path.join(folder_path, file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)  # Try loading the JSON file
        print(f"{file}: ✅ Valid JSON")
    except json.JSONDecodeError as e:
        print(f"{file}: ❌ Invalid JSON - {e}")
        all_valid = False
    except Exception as e:
        print(f"{file}: ❌ Error reading file - {e}")
        all_valid = False

# Final result
if all_valid:
    print("\nAll JSON files are valid ✅")
else:
    print("\nSome JSON files are invalid ❌")
