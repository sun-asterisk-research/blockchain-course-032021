import secrets
from bitcoin import BitcoinWallet

#generate random private key
bits = secrets.randbits(256)
bits_hex = hex(bits)
private_key = bits_hex[2:]
print("private key:", private_key)

#genarate public key from private key
public_key = BitcoinWallet.private_to_public(private_key)
print("public key: ", public_key)

#genarate bitcoin address
address = BitcoinWallet.public_to_address(public_key)
print("bitcoin address: ", address)
