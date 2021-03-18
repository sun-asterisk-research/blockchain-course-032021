let crypto = require('crypto');
let elliptic = require('elliptic');
let ec = new elliptic.ec('secp256k1');
let sha256 = require('js-sha256');
let ripemd160 = require('ripemd160');
let base58 = require('bs58');


//securely randomly generate 256 bits (32 bytes)
let privateKey = crypto.randomBytes(32).toString('hex');

//get public and private key from ecdsa
let publicKey =  ec.keyFromPrivate(privateKey).getPublic();

console.log(`Private key: ${privateKey}`);
console.log("Public key :", publicKey.encode("hex").substr(2));

//Perform SHA-256 hashing on the public key
let hash = sha256.create();
hash.update(publicKey.encode("hex").substr(2));

var pubKeyHash = hash.hex();

//Perform RIPEMD-160 hashing on the result of SHA-256
let step1 = new ripemd160().update(pubKeyHash).digest();
//Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
let step2 = Buffer.from("00" + step1.toString('hex'), 'hex');
//Perform SHA-256 hash on the extended RIPEMD-160 result
let step3 = sha256(step2);
//Perform SHA-256 hash on the result of the previous SHA-256 hash
let step4 = sha256(step3);
//Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
let checksum = step4.substring(0, 8);
//Add the 4 checksum bytes at the end of extended RIPEMD-160 hash from step 2
let step5 = step2.toString('hex') + checksum;
//Convert the result from a byte string into a base58 string using Base58Check encoding
let address = base58.encode(Buffer.from(step5, 'hex'));

console.log('Address: ' + address.toString());
console.log(address.toString().length);



