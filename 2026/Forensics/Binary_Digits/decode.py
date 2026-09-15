data = open("digits.bin", "rb").read().strip()
bits = data.decode("ascii")


bits = "".join(bits.split())


pad = (-len(bits)) % 8
bits += "0" * pad

out = bytearray()
for i in range(0, len(bits), 8):
	out.append(int(bits[i:i+8], 2))
	
	open("decoded.bin", "wb").write(out)
	print("wrote", len(out), "bytes")
