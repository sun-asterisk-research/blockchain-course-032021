####### with bitcoin module #######

from bitcoin import *

def one_hit():
	private_key = random_key()
	public_key = privtopub(private_key)
	address = pubtoaddr(public_key)
	
	return private_key, public_key, address


####### without bitcoin module #######

import random
import ecdsa
import codecs
import hashlib
import base58


def generate_private_key():
	bits = random.getrandbits(256)
	private_key = hex(bits)[2:]

	return private_key if private_key_is_valid(private_key) else generate_private_key()


def private_key_is_valid(private_key):
	min_value = int('0x01', 16)
	max_value = int('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140', 16)
	private_key_value = int(private_key, 16)
	
	return True if (private_key_value >= min_value and private_key_value <= max_value) else False
	
	
def generate_public_key(private_key):
	sk = ecdsa.SigningKey.from_string(codecs.decode(private_key, 'hex'), curve=ecdsa.SECP256k1)
	vk = sk.verifying_key
	# 04: uncompressed
	public_key = '04' + vk.to_string().hex()
	
	return public_key
	

def generate_bitcoin_address(public_key):
	encrypted_public_key = encryption_public_key(public_key)
	# add prefix version number
	encrypted_public_key = '00' + encrypted_public_key

	checksum = get_checksum(encrypted_public_key)

	hex_address = encrypted_public_key + checksum
	
	# encoding tmp_address with base58
	bitcoin_address_bytes = base58.b58encode(bytes.fromhex(hex_address))
	bitcoin_address = codecs.decode(bitcoin_address_bytes, 'utf-8')
	
	return bitcoin_address
	
# encrypted public key = RIPEMD-160(SHA-256(public key))
def encryption_public_key(public_key):
	public_key_bytes = codecs.decode(public_key, 'hex')
	# SHA-256 for the public key
	sha256_pkb = hashlib.sha256(public_key_bytes)
	# RIPEMD-160 for the SHA-256
	ripemd160_pkb = hashlib.new('ripemd160')
	ripemd160_pkb.update(sha256_pkb.digest())
	ripemd160_pkb_hex = ripemd160_pkb.digest().hex()
	
	return ripemd160_pkb_hex

# checksum = first 4 bytes of SHA-256(SHA-256(encrypted public key))
# note : - before add prefix version number for encrypted public key
#	 - 4 bytes = 8 bits
def get_checksum(encrypted_public_key):
	encrypted_public_key_bytes = codecs.decode(encrypted_public_key, 'hex')
	double_hash = hashlib.sha256(hashlib.sha256(encrypted_public_key_bytes).digest())
	double_hash_hex = double_hash.digest().hex()
	checksum = double_hash_hex[:8]

	return checksum
	

if __name__ == '__main__':
	
#	private_key, public_key, address = one_hit()
	
	private_key = generate_private_key()
	public_key = generate_public_key(private_key)
	address = generate_bitcoin_address(public_key)
	
	print('\n- private key:\n' + private_key + '\n')
	print('- public key:\n' + public_key + '\n')
	print('- bitcoin address:\n' + address + '\n')
	
	
	
	
	
	
	
