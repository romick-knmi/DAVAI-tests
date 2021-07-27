#!/usr/bin/bash
# RUN THE NRV-SET OF TESTS

# ASSIM
# =====
# BSM = Bator+Screening+Minim
./runjob.py -t assim.BSM_4D_arpege -n BSM_4D_arpege
./runjob.py -t assim.BSM_3D_arome -n BSM_3D_arome

# FORECASTS
# =========
# F_ifs = Forecast IFS
./runjob.py -t forecasts.F_ifs -n F_ifs
# PPF = PGD-Prep-Forecast
./runjob.py -t forecasts.PPF_arpege -n PPF_arpege
./runjob.py -t forecasts.PPF_arome -n PPF_arome
#./runjob.py -t forecasts.series -n fc-canonical-series

# FULLPOS
# =======
#./runjob.py -t fullpos.series -n fullpos-canonical-series


# ---------------------------------------------------------------------------------------------------------
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')
echo ""
echo "===================================================================================================="
echo "=== DAVAI NRV test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
