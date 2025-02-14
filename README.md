# GoshtLock
Voici GoshtLock, un script qui chiffre et déchiffre des fichiers avec trois couches de chiffrement (AES, ChaCha20, Blowfish). Il génère 10 mots de passe uniques pour sécuriser les données et crée des fichiers .goshtlock. 🔒

## 📌 Utilisation :

**Chiffrer un fichier :**
```python goshtlock.py encrypt fichier.txt```
exemple : python C:\Users\starw\Desktop\goshtlock.py encrypt C:\Users\starw\Desktop\exemple
exemple : python C:\Users\starw\Desktop\goshtlock.py encrypt C:\Users\starw\Desktop\exemple.mp4

**Déchiffrer un fichier .goshtlock avec les clés :**
```python goshtlock.py decrypt fichier.goshtlock fichier.keys```
exemple : python C:\Users\starw\Desktop\goshtlock.py encrypt C:\Users\starw\Desktop\exemple.zip.goshtlock C:\Users\starw\Desktop\exemple.zip.keys
exemple : python C:\Users\starw\Desktop\goshtlock.py encrypt C:\Users\starw\Desktop\exemple.mp4.goshtlock C:\Users\starw\Desktop\exemple.mp4.keys
