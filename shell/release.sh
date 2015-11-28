#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: release.sh
#        USAGE: release [git-repo]
#  DESCRIPTION: Generate a .tar.bz2 of a git repository.
# REQUIREMENTS: Have the command git install in your system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

if [ $# -ne 1 ]; then
  echo "Usage: $0 [git-repo]"
  exit 1
fi
ARG="$1"

# Remove trailing slash from argument
il=$((${#ARG}-1))
if [ "${ARG:$il:1}" = "/" ]; then
  ARG=${ARG:0:$il}
fi

if [ ! -d ${ARG} ]; then
  echo "Directory '${ARG}' does not exist!"
  exit 1
fi

pushd ${ARG}
GITTAG=`git describe --always --tag`
popd

PACKNAME=${ARG}_${GITTAG}
echo ${PACKNAME}

if [ -d ${PACKNAME} ]; then
  rm -rf ${PACKNAME}
fi
mkdir ${PACKNAME}
cp -R ${ARG}/* ${PACKNAME}
if [ -e ${PACKNAME}/autogen.sh ]; then
  rm ${PACKNAME}/autogen.sh
fi

# Compress
tar -cf ${PACKNAME}.tar ${PACKNAME}/
bzip2 ${PACKNAME}.tar
rm -r ${PACKNAME}

if [ $? -eq 0 ]; then
  echo "Generated file ${PACKNAME}.tar.bz2"
else
  echo "Something get wrong..."
  exit 1
fi

exit 0
