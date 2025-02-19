from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

SALT_SIZE = 8
BUFFER_SIZE = 4096
KEY_SIZE = 32
IV_SIZE = 16


def derive_key_and_iv(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """Generate key and IV from password and salt using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE + IV_SIZE,
        salt=salt,
        iterations=100000,
    )
    key_iv = kdf.derive(password.encode())
    return key_iv[:KEY_SIZE], key_iv[KEY_SIZE:KEY_SIZE + IV_SIZE]


def encrypt_file(in_filename: str, out_filename: str, password: str) -> bool:
    try:
        # Generate random salt
        salt = os.urandom(SALT_SIZE)

        # Derive key and IV
        key, iv = derive_key_and_iv(password, salt)

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        with open(in_filename, 'rb') as fin, open(out_filename, 'wb') as fout:
            # Write salt at the beginning
            fout.write(salt)

            # Read and encrypt file
            while True:
                chunk = fin.read(BUFFER_SIZE)
                if not chunk:
                    break

                # Pad the last chunk if necessary
                if len(chunk) % 16 != 0:
                    padding_length = 16 - (len(chunk) % 16)
                    chunk += bytes([padding_length]) * padding_length

                encrypted_chunk = encryptor.update(chunk)
                fout.write(encrypted_chunk)

            # Write final block
            fout.write(encryptor.finalize())

        return True
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return False


def decrypt_file(in_filename: str, out_filename: str, password: str) -> bool:
    try:
        with open(in_filename, 'rb') as fin:
            # Read salt
            salt = fin.read(SALT_SIZE)

            # Derive key and IV
            key, iv = derive_key_and_iv(password, salt)

            # Create cipher
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            with open(out_filename, 'wb') as fout:
                while True:
                    chunk = fin.read(BUFFER_SIZE)
                    if not chunk:
                        break

                    decrypted_chunk = decryptor.update(chunk)

                    # For the last chunk, remove padding
                    if not chunk:
                        decrypted_chunk = decryptor.finalize()
                        if decrypted_chunk:
                            padding_length = decrypted_chunk[-1]
                            decrypted_chunk = decrypted_chunk[:-padding_length]

                    fout.write(decrypted_chunk)

                # Handle final block
                final_chunk = decryptor.finalize()
                if final_chunk:
                    padding_length = final_chunk[-1]
                    final_chunk = final_chunk[:-padding_length]
                    fout.write(final_chunk)

        return True
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return False


def main():
    import sys

    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <encrypt|decrypt> <input_file> <output_file> <passphrase>")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    password = sys.argv[4]

    if mode == "encrypt":
        if encrypt_file(input_file, output_file, password):
            print("File encrypted successfully.")
        else:
            print("Encryption failed.")
            sys.exit(1)
    elif mode == "decrypt":
        if decrypt_file(input_file, output_file, password):
            print("File decrypted successfully.")
        else:
            print("Decryption failed.")
            sys.exit(1)
    else:
        print("Invalid mode. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
