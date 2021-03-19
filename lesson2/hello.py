from cryptotools.BTC import generate_keypair, push, script_to_address, OP

private, public = generate_keypair()
print(private.hex())
print(public.hex())
print(public.to_address('P2PKH'))


