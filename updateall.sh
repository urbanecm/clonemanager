#!/bin/bash

scriptdir="`dirname \"$0\"`"
dir="$scriptdir/.."
host=`hostname | cut -d. -f 1`
$scriptdir/clone.sh &> /dev/null # Ensure all repos exists

while read repo; do
	echo Processing $repo...
	prevpwd=$PWD
	cd $dir/$repo
	git-wmfupdate
	cd $prevpwd
done < $scriptdir/$host.txt
