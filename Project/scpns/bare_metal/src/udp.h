#ifndef __UDP_H
#define __UDP_H

#ifdef __cplusplus
extern "C" {
#endif

#define ETHMAC_EV_SRAM_WRITER	0x1
#define ETHMAC_EV_SRAM_READER	0x1

#define IPTOINT(a, b, c, d) ((a << 24)|(b << 16)|(c << 8)|d)

#define UDP_BUFSIZE (5*1532)

typedef void (*udp_callback)(unsigned int src_ip, unsigned short src_port, unsigned short dst_port, void *data, unsigned int length);

void udp_ip_set(unsigned int ip);
void udp_mac_set(const unsigned char *macaddr);
void start_udp(const unsigned char *macaddr, unsigned int ip);
int arp_udp_resolve(unsigned int ip);
void *udp_tx_buffer_get(void);
int send_udp(unsigned short src_port, unsigned short dst_port, unsigned int length);
void udp_callback_set(udp_callback callback);
void service_udp(void);

void ethernet_init(void);
void eth_mode(void);

#ifdef __cplusplus
}
#endif

#endif /* __UDP_H */
