#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: video2jpeg.sh
#        USAGE: video2jpeg [video_file] [quality]
#  DESCRIPTION: Converts a video to a sequence of jpeg files '%05d.jpeg'.
# REQUIREMENTS: Gstreamer software installed, version 1.0, and some plugins.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

if [ "$#" != "2" ]; then
  echo "Usage: $0 [video_file] [quality]"
  exit 1
fi

gst-launch-1.0 filesrc location="$1" ! decodebin ! \
  jpegenc quality=$2 idct-method=2 ! \
  multifilesink location=%05d.jpeg

exit 0
