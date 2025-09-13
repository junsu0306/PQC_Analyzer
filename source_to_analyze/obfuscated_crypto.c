#include <string.h>

static const unsigned char s_box[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    // ... (remaining bytes are omitted for brevity) ...
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

// Obfuscated function names
void op_step1(unsigned char *state) {
    for (int i = 0; i < 16; i++) {
        state[i] = s_box[state[i]];
    }
}
void op_step2(unsigned char *state) { /* Shift rows logic */ }
void op_step3(unsigned char *state) { /* Mix columns logic */ }

// Main processing function with a generic name
void process_chunk(unsigned char *data_chunk, const unsigned char *key_material) {
    for (int round = 0; round < 10; ++round) {
        op_step1(data_chunk);
        op_step2(data_chunk);
        op_step3(data_chunk);
    }
}
