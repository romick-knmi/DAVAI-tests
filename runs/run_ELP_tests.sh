#!/usr/bin/bash

davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt loadedjaplugins=davai'

# Arpege 4D Bator+Screening+Minim -- by obstype
$davai_mkjob_run task=assim.BSM_arpege_4D__obstype name=BSM_arpege_4D__obstype

echo "DAVAI test bench launched through job scheduler !"
echo "Checkout Ciboulai for results !"
