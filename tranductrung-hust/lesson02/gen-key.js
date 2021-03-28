const ec = require("elliptic").ec;
const sha256 = require('js-sha256');
const ripemd160 = require('ripemd160');
const base58 = require('bs58');
const crypto = require('crypto');

//convert Byte array to Hex string
function toHexString(byteArray) { 
    return Array.from(byteArray, function (byte) {
        return ('0' + (byte & 0xFF).toString(16)).slice(-2);
    }).join('')
}

//GENERATE PRIVATE KEY
var randArr = new Uint8Array(32); //create a typed array of 32 bytes (256 bits)
var privateKeyBytes = crypto.randomFillSync(randArr); //populate array with cryptographically secure random numbers
var privateKey = toHexString(privateKeyBytes); //hex string of our private key

//create ecdsa
const ecdsa = new ec('secp256k1');

//GENERATE PRIVATE KEY
var publicKey = ecdsa.keyFromPrivate(privateKey).getPublic('hex'),
    
//create SHA256 hash of public key
hash = sha256(Buffer.from(publicKey, 'hex')),
//create ripemd160 hash of SHA256 hash
publicKeyHash = new ripemd160().update(Buffer.from(hash, 'hex')).digest();

//GENERATE ADDRESS
const step1 = Buffer.from("00" + publicKeyHash.toString('hex'), 'hex');
// step 2 - create SHA256 hash of step 1
const step2 = sha256(step1);
// step 3 - create SHA256 hash of step 2
const step3 = sha256(Buffer.from(step2, 'hex'));
// step 4 - find the 1st byte of step 3 - save as "checksum"
const checksum = step3.substring(0, 8);
// step 5 - add step 1 + checksum
const step4 = step1.toString('hex') + checksum;
// return base 58 encoding of step 5
const address = base58.encode(Buffer.from(step4, 'hex'));

console.log("\nprivate key: " + privateKey);
console.log("\npublic key: " + publicKey);
console.log("\naddress: " + address);

