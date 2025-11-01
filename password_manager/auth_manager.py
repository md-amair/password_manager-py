"""
AuthenticationManager - Handles master password authentication
Uses bcrypt for secure password hashing
"""

import bcrypt
from password_manager.credential_store import CredentialStore
from password_manager.menu_ui import MenuUI


class AuthenticationManager:
    """Manages master password authentication"""

    MAX_LOGIN_ATTEMPTS = 3

    def __init__(self, credential_store=None, menu_ui=None):
        """
        Initialize AuthenticationManager

        Args:
            credential_store (CredentialStore, optional): Credential store instance
            menu_ui (MenuUI, optional): Menu UI instance for user interaction
        """
        self.credential_store = credential_store or CredentialStore()
        self.menu_ui = menu_ui or MenuUI()

    def authenticate(self):
        """
        Main authentication flow

        First run: Create master password
        Subsequent runs: Verify master password (3 attempts max)

        Returns:
            str: The master password if authentication successful

        Raises:
            SystemExit: If authentication fails or max attempts exceeded
        """
        # Check if credentials file exists
        if not self.credential_store.file_exists():
            # First run: Create master password
            master_password = self._create_master_password()
            return master_password
        else:
            # Subsequent run: Verify master password
            master_password = self._verify_master_password()
            return master_password

    def _create_master_password(self):
        """
        Create a new master password on first run

        Returns:
            str: The master password

        Raises:
            SystemExit: If user input is invalid
        """
        while True:
            # Prompt for password creation
            password = self.menu_ui.get_password_input("Create a master password: ")

            # Check password length
            if len(password) < 8:
                print("Password must be at least 8 characters")
                continue

            # Prompt for confirmation
            confirmation = self.menu_ui.get_password_input("Confirm master password: ")

            # Check if passwords match
            if password != confirmation:
                print("Passwords do not match. Please try again.")
                continue

            # Valid password, hash and save
            password_hash = self._hash_password(password)
            self.credential_store.initialize_file(password_hash)

            return password

    def _verify_master_password(self):
        """
        Verify master password on subsequent runs (3 attempts max)

        Returns:
            str: The master password if correct

        Raises:
            SystemExit: If max attempts exceeded
        """
        attempts_remaining = self.MAX_LOGIN_ATTEMPTS

        while attempts_remaining > 0:
            # Prompt for password
            password = self.menu_ui.get_password_input("Enter master password: ")

            # Load stored hash
            try:
                stored_hash, _ = self.credential_store.load_credentials()
            except Exception as e:
                print(str(e))
                raise SystemExit

            # Verify password
            if self._verify_password(password, stored_hash):
                return password

            # Incorrect password
            attempts_remaining -= 1
            if attempts_remaining > 0:
                print(f"Invalid master password. {attempts_remaining} attempts remaining.")
            else:
                print("Too many failed attempts. Exiting.")
                raise SystemExit

    def _hash_password(self, password):
        """
        Hash a password using bcrypt

        Args:
            password (str): The password to hash

        Returns:
            str: The hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def _verify_password(self, input_password, stored_hash):
        """
        Verify a password against a bcrypt hash

        Args:
            input_password (str): The password to verify
            stored_hash (str): The stored bcrypt hash

        Returns:
            bool: True if password matches hash, False otherwise
        """
        return bcrypt.checkpw(input_password.encode(), stored_hash.encode())
