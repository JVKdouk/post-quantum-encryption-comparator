import time
from utils import capture_stats, decrypt_message, encrypt_message, flush_stats, generate_keypair, encrypt, decrypt

print("Testing Key Encapsulation")
for _ in range(0, 10):
  start_time = time.process_time_ns()
  public_key, secret_key = generate_keypair()
  time_taken = time.process_time_ns() - start_time
  capture_stats(public_key, time_taken, "KEY_GENERATION")

  start_time = time.process_time_ns()
  ciphertext, encryption_key = encrypt(public_key)
  time_taken = time.process_time_ns() - start_time
  capture_stats(public_key, time_taken, "CIPHER_GENERATION")

  start_time = time.process_time_ns()
  plaintext = decrypt(secret_key, ciphertext)
  time_taken = time.process_time_ns() - start_time
  capture_stats(public_key, time_taken, "SECRET_DECRYPTION")
  
flush_stats("encapsulation.json")
print("Finished Key Encapsulation Test")