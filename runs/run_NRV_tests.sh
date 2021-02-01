#/usr/bin/bash

alias davai_mkjob_run='python vortex/bin/mkjob.py -j profile=rd-belenos-mt loadedjaplugins=davai'
davai_mkjob_run task=assim.BSM name=BSM-4D-arpege
davai_mkjob_run task=assim.BSM name=BSM-3D-arome
davai_mkjob_run task=forecasts.series name=fc-canonical-series
davai_mkjob_run task=fullpos.series name=fullpos-canonical-series

