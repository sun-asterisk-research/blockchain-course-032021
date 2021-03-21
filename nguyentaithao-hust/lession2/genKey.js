const crypto = require('crypto');

//convert Byte array to Hex string
function toHexString(randArray) { 
    return Array.from(randArray, function (byte) {
        return ('0' + (byte & 0xFF).toString(16)).slice(-2);
    }).join('')
}

// generating private key
let privateKey = new Uint8Array(32);; 
crypto.randomFillSync(privateKey);
privateKey = toHexString(privateKey);






// show result
console.log('> Private key: ', privateKey);