"""
CredentialStore - Handles data persistence for credentials
Manages loading and saving credentials to JSON file
"""

import json
import os
from datetime import datetime


class CredentialStore:
    """Handles file I/O for credential storage"""

    CREDENTIALS_FILE = "credentials.json"

    def __init__(self, file_path=None):
        """
        Initialize CredentialStore

        Args:
            file_path (str, optional): Path to credentials file. Defaults to credentials.json in current directory
        """
        self.file_path = file_path or self.CREDENTIALS_FILE

    def file_exists(self):
        """
        Check if credentials file exists

        Returns:
            bool: True if credentials file exists, False otherwise
        """
        return os.path.exists(self.file_path)

    def initialize_file(self, master_password_hash):
        """
        Create a new credentials file with empty credentials list and master password hash

        Args:
            master_password_hash (str): The hashed master password to store

        Raises:
            Exception: If file creation fails
        """
        data = {
            "master_password_hash": master_password_hash,
            "credentials": []
        }

        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

            # Set file permissions to readable/writable by owner only (Unix-like systems)
            try:
                os.chmod(self.file_path, 0o600)
            except Exception:
                # Windows or systems that don't support chmod
                pass
        except PermissionError:
            raise Exception("Cannot write to credentials file. Check permissions.")
        except Exception as e:
            raise Exception(f"Failed to create credentials file. Error: {str(e)}")

    def load_credentials(self):
        """
        Load and parse credentials from JSON file

        Returns:
            tuple: (master_password_hash, credentials_list)

        Raises:
            Exception: If file is corrupted or cannot be read
        """
        if not self.file_exists():
            return None, []

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            master_password_hash = data.get("master_password_hash")
            credentials_list = data.get("credentials", [])

            return master_password_hash, credentials_list
        except json.JSONDecodeError:
            raise Exception("Credentials file corrupted. Please restore from backup.")
        except PermissionError:
            raise Exception("Cannot read credentials file. Check permissions.")
        except Exception as e:
            raise Exception(f"Failed to load credentials. Error: {str(e)}")

    def save_credentials(self, master_password_hash, credentials_list):
        """
        Save credentials to JSON file

        Args:
            master_password_hash (str): The hashed master password to store
            credentials_list (list): List of credential dictionaries

        Raises:
            Exception: If file cannot be written
        """
        data = {
            "master_password_hash": master_password_hash,
            "credentials": credentials_list
        }

        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

            # Set file permissions to readable/writable by owner only
            try:
                os.chmod(self.file_path, 0o600)
            except Exception:
                # Windows or systems that don't support chmod
                pass
        except PermissionError:
            raise Exception("Cannot write to credentials file. Check permissions.")
        except Exception as e:
            raise Exception(f"Failed to save credentials. Error: {str(e)}")

    @staticmethod
    def get_iso_timestamp():
        """
        Get current timestamp in ISO 8601 format

        Returns:
            str: Timestamp in format "YYYY-MM-DDTHH:MM:SS"
        """
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
