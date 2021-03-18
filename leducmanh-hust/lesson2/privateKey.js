let elliptic = require('elliptic');
let sha3_256 = require('js-sha3').sha3_256;
let ec = new elliptic.ec('secp256k1');
let crypto = require('crypto');
let ripemd160 = require('ripemd160');
let base58 = require('bs58');

//securely randomly generate 256 bits (32 bytes)
let privKey = crypto.randomBytes(32).toString('hex');

//get public and private key from ecdsa
let keyPair = ec.keyFromPrivate(privKey);

let pubKey = keyPair.getPublic();

console.log(`Private key: ${privKey}`);
console.log("Public key :", pubKey.encode("hex").substr(2));
console.log("Public key (compressed):", pubKey.encodeCompressed("hex"));

//SHA256 of public key
hash = sha3_256(Buffer.from(pubKey.encode("hex"), 'hex'));

//RIPEDM160 of SHA256
publicKeyHash = new ripemd160().update(Buffer.from(hash, 'hex')).digest();
 
//step 1 - add prefix "00" in hex
let step1 = Buffer.from("00" + publicKeyHash.toString('hex'), 'hex');
//step 2 - create SHA256 hash of step 1
let step2 = sha3_256(step1);
//step 3 - create SHA256 hash of step 2
let step3 = sha3_256(Buffer.from(step2, 'hex'));
//step 4 - find the 1st byte of step 3 - save as "checksum"
let checksum = step3.substring(0, 8);
//step 5 - add step 1 + checksum
let step4 = step1.toString('hex') + checksum;
//return base 58 encoding of step 5
let address = base58.encode(Buffer.from(step4, 'hex'));

console.log("Address:", address.toString());
console.log(address.toString().length)