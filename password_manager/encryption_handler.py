"""
EncryptionHandler - Handles password encryption and decryption
Uses Fernet (symmetric encryption) with PBKDF2 key derivation from master password
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class EncryptionHandler:
    """Handles encryption and decryption of passwords using Fernet and PBKDF2"""

    SALT_LENGTH = 16  # 16-byte salt as specified
    ITERATIONS = 100000  # 100,000 iterations for PBKDF2

    def encrypt_password(self, plain_password, master_password):
        """
        Encrypt a password using Fernet with random salt

        Args:
            plain_password (str): The password to encrypt
            master_password (str): The master password to derive encryption key from

        Returns:
            str: Base64-encoded string combining salt + encrypted password
        """
        # Generate random 16-byte salt
        salt = os.urandom(self.SALT_LENGTH)

        # Derive encryption key from master password using PBKDF2
        key = self._derive_key(master_password, salt)

        # Encrypt the password using Fernet
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(plain_password.encode())

        # Combine salt + encrypted password and encode as Base64 for storage
        combined = salt + encrypted_password
        encrypted_stored_value = base64.b64encode(combined).decode()

        return encrypted_stored_value

    def decrypt_password(self, encrypted_stored_value, master_password):
        """
        Decrypt a password using Fernet with extracted salt

        Args:
            encrypted_stored_value (str): Base64-encoded string (salt + encrypted password)
            master_password (str): The master password to derive decryption key from

        Returns:
            str: The decrypted plain password
        """
        # Decode from Base64 to get combined salt + encrypted password
        combined = base64.b64decode(encrypted_stored_value.encode())

        # Extract salt (first 16 bytes) and encrypted password (rest)
        salt = combined[:self.SALT_LENGTH]
        encrypted_password = combined[self.SALT_LENGTH:]

        # Derive decryption key from master password using same salt
        key = self._derive_key(master_password, salt)

        # Decrypt the password using Fernet
        fernet = Fernet(key)
        plain_password = fernet.decrypt(encrypted_password).decode()

        return plain_password

    def _derive_key(self, master_password, salt):
        """
        Derive a Fernet-compatible encryption key from master password and salt

        Args:
            master_password (str): The master password
            salt (bytes): Random salt for key derivation

        Returns:
            bytes: Fernet-compatible key (44 characters base64-encoded)
        """
        # Use PBKDF2HMAC to derive a key from master password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes for AES-256
            salt=salt,
            iterations=self.ITERATIONS,
            backend=default_backend()
        )
        key_material = kdf.derive(master_password.encode())

        # Fernet requires base64-encoded key
        key = base64.urlsafe_b64encode(key_material)
        return key
