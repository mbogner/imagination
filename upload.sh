#!/bin/bash
rsync -avu --delete --progress tmp/target/ manuel@tank:/data/manuel/attic/pictures2/
