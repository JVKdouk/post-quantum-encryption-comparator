from socket import *
import sys
import time

from utils import ALGORITHM, CIPHER_SIZE, SERVER_PORT, capture_stats, decrypt, flush_stats, load_private_key, load_public_key, encrypt_message, decrypt_message

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', SERVER_PORT))
serverSocket.listen(0)

print(f'[SERVER] Loading Public Key...')
public_key = load_public_key()

print(f'[SERVER] Loading Private Key...')
private_key = load_private_key()

print(f'[SERVER] Running Algorithm {ALGORITHM}')
print(f'[SERVER] Listening on Port {SERVER_PORT}')

def read_buffer(size):
  data = b''
  total_bytes = 0

  while (total_bytes < size) if size > 0 else (True):
    try:
      segment = socket.recv(2048)
      if (size == 0): socket.setblocking(False)
    except BlockingIOError:
      socket.setblocking(True)
      break

    data += segment
    total_bytes += len(segment)
    
  return data

def send_encrypted_message(socket, message: str):
  global secret
  encrypted_message = encrypt_message(secret, message.encode())
  socket.send(encrypted_message)

while True:
  # Wait for connections to come through
  socket, addr = serverSocket.accept()
  secret = b'' # Connection secret, common between server and client
  
  while True:
    operation = socket.recv(4).decode('charmap')
    
    if len(operation) == 0:
      print("[SERVER] Client Terminated Connection")
      flush_stats("server.json")
      sys.exit(0)
      break
    
    match operation:
      case "REQT": # Receive Request
        print("[SERVER] Client Request Public Key")
        socket.send(public_key)
      case "CPHR": # Receive Cipher
        print("[SERVER] Decoding Cipher")
        cipher = read_buffer(CIPHER_SIZE)
        
        start_time = time.process_time_ns()
        secret = decrypt(private_key, cipher)
        time_taken = time.process_time_ns() - start_time
        capture_stats(cipher, time_taken, "CIPHER")
        
        print("[SERVER] Calculated Shared Secret")
        socket.send(b"ACK")
      case "DISC": # Disconnect
        socket.close()
        break
      case "DATA": # Encrypted Datagram
        data = read_buffer(0)
        
        start_time = time.process_time_ns()
        decrypted_message = decrypt_message(secret, data).decode()
        time_taken = time.process_time_ns() - start_time
        capture_stats(data, time_taken, "DATA")
        
        print("[SERVER] Got Data:", decrypted_message)