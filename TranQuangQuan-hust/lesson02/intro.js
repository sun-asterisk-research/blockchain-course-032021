const ec = require("elliptic").ec;
const sha256 = require('js-sha256');
const ripemd160 = require('ripemd160');
const base58 = require('bs58');
const crypto = require('crypto');

function toHexString(byteArray) { 
    return Array.from(byteArray, (byte) =>{
        return ('0' + (byte & 0xFF).toString(16)).slice(-2);}).join('')
}
var randArr = new Uint8Array(32); 
var privateKeyBytes = crypto.randomFillSync(randArr); 
var privateKey = toHexString(privateKeyBytes); 
const ecdsa = new ec('secp256k1');
var publicKey = ecdsa.keyFromPrivate(privateKey).getPublic('hex'),
hash = sha256(Buffer.from(publicKey, 'hex')),
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

const address = base58.encode(Buffer.from(step4, 'hex'));

console.log("\nprivate key: " + privateKey);
console.log("\npublic key: " + publicKey);
console.log("\naddress: " + address);