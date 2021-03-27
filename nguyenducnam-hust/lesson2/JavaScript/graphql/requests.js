const axios = require("axios");
const bitcoin = require("bitcoinjs-lib");

module.exports = {
  getPrices: async () => {
    const url = "https://blockchain.info/ticker?currency=MXN";
    try {
      return await axios.get(url);
    } catch (error) {
      console.error(error);
    }
  },
  generateKeyPairs: () => {
    /*It can generate a random address [and support the retrieval of transactions for that address (via 3PBP)*/
      const keyPair = bitcoin.ECPair.makeRandom();
      const { address } = bitcoin.payments.p2pkh({ pubkey: keyPair.publicKey });
      const publicKey = keyPair.publicKey.toString("hex");
      const privateKey = keyPair.toWIF();
      return { address, privateKey, publicKey };
    }
};