#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: jpeg2avi.sh
#        USAGE: jpeg2avi
#               [jpeg_path] [start_index] [fps] [bitrate-bps] [output_file]
#  DESCRIPTION: Converts a sequence of jpeg files in the format '%05d.jpeg',
#               startting fron index start_index. The output file is in AVI
#               format.
# REQUIREMENTS: Gstreamer software installed, version 0.10, and some plugins.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

if [ "$#" != "5" ]; then
  echo "Usage: $0 [jpeg_path] [start_index] [fps] [bitrate-bps] [output_file]"
  exit 1
fi

gst-launch-0.10 multifilesrc location="$1/%05d.jpeg" \
  start-index=$2 \
  caps=image/jpeg,framerate=$3/1 ! jpegdec ! ffmpegcolorspace ! \
  xvidenc bitrate=$4 ! avimux ! filesink location="$5"

exit 0
