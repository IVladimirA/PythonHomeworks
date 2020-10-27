def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    n = len(keyword)
    for i in range(len(plaintext)):
        curr = ord(plaintext[i])
        curr_key = keyword[i % n]
        if ord(curr_key) >= ord('A') and ord(curr_key) <= ord('Z'):
            move = ord(curr_key) - ord('A')
        else:
            move = ord(curr_key) - ord('a')

        if curr >= ord('A') and curr <= ord('Z'):
            ciphertext += chr(ord('A') + (curr - ord('A') + move) % 26)
        elif curr >= ord('a') and curr <= ord('z'):
            ciphertext += chr(ord('a') + (curr - ord('a') + move) % 26)
        else:
            ciphertext += chr(curr)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    n = len(keyword)
    for i in range(len(ciphertext)):
        curr = ord(ciphertext[i])
        curr_key = keyword[i % n]
        if ord(curr_key) >= ord('A') and ord(curr_key) <= ord('Z'):
            move = ord(curr_key) - ord('A')
        else:
            move = ord(curr_key) - ord('a')

        if curr >= ord('A') and curr <= ord('Z'):
            plaintext += chr(ord('A') + (curr - ord('A') - move + 26) % 26)
        elif curr >= ord('a') and curr <= ord('z'):
            plaintext += chr(ord('a') + (curr - ord('a') - move + 26) % 26)
        else:
            plaintext += chr(curr)
    return plaintext
