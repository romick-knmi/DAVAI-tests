#!/usr/bin/bash

local_profile="rd-`davai guess_host`-mt"
davai_mkjob_run="python vortex/bin/mkjob.py -j profile=$local_profile"



# Arpege 4D Bator+Screening+Minim
#$davai_mkjob_run task=assim.BSM4D_arpege name=BSM4D_arpege

# Arome 3D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM3D_arome name=BSM3D_arome

#davai_mkjob_run task=forecasts.series name=fc-canonical-series
#davai_mkjob_run task=fullpos.series name=fullpos-canonical-series



echo ""
echo "===================================================================================================="
echo "=== DAVAI NRV test bench launched through job scheduler !"
davai_server=$(grep davai_server conf/davai_*.ini | head -n 1 | awk -F '=' '{print $2}')
echo "=== Checkout Ciboulai for results: $davai_server "
echo "===================================================================================================="
