from cryptotools.BTC import generate_keypair, push, script_to_address, OP
privateKey, publicKey = generate_keypair()
print(privateKey.hex())
print(publicKey.hex())
print(publicKey.to_address('P2PKH'))