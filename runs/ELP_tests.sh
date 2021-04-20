#!/usr/bin/bash

host=$(davai_guess_host)
local_profile="rd-$host-mt"
davai_mkjob_run="python vortex/bin/mkjob.py -j profile=$local_profile"



# === Arpege Assimilation ===

# Arpege 4D Bator+Screening+Minim -- all obs
$davai_mkjob_run task=assim.BSM_4D_arpege name=BSM_4D_arpege

# Arpege 4D Bator+Screening -- by obstype
$davai_mkjob_run task=assim.BS_4D_arpege__obstype name=BS_4D_arpege__obstype

# Arpege 3D Bator+Screening+Minim -- all obs
$davai_mkjob_run task=assim.BSM_3D_arpege name=BSM_3D_arpege

# Arpege 3D Bator+Screening -- by obstype
$davai_mkjob_run task=assim.BS_3D_arpege__obstype name=BS_3D_arpege__obstype



# === Arome Assimilation ===

# Arome 3D Bator+Screening+Minim -- all obs
$davai_mkjob_run task=assim.BSM_3D_arome name=BSM_3D_arome

# Arome 3D Bator+Screening -- by obstype
$davai_mkjob_run task=assim.BS_3D_arome__obstype name=BS_3D_arome__obstype



echo ""
echo "===================================================================================================="
echo "=== DAVAI ELP test bench launched through job scheduler !"
davai_server=$(grep davai_server conf/davai_*.ini | head -n 1 | awk -F '=' '{print $2}')
echo "=== Checkout Ciboulai for results: $davai_server "
echo "===================================================================================================="
