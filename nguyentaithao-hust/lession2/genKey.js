let crypto = require('crypto');
let ec = require("elliptic").ec;
let sha256 = require('js-sha256');
let ripemd160 = require('ripemd160');
let base58 = require('bs58');

//convert Byte array to Hex string
function toHexString(randArray) { 
    return Array.from(randArray, function (byte) {
        return ('0' + (byte & 0xFF).toString(16)).slice(-2);
    }).join('')
}

// generating private key
var privateKey = new Uint8Array(32);
crypto.randomFillSync(privateKey);
privateKey = toHexString(privateKey);


//create ecdsa
const ecdsa = new ec('secp256k1');

// generating public key
var publicKey = ecdsa.keyFromPrivate(privateKey).getPublic('hex');


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


// show result
console.log('> Private key: ', privateKey);
console.log('> Public key: ', publicKey);
console.log('> Address: ', address);