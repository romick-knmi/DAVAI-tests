#!/usr/bin/bash
# RUN THE ELP-SET OF TESTS

# ASSIM
# =====
# BSM = Bator+Screening+Minim
# __obstype indicates one Bator+Screening execution per obstype
# -------------------------------------------------------------
# Arpege
python3 vortex/bin/mkjob.py task=assim.BSM_3D_arpege name=BSM_3D_arpege
python3 vortex/bin/mkjob.py task=assim.BSM_4D_arpege name=BSM_4D_arpege
python3 vortex/bin/mkjob.py task=assim.BS_3D_arpege__obstype name=BS_3D_arpege__obstype
python3 vortex/bin/mkjob.py task=assim.BS_4D_arpege__obstype name=BS_4D_arpege__obstype
# Arome
python3 vortex/bin/mkjob.py task=assim.BSM_3D_arome name=BSM_3D_arome
python3 vortex/bin/mkjob.py task=assim.BS_3D_arome__obstype name=BS_3D_arome__obstype

# ... (to be completed)

# ---------------------------------------------------------------------------------------------------------
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
DAVAI_SERVER=$(grep davai_server conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}')
echo ""
echo "===================================================================================================="
echo "=== DAVAI ELP test bench launched through job scheduler !"
echo "=== Checkout Ciboulai for results: $DAVAI_SERVER "
echo "===================================================================================================="
