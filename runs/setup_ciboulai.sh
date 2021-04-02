#/usr/bin/bash

python vortex/bin/mkjob.py -j profile=void name=ciboulai_xpsetup task=ciboulai_xpsetup
# TODO: move to rd-void (and then remove exec+rm)
python ciboulai_xpsetup.py
rm -f ciboulai_xpsetup.py

