let elliptic = require('elliptic');
let sha3_256 = require('js-sha3').sha3_256;
let ec = new elliptic.ec('secp256k1');
let crypto = require('crypto');

let privKey = crypto.randomBytes(32).toString('hex');

// let keyPair = ec.genKeyPair();
let keyPair = ec.keyFromPrivate(privKey);

let pubKey = keyPair.getPublic();

console.log(`Private key: ${privKey}`);
console.log("Public key :", pubKey.encode("hex").substr(2));
console.log("Public key (compressed):", pubKey.encodeCompressed("hex"));

hash = sha3_256(Buffer.from(publicKey, 'hex'));
publicKeyHash = new ripemd160().update(Buffer.from(hash, 'hex')).digest();  