#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 [guess]"
  exit 1
fi

gpg  --output - ~/.mine.gpg | grep -i "$1"

exit 0
