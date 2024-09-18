#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <irq.h>
#include <system.h>
#include <generated/csr.h>
#include <generated/mem.h>

#include <libbase/uart.h>
#include <libliteeth/udp.h>

#define ETHERNET_BUFFER_SIZE 1536

// Callback function to handle incoming UDP packets
static void print_packet(unsigned int src_ip, unsigned short src_port, unsigned short dst_port,
                         void *data, unsigned int length) {
    char ip_str[16];
    sprintf(ip_str, "%d.%d.%d.%d", (src_ip >> 24) & 0xff, (src_ip >> 16) & 0xff,
            (src_ip >> 8) & 0xff, src_ip & 0xff);

    printf("Received UDP packet from %s:%d to port %d\n", ip_str, src_port, dst_port);
    printf("Packet length: %d bytes\n", length);
    printf("Packet contents:\n");

    // Print packet contents
    unsigned char *packet_data = (unsigned char *)data;
    for (unsigned int i = 0; i < length; i++) {
        printf("%02x ", packet_data[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    printf("\n\n");
}


int main(void)
{
#ifdef CONFIG_CPU_HAS_INTERRUPT
    irq_setmask(0);
    irq_setie(1);
#endif
    uart_init();

	eth_init();

    // Set up MAC and IP address (you may need to adjust these)
    unsigned char mac_addr[6] = {0x10, 0xe2, 0xd5, 0x00, 0x00, 0x00};
    unsigned int ip_addr = IPTOINT(192, 168, 1, 50);  // Adjust as needed

    udp_start(mac_addr, ip_addr);
    udp_set_callback(print_packet);

    while (1) {
        udp_service();
    }

    return 0;
}