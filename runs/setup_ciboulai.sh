#/usr/bin/bash

python vortex/bin/mkjob.py -j profile=void name=ciboulai_xpsetup task=ciboulai_xpsetup
python ciboulai_xpsetup.py
rm -f ciboulai_xpsetup.py

