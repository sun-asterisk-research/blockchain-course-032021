import hashlib
import base58
import ecdsa

from ecdsa.keys import SigningKey
from utilitybelt import dev_random_entropy
from binascii import hexlify, unhexlify

def random_secret_exponent(curve_order):
    while True:
        random_hex = hexlify(dev_random_entropy(32))
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            return random_int

def generate_private_key():
    curve = ecdsa.curves.SECP256k1
    se = random_secret_exponent(curve.order)
    from_secret_exponent = ecdsa.keys.SigningKey.from_secret_exponent
    return hexlify(from_secret_exponent(se, curve, hashlib.sha256).to_string())

def generate_public_key(private_key_hex):
    hash160 = ripe_hash(private_key_hex)
    public_key_and_version_hex = b"04" + hash160 
    checksum = double_hash(public_key_and_version_hex)[:4]
    return base58.b58encode(public_key_and_version_hex + checksum)

def ripe_hash(key):
    ret = hashlib.new('ripemd160')
    ret.update(hashlib.sha256(key).digest())
    return ret.digest()

def double_hash(key):
    return hashlib.sha256(hashlib.sha256(key).digest()).digest()

def main():
    private_key_hex = generate_private_key()
    public_key_hex = generate_public_key(private_key_hex)
    print("Private Key: {}".format(private_key_hex))
    print("Public Key: {}".format(public_key_hex))


if __name__ == '__main__':
    main()