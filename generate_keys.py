from utils import generate_keypair

public_key, secret_key = generate_keypair()
print("Generating Keys")

# Store keys for future usage
public_key_file = open("./keys/key.pub", "wb+")
public_key_file.write(public_key)
public_key_file.close()

private_key_file = open("./keys/key.pem", "wb+")
private_key_file.write(secret_key)
private_key_file.close()

print("Finished Key Generation")