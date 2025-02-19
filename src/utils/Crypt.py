from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class FileEncryptor:
    SALT_SIZE = 8
    BUFFER_SIZE = 4096
    KEY_SIZE = 32
    IV_SIZE = 16

    def __init__(self, password: str = None):
        self.password = password

    def _derive_key_and_iv(self, password: str, salt: bytes) -> tuple[bytes, bytes]:
        """Generate key and IV from password and salt using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE + self.IV_SIZE,
            salt=salt,
            iterations=100000,
        )
        key_iv = kdf.derive(password.encode())
        return key_iv[:self.KEY_SIZE], key_iv[self.KEY_SIZE:self.KEY_SIZE + self.IV_SIZE]

    def encrypt_file(self, in_filename: str, out_filename: str, password: str = None) -> bool:
        try:
            use_password = password or self.password
            if not use_password:
                raise ValueError("Password not provided")

            salt = os.urandom(self.SALT_SIZE)
            key, iv = self._derive_key_and_iv(use_password, salt)

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            with open(in_filename, 'rb') as fin, open(out_filename, 'wb') as fout:
                fout.write(salt)

                while True:
                    chunk = fin.read(self.BUFFER_SIZE)
                    if not chunk:
                        break

                    if len(chunk) % 16 != 0:
                        padding_length = 16 - (len(chunk) % 16)
                        chunk += bytes([padding_length]) * padding_length

                    encrypted_chunk = encryptor.update(chunk)
                    fout.write(encrypted_chunk)

                fout.write(encryptor.finalize())

            return True
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return False

    def decrypt_file(self, in_filename: str, out_filename: str, password: str = None) -> bool:
        try:
            use_password = password or self.password
            if not use_password:
                raise ValueError("Password not provided")

            with open(in_filename, 'rb') as fin:
                salt = fin.read(self.SALT_SIZE)
                key, iv = self._derive_key_and_iv(use_password, salt)

                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                decryptor = cipher.decryptor()

                with open(out_filename, 'wb') as fout:
                    while True:
                        chunk = fin.read(self.BUFFER_SIZE)
                        if not chunk:
                            break

                        decrypted_chunk = decryptor.update(chunk)

                        if not chunk:
                            decrypted_chunk = decryptor.finalize()
                            if decrypted_chunk:
                                padding_length = decrypted_chunk[-1]
                                decrypted_chunk = decrypted_chunk[:-padding_length]

                        fout.write(decrypted_chunk)

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

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <encrypt|decrypt> <filename>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    encryptor = FileEncryptor()

    if mode == "encrypt":
        output_file = filename + ".encrypted"
        password = input("Enter password for encryption: ")
        if encryptor.encrypt_file(filename, output_file, password):
            print(f"File encrypted successfully to {output_file}")
        else:
            print("Encryption failed.")
            sys.exit(1)
    elif mode == "decrypt":
        if not filename.endswith(".encrypted"):
            print("Error: File must have .encrypted extension")
            sys.exit(1)
        output_file = filename.replace(".encrypted", "")
        password = input("Enter password for decryption: ")
        if encryptor.decrypt_file(filename, output_file, password):
            print(f"File decrypted successfully to {output_file}")
        else:
            print("Decryption failed.")
            sys.exit(1)
    else:
        print("Invalid mode. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
