import os
import shutil
import argparse
from datetime import datetime, timedelta

def backup_recent_files(source_dirs, extensions, backup_root):

    three_days_ago = datetime.now() - timedelta(days=3)

    backup_dir = os.path.join(backup_root, f"copy-{datetime.now().strftime('%Y-%m-%d')}")
    os.makedirs(backup_dir, exist_ok=True)

    for source_dir in source_dirs:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    file_path = os.path.join(foldername, filename)

                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime > three_days_ago:

                        relative_path = os.path.relpath(foldername, source_dir)
                        destination_dir = os.path.join(backup_dir, relative_path)
                        os.makedirs(destination_dir, exist_ok=True)
                        shutil.copy2(file_path, destination_dir)
                        print(f"Skopiowano: {file_path} do {destination_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kopia zapasowa plików zmodyfikowanych w ostatnich 3 dniach.")
    parser.add_argument("--sources", nargs='+', required=True)
    parser.add_argument("--extensions", nargs='+', required=True)
    parser.add_argument("--backup", required=True)
    args = parser.parse_args()

    backup_recent_files(args.sources, args.extensions, args.backup)
