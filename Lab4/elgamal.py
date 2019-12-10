import random

from fractions import gcd

# GENERATE KEYS
def generate_keys(bits_number=256, test_accuracy=32):
    p = find_prime(bits_number, test_accuracy)
    g = pow(find_primitive_root(p), 2, p)
    x = random.randint(1, (p - 1) // 2 )
    y = pow(g, x, p)

    return (p, g, y), (p, g, x)


#https://ru.wikipedia.org/wiki/Тест_Соловея_—_Штрассена
def is_prime(number, test_accuracy):
    for _ in range(test_accuracy):
        a = random.randint(2, number - 1)

        if gcd(a, number) > 1:
            return False
            
        if not pow(a, (number - 1) // 2, number) == jacobi(a, number) % number:
            return False

    return True


def jacobi(a, n):
    if a == 0:
        if n == 1:
            return 1

        return 0

    if a == -1:
        if n % 2 == 0:
            return 1

        return -1
        
    if a == 1:
        return 1
        
    if a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        if n % 8 == 3 or n % 8 == 5:
            return -1
            
    if a >= n:
        return jacobi(a % n, n)

    if a % 2 == 0:
            return jacobi(2, n) * jacobi(a // 2, n)
        
    if a % 4 == 3 and n % 4 == 3:
        return -1 * jacobi(n, a)
        
    return jacobi(n, a)


def find_primitive_root(p):
    if p == 2:
        return 1
        
    p1 = 2
    p2 = (p - 1) // p1

    while True:
        g = random.randint(2, p - 1)
        
        if not pow(g, (p - 1) // p1, p) == 1 and not pow(g, (p - 1) // p2, p) == 1:
            return g


def find_prime(bits_number, test_accuracy):
    while True:
        while True:
            p = 0
            while p % 2 == 0:
                p = random.randint(2 ** (bits_number - 2), 2 ** (bits_number - 1))

            if is_prime(p, test_accuracy):
                break

        p = p * 2 + 1
        if is_prime(p, test_accuracy):
            return p


# ENCRYPT
def encrypt(text, key, bits_number=256):
    z = encode(text, bits_number)
    p, g, y = key

    cipher_pairs = []
    #i is an integer in z
    for i in z:
        k = random.randint(0, p)
        a = pow(g, k, p)
        b = (i * pow(y, k, p)) % p
        cipher_pairs.append([a, b])

    encrypted_string = ""
    for pair in cipher_pairs:
        encrypted_string += str(pair[0]) + ' ' + str(pair[1]) + ' '

    return encrypted_string


def encode(text, bits_number):
    byte_array = bytearray(text, 'utf-16')

    encoded_bytes = []

    bytes_number = bits_number // 8

    j = -1 * bytes_number
    for i in range(len(byte_array)):
        if i % bytes_number == 0:
            j += bytes_number
            encoded_bytes.append(0)
            
        encoded_bytes[j//bytes_number] += byte_array[i] * (2 ** (8 * (i % bytes_number)))

    return encoded_bytes


# DECRYPT
def decrypt(text, key, bits_number=256):
    plain_text = []
    p, g, x = key

    cipher_array = text.split()
    if not len(cipher_array) % 2 == 0:
        return "Malformed Cipher Text"

    for i in range(0, len(cipher_array), 2):
        a = int(cipher_array[i])
        b = int(cipher_array[i+1])

        s = pow(a, x, p)
        plain = (b * pow(s, p - 2, p)) % p
        plain_text.append(plain)

    decryptedText = decode(plain_text, bits_number)
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])

    return decryptedText


def decode(text, bits_number):
    bytes_array = []

    bytes_number = bits_number // 8

    for byte in text:
        for i in range(bytes_number):
            temp = byte
            
            for j in range(i + 1, bytes_number):
                temp = temp % (2 ** (8 * j))

            letter = temp // (2 ** (8 * i))
            bytes_array.append(letter)
            
            byte = byte - (letter * (2 ** (8 * i)))

    decodedText = bytearray(b for b in bytes_array).decode('utf-16')

    return decodedText
