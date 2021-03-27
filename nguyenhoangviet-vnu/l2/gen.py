import collections
import numpy as np
import math
a = 0
b = 7
p = pow(2,256) - pow(2, 32) - pow(2,9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1

x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 
y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

G = (x,y)
def inverse_mod(k, p):
    """Returns the inverse of k modulo p.
    This function returns the only integer x such that (x * k) % p == 1.
    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p

def add(X,Y):
	if X[0] == 0 and X[1] == 0: return Y
	if Y[0] == 0 and Y[1] == 0: return X
	if X[0] == Y[0]:
		if X[1] == -Y[1]: return(0,0)

	if X[0] == Y[0]:
		lamda = (3 * X[0] * X[0]+ a) / inverse_mod(2 * X[1], p)
	else :
		lamda = (X[1] - Y[1]) * inverse_mod(X[0] - Y[0], p)

	x = lamda * lamda - X[0] - X[1]
	y = X[1] + lamda * (x - X[0])

	return (x % p, -y % p)

def pow(X, n):
	if n == 1: 
		return X
	if n == 2: 
		return add(X,X)

	halve = pow(X,n/2)
	m = add(halve, halve)

	if n % 2 == 0: return m
	return add(m, X)

def check(x,y):
	return (x * x * x + 7 - y * y) % p

privateKey = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDCE6AF48A03BBFD25E8CD0364140

while privateKey > 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140:
	privateKey = 0
	for i in range(0,8):
		privateKey = privateKey * 0xFFFF + np.random.choice(0xFFFF)

print(privateKey)
publicKey = pow(G,privateKey)
x = format(publicKey[0], 'x')
y = format(publicKey[1], 'x')
print("0x04" + x + y)
