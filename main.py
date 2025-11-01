#!/usr/bin/env python3
"""
Password Manager - Secure local password management application
Entry point for the password manager console application
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_manager.password_manager import PasswordManager
from password_manager.auth_manager import AuthenticationManager
from password_manager.credential_store import CredentialStore
from password_manager.encryption_handler import EncryptionHandler
from password_manager.menu_ui import MenuUI


def main():
    """Main entry point for the password manager application"""
    try:
        # Initialize components
        credential_store = CredentialStore()
        encryption_handler = EncryptionHandler()
        menu_ui = MenuUI()

        # Create authentication manager and authenticate
        auth_manager = AuthenticationManager(credential_store, menu_ui)
        master_password = auth_manager.authenticate()

        # Create password manager and set master password
        password_manager = PasswordManager(credential_store, encryption_handler, menu_ui)
        password_manager.set_master_password(master_password)

        # Run the main menu loop
        password_manager.run_menu_loop()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except SystemExit:
        # Allow normal system exit
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
