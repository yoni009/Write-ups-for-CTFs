with open("team_417.sav", "rb") as f:
    data = f.read()

print("Offset 0-12 (Header) :", data[:12].hex())
print("Offset 12-80 (Body)  :", data[12:80])
print("Hex View             :", data[12:80].hex())
