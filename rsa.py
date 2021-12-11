import random
import requests
import utils


def phi(p: int, q: int):
    return (p - 1) * (q - 1)

def extended_gcd(num1: int, num2: int):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        g, y, x = extended_gcd(num2 % num1, num1)
        return (g, x - (num2 // num1) * y, y)

def encrypt(n: int, e: int, message: str):
    m = utils.bytes_to_int(message.encode())
    return pow(m, e, n)

def decrypt(n: int, d: int, c: int):
    m = pow(c, d, n)
    return utils.int_to_bytes(m).decode()

def get_private_key(e: int, p: int, q: int):
    return extended_gcd(e, phi(p, q))[1]

def factordb(n: int, json=False):
    "Queries the factordb api for known factors for the given number"
    req = requests.get('http://factordb.com/api', params={"query": n})
    data = req.json()
    if json:
        return data
    return data.get('factors', [])

def iroot(num: int, root: int) -> tuple[int, bool]:
    "Returns and integer root of the given number and also whether it is a perfect root or not"
    u, s = num, num+1
    while u < s:
        s = u
        t = (root-1) * s + num // pow(s, root-1)
        u = t // root
    return s, s ** root == num


class RSA:
    p: int
    q: int
    e: int
    d: int

    def generate_keys(self, length = 1024, e = 65537):
        self.p = self.generate_prime(length)
        self.q = self.generate_prime(length)

        # Get public key
        self.n = self.p * self.q
        self.e = e

        # Get private key
        self.d = get_private_key(e, self.p, self.q)

    def is_prime(self, num: int) -> bool:
        small_primes = (
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
            43, 47,53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        )

        for prime in small_primes:
            if num == prime:
                return True
            if num % prime == 0:
                return False
        
        return self.miller_rabin(num)

    def miller_rabin(self, num: int, k: int = 64) -> bool:
        # Write n as (2^r) x d + 1 with d odd 
        # (by factoring out powers of 2 from n − 1)
        d, r = num - 1, 0
        while d % 2 == 0:
            d //= 2
            r += 1

        # Do trials k times
        for _ in range(k):
            # pick a random integer a in the range [2, n − 2]
            # Compute: x = (a^d) % n
            # If x == 1 or x == n-1, return true.
            a = random.randint(2, num - 2)
            x = pow(a, d, num)

            if x != 1:
                # Do following until x == n-1, r - 1 times
                i = 0
                while x != (num - 1):
                    if i == r-1:
                        return False
                    else:
                        i += 1
                        x = pow(x, 2, num)
        return True

    def generate_prime(self, length: int) -> int:
        num = random.randrange(2**(length-1)+1, 2**(length)-1)

        while not self.is_prime(num):
            num = random.randrange(2**(length-1)+1, 2**(length)-1)
        
        return num


if __name__ == "__main__":
    r = RSA()
    r.generate_keys()

    message = "Hello World" * 23
    c = encrypt(message)
    m = decrypt(c)

    assert m == message