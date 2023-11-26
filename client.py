import json
from socket import *
import sys
import time

from utils import CLIENT_SAMPLES, SERVER_PORT, PUBLIC_KEY_SIZE, capture_stats, encrypt, encrypt_message, flush_stats

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(('0.0.0.0', SERVER_PORT))
secret = b''

stats = []

# Pass 0 to read until the buffer is empty
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

def perform_handshake():
  global secret
  socket.send(b"REQT") # Request public key from server
  public_key = read_buffer(PUBLIC_KEY_SIZE) # Wait for public key from server
  
  # Time taken to generate secret
  start_time = time.process_time_ns()
  cipher, secret = encrypt(public_key)
  time_taken = time.process_time_ns() - start_time
  capture_stats(cipher, time_taken, "CIPHER")

  socket.send(b"CPHR" + cipher) # Send cipher to server
  ack = read_buffer(3) # Wait for acknowledgement
  if ack != b'ACK': raise Exception("Failed to share secret with server")
  return bytearray(secret)

def send_encrypted_message(message: str):
  global secret
  (encrypted_message, time) = encrypt_message(secret, message.encode())
  capture_stats(encrypted_message, time, "DATA")
  socket.send(b"DATA" + encrypted_message)

secret = perform_handshake()

# Send data 10 times
for _ in range(0, CLIENT_SAMPLES):
  send_encrypted_message("HELLO THERE")
  time.sleep(0.5)
  
flush_stats("client.json")
