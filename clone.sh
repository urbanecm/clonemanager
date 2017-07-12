#!/bin/bash
scriptdir="`dirname \"$0\"`"
dir="$scriptdir/.."

# Clone all repos
while read repo; do
	echo Processing $repo...
	mkdir -p $dir/$repo
	git clone ssh://gerrit/$repo.git $dir/$repo
	prevpwd=$PWD
	cd $dir/$repo
	git review -s
	cd $prevpwd
done < $scriptdir/repos.txt
