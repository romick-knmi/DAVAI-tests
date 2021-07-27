#!/usr/bin/bash

# ASSIM
# =====
# BSM = Bator+Screening+Minim
# __obstype indicates one Bator+Screening execution per obstype
# -------------------------------------------------------------
# Arpege
./runjob.py -t assim.BSM_3D_arpege -n BSM_3D_arpege
./runjob.py -t assim.BSM_4D_arpege -n BSM_4D_arpege
./runjob.py -t assim.BS_3D_arpege__obstype -n BS_3D_arpege__obstype
./runjob.py -t assim.BS_4D_arpege__obstype -n BS_4D_arpege__obstype
# Arome
./runjob.py -t assim.BSM_3D_arome -n BSM_3D_arome
./runjob.py -t assim.BS_3D_arome__obstype -n BS_3D_arome__obstype


# ---------------------------------------------------------------------------------------------------------
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')
echo ""
echo "===================================================================================================="
echo "=== DAVAI ELP test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
