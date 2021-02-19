#!/usr/bin/bash

davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt'

# Arpege 4D Bator+Screening+Minim
#$davai_mkjob_run task=assim.BSM_arpege_4D name=BSM_arpege_4D

# Arome 3D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM_arome_3D name=BSM_arome_3D

#davai_mkjob_run task=assim.BSM name=BSM-arome-3D
#davai_mkjob_run task=forecasts.series name=fc-canonical-series
#davai_mkjob_run task=fullpos.series name=fullpos-canonical-series

echo "DAVAI NRV test bench launched through job scheduler !"
echo "Checkout Ciboulai for results !"
