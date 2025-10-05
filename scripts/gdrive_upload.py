#!/usr/bin/env python3
"""
Bigger Boss Agent System - Google Drive Upload Integration
Automatically uploads client documents to organised Google Drive folders.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GoogleDriveUploader:
    """Google Drive uploader with rclone integration."""

    def __init__(self, rclone_remote: str = "googledrive"):
        """
        Initialise Google Drive uploader.

        Args:
            rclone_remote: Name of rclone remote configuration
        """
        self.rclone_remote = rclone_remote
        # Use local rclone executable
        self.rclone_path = os.path.join(os.path.dirname(__file__), '..', 'tools', 'rclone.exe')
        if not os.path.exists(self.rclone_path):
            self.rclone_path = "rclone"  # Fallback to system PATH
        self.client_folder_mapping = self._load_client_mappings()
        self.upload_config = {
            "max_retries": 3,
            "chunk_size": "8M",
            "transfers": 4,
            "checkers": 8,
            "create_empty_dirs": True,
            "no_check_certificate": False,
            "stats": "1m",
        }

    def _load_client_mappings(self) -> Dict[str, str]:
        """Load client to Google Drive folder mappings."""
        # Default client folder mappings - All files go to SEO\Content
        default_mappings = {
            'lunadigitalmarketing_com_au': 'SEO/Content/Luna Digital Marketing',
            'simplysolarsolutions_com_au': 'SEO/Content/Simply Solar Solutions',
            'greenpowersolutions_com_au': 'SEO/Content/Green Power Solutions',
            'sydneycoachcharter_com_au': 'SEO/Content/Sydney Coach Charter',
            'precisionuppergisurgery_com_au': 'SEO/Content/Precision Upper GI Surgery',
            'endeurology_com_au': 'SEO/Content/Endeurology',
            'capitalsmiles_com_au': 'SEO/Content/Capital Smiles',
            'centreforgastrointestinalhealth_com_au': 'SEO/Content/Centre for GI Health',
            'drjuliacrawford_com_au': 'SEO/Content/Dr Julia Crawford',
            'familyfocuslegal_com_au': 'SEO/Content/Family Focus Legal',
            'discoverwebsolutions_com_au': 'SEO/Content/Discover Web Solutions',
            'allsparkelectrical_net': 'SEO/Content/Allspark Electrical',
            # Default fallback for new clients
            'default': 'SEO/Content',
        }

        # Try to load custom mappings from config file
        config_file = Path(__file__).parent / "gdrive_mappings.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    custom_mappings = json.load(f)
                    default_mappings.update(custom_mappings)
                logger.info(f"Loaded custom client mappings from {config_file}")
            except Exception as e:
                logger.warning(f"Could not load custom mappings: {e}")

        return default_mappings

    def _extract_client_domain(self, file_path: str) -> Optional[str]:
        """Extract client domain from file path."""
        path_parts = Path(file_path).parts

        # Look for 'clients' folder in path
        if 'clients' in path_parts:
            clients_index = path_parts.index('clients')
            if len(path_parts) > clients_index + 1:
                return path_parts[clients_index + 1]

        return None

    def _get_file_category(self, file_path: str) -> str:
        """Determine file category based on path and name."""
        path_str = str(file_path).lower()

        if '/strategy/' in path_str:
            return 'Strategy'
        elif '/research/' in path_str:
            return 'Research'
        elif '/content/' in path_str:
            return 'Content'
        elif '/technical/' in path_str:
            return 'Technical'
        elif '/implementation/' in path_str:
            return 'Implementation'
        elif 'checklist' in path_str:
            return 'Project Management'
        elif 'summary' in path_str or 'report' in path_str:
            return 'Reports'
        else:
            return 'General'

    def _build_gdrive_path(self, file_path: str, client_domain: Optional[str] = None) -> str:
        """Build Google Drive path for file upload."""
        if not client_domain:
            client_domain = self._extract_client_domain(file_path)

        if not client_domain:
            # Fallback to SEO/Content
            base_folder = "SEO/Content"
        else:
            base_folder = self.client_folder_mapping.get(
                client_domain,
                f"SEO/Content/{client_domain.replace('_', ' ').title()}"
            )

        # Add date-based subfolder
        date_folder = datetime.now().strftime("%Y-%m")

        # Add category subfolder
        category = self._get_file_category(file_path)

        # Construct final path
        gdrive_path = f"{base_folder}/{date_folder}/{category}"

        return gdrive_path

    def _check_rclone_config(self) -> bool:
        """Check if rclone is configured properly."""
        try:
            result = subprocess.run(
                [self.rclone_path, "config", "show", self.rclone_remote],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info(f"rclone remote '{self.rclone_remote}' is configured")
                return True
            else:
                logger.error(f"rclone remote '{self.rclone_remote}' not found")
                return False

        except FileNotFoundError:
            logger.error("rclone not found. Please install rclone.")
            return False
        except Exception as e:
            logger.error(f"Error checking rclone config: {e}")
            return False

    def _upload_with_rclone(self, local_path: str, remote_path: str) -> bool:
        """Upload file using rclone."""
        try:
            # Build rclone command
            cmd = [
                self.rclone_path, "copy",
                local_path,
                f"{self.rclone_remote}:{remote_path}",
                "--progress",
                f"--retries={self.upload_config['max_retries']}",
                f"--transfers={self.upload_config['transfers']}",
                f"--checkers={self.upload_config['checkers']}",
                f"--stats={self.upload_config['stats']}",
            ]

            if self.upload_config["create_empty_dirs"]:
                cmd.append("--create-empty-src-dirs")

            logger.info(f"Uploading {local_path} to {remote_path}")
            logger.debug(f"rclone command: {' '.join(cmd)}")

            # Execute rclone command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info(f"Successfully uploaded {local_path}")
                return True
            else:
                logger.error(f"rclone upload failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error during rclone upload: {e}")
            return False

    def _create_upload_log(self, file_path: str, remote_path: str, success: bool) -> None:
        """Create upload log entry."""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "gdrive_uploads.log"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "local_path": str(file_path),
            "remote_path": remote_path,
            "success": success,
            "client_domain": self._extract_client_domain(file_path),
        }

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.warning(f"Could not write upload log: {e}")

    def upload_file(
        self,
        file_path: str,
        client_domain: Optional[str] = None,
        custom_path: Optional[str] = None
    ) -> bool:
        """
        Upload file to Google Drive.

        Args:
            file_path: Path to file to upload
            client_domain: Client domain override
            custom_path: Custom Google Drive path override

        Returns:
            True if upload successful, False otherwise
        """
        file_path = Path(file_path)

        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False

        # Check rclone configuration
        if not self._check_rclone_config():
            logger.error("rclone not properly configured")
            return False

        try:
            # Determine remote path
            if custom_path:
                remote_path = custom_path
            else:
                remote_path = self._build_gdrive_path(str(file_path), client_domain)

            # Upload file
            success = self._upload_with_rclone(str(file_path), remote_path)

            # Log upload attempt
            self._create_upload_log(str(file_path), remote_path, success)

            if success:
                logger.info(f"✅ Upload completed: {file_path.name}")
                print(f"✅ Uploaded to Google Drive: {remote_path}/{file_path.name}")
            else:
                logger.error(f"❌ Upload failed: {file_path.name}")
                print(f"❌ Upload failed: {file_path.name}")

            return success

        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            return False

    def upload_folder(
        self,
        folder_path: str,
        client_domain: Optional[str] = None,
        file_patterns: Optional[list] = None
    ) -> Dict[str, bool]:
        """
        Upload all files in a folder to Google Drive.

        Args:
            folder_path: Path to folder to upload
            client_domain: Client domain override
            file_patterns: List of file patterns to match (e.g., ['*.docx', '*.pdf'])

        Returns:
            Dictionary mapping file paths to upload success status
        """
        folder_path = Path(folder_path)

        if not folder_path.exists() or not folder_path.is_dir():
            logger.error(f"Folder does not exist: {folder_path}")
            return {}

        # Default file patterns
        if not file_patterns:
            file_patterns = ['*.docx', '*.pdf', '*.md']

        results = {}

        try:
            # Find all matching files
            files_to_upload = []
            for pattern in file_patterns:
                files_to_upload.extend(folder_path.rglob(pattern))

            logger.info(f"Found {len(files_to_upload)} files to upload")

            # Upload each file
            for file_path in files_to_upload:
                success = self.upload_file(str(file_path), client_domain)
                results[str(file_path)] = success

            return results

        except Exception as e:
            logger.error(f"Error uploading folder: {e}")
            return {}

    def setup_rclone_config(self, interactive: bool = True) -> bool:
        """
        Set up rclone configuration for Google Drive.

        Args:
            interactive: Whether to use interactive configuration

        Returns:
            True if setup successful, False otherwise
        """
        try:
            if interactive:
                print("Setting up rclone Google Drive configuration...")
                print("Please follow the interactive prompts:")

                result = subprocess.run([
                    self.rclone_path, "config", "create",
                    self.rclone_remote, "drive"
                ])

                return result.returncode == 0

            else:
                # Non-interactive setup requires client ID and secret
                client_id = config('GOOGLE_DRIVE_CLIENT_ID', default=None)
                client_secret = config('GOOGLE_DRIVE_CLIENT_SECRET', default=None)

                if not client_id or not client_secret:
                    logger.error("GOOGLE_DRIVE_CLIENT_ID and GOOGLE_DRIVE_CLIENT_SECRET must be set")
                    return False

                # Create rclone config
                result = subprocess.run([
                    self.rclone_path, "config", "create",
                    self.rclone_remote, "drive",
                    f"client_id={client_id}",
                    f"client_secret={client_secret}",
                    "scope=drive"
                ])

                if result.returncode == 0:
                    print("✅ rclone configuration created successfully")
                    print("🔐 You may need to complete OAuth authentication")
                    return True
                else:
                    print("❌ Failed to create rclone configuration")
                    return False

        except Exception as e:
            logger.error(f"Error setting up rclone: {e}")
            return False


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Upload files to Google Drive with client folder organisation'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Upload file command
    upload_parser = subparsers.add_parser('upload', help='Upload a file')
    upload_parser.add_argument('file_path', help='Path to file to upload')
    upload_parser.add_argument('--client', help='Client domain override')
    upload_parser.add_argument('--path', help='Custom Google Drive path')

    # Upload folder command
    folder_parser = subparsers.add_parser('folder', help='Upload folder contents')
    folder_parser.add_argument('folder_path', help='Path to folder to upload')
    folder_parser.add_argument('--client', help='Client domain override')
    folder_parser.add_argument(
        '--patterns',
        nargs='+',
        default=['*.docx', '*.pdf', '*.md'],
        help='File patterns to match'
    )

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup rclone configuration')
    setup_parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Use non-interactive setup (requires env vars)'
    )

    # Global options
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return

    uploader = GoogleDriveUploader()

    try:
        if args.command == 'upload':
            success = uploader.upload_file(args.file_path, args.client, args.path)
            sys.exit(0 if success else 1)

        elif args.command == 'folder':
            results = uploader.upload_folder(args.folder_path, args.client, args.patterns)
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            print(f"✅ Uploaded {successful}/{total} files successfully")
            sys.exit(0 if successful == total else 1)

        elif args.command == 'setup':
            success = uploader.setup_rclone_config(not args.non_interactive)
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()