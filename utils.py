import json
import time
import pqcrypto.kem.saber as algorithm
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

generate_keypair = algorithm.generate_keypair
decrypt = algorithm.decrypt
encrypt = algorithm.encrypt

PUBLIC_KEY_SIZE = algorithm.PUBLIC_KEY_SIZE
CIPHER_SIZE = algorithm.CIPHERTEXT_SIZE
SERVER_PORT = 8001
CLIENT_SAMPLES = 10
ALGORITHM = algorithm.__name__.split('.')[2]
AES_IV = '1234123412341234'.encode('utf8')

stats = []
def capture_stats(data: bytes, delay: int, label: str):
  global stats
  stats.append({
    "length": len(data),
    "time": round(delay, 6),
    "label": label,
    "timestamp": time.time_ns()
  })

  return data

def flush_stats(filename: str):
  global stats
  file = open(f"./stats/{filename}", "w+")
  file.write(json.dumps({
    "algorithm": ALGORITHM,
    "public_key_size": algorithm.PUBLIC_KEY_SIZE,
    "cipher_text_size": algorithm.CIPHERTEXT_SIZE,
    "secret_key_size": algorithm.SECRET_KEY_SIZE,
    "plaintext_size": algorithm.PLAINTEXT_SIZE,
    "samples": CLIENT_SAMPLES,
    "stats": stats
  }))

def setup_cipher(key: bytes):
  return AES.new(key, AES.MODE_CBC, AES_IV)

def encrypt_message(key: str, message: str):
  start = time.process_time_ns()
  padded_message = pad(message, AES.block_size)
  cipher = setup_cipher(key)
  return (cipher.encrypt(padded_message), time.process_time_ns() - start)
  
def decrypt_message(key: str, message: bytes):
  cipher = setup_cipher(key)
  decrypted_message = cipher.decrypt(message)
  return unpad(decrypted_message, AES.block_size)

def load_public_key():
  public_key_file = open('./keys/key.pub', 'rb')
  public_key = public_key_file.read()
  if (len(public_key) == 0): raise Exception("Failed to load public key...")
  return public_key

def load_private_key():
  private_key_file = open('./keys/key.pem', 'rb')
  private_key = private_key_file.read()
  if (len(private_key) == 0): raise Exception("Failed to load private key...")
  return private_key