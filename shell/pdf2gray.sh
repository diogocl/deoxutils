#!/bin/bash

# Sanity check
if [ ! -x "$(which gs)" ]
then
  echo "You must instal the Ghostscript (gs) program!"
  exit 1
fi

# Parameters check
if [ "$#" != "2" ]
then
  echo "Usage: $0 [input.pdf] [output.pdf]"
  exit 0
fi

gs \
	-sOutputFile="$2" \
	-sDEVICE=pdfwrite \
	-sColorConversionStrategy=Gray \
	-dProcessColorModel=/DeviceGray \
	-dCompatibilityLevel=1.4 \
	-dNOPAUSE \
	-dBATCH \
	"$1"
