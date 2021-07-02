import string


class Ceaser:
    def encrypt(self, message, shift=13, alphabet=string.ascii_uppercase):
        ciphertext = ""
        n = len(alphabet)
        for ch in message:
            if ch.isupper() and ch in alphabet.upper():
                ch = chr(((ord(ch) - 65) + shift) % n + 65) 
            elif ch.islower() and ch in alphabet.lower():
                ch = chr(((ord(ch) - 97) + shift) % n + 97) 

            ciphertext += ch
        
        return ciphertext
    
    def decrypt(self, ciphertext, shift=13, alphabet=string.ascii_uppercase):
        return self.encrypt(ciphertext, -shift, alphabet)


if __name__ == "__main__":
    c = Ceaser()
    message = "hello world"

    cipher = c.encrypt(message)
    print(cipher)

    m = c.decrypt(cipher)
    print(m)
    assert m == message