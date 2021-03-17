import secrets
bits = secrets.randbits(256)
bitsHex = hex(bits)
pKey = bitsHex[2:]
print(pKey)