import binascii
import struct


def string_xor(s1, s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def bytes_to_int(b):
	return int(binascii.hexlify(b), 16)


def int_to_bytes(num):
	return binascii.unhexlify('%x' % num)


def little_endian(num):
	return struct.pack('I', num)


def big_endian(num):
	return struct.pack('>I', num)