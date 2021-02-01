#/usr/bin/bash

if [ "$1" == "" ] || [ "$2" == "" ]; then
  echo "usage: $0 TASK JOBNAME"
  echo "TASK: name as to be found under tasks/ (e.g. forecasts/arome)"
  echo "JOBNAME: configuration of task, as to be found in config file"
  exit
fi

TASK=$1
JOBNAME=$2

# build
python vortex/bin/mkjob.py -j profile=rd-belenos-mt loadedjaplugins=davai name=$JOBNAME task=$TASK
