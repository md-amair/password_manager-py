"""
MenuUI - Console user interface for password manager
Handles menu display, input collection, and table formatting
"""

import os
import sys
import getpass


class MenuUI:
    """Handles console-based user interface and menus"""

    MENU_WIDTH = 30

    def display_main_menu(self):
        """
        Display main menu and get user choice

        Returns:
            int: User's choice (1-6), or None if invalid input
        """
        print()
        print("====== PASSWORD MANAGER ======")
        print("1. Add new credential")
        print("2. View all credentials")
        print("3. Search credentials")
        print("4. Edit credential")
        print("5. Delete credential")
        print("6. Exit")
        print("===============================")

        while True:
            choice = self.get_user_input("Enter your choice (1-6): ")
            if choice and choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("Invalid choice. Please enter 1-6.")

    def get_user_input(self, prompt):
        """
        Get user input and trim whitespace

        Args:
            prompt (str): The prompt to display

        Returns:
            str: The user's input (trimmed)
        """
        try:
            user_input = input(prompt)
            return user_input.strip()
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            raise SystemExit
        except Exception as e:
            print(f"Error reading input: {str(e)}")
            return ""

    def get_password_input(self, prompt):
        """
        Get password input with masking (asterisks)

        Args:
            prompt (str): The prompt to display

        Returns:
            str: The password entered
        """
        try:
            # Use getpass for secure password input with masking
            password = getpass.getpass(prompt)
            return password
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            raise SystemExit
        except Exception as e:
            print(f"Error reading password: {str(e)}")
            return ""

    def display_table(self, credentials, mask_passwords=False, reveal_password=None):
        """
        Display credentials in a formatted table

        Args:
            credentials (list): List of credential dictionaries
            mask_passwords (bool): If True, show passwords as asterisks
            reveal_password (dict): Dict with {credential_id: plaintext_password} for selective reveal
        """
        if not credentials:
            print()
            print("No credentials saved yet.")
            print()
            return

        # Column widths
        website_width = 20
        username_width = 20
        password_width = 20
        created_width = 25
        updated_width = 25

        # Print header
        print()
        print("====== YOUR CREDENTIALS ======")
        print(f"{'Website':<{website_width}} | {'Username':<{username_width}} | {'Password':<{password_width}} | {'Created (YY-MM-DD HH:MM)':<{created_width}} | {'Updated (YY-MM-DD HH:MM)':<{updated_width}}")
        print("-" * 130)

        # Print rows
        for credential in credentials:
            website = self._truncate(credential.get('website', ''), website_width)
            username = self._truncate(credential.get('username', ''), username_width)

            if mask_passwords:
                password = "****"
            else:
                password = self._truncate(credential.get('decrypted_password', '****'), password_width)

            created = self._format_timestamp(credential.get('created_at', 'N/A'))
            updated = self._format_timestamp(credential.get('updated_at', 'N/A'))

            print(f"{website:<{website_width}} | {username:<{username_width}} | {password:<{password_width}} | {created:<{created_width}} | {updated:<{updated_width}}")

        print("-" * 130)
        print(f"Total: {len(credentials)} credential{'s' if len(credentials) != 1 else ''}")
        print()

    def display_search_results(self, credentials):
        """
        Display search results with masked passwords

        Args:
            credentials (list): List of matching credentials (with decrypted_password field)
        """
        if not credentials:
            print()
            print("No credentials match your search.")
            print()
            return

        # Column widths
        website_width = 20
        username_width = 25
        password_width = 30

        # Print header
        print()
        print("====== SEARCH RESULTS ======")
        print(f"{'Website':<{website_width}} | {'Username':<{username_width}} | {'Password':<{password_width}}")
        print("-" * 75)

        # Print rows (with masked passwords)
        for credential in credentials:
            website = self._truncate(credential.get('website', ''), website_width)
            username = self._truncate(credential.get('username', ''), username_width)
            password = "****"

            print(f"{website:<{website_width}} | {username:<{username_width}} | {password:<{password_width}}")

        print("-" * 75)
        print(f"Found {len(credentials)} credential{'s' if len(credentials) != 1 else ''}")
        print()

    def display_edit_list(self, credentials):
        """
        Display numbered list of credentials for edit selection

        Args:
            credentials (list): List of credentials to display

        Returns:
            int: User's selection (1 to len, or 0 to cancel), or -1 if invalid
        """
        if not credentials:
            print()
            print("No credentials to edit.")
            print()
            return -1

        print()
        print("====== SELECT CREDENTIAL TO EDIT ======")
        print()

        for i, credential in enumerate(credentials, 1):
            website = credential.get('website', '')
            username = credential.get('username', '')
            print(f"{i}. {website} ({username})")

        print("========================================")
        print()

        while True:
            choice = self.get_user_input("Enter the number (or 0 to cancel): ")
            if choice == "0":
                return 0  # Cancel

            try:
                num = int(choice)
                if 1 <= num <= len(credentials):
                    return num
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid selection. Please enter a valid number.")

    def display_delete_list(self, credentials):
        """
        Display numbered list of credentials for deletion selection

        Args:
            credentials (list): List of credentials to display

        Returns:
            int: User's selection (1 to len, or 0 to cancel), or -1 if invalid
        """
        if not credentials:
            print()
            print("No credentials to delete.")
            print()
            return -1

        print()
        print("====== SELECT CREDENTIAL TO DELETE ======")
        print()

        for i, credential in enumerate(credentials, 1):
            website = credential.get('website', '')
            username = credential.get('username', '')
            print(f"{i}. {website} ({username})")

        print("=========================================")
        print()

        while True:
            choice = self.get_user_input("Enter the number (or 0 to cancel): ")
            if choice == "0":
                return 0  # Cancel

            try:
                num = int(choice)
                if 1 <= num <= len(credentials):
                    return num
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid selection. Please enter a valid number.")

    def display_delete_confirmation(self, credential):
        """
        Display credential details for deletion confirmation

        Args:
            credential (dict): The credential to confirm deletion for

        Returns:
            bool: True if user confirms (yes), False otherwise
        """
        print()
        print("====== DELETE CONFIRMATION ======")
        print(f"Website: {credential.get('website', '')}")
        print(f"Username: {credential.get('username', '')}")
        print(f"Password: {credential.get('decrypted_password', '')}")
        print("====================================")

        while True:
            response = self.get_user_input("Are you sure? (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")

    def clear_screen(self):
        """Clear the console screen (cross-platform)"""
        try:
            if sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
        except Exception:
            # If clear fails, just print newlines
            print("\n" * 5)

    @staticmethod
    def _truncate(text, width):
        """
        Truncate text to width with ellipsis if needed

        Args:
            text (str): Text to truncate
            width (int): Maximum width

        Returns:
            str: Truncated text
        """
        if len(text) > width:
            return text[:width-3] + "..."
        return text

    @staticmethod
    def _format_timestamp(timestamp):
        """
        Format ISO timestamp to a more readable format

        Args:
            timestamp (str): ISO timestamp string (YYYY-MM-DDTHH:MM:SS)

        Returns:
            str: Formatted timestamp (YYYY-MM-DD HH:MM)
        """
        if not timestamp or timestamp == 'N/A':
            return 'N/A'
        
        try:
            # Format: 2024-01-15T14:30:45 -> 2024-01-15 14:30
            parts = timestamp.split('T')
            if len(parts) == 2:
                date = parts[0]
                time = parts[1].split(':')[:2]  # Take only hours and minutes
                return f"{date} {':'.join(time)}"
            return timestamp
        except Exception:
            return timestamp
            
