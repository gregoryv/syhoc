#!/bin/bash

[[ -z $PREV ]] && echo "set PREV" && exit 1
[[ -z $TAG ]] && export TAG=main

export DEST=docs/$TAG
export DATE=$(date -u +%F)
export stp=stp

#
#  EIDT docs/$TAG/spec.txt and add header
#
echo "Version....: [${TAG#v}]
Obsoletes..: [${PREV#v}]
Published..: $DATE
Author.....: Gregory Vincic

[${TAG#v}]: https://gregoryv.github.io/syhoc/$TAG
[${PREV#v}]: https://gregoryv.github.io/syhoc/$PREV
" > header.txt

set -o xtrace
mkdir -p $DEST
git restore --source $TAG -- spec.txt
cp spec.txt $DEST

# Generate published version
$stp -i template.txt -o $DEST/index.html

# move into docs so the diff titles are nice
pushd docs
python3 pydiff.py -file-a $PREV/spec.txt -file-b $TAG/spec.txt -o $TAG/diff_$PREV.html
popd

rm spec.txt


#
# add an entry in docs/index.html
#
