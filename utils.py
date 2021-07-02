import binascii


def string_xor(s1, s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def bytes_to_int(self, b):
	return int(binascii.hexlify(b), 16)

def int_to_bytes(self, num):
	return binascii.unhexlify('%x' % num)