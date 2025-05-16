from cryptography.fernet import Fernet
import base64
import os

# Generate key once and reuse
SECRET_KEY = os.getenv('SECRET_KEY') or Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt_card_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_card_data(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

def mask_card_number(card_number: str) -> str:
    return '**** **** **** ' + card_number[-4:]
