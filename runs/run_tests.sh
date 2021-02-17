#!/usr/bin/bash

davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt loadedjaplugins=davai'

# Arpege 4D Bator+Screening+Minim
$davai_mkjob_run task=assim.BSM_arpege_4D name=BSM_arpege_4D

#davai_mkjob_run task=assim.BSM name=BSM-arome-3D
#davai_mkjob_run task=forecasts.series name=fc-canonical-series
#davai_mkjob_run task=fullpos.series name=fullpos-canonical-series

