#!/usr/bin/bash

davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt'

# === Arpege Assimilation ===

# Arpege 4D Bator+Screening+Minim
#$davai_mkjob_run task=assim.BSM4D_arpege name=BSM4D_arpege

# Arpege 4D Bator+Screening+Minim -- by obstype
#$davai_mkjob_run task=assim.BSM4D_arpege__obstype name=BSM4D_arpege__obstype

# Arpege 3D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM3D_arpege name=BSM3D_arpege

# Arpege 3D Bator+Screening+Minim -- by obstype
$davai_mkjob_run task=assim.BSM3D_arpege__obstype name=BSM3D_arpege__obstype

# === Arome Assimilation ===

# Arome 3D Bator+Screening+Minim
#$davai_mkjob_run task=assim.BSM3D_arome name=BSM3D_arome

# Arome 3D Bator+Screening+Minim -- by obstype
$davai_mkjob_run task=assim.BSM3D_arome__obstype name=BSM3D_arome__obstype

echo "DAVAI ELP test bench launched through job scheduler !"
echo "Checkout Ciboulai for results !"
