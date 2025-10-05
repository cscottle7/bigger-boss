"""
Google Drive Folder Deduplication Script

Finds and merges duplicate client folders in Google Drive using RClone.
Handles exact duplicates and similar folder names.

Usage:
    python deduplicate_google_drive_folders.py              # Dry run (safe, no changes)
    python deduplicate_google_drive_folders.py --list       # List all folders with status
    python deduplicate_google_drive_folders.py --execute    # Execute merge
"""

import subprocess
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re


class GoogleDriveFolderDeduplicator:
    def __init__(self, remote_name="googledrive", remote_path="SEO/Content"):
        self.remote_name = remote_name
        self.remote_path = remote_path
        self.full_remote = f"{remote_name}:{remote_path}"

    def normalize_folder_name(self, folder_name):
        """Normalize folder name for comparison"""
        # Remove common variations
        name = folder_name.lower()
        name = name.replace(' com au', '')
        name = name.replace(' com', '')
        name = name.replace(' net au', '')
        name = name.replace(' net', '')
        name = name.replace(' org au', '')
        name = name.replace(' org', '')

        # Remove extra spaces and special chars
        name = re.sub(r'\s+', '_', name.strip())
        name = re.sub(r'[^a-z0-9_]', '', name)

        return name

    def list_folders(self):
        """List all folders in Google Drive path"""
        try:
            result = subprocess.run(
                ['rclone', 'lsjson', self.full_remote, '--dirs-only'],
                capture_output=True,
                text=True,
                check=True
            )

            folders = json.loads(result.stdout)
            return [(f['Name'], f['ModTime']) for f in folders]

        except subprocess.CalledProcessError as e:
            print(f"ERROR - Failed to list folders: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"ERROR - Failed to parse folder list: {e}")
            return []

    def find_duplicates(self):
        """Find all duplicate folders"""
        folders = self.list_folders()

        if not folders:
            print("No folders found or error occurred")
            return {}

        # Group folders by normalized name
        groups = defaultdict(list)
        for folder_name, mod_time in folders:
            if folder_name == 'Client Folder Template':
                continue
            normalized = self.normalize_folder_name(folder_name)
            groups[normalized].append((folder_name, mod_time))

        # Find groups with multiple folders
        duplicates = {key: folders for key, folders in groups.items() if len(folders) > 1}

        if duplicates:
            print(f"Found {len(duplicates)} groups with duplicates:\n")

            for normalized, folder_list in duplicates.items():
                print(f"\nGroup: {normalized}")
                print(f"  {len(folder_list)} folders:")

                # Sort by modification time (newest first)
                folder_list.sort(key=lambda x: x[1], reverse=True)

                for i, (name, mod_time) in enumerate(folder_list):
                    if i == 0:
                        print(f"    KEEP: {name} (modified: {mod_time})")
                    else:
                        print(f"    MERGE: {name} (modified: {mod_time})")

        return duplicates

    def merge_folders(self, dry_run=True):
        """Merge duplicate folders"""
        duplicates = self.find_duplicates()

        if not duplicates:
            print("\nNo duplicate folders found!")
            return

        print("\n" + "="*60)
        if dry_run:
            print("DRY RUN - Showing what would happen (no changes made)")
        else:
            print("EXECUTING MERGE - This will make changes!")
        print("="*60 + "\n")

        for normalized, folder_list in duplicates.items():
            # Sort by modification time (newest first) - keep the newest
            folder_list.sort(key=lambda x: x[1], reverse=True)
            keep_folder = folder_list[0][0]
            merge_folders = [name for name, _ in folder_list[1:]]

            print(f"\nGroup: {normalized}")
            print(f"  KEEP: {keep_folder}")

            for merge_folder in merge_folders:
                print(f"  MERGE: {merge_folder} -> {keep_folder}")

                # Get contents of folder to merge
                source_path = f"{self.full_remote}/{merge_folder}"
                dest_path = f"{self.full_remote}/{keep_folder}"

                if not dry_run:
                    # Copy contents from merge folder to keep folder
                    try:
                        print(f"    Copying contents from {merge_folder}...")
                        subprocess.run(
                            ['rclone', 'copy', source_path, dest_path, '-v'],
                            check=True,
                            capture_output=True,
                            text=True
                        )

                        # Delete the now-empty duplicate folder
                        print(f"    Deleting {merge_folder}...")
                        subprocess.run(
                            ['rclone', 'purge', source_path],
                            check=True,
                            capture_output=True,
                            text=True
                        )

                        print(f"    SUCCESS - Merged {merge_folder}")

                    except subprocess.CalledProcessError as e:
                        print(f"    ERROR - Failed to merge {merge_folder}: {e}")
                        print(f"    STDERR: {e.stderr}")

        if dry_run:
            print("\n" + "="*60)
            print("DRY RUN - This was a DRY RUN - no changes made")
            print("To execute, run: python deduplicate_google_drive_folders.py --execute")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("SUCCESS - Merge complete!")
            print("="*60)

    def list_all_folders(self):
        """List all folders with their status"""
        folders = self.list_folders()

        if not folders:
            print("No folders found or error occurred")
            return

        print(f"\nAll Google Drive Folders ({len(folders)}):\n")

        # Group for duplicate detection
        groups = defaultdict(list)
        for folder_name, mod_time in folders:
            normalized = self.normalize_folder_name(folder_name)
            groups[normalized].append(folder_name)

        # Sort folders alphabetically
        folders_sorted = sorted(folders, key=lambda x: x[0])

        for folder_name, mod_time in folders_sorted:
            if folder_name == 'Client Folder Template':
                print(f"   [TEMPLATE] {folder_name}")
            else:
                normalized = self.normalize_folder_name(folder_name)
                if len(groups[normalized]) > 1:
                    print(f"   [DUPLICATE] {folder_name} (modified: {mod_time})")
                else:
                    print(f"   [OK] {folder_name}")


def main():
    import sys

    deduplicator = GoogleDriveFolderDeduplicator()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        print("EXECUTING MERGE - This will make changes to Google Drive!")
        response = input("Are you sure? Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("CANCELLED")
            return
        deduplicator.merge_folders(dry_run=False)
    elif len(sys.argv) > 1 and sys.argv[1] == '--list':
        deduplicator.list_all_folders()
    else:
        # Default: dry run
        print("Running in DRY RUN mode (safe, no changes will be made)")
        print("Use --execute to actually merge folders")
        print("Use --list to see all folders\n")
        deduplicator.merge_folders(dry_run=True)


if __name__ == "__main__":
    main()
