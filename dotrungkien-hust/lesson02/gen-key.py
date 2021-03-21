import secrets
import codecs
import ecdsa
import hashlib
import base58

def gen_private_key():
  bits=secrets.randbits(256)
  bits_hex=hex(bits)
  private_key=bits_hex[2:]
  return private_key

def check_private_key(x):
  check_point='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141'
  check_point.lower()
  if x < check_point:
    return True
  return False

def private_to_public(private_key):
  private_key_bytes = codecs.decode(private_key, 'hex')
  # Get ECDSA public key
  key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
  key_bytes = key.to_string()
  key_hex = codecs.encode(key_bytes, 'hex')
  # Add bitcoin byte
  bitcoin_byte = b'04'
  public_key = bitcoin_byte + key_hex
  return public_key

def public_key_to_address(public_key):
  public_key_bytes = codecs.decode(public_key, 'hex')
  #apply SHA-256 to the public key
  sha256_pk = hashlib.sha256(public_key_bytes)
  #print(sha256_pk)
  sha256_pk_digest = sha256_pk.digest()
  #print(sha256_pk_digest)
  # apply ripemd160 to the SHA256
  ripemd160_pk = hashlib.new('ripemd160')
  ripemd160_pk.update(sha256_pk_digest)
  ripemd160_pk_digest = ripemd160_pk.digest()
  ripemd160_pk_hex = codecs.encode(ripemd160_pk_digest, 'hex')
  #print(ripemd160_pk_hex)
  step1=ripemd160_pk_hex
  #step 2 is add network byte in front of RIPEMD-160 hash
  network_bitcoin_public_key = b'00' + ripemd160_pk_hex
  step2=codecs.decode(network_bitcoin_public_key,'hex')
  #print(step2)
  #step3 is double SHA256 to checksum
  sha256_npk = hashlib.sha256(step2)
  sha256_npk_digest = sha256_npk.digest()
  sha256_2_npk = hashlib.sha256(sha256_npk_digest)
  sha256_2_npk_digest = sha256_2_npk.digest()
  sha256_2_hex = codecs.encode(sha256_2_npk_digest, 'hex')
  checksum = sha256_2_hex[:8]
  # Concatenate public key and checksum to get the address
  address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
  wallet_address = base58.b58encode(address_hex)
  return wallet_address

private_key=gen_private_key()
while (check_private_key(private_key)==False):
  private_key=gen_private_key()

public_key=private_to_public(private_key)
address=public_key_to_address(public_key)
print(' private_key:',private_key,'\n','public_key:',public_key.decode('utf-8'),'\n','address:',address.decode('utf-8'))
