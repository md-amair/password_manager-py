# Implementation Plan - Password Manager

## Core Specifications

**Type:** Console-based credential manager
**Language:** Python 3.8+
**Architecture:** OOP (5 classes)
**Storage:** JSON file (local, no DB)
**Security:** bcrypt (master) + Fernet (credentials)

---

## System Architecture

### Class Structure

1. **PasswordManager** - Main controller
   - Orchestrates CRUD operations
   - Manages session state
   - Menu loop coordinator

2. **AuthenticationManager** - Access control
   - Master password verification (bcrypt)
   - First-run password creation
   - 3-attempt retry policy

3. **EncryptionHandler** - Crypto engine
   - Fernet symmetric encryption
   - PBKDF2HMAC key derivation (100k iterations)
   - Random 16-byte salt per password

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
- **First Run:** Create master password (8+ chars, confirm, bcrypt hash)
- **Login:** Verify password (3 attempts max, then exit)
- **Storage:** Hash stored in credentials.json

### 2. Add Credential
- **Input:** Website (1-100 chars), Username (1-100 chars), Password (1-500 chars)
- **Process:** Validate → Check duplicates (warn) → Encrypt password → Generate UUID → Save
- **Storage:** JSON with encrypted_password, created_at, updated_at timestamps

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

| Error Type | Exception | User Message |
|------------|-----------|--------------|
| File not found | FileNotFoundError | "No credentials saved yet" |
| File corrupted | json.JSONDecodeError | "Credentials file corrupted. Restore from backup." |
| Permission denied | PermissionError | "Cannot read/write file. Check permissions." |
| Decryption failed | InvalidToken | "Error decrypting password for [website]" |
| Invalid input | ValueError | Field-specific validation message |

**Policy:** Never expose stack traces. Always provide actionable guidance.

---

## Menu Interface

```
====== PASSWORD MANAGER ======
1. Add new credential
2. View all credentials
3. Search credentials
4. Edit credential
5. Delete credential
6. Exit
===============================
Enter your choice (1-6):
```

**Input Validation:**
- Trim whitespace
- Accept 1-6 only
- Invalid: "Invalid choice. Please enter 1-6."

**Password Input:**
- Use getpass module (hidden input)
- Cross-platform compatible

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

## Testing Checklist

- [x] First-run password creation with validation
- [x] Login with 3-attempt limit
- [x] Add credential with duplicate detection
- [x] View all with decryption
- [x] Search by website/username with reveal
- [x] Edit with selective field update
- [x] Delete with confirmation
- [x] Encryption/decryption roundtrip
- [x] File corruption handling
- [x] Permission error handling

---

## Notes

- No database required (JSON file storage)
- No internet connection needed (fully offline)
- No external services (local-only operation)
- Master password unrecoverable by design (security feature)
- Credentials never transmitted or logged
