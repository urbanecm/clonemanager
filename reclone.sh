#!/bin/bash
scriptdir="`dirname \"$0\"`"
dir="$scriptdir/.."
host=`hostname | cut -d. -f 1`

rm -rf $(ls $dir | grep -v $scriptdir)
$scriptdir/clone.sh
