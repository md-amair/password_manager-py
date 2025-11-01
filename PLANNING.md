# Implementation Plan - Password Manager

## Core Specifications

**Type:** Console-based credential management system
**Language:** Python 3.8 or higher
**Architecture:** Object-oriented design with five classes
**Storage:** Local JSON file without database requirements
**Security:** bcrypt for master password, Fernet for credential encryption

---

## System Architecture

### Class Structure

1. **PasswordManager** - Main controller
   - Orchestrates CRUD operations
   - Manages session state
   - Menu loop coordinator

2. **AuthenticationManager** - Access control
   - Master password verification using bcrypt
   - Initial password creation workflow
   - Three-attempt authentication policy

3. **EncryptionHandler** - Cryptographic operations
   - Fernet symmetric encryption algorithm
   - PBKDF2HMAC key derivation with 100,000 iterations
   - Random 16-byte salt generated per password

4. **CredentialStore** - Persistence layer
   - JSON file I/O
   - Data serialization/deserialization
   - File permission management

5. **MenuUI** - Interface layer
   - Console rendering
   - Input validation & masking
   - Table formatting

---

## Operations

### 1. Authentication Flow
- **First Run:** Create master password (8 or more characters, confirmation required, bcrypt hashing)
- **Login:** Verify password (maximum three attempts, then session termination)
- **Storage:** Hash stored in credentials.json file

### 2. Add Credential
- **Input:** Website (1-100 characters), Username (1-100 characters), Password (1-500 characters)
- **Process:** Validate input, check for duplicates with warning, encrypt password, generate UUID, save to storage
- **Storage:** JSON format with encrypted_password, created_at, and updated_at timestamps

### 3. View Credentials
- **Flow:** Load JSON → Decrypt all passwords → Display table format
- **Output:** Website (20), Username (25), Password (30) columns with truncation
- **Error:** Handle decryption failures gracefully

### 4. Search Credentials
- **Input:** Search type (1=Website, 2=Username) + search term
- **Process:** Case-insensitive substring match → Decrypt → Display masked
- **Reveal:** Prompt per credential to show plaintext password

### 5. Edit Credential ⭐
- **Flow:** Select from list → Show current values → Prompt for new (blank=keep) → Re-encrypt if changed → Update timestamp
- **Fields:** Website, Username, Password (selective update)
- **Validation:** Same constraints as Add operation

### 6. Delete Credential
- **Flow:** Select from list → Show full details (decrypted) → Confirm → Remove → Clear screen
- **Confirmation:** Case-insensitive yes/no, default to no

### 7. Exit
- **Action:** Display goodbye message, clean shutdown

---

## Data Format

```json
{
  "master_password_hash": "$2b$12$...",
  "credentials": [
    {
      "id": "uuid4-string",
      "website": "example.com",
      "username": "user@example.com",
      "encrypted_password": "base64(salt+fernet_encrypted)",
      "created_at": "2025-10-31T10:30:00",
      "updated_at": "2025-10-31T15:45:00"
    }
  ]
}
```

---

## Security Implementation

### Master Password
- Algorithm: bcrypt with auto-generated salt
- Storage: Hashed only, never plaintext
- Validation: 3 failed attempts → exit

### Credential Encryption
- Algorithm: Fernet (AES-128 in CBC mode)
- Key Derivation: PBKDF2HMAC-SHA256, 100k iterations
- Salt: 16 random bytes per password (prepended to ciphertext)
- Encoding: Base64 for JSON storage

### File Permissions
- chmod 600 (owner read/write only) on Unix-like systems
- Graceful degradation on Windows

---

## Error Handling

**Exceptions Caught:** FileNotFoundError, PermissionError, json.JSONDecodeError, InvalidToken, ValueError
**Policy:** User-friendly messages, no stack traces, actionable guidance

---

## Menu Interface

6-option menu (Add/View/Search/Edit/Delete/Exit)
Input validation: Trim whitespace, accept 1-6, getpass for password masking

---

## File Structure

```
password_manager-py/
├── main.py                      # Entry point
├── credentials.json             # Data (auto-generated)
├── password_manager/
│   ├── __init__.py
│   ├── password_manager.py      # Controller
│   ├── auth_manager.py          # Authentication
│   ├── encryption_handler.py    # Crypto
│   ├── credential_store.py      # I/O
│   └── menu_ui.py               # Interface
├── README.md
├── PLANNING.md                  # This file
└── .gitignore
```

---

## Dependencies

**External:**
- bcrypt (5.0.0+)
- cryptography (46.0.0+)

**Standard Library:**
- json, uuid, os, sys, getpass, datetime

**Install:**
```bash
pip install bcrypt cryptography
```

---

## Implementation Status

✅ All 6 operations fully implemented
✅ Security layer complete (bcrypt + Fernet)
✅ Error handling comprehensive
✅ OOP architecture with 5 classes
✅ 1,084 lines of production code
✅ Cross-platform compatible

**Branch:** compyle/password-manager-console
**Repository:** https://github.com/md-amair/password_manager-py

---

## Notes

- Fully offline (no DB, no internet, no external services)
- Master password unrecoverable by design (security feature)
- All tests passed: Auth, CRUD, encryption, error handling
