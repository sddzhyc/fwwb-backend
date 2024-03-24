# from Crypto.Cipher import AES
# import base64
# import os
from cryptography.fernet import Fernet

class CrypteService:
    def __init__(self, key=b'66nK9iaCXgCBkRU_li5n5VGz00ZzPoPGa3AEe7Pkxp8=') -> None:
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data: str) -> str:
        """Encrypts the data."""
        cipher_text = self.cipher_suite.encrypt(data.encode())
        return cipher_text.decode()

    def decrypt_data(self, cipher_text: str) -> str:
        """Decrypts the data."""
        data = self.cipher_suite.decrypt(cipher_text.encode())
        return data.decode()

    #对字典中的所有字符串进行加密
    def encrypt_dict(self, data: dict) -> dict:
        for key in data:
            if isinstance(data[key], str):
                data[key] = self.encrypt_data(data[key])
        return data
    #对字典中的所有字符串进行解密
    def decrypt_dict(self, data: dict) -> dict:
        for key in data:
            if isinstance(data[key], str):
                data[key] = self.decrypt_data(data[key])
        return data


key = b'66nK9iaCXgCBkRU_li5n5VGz00ZzPoPGa3AEe7Pkxp8='

#test


def test_encrypt_data():
    # Arrange
    service = CrypteService(key)
    data = "Hello, World!"

    # Act
    encrypted_data = service.encrypt_data(data)

    # Assert
    assert encrypted_data != data
    assert isinstance(encrypted_data, str)

def test_decrypt_data():
    # Arrange
    service = CrypteService(key)
    data = "Hello, World!"
    encrypted_data = service.encrypt_data(data)

    # Act
    decrypted_data = service.decrypt_data(encrypted_data)

    # Assert
    assert decrypted_data == data
    assert isinstance(decrypted_data, str)

def test_custom_key():
    # Arrange
    key = b'66nK9iaCXgCBkRU_li5n5VGz00ZzPoPGa3AEe7Pkxp8='
    service = CrypteService(key=key)
    data = "Hello, World!"

    # Act
    encrypted_data = service.encrypt_data(data)
    decrypted_data = service.decrypt_data(encrypted_data)

    # Assert
    assert decrypted_data == data
    assert isinstance(encrypted_data, str)
    assert isinstance(decrypted_data, str)

def test_invalid_key():
    # Arrange
    key = b'invalid_key'
    service = CrypteService(key=key)
    data = "Hello, World!"

    # Act
    encrypted_data = service.encrypt_data(data)
    decrypted_data = service.decrypt_data(encrypted_data)

    # Assert
    assert decrypted_data != data
    assert isinstance(encrypted_data, str)
    assert isinstance(decrypted_data, str)

test_encrypt_data()
