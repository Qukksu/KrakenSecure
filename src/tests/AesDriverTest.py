from src.utils.AesDriver import AesDriver

aes = AesDriver(aes_file_path="../utils/encrypted_aes_mac")

def test_register():
        passwd = input("Кодовая фраза для регистрации: ")
        if aes.encrypt("test/db.txt", "test/db.txt", passwd) == 1:
                print("error")

def test_db():
        passwd = input("Кодовая фраза для авторизации")
        if aes.decrypt("test/db.txt", "test/db.txt", passwd) == 1:
                print("err")
        else:
                print("confirm")

test_register()
test_db()



# code_ = aes.encrypt("test/file.txt",
#         "test/file_enc.txt",
#         "")
#
# print("encrypt: ", code_)

# code_2 = aes.decrypt("test/file_enc.txt",
#         "test/file_dec.txt",
#         "")
#
# print("decrypt: ", code_2)

# code_3 = aes.decrypt("test/file_enc.txt",
#         "test/file_dec.txt",
#         "root")
#
# print(code_3)