#!/bin/bash -e

[[ -z $PREV ]] && echo "set PREV" && exit 1

export REL=$1
export TAG=$1
[[ -z $REL ]] && export TAG=main && export REL="unreleased"


export DEST=docs/$REL
export DATE=$(date -u +%F)
export stp=stp

#
#  EIDT docs/$TAG/spec.txt and add header
#
echo "Version....: ${REL#v}
Obsoletes..: [${PREV#v}]
Published..: $DATE
Author.....: Gregory Vincic

[${PREV#v}]: diff_$PREV.html
" > header.txt

set -o xtrace
mkdir -p $DEST
git restore --source $TAG -- spec.txt
cp spec.txt $DEST

# Generate published version
$stp -i template.txt -o $DEST/index.html

# move into docs so the diff titles are nice
pushd docs
python3 pydiff.py -file-a $PREV/spec.txt -file-b $REL/spec.txt -o $REL/diff_$PREV.html
popd

rm spec.txt header.txt


#
# add an entry in docs/index.html
#
