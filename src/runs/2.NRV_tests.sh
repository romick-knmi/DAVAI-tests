#!/usr/bin/bash
# RUN THE NRV-SET OF TESTS

# ASSIM
# =====
# BSM = Bator+Screening+Minim
# BsC = Bator_surf+Canari
python3 vortex/bin/mkjob.py -j task=assim.BSM_4D_arpege name=BSM_4D_arpege
python3 vortex/bin/mkjob.py -j task=assim.BSM_3D_arome name=BSM_3D_arome
python3 vortex/bin/mkjob.py -j task=assim.BsC_arpege name=BsC_arpege

# FORECASTS
# =========
python3 vortex/bin/mkjob.py -j task=forecasts.standalone_forecasts name=standalone_forecasts
python3 vortex/bin/mkjob.py -j task=forecasts.canonical_forecasts name=canonical_forecasts

# MIXS
# ====
# PF = Prep-Forecast (using older PGD)
# PPF = PGD-Prep-Forecast (using new PGD)
python3 vortex/bin/mkjob.py -j task=mixs.PF name=PF
python3 vortex/bin/mkjob.py -j task=mixs.PPF name=PPF


# FULLPOS
# =======
# Fp_lbc = Fullpos creation of LBC files
python3 vortex/bin/mkjob.py -j task=fullpos.Fp_lbc name=Fp_lbc

# SURFEX
# ======
# PP_geo = PGD+Prep on a range of Gauss & LAM geometries
python3 vortex/bin/mkjob.py -j task=surfex.PP_geo name=PP_geo

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
