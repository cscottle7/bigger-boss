#!/usr/bin/env python3
"""
Batch Reconversion Script for Existing DOCX Files
Fixes .docx files that were created with the old plain-text converter
by reconverting them using the new rich-text converter.

Features:
- Finds all .md files with corresponding .docx files in clients/ folder
- Reconverts using enhanced markdown→DOCX converter
- Provides dry-run mode to preview changes
- Tracks progress and success/failure rates
- Backs up original files before reconversion

Usage:
    python scripts/reconvert_existing_docx.py --dry-run
    python scripts/reconvert_existing_docx.py --execute
    python scripts/reconvert_existing_docx.py --execute --backup
"""

import argparse
import logging
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import io

# Fix Windows Unicode encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocxReconverter:
    """
    Batch reconverter for existing .docx files created with old plain-text converter.
    """

    def __init__(self, backup_enabled: bool = True):
        self.script_dir = Path(__file__).parent
        self.root_dir = self.script_dir.parent
        self.clients_dir = self.root_dir / "clients"
        self.converter_script = self.script_dir / "convert_my_docs.py"
        self.backup_enabled = backup_enabled
        self.backup_dir = self.root_dir / "backups" / f"docx_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.stats = {
            'total_found': 0,
            'reconverted': 0,
            'failed': 0,
            'skipped': 0,
            'backed_up': 0
        }

    def find_docx_with_md_source(self) -> List[Tuple[Path, Path]]:
        """
        Find all .docx files that have corresponding .md source files.

        Returns:
            List of tuples: (md_file_path, docx_file_path)
        """
        pairs = []

        if not self.clients_dir.exists():
            logger.error(f"Clients directory not found: {self.clients_dir}")
            return pairs

        # Find all .md files
        for md_file in self.clients_dir.rglob("*.md"):
            # Skip system files and templates
            if any(part.startswith('.') for part in md_file.parts):
                continue
            if any(part in ['CLIENT_FOLDER_TEMPLATE', 'temp', 'tmp', '__pycache__', 'templates'] for part in md_file.parts):
                continue

            # Check if corresponding .docx exists
            docx_file = md_file.with_suffix('.docx')
            if docx_file.exists():
                pairs.append((md_file, docx_file))

        self.stats['total_found'] = len(pairs)
        return pairs

    def needs_reconversion(self, docx_file: Path) -> bool:
        """
        Check if .docx file needs reconversion.
        Currently returns True for all files, but could be enhanced to check file content.

        Args:
            docx_file: Path to .docx file

        Returns:
            True if file should be reconverted
        """
        # For now, reconvert all files since we can't easily detect old format
        # Could be enhanced to:
        # 1. Check file creation date (if before fix date)
        # 2. Open .docx and check for markdown syntax in text
        return True

    def backup_file(self, file_path: Path) -> bool:
        """
        Create backup of existing .docx file.

        Args:
            file_path: Path to file to backup

        Returns:
            True if backup successful
        """
        if not self.backup_enabled:
            return True

        try:
            # Create backup directory structure
            relative_path = file_path.relative_to(self.clients_dir)
            backup_path = self.backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            self.stats['backed_up'] += 1
            logger.debug(f"Backed up: {file_path} -> {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to backup {file_path}: {e}")
            return False

    def reconvert_file(self, md_file: Path, docx_file: Path) -> bool:
        """
        Reconvert .md file to .docx using enhanced converter.

        Args:
            md_file: Path to source .md file
            docx_file: Path to target .docx file

        Returns:
            True if reconversion successful
        """
        try:
            # Backup original .docx file
            if not self.backup_file(docx_file):
                logger.warning(f"Backup failed for {docx_file}, skipping reconversion")
                self.stats['skipped'] += 1
                return False

            # Delete old .docx file
            docx_file.unlink()
            logger.debug(f"Deleted old file: {docx_file}")

            # Run converter script
            cmd = [
                sys.executable,
                str(self.converter_script),
                str(md_file)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                logger.info(f"Successfully reconverted: {md_file.name}")
                self.stats['reconverted'] += 1
                return True
            else:
                logger.error(f"Conversion failed for {md_file}: {result.stderr}")
                self.stats['failed'] += 1
                return False

        except Exception as e:
            logger.error(f"Error reconverting {md_file}: {e}")
            self.stats['failed'] += 1
            return False

    def run_dry_run(self, file_pairs: List[Tuple[Path, Path]]):
        """
        Show what would be reconverted without making changes.

        Args:
            file_pairs: List of (md_file, docx_file) tuples
        """
        print("\n" + "="*70)
        print("DRY RUN MODE - No files will be modified")
        print("="*70)
        print(f"\nFound {len(file_pairs)} .docx files with .md sources\n")

        if not file_pairs:
            print("No files to reconvert.")
            return

        # Group by client folder
        client_groups = {}
        for md_file, docx_file in file_pairs:
            # Get client folder name (first folder under clients/)
            try:
                client_name = md_file.relative_to(self.clients_dir).parts[0]
                if client_name not in client_groups:
                    client_groups[client_name] = []
                client_groups[client_name].append((md_file, docx_file))
            except Exception:
                continue

        # Display grouped by client
        for client_name, files in sorted(client_groups.items()):
            print(f"\n{client_name}/")
            for md_file, docx_file in files:
                relative_md = md_file.relative_to(self.clients_dir)
                print(f"  - {relative_md}")

        print(f"\n{'='*70}")
        print(f"Total files to reconvert: {len(file_pairs)}")
        if self.backup_enabled:
            print(f"Backup location: {self.backup_dir}")
        else:
            print("Backups: DISABLED")
        print(f"{'='*70}\n")

    def run_batch_reconversion(self, file_pairs: List[Tuple[Path, Path]]):
        """
        Execute batch reconversion of all file pairs.

        Args:
            file_pairs: List of (md_file, docx_file) tuples
        """
        print("\n" + "="*70)
        print("BATCH RECONVERSION - Processing files")
        print("="*70)
        print(f"\nProcessing {len(file_pairs)} files...\n")

        if not file_pairs:
            print("No files to reconvert.")
            return

        for idx, (md_file, docx_file) in enumerate(file_pairs, 1):
            print(f"[{idx}/{len(file_pairs)}] Processing: {md_file.name}")
            self.reconvert_file(md_file, docx_file)

        self.print_statistics()

    def print_statistics(self):
        """Print reconversion statistics."""
        stats = self.stats
        print("\n" + "="*70)
        print("RECONVERSION STATISTICS")
        print("="*70)
        print(f"Total files found:        {stats['total_found']}")
        print(f"Successfully reconverted: {stats['reconverted']}")
        print(f"Failed conversions:       {stats['failed']}")
        print(f"Skipped files:            {stats['skipped']}")
        if self.backup_enabled:
            print(f"Files backed up:          {stats['backed_up']}")
            print(f"Backup location:          {self.backup_dir}")

        if stats['total_found'] > 0:
            success_rate = (stats['reconverted'] / stats['total_found']) * 100
            print(f"Success rate:             {success_rate:.1f}%")

        print("="*70)


def main():
    """Main entry point for batch reconversion script."""
    parser = argparse.ArgumentParser(
        description='Batch reconvert existing .docx files with rich text formatting'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be reconverted without making changes'
    )
    group.add_argument(
        '--execute',
        action='store_true',
        help='Execute batch reconversion'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Disable backup of original files (not recommended)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Auto-confirm execution without prompting'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check if converter script exists
    converter_script = Path(__file__).parent / "convert_my_docs.py"
    if not converter_script.exists():
        print(f"ERROR: Converter script not found: {converter_script}")
        sys.exit(1)

    # Create reconverter instance
    backup_enabled = not args.no_backup
    reconverter = DocxReconverter(backup_enabled=backup_enabled)

    try:
        # Find all .docx files with .md sources
        print("Scanning for .docx files with .md sources...")
        file_pairs = reconverter.find_docx_with_md_source()

        if args.dry_run:
            # Dry run mode
            reconverter.run_dry_run(file_pairs)
            sys.exit(0)

        elif args.execute:
            # Execute reconversion
            if not file_pairs:
                print("No files found to reconvert.")
                sys.exit(0)

            # Confirm execution
            print(f"\nFound {len(file_pairs)} files to reconvert.")
            if backup_enabled:
                print(f"Backups will be saved to: {reconverter.backup_dir}")
            else:
                print("WARNING: Backups are DISABLED. Original files will be lost!")

            if not args.yes:
                response = input("\nProceed with batch reconversion? (yes/no): ").strip().lower()
                if response != 'yes':
                    print("Reconversion cancelled.")
                    sys.exit(0)
            else:
                print("\nAuto-confirmed with --yes flag. Starting reconversion...")

            reconverter.run_batch_reconversion(file_pairs)
            sys.exit(0 if reconverter.stats['failed'] == 0 else 1)

    except KeyboardInterrupt:
        print("\n\nReconversion cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Batch reconversion failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
