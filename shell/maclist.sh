#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: maclist.sh
#        USAGE: maclist [network]
#  DESCRIPTION: Scans the network using nmap and list all MAC address found.
# REQUIREMENTS: Command nmap installed in your system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

if [ $# -ne 1 ]; then
  echo "Usage: $0 [network]"
  echo "       example: $0 192.168.0."
  exit 1
fi
NETWORK="$1"

echo -e "Scanning network $NETWORK*...\n"
nmap -sP $NETWORK* > /dev/null

arp -n | grep -v incomplete

exit 0
