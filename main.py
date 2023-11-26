from utils import decrypt_message, encrypt_message, generate_keypair, encrypt, decrypt

public_key, secret_key = generate_keypair()
ciphertext, encryption_key = encrypt(public_key)
print(len(public_key), len(secret_key), len(encryption_key))
print(len(encryption_key), encryption_key.decode('charmap'))

formatted_key = bytearray(encryption_key)
print(formatted_key)

message = b"This is a message!"
encrypted_message = encrypt_message(formatted_key, message)
decrypted_message = decrypt_message(formatted_key, encrypted_message)