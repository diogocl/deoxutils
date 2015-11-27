#!/bin/bash

# You can use this script to install or to uninstall this set of files.
# To install, just type ./install.sh.
# To uninstall, type ./install.sh uninstall, or type ./install help.
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
target_dir="/usr/local"

cd shell
shellfiles=$(ls *.sh)
cd ..

for ff in $shellfiles; do
	f=${ff%.*}
	dest="$target_dir/bin/$f"
	if [ $# -eq 0 ]; then
		# Installation
		if [ -d "$dest" ]; then
			echo "  Error! '$dest' is a directory!"
			continue
		fi
		cp "shell/${ff}" "$target_dir/bin/$f"
		chmod +x "$target_dir/bin/$f"
		echo -e "  $ff \t\t--> $f (chmod +x) --> $target_dir/bin"
	else
		# Uninstallation
		rm -f "$target_dir/bin/$f"
		echo -e "  Cleanning '$target_dir/bin/$f'"
	fi
done

exit 0
