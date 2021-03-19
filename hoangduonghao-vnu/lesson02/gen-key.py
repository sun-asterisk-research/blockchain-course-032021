#!/usr/bin/env python

import collections
import random
import hashlib
import time
import binascii
import base58


class Ecdsa(object):
    """ Elliptic Curve Digital Signature Algorithm (only for bitcoin case) """

    def __init__(self):
        """ Elliptic Curve 'secp256k1' parameters (only for bitcoin case): """
        EllipticCurve = collections.namedtuple(
            "EllipticCurve", "name p a b g n h")
        self.__curve = EllipticCurve(
            "secp256k1",
            p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
            a=0,
            b=7,
            g=(
                # x
                0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
                # y
                0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
            ),
            n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            h=1
        )

    def __inverse_mod(self, a, m):
        m0 = m
        x, y = 1, 0

        if a < 0:
            return m - self.__inverse_mod(-a, m)

        if (m == 1):
            return 0

        while (a > 1):
            q = a // m
            t = m
            m = a % m
            a = t
            t = y
            y = x - q * y
            x = t
        if (x < 0):
            x = x + m0

        return x

    def __is_on_curve(self, point):
        """ Returns True if the given point lies on the elliptic curve. """
        if point is None:
            return True
        x, y = point
        return (y**2 - x**3 - self.__curve.a * x - self.__curve.b) % self.__curve.p == 0

    def __add(self, point1, point2):
        """ Return the result of point1 + point2 according to the group law. """
        if point1 is None:
            return point2
        if point2 is None:
            return point1
        x1, y1 = point1
        x2, y2 = point2
        if x1 == x2 and y1 != y2:
            return None
        if x1 == x2:
            m = (3 * x1 * x1 + self.__curve.a) * \
                self.__inverse_mod(2 * y1, self.__curve.p)
        else:
            m = (y1 - y2) * self.__inverse_mod(x1 - x2, self.__curve.p)
        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % self.__curve.p, -y3 % self.__curve.p)
        return result

    def __scalar_multiply(self, k, point):
        """ Double and point_add algorithm """
        if k % self.__curve.n == 0 or point is None:
            return None
        result = None
        addend = point
        while k:
            if k & 1:
                result = self.__add(result, addend)
            addend = self.__add(addend, addend)
            k >>= 1
        assert self.__is_on_curve(result)
        return result

    def gen_key(self):
        """ Generate a random private-public key pair. """
        private_key = random.randrange(1, self.__curve.n - 1)
        public_key = self.__scalar_multiply(private_key, self.__curve.g)

        private_key = str(hex(private_key))[2:]
        public_key = "02" + str(hex(public_key[0]))[2:]
        return private_key, public_key


def createWalletAddress(public_key):
    public_key_sha256Hashing = hashlib.sha256(
        binascii.unhexlify(public_key)).hexdigest()

    hash256_ridemp160Hashing = hashlib.new(
        'ripemd160', binascii.unhexlify(public_key_sha256Hashing))
    
    add_version_number = '00' + hash256_ridemp160Hashing.hexdigest()

    hash = add_version_number

    for x in range(1, 3):
        hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()

    checksum = hash[:8]

    appendChecksum = add_version_number + checksum

    bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))

    return bitcoinAddress.decode('utf8')


def main():

    ecdsa = Ecdsa()
    private_key, public_key = ecdsa.gen_key()
    bitcoinAddress = createWalletAddress(public_key)

    print("Private key: ", private_key)
    print("Public key: ", public_key)
    print("Bitcoin address: ", bitcoinAddress)


if __name__ == "__main__":
    main()
