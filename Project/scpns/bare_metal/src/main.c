#include <stdio.h>
#include <string.h>
#include "aes_custom.h"

#include <irq.h>
#include <libbase/uart.h>
#include <libbase/console.h>
#include <generated/csr.h>

void aes_key_expansion(const unsigned char *key);

// AES-128 key schedule (11 round keys, 4 words each)
unsigned int aes_key_schedule[44];

// Function to expand the AES-128 key (simplified for this example)
void aes_key_expansion(const unsigned char *key) {
    // Copy the original key into the first 4 words of the key schedule
    for (int i = 0; i < 4; i++) {
        aes_key_schedule[i] = vexriscv_aes_load_unaligned(key + 4 * i);
    }
    // For simplicity, we'll fill the rest with a simple pattern
    // In a real implementation, you would use the proper key expansion algorithm
    for (int i = 4; i < 44; i++) {
        aes_key_schedule[i] = aes_key_schedule[i-4] ^ (i * 0x01010101);
    }
}

void print_hex(const unsigned char *buf, int len) {
    for (int i = 0; i < len; i++) {
        printf("%02x", buf[i]);
    }
    printf("\n");
}


int main(void) {
#ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
#endif
	uart_init();
    // Hardcoded 16-byte key for AES-128
    unsigned char key[16] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                             0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F};

    // Hardcoded 16-byte input
    unsigned char input[16] = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
                               0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};

    unsigned char encrypted[16];
    unsigned char decrypted[16];


    // Key expansion
    aes_key_expansion(key);

    printf("Original message: ");
    print_hex(input, 16);

    // Encrypt
    vexriscv_aes_encrypt(input, encrypted, aes_key_schedule, 10); // 10 rounds for AES-128

    printf("Encrypted message: ");
    print_hex(encrypted, 16);

    // Decrypt
    vexriscv_aes_decrypt(encrypted, decrypted, aes_key_schedule, 10);

    printf("Decrypted message: ");
    print_hex(decrypted, 16);

    return 0;

}