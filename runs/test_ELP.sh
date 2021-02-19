#!/usr/bin/bash

davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt'

# === Arpege Assimilation ===

# Arpege 4D Bator+Screening+Minim
#$davai_mkjob_run task=assim.job_BSM_arpege_4D name=BSM_arpege_4D

# Arpege 4D Bator+Screening+Minim -- by obstype
#$davai_mkjob_run task=assim.BSM_arpege_4D__obstype name=BSM_arpege_4D__obstype

# Arpege 3D Bator+Screening+Minim
#$davai_mkjob_run task=assim.job_BSM_arpege_3D name=BSM_arpege_3D

# Arpege 3D Bator+Screening+Minim -- by obstype
#$davai_mkjob_run task=assim.BSM_arpege_3D__obstype name=BSM_arpege_3D__obstype

# === Arome Assimilation ===

# Arome 3D Bator+Screening+Minim -- by obstype
$davai_mkjob_run task=assim.BSM_arome_3D__obstype name=BSM_arome_3D__obstype

echo "DAVAI ELP test bench launched through job scheduler !"
echo "Checkout Ciboulai for results !"
