#!/bin/bash

echo 1 > /proc/sys/net/ipv4/ip_forward
INET="wlan0"
INETIP="$(ifconfig ${INET} | sed -nr 's/.*inet ([^ ]+).*/\1/p')"
iptables -t nat -A POSTROUTING -o ${INET} -j SNAT --to-source ${INETIP}

