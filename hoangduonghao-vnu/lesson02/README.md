# Lesson 2 assignment

## Generate a random private-public ECDSA key pair, base on 'secp256k1' parameters

* 'secp256k1' parameters: <http://www.secg.org/sec2-v2.pdf>
* Euclidean Algorithm and Multiplicative Inverses: <https://www.math.utah.edu/~fguevara/ACCESS2013/Euclid.pdf>

## Generate bitcoin address from ECDSA public key

* reference: <https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses>

## Setup

`python -m venv env`

`source env/bin/activate`

`pip install -r requirement.txt`

`python gen_key.py`
