#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: video2png.sh
#        USAGE: video2png [video_file]
#  DESCRIPTION: Converts a video to a sequence of png files '%05d.png'.
# REQUIREMENTS: Gstreamer software installed, version 1.0, and some plugins.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

if [ "$#" != "1" ]; then
  echo "Usage: $0 [video_file]"
  exit 1
fi

gst-launch-1.0 filesrc location="$1" ! decodebin ! videoconvert ! \
  pngenc snapshot=false compression-level=1 ! \
  multifilesink location=%05d.png

exit 0
