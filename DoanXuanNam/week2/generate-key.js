const crypto = require('crypto');
const Base58 = require('bs58');
const EC = require('elliptic').ec;
const sha256 = require('js-sha256');
const ripemd160 = require('ripemd160');
const { randomFillSync } = require("crypto");

// 1.Generate private key
var a = new Uint8Array(32); 
var _privateKey = Buffer.from(randomFillSync(a).buffer, a.byteOffset, a.byteLength).toString('hex');
console.log("Private Key is : ",_privateKey);


// 2.Generate public key
var ecdsa = new EC('secp256k1');
var _publicKey = ecdsa.keyFromPrivate(_privateKey).getPublic('hex');
console.log("Public Key is : ",_publicKey);


// 3.Generate address
function generateAddress(publicKey) {
    const ripemd160_encode = new ripemd160();
    const hash1 = sha256.create();
    
    var first_key = "0x04" + publicKey;// + 0x04
    var second_key = hash1.update(first_key).hex();
    var third_key = ripemd160_encode.update(second_key).digest('hex');


    var mainnetKey = "0x6f" + third_key;
    var hash2 = sha256.create();
    var fourth_key = hash2.update(mainnetKey).hex();


    var hash3 = sha256.create();
    var fifth_key = hash3.update(fourth_key).hex();

    var checksum = fifth_key.substr(0,8);
    var subKey2 = mainnetKey + checksum;
    var inputKey = subKey2.substr(2,subKey2.length);

    var input = Buffer.from(inputKey,'hex');
    var address = Base58.encode(input);

    return "1" + address;
}

console.log("Address is : ",generateAddress(_publicKey))


