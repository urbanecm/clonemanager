#!/bin/bash
scriptdir="`dirname \"$0\"`"
dir="$scriptdir/.."
host=`hostname | cut -d. -f 1`
exclude="11cloneManager"

for i in $(ls $dir | grep -v $exclude); do
	echo $i
done
$scriptdir/clone.sh
