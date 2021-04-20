#!/usr/bin/bash

host=$(davai guess_host)
local_profile="rd-$host-mt"
davai_mkjob_run="python vortex/bin/mkjob.py -j profile=$local_profile"



# Arpege 4D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM_4D_arpege name=BSM_4D_arpege

# Arome 3D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM_3D_arome name=BSM_3D_arome

# Series of canonical forecasts
#davai_mkjob_run task=forecasts.series name=fc-canonical-series

# Series of canonical fullpos
#davai_mkjob_run task=fullpos.series name=fullpos-canonical-series



echo ""
echo "===================================================================================================="
echo "=== DAVAI NRV test bench launched through job scheduler !"
davai_server=$(grep davai_server conf/davai_*.ini | head -n 1 | awk -F '=' '{print $2}')
echo "=== Checkout Ciboulai for results: $davai_server "
echo "===================================================================================================="
