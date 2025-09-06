#include <openssl/evp.h>
#include <openssl/rsa.h>

/*
 * This function uses AES, which is a non-PQC symmetric algorithm.
 */
int encrypt_data_aes(unsigned char *plaintext, int len, unsigned char *key, unsigned char *iv, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;
    int ciphertext_len;
    if(!(ctx = EVP_CIPHER_CTX_new())) return -1;
    // The line below uses a non-PQC algorithm
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)) return -1;
    // ... encryption logic ...
    EVP_CIPHER_CTX_free(ctx);
    return ciphertext_len;
}

/*
 * This function uses RSA, which is a non-PQC asymmetric algorithm.
 */
int encrypt_data_rsa(unsigned char *data, int data_len, RSA *rsa_key, unsigned char *encrypted) {
    return RSA_public_encrypt(data_len, data, encrypted, rsa_key, RSA_PKCS1_PADDING);
}
