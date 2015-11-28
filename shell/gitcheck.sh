#!/bin/bash
#-----------------------------------------------------------------------------
#         FILE: gitcheck.sh
#        USAGE: gitcheck [PATH | help]
#  DESCRIPTION: This script iterates over the given directory (or over to
#               current one, if no parameters given) and search for all git
#               repositories inside. For each repo, shows the current branch
#               and the current state. Type gitcheck help for more info.
# REQUIREMENTS: The program git must be installed in your system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

# Global counter for repos
global_num=0

# print_line [branch_colored] [path]
function print_line {
  printf "%3d " $global_num
  echo -en "$1"
  for i in $(seq 1 $((34 - ${#1}))); do
    echo -n " "
  done
  echo -e "$2"
}

# dir_iterate [dir_path]
function dir_iterate {
  for d in "$1"/*; do
    dir_array[$i]=$d
    ((i++))
    if [ -d "$d" ]; then
      if [ -d "$d"/.git ]; then
        ((global_num++))
        pushd "$d" > /dev/null
        branch=`git branch | grep \* | awk '{print $2}'`
        if [ "" == "$branch" ]; then
          print_line "{\e[1;30mno branch\e[0m}" "$d"
          continue
        fi
        git update-index -q --refresh
        git diff-index --quiet HEAD --
        if [ 0 -eq $? ]; then
          ahead=`git status -sb | grep ahead`
          if [ "" == "$ahead" ]; then
            print_line "{\e[1;32m$branch\e[0m}" "$d"
          else
            print_line "{\e[1;34m$branch\e[0m}" "$d"
          fi
        else
          print_line "{\e[1;31m$branch\e[0m}" "$d"
        fi
        popd > /dev/null
      else
        dir_iterate "$d"
      fi
    fi
  done
}

function show_help {
  echo "Usage: $0 [PATH | help]"
  echo "Brief: List all git repositories, showing the currrent branch."
  echo "       The branch name is painted according to the following rules:"
  echo -e "       {\e[1;31mbranch\e[0m} -- uncommitted changes"
  echo -e "       {\e[1;34mbranch\e[0m} -- all committed, but not pushed to remote"
  echo -e "       {\e[1;32mbranch\e[0m} -- all committed and pushed"
  echo -e "       {\e[1;30mbranch\e[0m} -- no branch on repo"
}

function _main {
  if [ "" == "$1" ]; then
    dir_iterate `pwd`
  elif [ "help" == "$1" ]; then
    show_help
  else
    dir_iterate "$1"
  fi
  return 0
}

_main "$1"
exit $?
