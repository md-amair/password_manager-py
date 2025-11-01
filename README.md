# Password Manager

> Offline console-based credential vault with military-grade encryption. Zero cloud, zero DB, zero BS.

![Python](https://img.shields.io/badge/python-3.8+-blue) ![Status](https://img.shields.io/badge/status-production-brightgreen)

## Overview

Secure password management CLI built on OOP principles. Implements bcrypt+Fernet dual-layer encryption for local credential storage. Master password authentication gates access to full CRUD operations on encrypted credentials stored in JSON.

## Quick Start

```bash
git clone https://github.com/md-amair/password_manager-py.git
cd password_manager-py
pip install bcrypt cryptography
python main.py
```

## Application Flow

```
Startup → Auth (bcrypt) → Menu Loop → Operations → Persist (JSON) → Exit
         ↓
    [First Run: Create Master Password]
    [Subsequent: Verify (3 attempts max)]
                ↓
         ┌──────────────┐
         │  Main Menu   │
         └──────┬───────┘
                ├─→ Add      (encrypt → store)
                ├─→ View     (load → decrypt → display)
                ├─→ Search   (filter → decrypt → mask → reveal)
                ├─→ Edit     (select → modify → re-encrypt → update)
                ├─→ Delete   (confirm → remove → persist)
                └─→ Exit     (clean shutdown)
```

## Architecture

**OOP Design:** 5-class modular architecture
- `PasswordManager` - Orchestrator, handles CRUD
- `AuthenticationManager` - Master password validation
- `EncryptionHandler` - Fernet+PBKDF2 crypto ops
- `CredentialStore` - JSON file I/O
- `MenuUI` - Console interface & display

**Security Stack:**
- Master password: bcrypt adaptive hashing
- Credentials: Fernet (AES-128) symmetric encryption
- Key derivation: PBKDF2HMAC (100k iterations, 16-byte salt/password)
- Storage: Base64-encoded encrypted data in JSON

## Dependencies

**External:**
- `bcrypt` - Master password hashing
- `cryptography` - Fernet encryption & PBKDF2

**Standard Library:**
- `json`, `uuid`, `os`, `sys`, `getpass`, `datetime`

## Error Handling

**Graceful Degradation Strategy:**
- File I/O: Catches `FileNotFoundError`, `PermissionError`, `IOError`
- Parsing: Catches `json.JSONDecodeError` → "File corrupted" message
- Crypto: Catches `InvalidToken` → Decryption failure handling
- Input: Validates all user input, trims whitespace, enforces constraints
- Auth: 3-strike policy, then exit

**User-Facing:** Friendly messages, no stack traces, actionable suggestions

## Programming Concepts

**OOP:** Encapsulation, separation of concerns, dependency injection
**Patterns:** Controller, Strategy, Template method
**Security:** Defense in depth, least privilege, fail-safe defaults
**Data:** Dicts (credentials), lists (collections), UUIDs (identifiers)
**Functional:** Pure functions, immutability, side-effect isolation

## Stats

```
LOC:        1,084 lines
Files:      7 modules
Classes:    5 (OOP design)
Operations: 6 (Add/View/Search/Edit/Delete/Exit)
Security:   2-layer (bcrypt + Fernet)
```

## License

MIT © [MD Amair](https://github.com/md-amair)
