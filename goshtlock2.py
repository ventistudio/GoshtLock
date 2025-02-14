import os
import secrets
import hashlib
import base64
import shutil
import zipfile
import sys
# Vérification et installation des dépendances manquantes
def install_packages():
    try:
        import Crypto
    except ImportError:
        print("Installation des dépendances...")
        os.system(f"{sys.executable} -m pip install pycryptodome")
        print("Installation terminée. Relancez le script.")
        sys.exit()

install_packages()

from Crypto.Cipher import AES, ChaCha20, Blowfish
from Crypto.Util.Padding import pad, unpad

def generate_passwords(count=10, length=32):
    """Génère plusieurs mots de passe forts."""
    return [secrets.token_hex(length) for _ in range(count)]

def encrypt_data(data, passwords):
    """Chiffre les données en utilisant plusieurs couches de chiffrement."""
    for password in passwords:
        key = hashlib.sha256(password.encode()).digest()
        cipher_aes = AES.new(key, AES.MODE_CBC)
        data = cipher_aes.iv + cipher_aes.encrypt(pad(data, AES.block_size))
        
        cipher_chacha = ChaCha20.new(key=key[:32])
        data = cipher_chacha.nonce + cipher_chacha.encrypt(data)
        
        cipher_blowfish = Blowfish.new(key[:16], Blowfish.MODE_CBC)
        data = cipher_blowfish.iv + cipher_blowfish.encrypt(pad(data, Blowfish.block_size))
        
    return data

def decrypt_data(data, passwords):
    """Déchiffre les données en utilisant plusieurs couches inversées."""
    for password in reversed(passwords):
        key = hashlib.sha256(password.encode()).digest()
        
        iv_blowfish = data[:8]
        cipher_blowfish = Blowfish.new(key[:16], Blowfish.MODE_CBC, iv_blowfish)
        data = unpad(cipher_blowfish.decrypt(data[8:]), Blowfish.block_size)
        
        nonce_chacha = data[:8]
        cipher_chacha = ChaCha20.new(key=key[:32], nonce=nonce_chacha)
        data = cipher_chacha.decrypt(data[8:])
        
        iv_aes = data[:16]
        cipher_aes = AES.new(key, AES.MODE_CBC, iv_aes)
        data = unpad(cipher_aes.decrypt(data[16:]), AES.block_size)
        
    return data

def encrypt_file(file_path):
    """Chiffre un fichier et crée un .goshtlock"""
    passwords = generate_passwords()
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted_data = encrypt_data(data, passwords)
    
    with open(file_path + ".goshtlock", "wb") as f:
        f.write(encrypted_data)
    
    with open(file_path + ".keys", "w") as f:
        f.write("\n".join(passwords))
    print("Fichier chiffré avec succès !")

def decrypt_file(file_path, key_path):
    """Déchiffre un fichier .goshtlock avec les clés fournies"""
    with open(key_path, "r") as f:
        passwords = f.read().splitlines()
    
    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    
    try:
        decrypted_data = decrypt_data(encrypted_data, passwords)
        new_path = file_path.replace(".goshtlock", "_decrypted")
        with open(new_path, "wb") as f:
            f.write(decrypted_data)
        print(f"Fichier déchiffré avec succès : {new_path}")
    except Exception as e:
        print("Échec du déchiffrement. Mauvaises clés ?", e)

def encrypt_folder(folder_path):
    """Chiffre un dossier en le compressant avant."""
    zip_path = folder_path + ".zip"
    shutil.make_archive(folder_path, 'zip', folder_path)
    encrypt_file(zip_path)
    os.remove(zip_path)
    print(f"Dossier {folder_path} chiffré avec succès !")

def decrypt_folder(encrypted_zip_path, key_path):
    """Déchiffre un dossier compressé et le restaure."""
    decrypt_file(encrypted_zip_path, key_path)
    decrypted_zip_path = encrypted_zip_path.replace(".goshtlock", "_decrypted")
    folder_path = decrypted_zip_path.replace(".zip", "")
    
    with zipfile.ZipFile(decrypted_zip_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
    os.remove(decrypted_zip_path)
    print(f"Dossier {folder_path} restauré avec succès !")

# Exemple d'utilisation
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python goshtlock.py encrypt fichier.txt OU python goshtlock.py decrypt fichier.goshtlock fichier.keys")
    elif sys.argv[1] == "encrypt":
        if os.path.isdir(sys.argv[2]):
            encrypt_folder(sys.argv[2])
        else:
            encrypt_file(sys.argv[2])
    elif sys.argv[1] == "decrypt":
        if sys.argv[2].endswith(".zip.goshtlock"):
            decrypt_folder(sys.argv[2], sys.argv[3])
        else:
            decrypt_file(sys.argv[2], sys.argv[3])
