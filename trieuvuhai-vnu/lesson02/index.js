const secureRandom = require("secure-random");
const ec = require("elliptic").ec;
const sha256 = require('js-sha256');
const ripemd160 = require('ripemd160');
const base58 = require('bs58');

let Bitcoin = {};

Bitcoin.generatePrivateKey = () => {
    // generate ramdom private key
    const privateKey = secureRandom.randomBuffer(32).toString('hex');

    return privateKey;
};

Bitcoin.generatePublicKey = privateKey => {
    const ecdsa = new ec('secp256k1');
    // generate public key from private key with secp256k1
    const keys = ecdsa.keyFromPrivate(privateKey);
    const publicKey = keys.getPublic('hex');

    return publicKey;
}

Bitcoin.generatePublicKeyHash = publicKey => {
    // get publickey hash
    const hash = sha256(Buffer.from(publicKey, 'hex'));
    const publicKeyHash = new ripemd160().update(Buffer.from(hash, 'hex')).digest();

    return publicKeyHash;
}

Bitcoin.generatePublicAddress = publicKeyHash => {
    // step 1 - add prefix "00" in hex
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

    return address;
}

Bitcoin.generate = () => {
    const privateKey = Bitcoin.generatePrivateKey();
    console.log(`Private Key ${privateKey}`);
    const publicKey = Bitcoin.generatePublicKey(privateKey);
    console.log(`Public Key: ${publicKey}`);
    const publicKeyHash = Bitcoin.generatePublicKeyHash(publicKey);
    const address = Bitcoin.generatePublicAddress(publicKeyHash);
    console.log(`Address: ${address}`);
}

Bitcoin.generate();
