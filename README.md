# 🔐 Password Manager

A secure, offline, Python-based console application for managing your login credentials locally without any database or internet connection.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production-brightgreen)

---

## ✨ Features

### 🛡️ **Security First**
- **Master Password Protection** - Single master password protects all credentials
- **bcrypt Hashing** - Industry-standard password hashing for master password
- **Fernet Encryption** - Symmetric encryption for stored passwords
- **PBKDF2 Key Derivation** - 100,000 iterations with random 16-byte salt per password
- **Local Storage Only** - No cloud, no database, no internet required

### 📋 **Full CRUD Operations**
1. **Add** - Create new credential entries with duplicate detection
2. **View** - Display all credentials in formatted table with decrypted passwords
3. **Search** - Filter by website or username with masked password display
4. **Edit** - Update existing credentials (website, username, or password)
5. **Delete** - Remove credentials with confirmation
6. **Exit** - Clean application shutdown

### 🎯 **User-Friendly Interface**
- Clean console-based menu system
- Password masking during input
- Table-formatted credential display
- Intuitive number-based selection
- Comprehensive error handling

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/md-amair/password_manager-py.git
   cd password_manager-py
   ```

2. **Install dependencies**
   ```bash
   pip install bcrypt cryptography
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 📖 Usage Guide

### First Run - Create Master Password

When you run the application for the first time:

```
Create a master password: ********
Confirm master password: ********

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

**Requirements:**
- Master password must be at least 8 characters
- Passwords must match
- You have 3 attempts on subsequent logins

---

### Main Menu Operations

#### 1️⃣ Add New Credential

```
Website/Application name: github.com
Username: myusername
Password: ********

Credential saved successfully.
```

**Validation:**
- Website: 1-100 characters
- Username: 1-100 characters
- Password: 1-500 characters
- Duplicate detection with override option

---

#### 2️⃣ View All Credentials

```
====== YOUR CREDENTIALS ======
Website              | Username              | Password
---------------------------------------------------------------------------
github.com           | myusername            | mySecurePass123
gmail.com            | user@gmail.com        | anotherPassword
---------------------------------------------------------------------------
Total: 2 credentials
```

- Displays all credentials with decrypted passwords
- Formatted table with automatic truncation
- Shows credential count

---

#### 3️⃣ Search Credentials

```
Search by (1=Website, 2=Username): 1
Enter search term: github

====== SEARCH RESULTS ======
Website              | Username              | Password
---------------------------------------------------------------------------
github.com           | myusername            | ****
---------------------------------------------------------------------------
Found 1 credential

Reveal password for github.com? (yes/no): yes
Password: mySecurePass123
```

**Features:**
- Case-insensitive partial matching
- Initial display with masked passwords
- Selective password reveal

---

#### 4️⃣ Edit Credential ⭐ NEW

```
====== SELECT CREDENTIAL TO EDIT ======

1. github.com (myusername)
2. gmail.com (user@gmail.com)

========================================

Enter the number (or 0 to cancel): 1

====== EDIT CREDENTIAL ======
Current Website: github.com
Current Username: myusername
Current Password: mySecurePass123
=============================

Leave blank to keep current value

New Website [github.com]:
New Username [myusername]: newusername
Password (leave blank to keep current):

Credential updated successfully.
```

**Features:**
- Select credential from numbered list
- View current values
- Update any field (leave blank to keep current)
- Password re-encryption on change
- Automatic timestamp update

---

#### 5️⃣ Delete Credential

```
====== SELECT CREDENTIAL TO DELETE ======

1. github.com (myusername)
2. gmail.com (user@gmail.com)

=========================================

Enter the number (or 0 to cancel): 1

====== DELETE CONFIRMATION ======
Website: github.com
Username: myusername
Password: mySecurePass123
====================================
Are you sure? (yes/no): yes

Credential deleted successfully.
```

**Features:**
- Numbered selection
- Full credential details shown
- Confirmation required
- Screen cleared after deletion

---

#### 6️⃣ Exit

```
Thank you for using Password Manager. Goodbye!
```

Clean application shutdown with data persisted to file.

---

## 🏗️ Architecture

### Project Structure

```
password_manager-py/
├── main.py                          # Application entry point
├── credentials.json                 # Encrypted data storage (auto-generated)
├── password_manager/
│   ├── __init__.py                  # Package initializer
│   ├── password_manager.py          # Main controller (CRUD operations)
│   ├── auth_manager.py              # Authentication & master password
│   ├── encryption_handler.py        # Fernet encryption/decryption
│   ├── credential_store.py          # JSON file I/O operations
│   └── menu_ui.py                   # Console interface & display
├── README.md                        # This file
├── PLANNING.md                      # Detailed implementation plan
└── .gitignore                       # Git ignore rules
```

### Class Diagram

```
┌─────────────────────┐
│   PasswordManager   │ ◄─── Main Controller
│  (Orchestrates all) │
└──────────┬──────────┘
           │
           ├──► AuthenticationManager (Master password)
           │
           ├──► EncryptionHandler (Fernet + PBKDF2)
           │
           ├──► CredentialStore (JSON I/O)
           │
           └──► MenuUI (Console interface)
```

### Security Implementation

**Master Password:**
- Hashed with bcrypt (adaptive, salted)
- 3 login attempts maximum
- Never stored in plain text

**Credential Passwords:**
- Encrypted with Fernet (AES-128)
- Unique 16-byte salt per password
- PBKDF2HMAC key derivation (100,000 iterations)
- Base64 encoding for storage

**Data Storage:**
```json
{
  "master_password_hash": "$2b$12$...",
  "credentials": [
    {
      "id": "uuid-here",
      "website": "example.com",
      "username": "user@example.com",
      "encrypted_password": "base64-encoded-encrypted-data",
      "created_at": "2025-10-31T10:30:00",
      "updated_at": "2025-10-31T15:45:00"
    }
  ]
}
```

---

## 🔧 Technical Details

### Dependencies

**Required Packages:**
- `bcrypt` (5.0.0+) - Master password hashing
- `cryptography` (46.0.0+) - Password encryption

**Standard Library:**
- `json` - Data serialization
- `uuid` - Unique ID generation
- `os`, `sys` - System operations
- `getpass` - Secure password input
- `datetime` - Timestamp handling

### Installation Commands

```bash
# Using pip
pip install bcrypt cryptography

# Using pip with requirements (if you create requirements.txt)
pip install -r requirements.txt

# Using conda
conda install -c conda-forge bcrypt cryptography
```

### Python Version Support

- **Minimum:** Python 3.8
- **Recommended:** Python 3.10+
- **Tested on:** Python 3.12

### Platform Compatibility

✅ **Windows** - Full support
✅ **macOS** - Full support
✅ **Linux** - Full support

---

## 🛡️ Security Considerations

### What This Application Does
✅ Encrypts passwords with industry-standard algorithms
✅ Uses secure key derivation (PBKDF2 with 100k iterations)
✅ Stores data locally with file permissions
✅ Never logs or transmits passwords
✅ Implements authentication retry limits

### What This Application Does NOT Do
⚠️ Does not protect against malware on your computer
⚠️ Does not sync across devices
⚠️ Does not include backup/recovery mechanisms
⚠️ Does not protect against physical access to your machine

### Best Practices

1. **Choose a Strong Master Password**
   - At least 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Not reused from other services

2. **Backup Your Data**
   - Regularly backup `credentials.json`
   - Store backups in a secure location
   - Test restoration process

3. **Keep Your System Secure**
   - Use full-disk encryption
   - Keep OS and Python updated
   - Use antivirus software
   - Lock your computer when away

4. **Don't Share**
   - Never share your master password
   - Don't commit `credentials.json` to version control
   - Be cautious of screen sharing while using

---

## 📊 Project Statistics

- **Total Lines:** 1,084 lines of code
- **Files:** 7 Python modules
- **Classes:** 5 main classes (OOP design)
- **Operations:** 6 main operations (CRUD + Exit)
- **Security:** 2-layer encryption (bcrypt + Fernet)

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Solution: Install dependencies
pip install bcrypt cryptography
```

### "Permission denied" when running
```bash
# Solution: Make main.py executable (Unix/Linux/Mac)
chmod +x main.py
```

### "Credentials file corrupted" message
```bash
# Solution: Restore from backup or delete credentials.json to start fresh
# WARNING: Deleting credentials.json will erase all stored passwords
rm credentials.json
python main.py
```

### Forgot master password
Unfortunately, there is no recovery mechanism by design. The master password cannot be reset without losing all stored credentials. This is a security feature, not a bug.

**Prevention:**
- Write down master password and store securely
- Use a memorable but strong passphrase
- Consider using a password hint (but don't store it digitally)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue with details
2. **Suggest Features** - Describe your use case
3. **Submit Pull Requests** - Fix bugs or add features
4. **Improve Documentation** - Help others understand

### Development Setup

```bash
# Clone repository
git clone https://github.com/md-amair/password_manager-py.git
cd password_manager-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install bcrypt cryptography

# Run tests (if available)
python -m pytest
```

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**MD Amair**

- GitHub: [@md-amair](https://github.com/md-amair)
- Repository: [password_manager-py](https://github.com/md-amair/password_manager-py)

---

## 🙏 Acknowledgments

- **Python Cryptography Team** - For the excellent cryptography library
- **bcrypt Developers** - For secure password hashing
- **Open Source Community** - For inspiration and support

---

## 📚 Additional Resources

- [PLANNING.md](PLANNING.md) - Detailed implementation specifications
- [Python Cryptography Docs](https://cryptography.io/) - Encryption library documentation
- [bcrypt Documentation](https://github.com/pyca/bcrypt/) - Password hashing documentation

---

## ⚡ Quick Reference

### Common Commands
```bash
# Start application
python main.py

# Install dependencies
pip install bcrypt cryptography

# Backup data
cp credentials.json credentials.backup.json

# Reset application (WARNING: Deletes all data)
rm credentials.json
```

### Keyboard Shortcuts
- `Ctrl+C` - Cancel operation / Exit application
- `0` - Cancel selection (Edit/Delete operations)

---

## 🎯 Roadmap

Future enhancements being considered:

- [ ] Password generation feature
- [ ] Import/export functionality (CSV, JSON)
- [ ] Password strength indicator
- [ ] Credential categories/tags
- [ ] Recent passwords history
- [ ] Password expiry reminders
- [ ] Multi-language support
- [ ] GUI version (Tkinter/Qt)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐**

Made with ❤️ using Python

</div>