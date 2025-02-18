import os.path
import subprocess


class AesDriver:
    def __init__(self, aes_file_path="../utils/encrypted_aes_mac"):
        self._dir = aes_file_path
        if not os.path.exists(self._dir):
            raise Exception(f"File {self._dir} not found")

    def encrypt(self, input_file: str, output_file: str, passphrase: str) -> int:
        result = subprocess.run([self._dir, "encrypt", input_file, output_file, passphrase], capture_output=True,
                                text=True)
        return result.returncode

    def decrypt(self, input_file: str, output_file: str, passphrase: str) -> int:
        result = subprocess.run([self._dir, "decrypt", input_file, output_file, passphrase], capture_output=True,
                                text=True)
        print(result.stderr)
        return result.returncode
