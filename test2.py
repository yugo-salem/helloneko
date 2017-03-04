#!/usr/bin/env python
# encoding: utf-8

def parse_ip(ipstr):
    ip = map(int, ipstr.split('.'))
    assert len(ip) == 4
    assert (ip[0] >= 0) and (ip[0] <= 255)
    assert (ip[1] >= 0) and (ip[1] <= 255)
    assert (ip[2] >= 0) and (ip[2] <= 255)
    assert (ip[3] >= 0) and (ip[3] <= 255)
    return (ip[0]<<24)|(ip[1]<<16)|(ip[2]<<8)|(ip[3])

def ip2str(ip):
    return "%u.%u.%u.%u" %(((ip>>24)&0xFF), ((ip>>16)&0xFF), ((ip>>8)&0xFF), (ip&0xFF))


def main():
    ipstr="192.168.3.30"
    maskstr="255.255.0.0"

    ip=parse_ip(ipstr)
    mask=parse_ip(maskstr)
    netaddr=ip & mask
    broadcast=netaddr | (0xFFFFFFFF ^ mask)


    print("firstaddr="+ip2str(netaddr+1))
    print("lastaddr="+ip2str(broadcast-1))
    print("netaddr="+ip2str(netaddr))
    print("broadcast="+ip2str(broadcast))


if __name__ == '__main__':
    main()
