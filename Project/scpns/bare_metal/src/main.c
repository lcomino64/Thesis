#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <irq.h>
#include <system.h>
#include <generated/csr.h>
#include <generated/mem.h>

#include <libbase/uart.h>
#include <libliteeth/udp.h>


static unsigned char macadr[6] = {0x10, 0xe2, 0xd5, 0x00, 0x00, 0x00};
static unsigned int local_ip[4] = {192, 168, 1, 50};

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
    uart_init();
#ifdef CONFIG_CPU_HAS_INTERRUPT
    irq_setmask(0);
    irq_setie(0);
#endif

	eth_init();
    udp_start(macadr, IPTOINT(local_ip[0], local_ip[1], local_ip[2], local_ip[3]));

    // udp_set_callback(print_packet);

    while (1) {
        // udp_service();
    }

    return 0;
}