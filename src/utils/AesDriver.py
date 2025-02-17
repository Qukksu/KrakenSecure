import os.path
import subprocess


class AesDriver:
    def __init__(self):
        self._dir = "../utils/encrypted_aes"
        if not os.path.exists(self._dir):
            raise Exception(f"File {self._dir} not found")

    def encrypt(self, input_file: str, output_file: str, passphrase: str) -> None:
        subprocess.run([self._dir, "encrypt", input_file, output_file, passphrase])

    def decrypt(self, input_file: str, output_file: str, passphrase: str) -> None:
        subprocess.run([self._dir, "decrypt", input_file, output_file, passphrase])
