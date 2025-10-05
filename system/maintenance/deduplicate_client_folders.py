"""
Client Folder Deduplication Script
Merges duplicate client folders and enforces domain-based naming standard
"""

import os
import shutil
from pathlib import Path
import re
from collections import defaultdict

class ClientFolderDeduplicator:
    """Finds and merges duplicate client folders"""

    def __init__(self, clients_dir="clients"):
        self.clients_dir = Path(clients_dir)
        self.duplicates_found = []
        self.merge_plan = []

    def normalize_domain_name(self, folder_name):
        """Convert folder name to standard domain format"""
        # Remove common suffixes
        name = folder_name.lower()
        name = name.replace(' (1)', '').replace(' (2)', '').replace(' (3)', '').replace(' (4)', '')

        # Convert spaces to underscores
        name = name.replace(' ', '_')

        # Remove special characters
        name = re.sub(r'[^a-z0-9_]', '', name)

        return name

    def extract_domain_from_folder(self, folder_name):
        """Extract likely domain from folder name"""
        # If already in domain format (has _com_ or _au etc)
        if '_com_' in folder_name or '_net_' in folder_name or '_org_' in folder_name:
            return folder_name

        # Convert business name to domain format
        # e.g., "Capital Smiles" -> "capitalsmiles"
        normalized = self.normalize_domain_name(folder_name)

        # Try to append common TLD if not present
        if not any(tld in normalized for tld in ['_com_au', '_com', '_net_au', '_net']):
            # Default to .com.au for Australian businesses
            normalized += '_com_au'

        return normalized

    def find_duplicates(self):
        """Find all duplicate client folders"""
        if not self.clients_dir.exists():
            print(f"ERROR - Clients directory not found: {self.clients_dir}")
            return []

        folders = [f for f in self.clients_dir.iterdir() if f.is_dir()]

        # Group folders by normalized name
        groups = defaultdict(list)
        for folder in folders:
            if folder.name == 'CLIENT_FOLDER_TEMPLATE':
                continue

            normalized = self.normalize_domain_name(folder.name)
            groups[normalized].append(folder)

        # Find groups with multiple folders
        duplicates = {key: folders for key, folders in groups.items() if len(folders) > 1}

        return duplicates

    def create_merge_plan(self):
        """Create plan for merging duplicate folders"""
        duplicates = self.find_duplicates()

        if not duplicates:
            print("No duplicate folders found!")
            return []

        print(f"\nFound {len(duplicates)} sets of duplicate folders:\n")

        merge_plan = []

        for normalized_name, folders in duplicates.items():
            # Determine which folder to keep (prefer domain format)
            domain_formatted = [f for f in folders if '_com_' in f.name or '_net_' in f.name]

            if domain_formatted:
                keep_folder = domain_formatted[0]
            else:
                # Keep the one without (1), (2) suffix
                no_suffix = [f for f in folders if '(' not in f.name]
                keep_folder = no_suffix[0] if no_suffix else folders[0]

            merge_folders = [f for f in folders if f != keep_folder]

            plan_item = {
                'normalized_name': normalized_name,
                'keep': keep_folder,
                'merge': merge_folders,
                'action': 'merge'
            }

            merge_plan.append(plan_item)

            print(f"Group: {normalized_name}")
            print(f"   KEEP: {keep_folder.name}")
            for folder in merge_folders:
                print(f"   MERGE: {folder.name} -> {keep_folder.name}")
            print()

        return merge_plan

    def merge_folders(self, dry_run=True):
        """Merge duplicate folders"""
        merge_plan = self.create_merge_plan()

        if not merge_plan:
            return

        print(f"\n{'DRY RUN' if dry_run else 'EXECUTING'} - Merge Plan:\n")

        for item in merge_plan:
            keep_folder = item['keep']

            for merge_folder in item['merge']:
                print(f"\nMerging: {merge_folder.name} -> {keep_folder.name}")

                # Walk through all files in merge folder
                for root, dirs, files in os.walk(merge_folder):
                    rel_path = Path(root).relative_to(merge_folder)
                    target_dir = keep_folder / rel_path

                    # Create target directory if needed
                    if not dry_run:
                        target_dir.mkdir(parents=True, exist_ok=True)

                    # Copy/move files
                    for file in files:
                        source_file = Path(root) / file
                        target_file = target_dir / file

                        if target_file.exists():
                            print(f"   SKIP (exists): {rel_path / file}")
                        else:
                            print(f"   MOVE: {rel_path / file}")
                            if not dry_run:
                                shutil.copy2(source_file, target_file)

                # Remove empty merge folder
                if not dry_run:
                    shutil.rmtree(merge_folder)
                    print(f"   DELETED: {merge_folder.name}")

        if dry_run:
            print("\n" + "="*60)
            print("DRY RUN - This was a DRY RUN - no changes made")
            print("To execute, run: deduplicate_client_folders.py --execute")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("SUCCESS - Merge complete!")
            print("="*60)

    def list_all_folders(self):
        """List all client folders with their status"""
        if not self.clients_dir.exists():
            print(f"ERROR - Clients directory not found: {self.clients_dir}")
            return

        folders = sorted([f for f in self.clients_dir.iterdir() if f.is_dir()])

        print(f"\nAll Client Folders ({len(folders)}):\n")

        duplicates = self.find_duplicates()
        duplicate_folders = set()
        for folders_list in duplicates.values():
            duplicate_folders.update(folders_list)

        for folder in folders:
            if folder.name == 'CLIENT_FOLDER_TEMPLATE':
                print(f"   [TEMPLATE] {folder.name}")
            elif folder in duplicate_folders:
                print(f"   [DUPLICATE] {folder.name}")
            elif '_com_' in folder.name or '_net_' in folder.name:
                print(f"   [OK] {folder.name}")
            else:
                print(f"   [WARNING] {folder.name} (should use domain format)")


def main():
    """Main execution"""
    import sys

    deduplicator = ClientFolderDeduplicator()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        print("EXECUTING MERGE - This will make changes!")
        response = input("Are you sure? Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("CANCELLED")
            return
        deduplicator.merge_folders(dry_run=False)
    elif len(sys.argv) > 1 and sys.argv[1] == '--list':
        deduplicator.list_all_folders()
    else:
        # Default: dry run
        deduplicator.merge_folders(dry_run=True)


if __name__ == "__main__":
    main()
