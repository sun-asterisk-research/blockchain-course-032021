import hashlib
import random
import codecs
import base58
import ecdsa


def privateKey():
    bits = random.getrandbits(256)
    bits_hex = hex(bits)
    private_key = bits_hex[2:]
    return private_key

#import secrets
#    bits = secrets.randbits(256)
#    bits_hex = hex(bits)
#    private_key = bits_hex[2:]

def generate_public_key(private_key):

    sk = ecdsa.SigningKey.from_string(codecs.decode(private_key, 'hex'), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key() #this is your verification key (public key)

    public_key = '04' + vk.to_string().hex()
    return public_key



def generate_bitcoin_address(public_key):
    encrypted_public_key = publicKey(public_key)
    encrypted_public_key = '00' + encrypted_public_key    #     add prefix version number
    checksum = checksum_func(encrypted_public_key)
    hex_address = encrypted_public_key + checksum
    # encoding tmp_address with base58
    bitcoin_address_bytes = base58.b58encode(bytes.fromhex(hex_address))
    bitcoin_address = codecs.decode(bitcoin_address_bytes, 'utf-8')
    return bitcoin_address

# Encrypting the public key SHA-256 and RIPEMD-160
def publicKey(public_key):
    public_key_bytes = codecs.decode(public_key, 'hex')#     Run SHA-256 for the public key
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()    # Run RIPEMD-160 for the SHA-256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_hex = ripemd160_bpk.digest().hex()

    return ripemd160_bpk_hex

# Checksum
def checksum_func(publicKey):
    publicKey_bytes = codecs.decode(publicKey, 'hex')
    sha256_nbpk = hashlib.sha256(publicKey_bytes)
    sha256_nbpk_digest = sha256_nbpk.digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_hex = sha256_2_nbpk.digest().hex()
    # sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    checksum = sha256_2_hex[:8]
    return checksum

if __name__ == '__main__':

    private_key = privateKey()
    public_key = generate_public_key(private_key)
    address = generate_bitcoin_address(public_key)

    print('\n# private key:\n' + private_key)
    print('# public key:\n' + public_key)
    print('# bitcoin address:\n' + address)