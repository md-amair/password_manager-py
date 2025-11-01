"""
PasswordManager - Main application controller
Coordinates all operations: Add, View, Search, Edit, Delete credentials
"""

import uuid
from password_manager.credential_store import CredentialStore
from password_manager.encryption_handler import EncryptionHandler
from password_manager.menu_ui import MenuUI


class PasswordManager:
    """Main application controller for password management"""

    def __init__(self, credential_store=None, encryption_handler=None, menu_ui=None):
        """
        Initialize PasswordManager

        Args:
            credential_store (CredentialStore, optional): Credential store instance
            encryption_handler (EncryptionHandler, optional): Encryption handler instance
            menu_ui (MenuUI, optional): Menu UI instance
        """
        self.credential_store = credential_store or CredentialStore()
        self.encryption_handler = encryption_handler or EncryptionHandler()
        self.menu_ui = menu_ui or MenuUI()
        self.master_password = None
        self.master_password_hash = None
        self.credentials = []

    def set_master_password(self, master_password):
        """
        Set the master password after authentication

        Args:
            master_password (str): The verified master password
        """
        self.master_password = master_password
        # Load credentials and master password hash from file
        try:
            self.master_password_hash, self.credentials = self.credential_store.load_credentials()
        except Exception as e:
            print(str(e))
            raise SystemExit

    def run_menu_loop(self):
        """Main menu loop - displays menu and handles user choices"""
        while True:
            choice = self.menu_ui.display_main_menu()

            if choice == 1:
                self.add_credential()
            elif choice == 2:
                self.view_all_credentials()
            elif choice == 3:
                self.search_credentials()
            elif choice == 4:
                self.edit_credential()
            elif choice == 5:
                self.delete_credential()
            elif choice == 6:
                self.exit_application()

    def add_credential(self):
        """Add a new credential"""
        print()

        # Get website name
        website = self.menu_ui.get_user_input("Website/Application name: ").strip()
        if not website:
            print("Website name cannot be empty")
            return

        if len(website) > 100:
            print("Website name must be 100 characters or less")
            return

        # Get username
        username = self.menu_ui.get_user_input("Username: ").strip()
        if not username:
            print("Username cannot be empty")
            return

        if len(username) > 100:
            print("Username must be 100 characters or less")
            return

        # Get password
        password = self.menu_ui.get_password_input("Password: ")
        if not password:
            print("Password cannot be empty")
            return

        if len(password) > 500:
            print("Password must be 500 characters or less")
            return

        # Check for duplicate website+username combination
        for cred in self.credentials:
            if cred['website'].lower() == website.lower() and cred['username'].lower() == username.lower():
                response = self.menu_ui.get_user_input(
                    "A credential for this website/username already exists. Continue anyway? (yes/no): "
                ).lower().strip()
                if response not in ['yes', 'y']:
                    print("Credential not saved.")
                    return
                break

        # Encrypt password
        try:
            encrypted_password = self.encryption_handler.encrypt_password(password, self.master_password)
        except Exception as e:
            print(f"Failed to encrypt password. Error: {str(e)}")
            return

        # Create credential object
        credential = {
            "id": str(uuid.uuid4()),
            "website": website,
            "username": username,
            "encrypted_password": encrypted_password,
            "created_at": CredentialStore.get_iso_timestamp(),
            "updated_at": CredentialStore.get_iso_timestamp()
        }

        # Add to credentials list
        self.credentials.append(credential)

        # Save to file
        try:
            self.credential_store.save_credentials(self.master_password_hash, self.credentials)
            print("Credential saved successfully.")
        except Exception as e:
            print(f"Failed to save credential. Error: {str(e)}")
            # Remove from list if save failed
            self.credentials.pop()

    def view_all_credentials(self):
        """View all saved credentials"""
        print()

        if not self.credentials:
            print("No credentials saved yet.")
            return

        # Decrypt all passwords
        credentials_to_display = []
        for cred in self.credentials:
            try:
                decrypted_password = self.encryption_handler.decrypt_password(
                    cred['encrypted_password'],
                    self.master_password
                )
                display_cred = cred.copy()
                display_cred['decrypted_password'] = decrypted_password
                credentials_to_display.append(display_cred)
            except Exception as e:
                print(f"Error decrypting password for {cred.get('website')}. Your file may be corrupted.")
                return

        # Display table
        self.menu_ui.display_table(credentials_to_display, mask_passwords=False)

    def search_credentials(self):
        """Search credentials by website or username"""
        print()

        # Get search type
        search_type = self.menu_ui.get_user_input("Search by (1=Website, 2=Username): ").strip()
        if search_type not in ['1', '2']:
            print("Invalid search type. Please enter 1 or 2.")
            return

        # Get search term
        search_term = self.menu_ui.get_user_input("Enter search term: ").strip()
        if not search_term:
            print("Search term cannot be empty")
            return

        # Filter credentials
        search_type_int = int(search_type)
        matching_credentials = []

        for cred in self.credentials:
            if search_type_int == 1:
                # Search by website
                if search_term.lower() in cred['website'].lower():
                    matching_credentials.append(cred)
            else:
                # Search by username
                if search_term.lower() in cred['username'].lower():
                    matching_credentials.append(cred)

        if not matching_credentials:
            print()
            print("No credentials match your search.")
            print()
            return

        # Decrypt matching passwords
        credentials_to_display = []
        for cred in matching_credentials:
            try:
                decrypted_password = self.encryption_handler.decrypt_password(
                    cred['encrypted_password'],
                    self.master_password
                )
                display_cred = cred.copy()
                display_cred['decrypted_password'] = decrypted_password
                credentials_to_display.append(display_cred)
            except Exception as e:
                print(f"Error decrypting password for {cred.get('website')}. Your file may be corrupted.")
                return

        # Display results with masked passwords
        self.menu_ui.display_search_results(credentials_to_display)

        # Offer to reveal passwords
        for cred in credentials_to_display:
            response = self.menu_ui.get_user_input(
                f"Reveal password for {cred.get('website')}? (yes/no): "
            ).lower().strip()
            if response in ['yes', 'y']:
                print(f"Password: {cred.get('decrypted_password')}")

    def edit_credential(self):
        """Edit an existing credential"""
        print()

        if not self.credentials:
            print("No credentials to edit.")
            return

        # Display numbered list
        selection = self.menu_ui.display_edit_list(self.credentials)

        if selection == 0 or selection == -1:
            # Cancel or no credentials
            return

        # Get selected credential (selection is 1-indexed)
        selected_cred = self.credentials[selection - 1]

        # Decrypt current password for display
        try:
            decrypted_password = self.encryption_handler.decrypt_password(
                selected_cred['encrypted_password'],
                self.master_password
            )
        except Exception as e:
            print(f"Error decrypting password. Your file may be corrupted.")
            return

        # Show current values
        print()
        print("====== EDIT CREDENTIAL ======")
        print(f"Current Website: {selected_cred['website']}")
        print(f"Current Username: {selected_cred['username']}")
        print(f"Current Password: {decrypted_password}")
        print("=============================")
        print()
        print("Leave blank to keep current value")
        print()

        # Get new values
        new_website = self.menu_ui.get_user_input(f"New Website [{selected_cred['website']}]: ").strip()
        if not new_website:
            new_website = selected_cred['website']
        elif len(new_website) > 100:
            print("Website name must be 100 characters or less")
            return

        new_username = self.menu_ui.get_user_input(f"New Username [{selected_cred['username']}]: ").strip()
        if not new_username:
            new_username = selected_cred['username']
        elif len(new_username) > 100:
            print("Username must be 100 characters or less")
            return

        print("Password (leave blank to keep current): ")
        new_password = self.menu_ui.get_password_input("")
        if not new_password:
            # Keep current password
            new_encrypted_password = selected_cred['encrypted_password']
        else:
            if len(new_password) > 500:
                print("Password must be 500 characters or less")
                return
            # Encrypt new password
            try:
                new_encrypted_password = self.encryption_handler.encrypt_password(new_password, self.master_password)
            except Exception as e:
                print(f"Failed to encrypt password. Error: {str(e)}")
                return

        # Update credential
        selected_cred['website'] = new_website
        selected_cred['username'] = new_username
        selected_cred['encrypted_password'] = new_encrypted_password
        selected_cred['updated_at'] = CredentialStore.get_iso_timestamp()

        # Save to file
        try:
            self.credential_store.save_credentials(self.master_password_hash, self.credentials)
            print()
            print("Credential updated successfully.")
        except Exception as e:
            print(f"Failed to update credential. Error: {str(e)}")

    def delete_credential(self):
        """Delete a credential"""
        print()

        if not self.credentials:
            print("No credentials to delete.")
            return

        # Display numbered list
        selection = self.menu_ui.display_delete_list(self.credentials)

        if selection == 0 or selection == -1:
            # Cancel or no credentials
            return

        # Get selected credential (selection is 1-indexed)
        selected_cred = self.credentials[selection - 1]

        # Decrypt password for confirmation display
        try:
            decrypted_password = self.encryption_handler.decrypt_password(
                selected_cred['encrypted_password'],
                self.master_password
            )
        except Exception as e:
            print(f"Error decrypting password. Your file may be corrupted.")
            return

        # Show confirmation with full details
        confirmation_cred = selected_cred.copy()
        confirmation_cred['decrypted_password'] = decrypted_password

        if not self.menu_ui.display_delete_confirmation(confirmation_cred):
            # User chose not to delete
            return

        # Delete from list and save
        self.credentials.pop(selection - 1)

        try:
            self.credential_store.save_credentials(self.master_password_hash, self.credentials)
            self.menu_ui.clear_screen()
            print("Credential deleted successfully.")
        except Exception as e:
            print(f"Failed to delete credential. Error: {str(e)}")
            # Add back to list if save failed
            self.credentials.insert(selection - 1, selected_cred)

    def exit_application(self):
        """Exit the application"""
        print()
        print("Thank you for using Password Manager. Goodbye!")
        raise SystemExit
