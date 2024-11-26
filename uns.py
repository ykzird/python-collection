import os
import json
from datetime import datetime
import sqlite3

def find_files_for_index():
    folder_path = "/home/jkamping/uns/storage"

    found_files = [file for file in os.listdir(folder_path)]
    return found_files

#find_files_for_index()

def create_files():
    folder_path = "/home/jkamping/uns/storage"

    for i in range(10):
        with open(f"{folder_path}/file{i}.txt", "w") as f:
            f.write(f"File {i}")    

#create_files()
def create_file_metadata():
    folder_path = "/home/jkamping/uns/storage"

    # Get the list of files using the helper function
    files = find_files_for_index()

    # Collect metadata for all files
    all_metadata = []

    for file in files:
        file_metadata = {
            "file_name": file,
            "size_in_bytes": os.path.getsize(f"{folder_path}/{file}"),
            "type": os.path.splitext(file)[1],
            "location": f"{folder_path}/{file}",
            "modified_time": datetime.fromtimestamp(
                os.path.getmtime(f"{folder_path}/{file}")
            ).isoformat(),
        }
        all_metadata.append(file_metadata)

    # Write all metadata to a single JSON file
    metadata_file_path = f"{folder_path}/all_metadata.json"
    with open(metadata_file_path, "w") as f:
        json.dump(all_metadata, f, indent=4)

# Call the function to create a single metadata file
create_file_metadata()

def import_metadata_to_db():
    metadata_file_path = "/home/jkamping/uns/storage/all_metadata.json"

    with open(metadata_file_path, "r") as f:
        metadata = json.load(f)

    conn = sqlite3.connect("/home/jkamping/uns/uns.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS files (file_name TEXT, size_in_bytes INTEGER, type TEXT, location TEXT, modified_time TEXT)"
    )

    for item in metadata:
        cursor.execute(
            "INSERT INTO files (file_name, size_in_bytes, type, location, modified_time) VALUES (?, ?, ?, ?, ?)",
            (
                item["file_name"],
                item["size_in_bytes"],
                item["type"],
                item["location"],
                item["modified_time"],
            ),
        )

    conn.commit()
    conn.close()

import_metadata_to_db()