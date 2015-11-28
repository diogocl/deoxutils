#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: minpower.sh
#        USAGE: minpower
#  DESCRIPTION: This is a machine-specif script to set power management policy
#               to min_power. 
# REQUIREMENTS: Must be run as root.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

for i in $(seq 0 5); do
  if [ -e "/sys/class/scsi_host/host${i}/link_power_management_policy" ]; then
    echo "min_power" > \
      "/sys/class/scsi_host/host${i}/link_power_management_policy"
  fi
done

