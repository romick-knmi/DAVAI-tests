#!/usr/bin/bash
# RUN THE NRV-SET OF TESTS

# ASSIM
# =====
# BSM = Bator+Screening+Minim
python3 vortex/bin/mkjob.py task=assim.BSM_4D_arpege name=BSM_4D_arpege
python3 vortex/bin/mkjob.py task=assim.BSM_3D_arome name=BSM_3D_arome

# FORECASTS
# =========
# F_ifs = Forecast IFS
python3 vortex/bin/mkjob.py task=forecasts.F_ifs name=F_ifs
# PPF = PGD-Prep-Forecast
python3 vortex/bin/mkjob.py task=forecasts.PPF_arpege name=PPF_arpege
python3 vortex/bin/mkjob.py task=forecasts.PPF_arome name=PPF_arome
#python3 vortex/bin/mkjob.py task=forecasts.series name=fc-canonical-series

# FULLPOS
# =======
#python3 vortex/bin/mkjob.py task=fullpos.series name=fullpos-canonical-series

# ... (to be completed)

# ---------------------------------------------------------------------------------------------------------
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')
echo ""
echo "===================================================================================================="
echo "=== DAVAI NRV test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
