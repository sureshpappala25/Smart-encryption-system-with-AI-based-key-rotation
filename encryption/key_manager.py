from cryptography.fernet import Fernet
import os
from Crypto.PublicKey import RSA

KEY_FILE = "current_key.key"
RSA_PRIVATE_FILE = "private_key.pem"
RSA_PUBLIC_FILE = "public_key.pem"


def generate_key():
    """Generates a standard symmetric key (Fernet/AES compatible)."""
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

    return key


def generate_rsa_keys():
    """Generates a new RSA key pair for advanced security levels."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(RSA_PRIVATE_FILE, "wb") as f:
        f.write(private_key)
    with open(RSA_PUBLIC_FILE, "wb") as f:
        f.write(public_key)

    return public_key, private_key


def load_key():
    """Loads the symmetric key, generating it if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        return generate_key()

    with open(KEY_FILE, "rb") as f:
        key = f.read()

    return key


def load_rsa_keys():
    """Loads RSA keys, generating them if they don't exist."""
    if not os.path.exists(RSA_PRIVATE_FILE) or not os.path.exists(RSA_PUBLIC_FILE):
        return generate_rsa_keys()

    with open(RSA_PRIVATE_FILE, "rb") as f:
        priv = f.read()
    with open(RSA_PUBLIC_FILE, "rb") as f:
        pub = f.read()

    return pub, priv


def generate_file_specific_key():
    """Generates a unique symmetric key for an individual file (Fernet/AES compatible)."""
    return Fernet.generate_key().decode()