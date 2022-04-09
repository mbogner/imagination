#!/bin/bash
mkdir -p tmp/tank/
rsync -avu --delete --progress manuel@tank:/data/manuel/attic/pictures/ tmp/tank_bak/