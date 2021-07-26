#!/usr/bin/bash

# find appropriate mkjob profile in config file, and prepare commandline
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
local_profile=$(grep mkjob_profile conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')
DAVAI_MKJOB_RUN="python vortex/bin/mkjob.py -j profile=$local_profile"
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')



# Arpege 4D Bator+Screening+Minim
# -------------------------------
$DAVAI_MKJOB_RUN task=assim.BSM_4D_arpege name=BSM_4D_arpege

# Arome 3D Bator+Screening+Minim
# ------------------------------
$DAVAI_MKJOB_RUN task=assim.BSM_3D_arome name=BSM_3D_arome

# Series of canonical forecasts
# -----------------------------
$DAVAI_MKJOB_RUN task=forecasts.F_ifs name=F_ifs
# PPF = PGD-Prep-Forecast
$DAVAI_MKJOB_RUN task=forecasts.PPF_arpege name=PPF_arpege
#DAVAI_MKJOB_RUN task=forecasts.series name=fc-canonical-series

# Series of canonical fullpos
# ---------------------------
#DAVAI_MKJOB_RUN task=fullpos.series name=fullpos-canonical-series



echo ""
echo "===================================================================================================="
echo "=== DAVAI NRV test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
