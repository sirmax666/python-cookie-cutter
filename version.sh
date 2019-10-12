#!/bin/bash -
# Read version file
MAJOR=`cat version.yaml | sed -n 's/major\: *\(\S*\)/\1/p'`
MINOR=`cat version.yaml | sed -n 's/minor\: *\(\S*\)/\1/p'`
PATCH=`cat version.yaml | sed -n 's/patch\: *\(\S*\)/\1/p'`
echo -n "$MAJOR.$MINOR.$PATCH"