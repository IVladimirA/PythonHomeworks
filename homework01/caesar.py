import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
	ciphertext = ""
	for i in range(len(plaintext)):
		curr = ord(plaintext[i])
		if curr >= ord('A') and curr <= ord('Z'):
			ciphertext += chr(ord('A') + (curr - ord('A') + shift) % 26)
		elif curr >= ord('a') and curr <= ord('z'):
			ciphertext += chr(ord('a') + (curr - ord('a') + shift) % 26)
		else:
			ciphertext += chr(curr)
	return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
	plaintext = ""
	for i in range(len(ciphertext)):
		curr = ord(ciphertext[i])
		if curr >= ord('A') and curr <= ord('Z'):
			plaintext += chr(ord('A') + (curr - ord('A') - shift + 26) % 26)
		elif curr >= ord('a') and curr <= ord('z'):
			plaintext += chr(ord('a') + (curr - ord('a') - shift + 26) % 26)
		else:
			plaintext += chr(curr)
	return plaintext
