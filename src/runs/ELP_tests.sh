#!/usr/bin/bash

# find appropriate mkjob profile in config file, and prepare commandline
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
local_profile=$(grep mkjob_profile conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}' | xargs)
DAVAI_MKJOB_RUN="python vortex/bin/mkjob.py -j profile=$local_profile"
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')



# === Arpege Assimilation ===

# Arpege 4D Bator+Screening+Minim -- all obs
$DAVAI_MKJOB_RUN task=assim.BSM_4D_arpege name=BSM_4D_arpege

# Arpege 4D Bator+Screening -- by obstype
$DAVAI_MKJOB_RUN task=assim.BS_4D_arpege__obstype name=BS_4D_arpege__obstype

# Arpege 3D Bator+Screening+Minim -- all obs
$DAVAI_MKJOB_RUN task=assim.BSM_3D_arpege name=BSM_3D_arpege

# Arpege 3D Bator+Screening -- by obstype
$DAVAI_MKJOB_RUN task=assim.BS_3D_arpege__obstype name=BS_3D_arpege__obstype



# === Arome Assimilation ===

# Arome 3D Bator+Screening+Minim -- all obs
$DAVAI_MKJOB_RUN task=assim.BSM_3D_arome name=BSM_3D_arome

# Arome 3D Bator+Screening -- by obstype
$DAVAI_MKJOB_RUN task=assim.BS_3D_arome__obstype name=BS_3D_arome__obstype



echo ""
echo "===================================================================================================="
echo "=== DAVAI ELP test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
