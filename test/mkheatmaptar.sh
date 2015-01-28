#!/bin/bash
pushd plots
convert -delay 100 -loop 0 evt*.png brems.gif
i=0; for f in evt*.png; do i=$((i+1)) && cp $f brems$i.png; done; tar -cf brems.tar brems*.png
rm brems*.png
popd
