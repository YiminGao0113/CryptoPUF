import ctypes

# Load the shared library
lib = ctypes.CDLL('./tinyjambu/libtinyjambu.so')  # On Linux or macOS
# lib = ctypes.CDLL('tinyjambu.dll')    # On Windows

# Define function prototypes for encryption and decryption
lib.crypto_aead_encrypt.argtypes = [ctypes.POINTER(ctypes.c_ubyte),  # ciphertext output
                                    ctypes.POINTER(ctypes.c_ulonglong),  # ciphertext length output
                                    ctypes.POINTER(ctypes.c_ubyte),  # message input
                                    ctypes.c_ulonglong,  # message length
                                    ctypes.POINTER(ctypes.c_ubyte),  # associated data input
                                    ctypes.c_ulonglong,  # associated data length
                                    ctypes.POINTER(ctypes.c_ubyte),  # nsec
                                    ctypes.POINTER(ctypes.c_ubyte),  # nonce input
                                    ctypes.POINTER(ctypes.c_ubyte)]  # key input

lib.crypto_aead_decrypt.argtypes = [ctypes.POINTER(ctypes.c_ubyte),  # plaintext output
                                    ctypes.POINTER(ctypes.c_ulonglong),  # plaintext length output
                                    ctypes.POINTER(ctypes.c_ubyte),  # nsec
                                    ctypes.POINTER(ctypes.c_ubyte),  # ciphertext input
                                    ctypes.c_ulonglong,  # ciphertext length
                                    ctypes.POINTER(ctypes.c_ubyte),  # associated data input
                                    ctypes.c_ulonglong,  # associated data length
                                    ctypes.POINTER(ctypes.c_ubyte),  # nonce input
                                    ctypes.POINTER(ctypes.c_ubyte)]  # key input

def hex_to_byte_array(hex_str):
    return (ctypes.c_ubyte * (len(hex_str) // 2))(*[int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)])

def encrypt(plaintext, key_hex, nonce_hex):
    key = hex_to_byte_array(key_hex)
    nonce = hex_to_byte_array(nonce_hex)

    ciphertext = (ctypes.c_ubyte * 64)()
    ciphertext_len = ctypes.c_ulonglong()

    lib.crypto_aead_encrypt(ciphertext, ctypes.byref(ciphertext_len),
                            ctypes.cast(plaintext, ctypes.POINTER(ctypes.c_ubyte)),
                            len(plaintext), None, 0, None, nonce, key)

    ciphertext_hex = ''.join(f'{byte:02x}' for byte in ciphertext[:ciphertext_len.value])
    return ciphertext_hex

def decrypt(ciphertext_hex, key_hex, nonce_hex):
    ciphertext = hex_to_byte_array(ciphertext_hex)
    key = hex_to_byte_array(key_hex)
    nonce = hex_to_byte_array(nonce_hex)

    plaintext = (ctypes.c_ubyte * 64)()
    plaintext_len = ctypes.c_ulonglong()

    ret = lib.crypto_aead_decrypt(plaintext, ctypes.byref(plaintext_len), None,
                                  ciphertext, len(ciphertext), None, 0, nonce, key)
    
    if ret == 0:
        plaintext_bytes = bytes(plaintext[:plaintext_len.value]).decode('utf-8')
        return plaintext_bytes
    else:
        return "Decryption failed"
