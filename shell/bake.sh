#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: bake.sh
#        USAGE: bake
#  DESCRIPTION: This script can be used as an alternative to 'make'. In fact,
#               it call make, but show the output in a more friendly way.
# REQUIREMENTS: Have the comand make install in your system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

set -o pipefail

MAKE=`which make`
if [ $? -ne 0 ]; then
  echo "The command 'make' is not defined in your system."
  exit 1
fi

${MAKE} -j8 2> .make_err.log
if [ $? -ne 0 ]; then
  echo -e "\nBuild \e[1;31mfailed\e[0m!\n"
  export GREP_COLOR="01;33"
  cat .make_err.log | grep warning > .make_tmp.log
  cat .make_tmp.log | grep -n --color warning
  export GREP_COLOR="01;31"
  cat .make_err.log | grep error > .make_tmp.log
  cat .make_tmp.log | grep -n --color error
  echo
  rm -f .make_err.log
  rm -f .make_tmp.log
  exit 1
else
  echo -e "\nBuild \e[1;32mdone\e[0m!\n"
  export GREP_COLOR="01;33"
  cat .make_err.log | grep warning > .make_tmp.log
  cat .make_tmp.log | grep -n --color warning
  echo
  rm -f .make_err.log
  rm -f .make_tmp.log
  exit 0
fi

