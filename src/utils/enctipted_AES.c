#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>

#define SALT_SIZE 8           // Размер salt в байтах
#define BUFFER_SIZE 4096      // Размер буфера для чтения файла
#define KEY_SIZE 32           // Размер ключа для AES-256 (32 байта)
#define IV_SIZE 16            // Размер вектора инициализации для AES (16 байт)

// gcc enctipted_AES.c -o enctipted_AES -lcrypto

/*
 * Функция шифрования файла.
 * Параметры:
 *   in_filename  - имя входного файла
 *   out_filename - имя выходного файла
 *   password     - ключевая фраза для формирования ключа
 * Возвращает 1 при успехе, 0 при ошибке.
 */
int encrypt_file(const char *in_filename, const char *out_filename, const char *password) {
    FILE *fIn = NULL, *fOut = NULL;
    EVP_CIPHER_CTX *ctx = NULL;
    unsigned char salt[SALT_SIZE];
    unsigned char key[KEY_SIZE], iv[IV_SIZE];
    int bytes_read, out_len, final_out_len;
    unsigned char in_buf[BUFFER_SIZE];
    unsigned char out_buf[BUFFER_SIZE + EVP_MAX_BLOCK_LENGTH];
    
    // Открываем входной файл для чтения
    fIn = fopen(in_filename, "rb");
    if (!fIn) {
        fprintf(stderr, "Не удалось открыть входной файл: %s\n", in_filename);
        goto err;
    }
    
    // Открываем выходной файл для записи
    fOut = fopen(out_filename, "wb");
    if (!fOut) {
        fprintf(stderr, "Не удалось открыть выходной файл: %s\n", out_filename);
        goto err;
    }
    
    // Генерируем случайный salt
    if (RAND_bytes(salt, sizeof(salt)) != 1) {
        fprintf(stderr, "Ошибка генерации salt\n");
        goto err;
    }
    
    // Записываем salt в начало выходного файла (для последующего дешифрования)
    if (fwrite(salt, 1, sizeof(salt), fOut) != sizeof(salt)) {
        fprintf(stderr, "Ошибка записи salt в выходной файл\n");
        goto err;
    }
    
    /*
     * Формирование ключа и вектора инициализации из ключевой фразы и salt.
     * Используем функцию EVP_BytesToKey с алгоритмом EVP_sha256.
     */
    if (EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha256(),
                       salt, (unsigned char *)password, strlen(password),
                       1, key, iv) != KEY_SIZE) {
        fprintf(stderr, "Ошибка генерации ключа и IV\n");
        goto err;
    }
    
    // Создаём контекст шифрования
    ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        fprintf(stderr, "Ошибка создания контекста\n");
        goto err;
    }
    
    // Инициализируем шифрование: AES-256-CBC
    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv) != 1) {
        fprintf(stderr, "Ошибка инициализации шифрования\n");
        goto err;
    }
    
    // Читаем входной файл блоками и шифруем
    while ((bytes_read = fread(in_buf, 1, BUFFER_SIZE, fIn)) > 0) {
        if (EVP_EncryptUpdate(ctx, out_buf, &out_len, in_buf, bytes_read) != 1) {
            fprintf(stderr, "Ошибка процесса шифрования\n");
            goto err;
        }
        if (fwrite(out_buf, 1, out_len, fOut) != (size_t)out_len) {
            fprintf(stderr, "Ошибка записи шифрованных данных\n");
            goto err;
        }
    }
    
    // Финализируем шифрование
    if (EVP_EncryptFinal_ex(ctx, out_buf, &final_out_len) != 1) {
        fprintf(stderr, "Ошибка завершения шифрования\n");
        goto err;
    }
    if (fwrite(out_buf, 1, final_out_len, fOut) != (size_t)final_out_len) {
        fprintf(stderr, "Ошибка записи финальных данных\n");
        goto err;
    }
    
    // Освобождаем ресурсы и закрываем файлы
    EVP_CIPHER_CTX_free(ctx);
    fclose(fIn);
    fclose(fOut);
    return 1;
    
err:
    if (ctx) EVP_CIPHER_CTX_free(ctx);
    if (fIn) fclose(fIn);
    if (fOut) fclose(fOut);
    return 0;
}

/*
 * Функция дешифрования файла.
 * Параметры:
 *   in_filename  - имя входного файла (шифрованного)
 *   out_filename - имя выходного файла (расшифрованного)
 *   password     - ключевая фраза для формирования ключа
 * Возвращает 1 при успехе, 0 при ошибке.
 */
int decrypt_file(const char *in_filename, const char *out_filename, const char *password) {
    FILE *fIn = NULL, *fOut = NULL;
    EVP_CIPHER_CTX *ctx = NULL;
    unsigned char salt[SALT_SIZE];
    unsigned char key[KEY_SIZE], iv[IV_SIZE];
    int bytes_read, out_len, final_out_len;
    unsigned char in_buf[BUFFER_SIZE];
    unsigned char out_buf[BUFFER_SIZE + EVP_MAX_BLOCK_LENGTH];
    
    // Открываем входной файл для чтения
    fIn = fopen(in_filename, "rb");
    if (!fIn) {
        fprintf(stderr, "Не удалось открыть входной файл: %s\n", in_filename);
        goto err;
    }
    
    // Открываем выходной файл для записи
    fOut = fopen(out_filename, "wb");
    if (!fOut) {
        fprintf(stderr, "Не удалось открыть выходной файл: %s\n", out_filename);
        goto err;
    }
    
    // Считываем salt из начала файла
    if (fread(salt, 1, sizeof(salt), fIn) != sizeof(salt)) {
        fprintf(stderr, "Ошибка чтения salt из файла\n");
        goto err;
    }
    
    /*
     * Восстанавливаем ключ и IV по ключевой фразе и salt
     */
    if (EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha256(),
                       salt, (unsigned char *)password, strlen(password),
                       1, key, iv) != KEY_SIZE) {
        fprintf(stderr, "Ошибка генерации ключа и IV\n");
        goto err;
    }
    
    // Создаём контекст дешифрования
    ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        fprintf(stderr, "Ошибка создания контекста\n");
        goto err;
    }
    
    // Инициализируем дешифрование: AES-256-CBC
    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv) != 1) {
        fprintf(stderr, "Ошибка инициализации дешифрования\n");
        goto err;
    }
    
    // Читаем зашифрованный файл блоками и дешифруем
    while ((bytes_read = fread(in_buf, 1, BUFFER_SIZE, fIn)) > 0) {
        if (EVP_DecryptUpdate(ctx, out_buf, &out_len, in_buf, bytes_read) != 1) {
            fprintf(stderr, "Ошибка процесса дешифрования\n");
            goto err;
        }
        if (fwrite(out_buf, 1, out_len, fOut) != (size_t)out_len) {
            fprintf(stderr, "Ошибка записи дешифрованных данных\n");
            goto err;
        }
    }
    
    // Финализируем дешифрование
    if (EVP_DecryptFinal_ex(ctx, out_buf, &final_out_len) != 1) {
        fprintf(stderr, "Неверная ключевая фраза или повреждён файл\n");
        goto err;
    }
    if (fwrite(out_buf, 1, final_out_len, fOut) != (size_t)final_out_len) {
        fprintf(stderr, "Ошибка записи финальных данных\n");
        goto err;
    }
    
    // Освобождаем ресурсы и закрываем файлы
    EVP_CIPHER_CTX_free(ctx);
    fclose(fIn);
    fclose(fOut);
    return 1;
    
err:
    if (ctx) EVP_CIPHER_CTX_free(ctx);
    if (fIn) fclose(fIn);
    if (fOut) fclose(fOut);
    return 0;
}

/*
 * Главная функция.
 * Использование:
 *   enctipted_AES <encrypt|decrypt> <input_file> <output_file> <passphrase>
 */
int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Использование: %s <encrypt|decrypt> <input_file> <output_file> <passphrase>\n", argv[0]);
        return EXIT_FAILURE;
    }
    
    if (strcmp(argv[1], "encrypt") == 0) {
        if (!encrypt_file(argv[2], argv[3], argv[4])) {
            fprintf(stderr, "Ошибка шифрования файла.\n");
            return EXIT_FAILURE;
        }
        printf("Файл успешно зашифрован.\n");
    } else if (strcmp(argv[1], "decrypt") == 0) {
        if (!decrypt_file(argv[2], argv[3], argv[4])) {
            fprintf(stderr, "Ошибка дешифрования файла.\n");
            return EXIT_FAILURE;
        }
        printf("Файл успешно дешифрован.\n");
    } else {
        fprintf(stderr, "Неверный режим. Используйте 'encrypt' или 'decrypt'.\n");
        return EXIT_FAILURE;
    }
    
    return EXIT_SUCCESS;
}
