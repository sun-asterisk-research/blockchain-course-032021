import secrets
import codecs
import hashlib
import ecdsa # 0.16.1
import base58check

### Private key ###
key = secrets.randbits(256)
private_key = hex(key)[2:]
    
### Public key ###
private_key_bytes = codecs.decode(private_key, 'hex')

# ECDSA public key
key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
key_bytes = key.to_string()
key_hex = codecs.encode(key_bytes, 'hex')

# Add bitcoin byte
bitcoin_byte = b'04'
public_key = bitcoin_byte + key_hex

### Address ###
public_key_bytes = codecs.decode(public_key, 'hex')

# SHA256
sha256_pkb = hashlib.sha256(public_key_bytes)
sha256_pkb = sha256_pkb.digest()

# RIPEMD-160
ripemd160_pkb = hashlib.new('ripemd160')
ripemd160_pkb.update(sha256_pkb)
ripemd160_pkb = ripemd160_pkb.digest()
ripemd160_pkb_hex = codecs.encode(ripemd160_pkb, 'hex')

# Add network byte
network_byte = b'00'
network_pkb = network_byte + ripemd160_pkb_hex
network_pkb_hex = codecs.decode(network_pkb, 'hex')

# Double SHA256
sha256_1_pkb = hashlib.sha256(network_pkb_hex)
sha256_1_pkb = sha256_1_pkb.digest()
sha256_2_pkb = hashlib.sha256(sha256_1_pkb)
sha256_2_pkb = sha256_2_pkb.digest()
sha256_2_hex = codecs.encode(sha256_2_pkb, 'hex')

# Checksum
checksum = sha256_2_hex[:8]

# Append checksum
address_hex = (network_pkb + checksum).decode('utf-8')
address_byte = codecs.decode(address_hex, 'hex')

# Base58
wallet_address = base58check.b58encode(address_byte)

print(wallet_address)