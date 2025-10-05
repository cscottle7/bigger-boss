"""
Centralized API Credential Management System
Handles API keys and credentials for autonomous operations
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APICredentialManager:
    """Manages API credentials for various services"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.credentials_file = self.config_dir / "credentials.json"
        self._credentials = {}
        self.load_credentials()
        
    def load_credentials(self) -> None:
        """Load credentials from file or environment variables"""
        # Try to load from file first
        if self.credentials_file.exists():
            try:
                with open(self.credentials_file, 'r') as f:
                    self._credentials = json.load(f)
            except Exception as e:
                logging.warning(f"Could not load credentials file: {e}")
        
        # Override with environment variables if available
        env_credentials = {
            'gtmetrix': {
                'api_key': os.getenv('GTMETRIX_API_KEY'),
                'username': os.getenv('GTMETRIX_USERNAME')
            },
            'serpapi': {
                'api_key': os.getenv('SERPAPI_API_KEY'),  # Primary SerpAPI account
                'api_key_backup': os.getenv('SERPAPI_API_KEY_BACKUP')  # Backup SerpAPI account
            },
            'jina': {  # JINA AI integration
                'api_key': os.getenv('JINA_API_KEY')
            },
            'google': {
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'cse_id': os.getenv('GOOGLE_CSE_ID')
            }
        }
        
        # Update credentials with environment variables
        for service, creds in env_credentials.items():
            if service not in self._credentials:
                self._credentials[service] = {}
            for key, value in creds.items():
                if value:  # Only update if environment variable is set
                    self._credentials[service][key] = value
    
    def get_credential(self, service: str, key: str) -> Optional[str]:
        """Get a specific credential"""
        return self._credentials.get(service, {}).get(key)
    
    def has_service_credentials(self, service: str) -> bool:
        """Check if we have credentials for a service"""
        service_creds = self._credentials.get(service, {})
        return any(value for value in service_creds.values())
    
    def set_credential(self, service: str, key: str, value: str) -> None:
        """Set a credential (for testing/development)"""
        if service not in self._credentials:
            self._credentials[service] = {}
        self._credentials[service][key] = value
        self._save_credentials()
    
    def _save_credentials(self) -> None:
        """Save credentials to file"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(self._credentials, f, indent=2)
        except Exception as e:
            logging.warning(f"Could not save credentials file: {e}")
    
    def get_available_services(self) -> list:
        """Get list of services with available credentials"""
        return [service for service in self._credentials.keys() 
                if self.has_service_credentials(service)]

# Global instance
credentials = APICredentialManager()