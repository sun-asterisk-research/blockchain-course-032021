using System;
using NBitcoin;

namespace lesson2
{
    class Program
    {
        static void Main(string[] args)
        {
            var privateKey = new Key();

            var bitcoinPrivateKey = privateKey.GetWif(Network.Main);

            var bitcoinPublicKey = bitcoinPrivateKey.PubKey;

            var address = bitcoinPublicKey.GetAddress(ScriptPubKeyType.Segwit, Network.Main);

            Console.WriteLine("Private Key: " + bitcoinPrivateKey);
            Console.WriteLine("Public Key: " + bitcoinPublicKey);
            Console.WriteLine("Address: " + address);
        }
    }
}
