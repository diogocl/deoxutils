#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: mkproject.sh
#        USAGE: mkproject [project_name] [folder_icon]
#  DESCRIPTION: This script creates a new directory structure as follows:
#               General directory tree:
#               -----------------------
#                 0_Documents
#                 1_Hardware
#                   0_Cad
#                 2_Software
#                   0_Bin
#                   1_Bugs
#                 3_Data
#                 .generated
#               -----------------------
# REQUIREMENTS: Have the script seticon.py installed in your system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

SETICONBIN=`which seticon`
if [ ! -x ${SETICONBIN} ]; then
  echo "Error! Command seticon not found."
  exit 1
fi

if [ $# != 1 ] && [ $# != 2 ]; then
  echo "Usage: $0 [project_name] [folder_icon]"
  exit 0
fi

PROJDIR="$1"
if [ ! -d ${PROJDIR} ]; then
  mkdir ${PROJDIR}
fi

pushd ${PROJDIR}
if [ ! -e .generated ]; then
  mkdir -p 0_Documents
  mkdir -p 1_Hardware
  mkdir -p 1_Hardware/0_Cad
  mkdir -p 2_Software
  mkdir -p 2_Software/0_Bin
  mkdir -p 2_Software/1_Bugs
  mkdir -p 3_Data
  seticon 0_Documents /usr/share/pixmaps/doc.png
  seticon 1_Hardware /usr/share/pixmaps/hardware.png
  seticon 2_Software /usr/share/pixmaps/software.png
  seticon 3_Data /usr/share/pixmaps/data.png
  echo `date` > .generated
else
  echo "File .generated found here! Nothing todo."
fi
popd

if [ $# == 2 ]; then
  echo "Setting folder icon..."
  ICON="$2"
  seticon ${PROJDIR} ${ICON}
fi

echo "All done."
exit 0
