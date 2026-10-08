with open("encoded.bin", "rb") as f:
    data = f.read()

print(f"Read {len(data)} bytes")

# Try the default key
decoded = bytes((b - 42) % 256 for b in data)
print(decoded[:200])

# Or brute force in case the key is different
for key in range(256):
    d = bytes((b - key) % 256 for b in data)
    if b"flag{" in d.lower() or b"ctf{" in d.lower():
        print(f"KEY={key}: {d}")
