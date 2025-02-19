from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class Crypt:
    """
    Класс для шифрования и дешифрования файлов с использованием AES и PBKDF2.
    """

    def __init__(self,
                 salt_size: int = 8,
                 buffer_size: int = 4096,
                 key_size: int = 32,
                 iv_size: int = 16):
        """
        Инициализирует объект Crypt с заданными размерами соли, буфера, ключа и вектора инициализации.

        Args:
            salt_size (int): Размер соли в байтах.
            buffer_size (int): Размер буфера для чтения/записи файлов в байтах.
            key_size (int): Размер ключа шифрования в байтах.
            iv_size (int): Размер вектора инициализации в байтах.
        """
        self.__SALT_SIZE = salt_size
        self.__BUFFER_SIZE = buffer_size
        self.__KEY_SIZE = key_size
        self.__IV_SIZE = iv_size

    def __derive_key_and_iv(self, password: str, salt: bytes) -> tuple[bytes, bytes]:
        """
        Генерирует ключ и вектор инициализации (IV) из пароля и соли с использованием PBKDF2.

        PBKDF2 (Password-Based Key Derivation Function 2) используется для "растягивания" ключа,
        что делает его более устойчивым к атакам перебором.

        Args:
            password (str): Пароль для генерации ключа.
            salt (bytes): Соль (случайные данные) для защиты от Rainbow Table-атак.

        Returns:
            tuple[bytes, bytes]: Кортеж, содержащий ключ и IV.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # Используем SHA256 для хеширования
            length=self.__KEY_SIZE + self.__IV_SIZE,  # Общая длина ключа и IV
            salt=salt,  # Соль
            iterations=100000,  # Количество итераций для "растягивания" ключа
        )
        key_iv = kdf.derive(password.encode())  # Генерируем ключ и IV из пароля
        return key_iv[:self.__KEY_SIZE], key_iv[self.__KEY_SIZE:self.__KEY_SIZE + self.__IV_SIZE]

    def encrypt_file(self, in_filename: str, out_filename: str, password: str) -> bool:
        """
        Шифрует файл с использованием AES в режиме CBC.

        AES (Advanced Encryption Standard) - симметричный алгоритм блочного шифрования.
        CBC (Cipher Block Chaining) - режим шифрования, в котором каждый блок шифруется
        с использованием результата шифрования предыдущего блока, что обеспечивает
        дополнительную безопасность.

        Args:
            in_filename (str): Имя входного файла.
            out_filename (str): Имя выходного файла.
            password (str): Пароль для шифрования.

        Returns:
            bool: True, если шифрование прошло успешно, False - в противном случае.
        """
        try:
            # Генерируем случайную соль
            salt = os.urandom(self.__SALT_SIZE)

            # Получаем ключ и IV
            key, iv = self.__derive_key_and_iv(password, salt)

            # Создаем объект шифра AES в режиме CBC
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            with open(in_filename, 'rb') as fin, open(out_filename, 'wb') as fout:
                # Записываем соль в начало файла
                fout.write(salt)

                # Читаем и шифруем файл
                while True:
                    chunk = fin.read(self.__BUFFER_SIZE)
                    if not chunk:
                        break

                    # Дополняем последний блок, если необходимо
                    if len(chunk) % 16 != 0:
                        padding_length = 16 - (len(chunk) % 16)
                        chunk += bytes([padding_length]) * padding_length

                    encrypted_chunk = encryptor.update(chunk)
                    fout.write(encrypted_chunk)

                # Записываем финальный блок
                fout.write(encryptor.finalize())

            return True
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return False

    def decrypt_file(self, in_filename: str, out_filename: str, password: str) -> bool:
        """
        Дешифрует файл, зашифрованный с использованием AES в режиме CBC.

        Args:
            in_filename (str): Имя входного файла.
            out_filename (str): Имя выходного файла.
            password (str): Пароль для дешифрования.

        Returns:
            bool: True, если дешифрование прошло успешно, False - в противном случае.
        """
        try:
            with open(in_filename, 'rb') as fin:
                # Читаем соль
                salt = fin.read(self.__SALT_SIZE)

                # Получаем ключ и IV
                key, iv = self.__derive_key_and_iv(password, salt)

                # Создаем объект шифра AES в режиме CBC
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                decryptor = cipher.decryptor()

                with open(out_filename, 'wb') as fout:
                    while True:
                        chunk = fin.read(self.__BUFFER_SIZE)
                        if not chunk:
                            break

                        decrypted_chunk = decryptor.update(chunk)

                        # Для последнего блока удаляем padding
                        if not chunk:
                            decrypted_chunk = decryptor.finalize()
                            if decrypted_chunk:
                                padding_length = decrypted_chunk[-1]
                                decrypted_chunk = decrypted_chunk[:-padding_length]

                        fout.write(decrypted_chunk)

                    # Обрабатываем финальный блок
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

    crypto = Crypt()

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    password = sys.argv[4]

    if mode == "encrypt":
        if crypto.encrypt_file(input_file, output_file, password):
            print("File encrypted successfully.")
        else:
            print("Encryption failed.")
            sys.exit(1)
    elif mode == "decrypt":
        if crypto.decrypt_file(input_file, output_file, password):
            print("File decrypted successfully.")
        else:
            print("Decryption failed.")
            sys.exit(1)
    else:
        print("Invalid mode. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
