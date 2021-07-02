import random
import utils


class RSA:
    def generate_keys(self, length = 1024, e = 65537):
        p = self.generate_prime(length)
        q = self.generate_prime(length)

        # Get public key
        self.n = p * q
        self.e = e

        # Get private key
        phi = (p - 1) * (q - 1)
        self.d = self.extended_gcd(e, phi)[1]


    def encrypt(self, message: str):
        m = utils.bytes_to_int(message.encode())
        return pow(m, self.e, self.n)

    def decrypt(self, c: int):
        m = pow(c, self.d, self.n)
        return utils.int_to_bytes(m).decode()

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
        for trials in range(k):
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

    def extended_gcd(self, num1, num2):
        if num1 == 0:
            return (num2, 0, 1)
        else:
            g, y, x = self.extended_gcd(num2 % num1, num1)
            return (g, x - (num2 // num1) * y, y)


if __name__ == "__main__":
    r = RSA()
    r.generate_keys()

    message = "Hello World" * 23
    c = r.encrypt(message)
    m = r.decrypt(c)

    assert m == message