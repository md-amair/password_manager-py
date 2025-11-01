# Password Manager

> Console-based credential management system with industry-standard encryption. Operates entirely offline without external dependencies.

![Python](https://img.shields.io/badge/python-3.8+-blue) ![Status](https://img.shields.io/badge/status-production-brightgreen)

## Overview

Secure password management command-line interface built on object-oriented programming principles. Implements bcrypt and Fernet dual-layer encryption for local credential storage. Master password authentication provides controlled access to full CRUD operations on encrypted credentials stored in JSON format.

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

**Object-Oriented Design:** Five-class modular architecture
- `PasswordManager` - Application orchestrator, manages CRUD operations
- `AuthenticationManager` - Master password validation
- `EncryptionHandler` - Fernet and PBKDF2 cryptographic operations
- `CredentialStore` - JSON file input/output operations
- `MenuUI` - Console interface and presentation layer

**Security Implementation:**
- Master password: bcrypt adaptive hashing algorithm
- Credentials: Fernet (AES-128) symmetric encryption
- Key derivation: PBKDF2HMAC with 100,000 iterations and 16-byte salt per password
- Storage format: Base64-encoded encrypted data in JSON structure

## Dependencies

**External:**
- `bcrypt` - Master password hashing
- `cryptography` - Fernet encryption & PBKDF2

**Standard Library:**
- `json`, `uuid`, `os`, `sys`, `getpass`, `datetime`

## Error Handling

**Exception Management:**
- File I/O: Handles `FileNotFoundError`, `PermissionError`, `IOError`
- Parsing: Handles `json.JSONDecodeError` with file corruption notification
- Cryptography: Handles `InvalidToken` for decryption failures
- Input: Validates all user input, normalizes whitespace, enforces constraints
- Authentication: Three-attempt limit with session termination

**User Interface:** Descriptive error messages without stack traces, actionable guidance provided

## Programming Concepts

**Object-Oriented Programming:** Encapsulation, separation of concerns, dependency injection
**Design Patterns:** Controller pattern, Strategy pattern, Template method pattern
**Security Principles:** Defense in depth, principle of least privilege, fail-safe defaults
**Data Structures:** Dictionaries for credentials, lists for collections, UUIDs for unique identifiers
**Functional Programming:** Pure functions, immutability constraints, side-effect isolation

## Project Metrics

```
Lines of Code:     1,084
Modules:           7
Classes:           5
Operations:        6 (Add, View, Search, Edit, Delete, Exit)
Security Layers:   2 (bcrypt master password + Fernet credential encryption)
```

## License

MIT © [MD Amair](https://github.com/md-amair)
