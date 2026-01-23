from cryptography.hazmat.primitives import hashes

# Read file
with open("Sample.txt", "rb") as f:
    data = f.read()

# Hash
digest = hashes.Hash(hashes.SHA256())
digest.update(data)
file_hash = digest.finalize()

print(file_hash.hex())  # unique fingerprint of file
