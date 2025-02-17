from src.utils.AesDriver import AesDriver

aes = AesDriver()

aes.encrypt("tests/file_for_testing.txt",
        "tests/file_for_testing_enc.txt",
        "root")

aes.decrypt("tests/file_for_testing_enc.txt",
        "tests/file_for_testing_dec.txt",
        "zero")

aes.decrypt("tests/file_for_testing_enc.txt",
        "tests/file_for_testing_dec.txt",
        "root")