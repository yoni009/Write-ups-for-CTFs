#!/bin/bash

shopt -s nullglob

myname=$(whoami)

cd /var/spool/"$myname"/foo || exit 
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
	if [ "$i" != "." ] && [ "$i" != ".." ];
	then
	echo "Handling $i"
	owner="$(stat --format "%U" "./$i")"
	if [ "${owner}" = "bandit23" ] && [ -f "$i" ]; then
		timeout -s 9 60 "./$i"
		fi
		rm -rf "./$i"
		fi
		
