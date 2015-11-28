#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: install.sh
#        USAGE: ./install.sh [uninstall | help]
#  DESCRIPTION: Use this script to install or to uninstall the set of files in
#               this project.
# REQUIREMENTS: Must be run as root.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.1
#      CREATED: 27/11/2015
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

help="\nHelp info:\n\
  To install, just type ./install.sh\n\
  To uninstall, type ./install.sh uninstall, or type ./install help\n"
if [ $# -gt 0 ] && [ "$1" != "uninstall" ] && [ "$1" != "help" ]; then
  echo -e "\nError: unrecognized parameter '$1'\n"
  echo -e ${help}
  exit 1
elif [ $# -gt 0 ] && [ "$1" == "help" ]; then
  echo -e ${help}
  exit 0
fi

# This script must be run root, once we have to copy files to /usr/local
if [ $EUID -ne 0 ]; then
  echo "This script must be run as root." 1>&2
  exit 1
fi

# If we are here, the parameter is right.
target_dir="/usr/local/bin"
icons_dir="/usr/share/pixmaps"

# Install / uninstall shell scripts
cd shell
shellfiles=$(ls *.sh)
cd ..
for ff in $shellfiles; do
  f=${ff%.*}
  dest="$target_dir/$f"
  if [ $# -eq 0 ]; then
    # Installation
    if [ -d "$dest" ]; then
      echo "  Error! '$dest' is a directory!"
      continue
    fi
    cp "shell/$ff" "$target_dir/$f"
    chmod +x "$target_dir/$f"
    echo -e "  $ff \t--> $target_dir/$f"
  else
    # Uninstallation
    rm -f "$target_dir/$f"
    echo -e "  Cleanning '$target_dir/$f'"
  fi
done

# Install / uninstall python programs
cd python
pythonfiles=$(ls *.py)
cd ..
for ff in $pythonfiles; do
  f=${ff%.*}
  dest="$target_dir/$f"
  if [ $# -eq 0 ]; then
    # Installation
    if [ -d "$dest" ]; then
      echo "  Error! '$dest' is a directory!"
      continue
    fi
    cp "python/$ff" "$target_dir/$f"
    chmod +x "$target_dir/$f"
    echo -e "  $ff \t--> $target_dir/$f"
  else
    # Uninstallation
    rm -f "$target_dir/$f"
    echo -e "  Cleanning '$target_dir/$f'"
  fi
done

# Install / uninstall image icons
cd icons
iconsfiles=$(ls *.png)
cd ..
for ff in $iconsfiles; do
  if [ $# -eq 0 ]; then
    # Installation
    cp "icons/$ff" "$icons_dir/$ff"
    echo -e "  $ff \t--> $icons_dir/$ff"
  else
    # Uninstallation
    rm -f "$icons_dir/$ff"
    echo -e "  Cleanning '$icons_dir/$ff'"
  fi
done

exit 0
