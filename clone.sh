#!/bin/bash
scriptdir="`dirname \"$0\"`"
dir="$scriptdir/.."
host=`hostname | cut -d. -f 1`

# Clone all repos
while read repo; do
	echo Processing $repo...
	mkdir -p $dir/$repo
	git clone ssh://urbanecm@gerrit.wikimedia.org:29418/$repo.git $dir/$repo
	prevpwd=$PWD
	cd $dir/$repo
	git review --remote origin -s
	git config user.email "martin.urbanec@wikimedia.cz"
	cd $prevpwd
done < $scriptdir/$host.txt
