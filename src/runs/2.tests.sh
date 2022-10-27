#!/usr/bin/bash
# RUN THE TESTS

vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
USECASE=$(grep -P "usecase\s+=" conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}' | awk '{print $0}')

if [ "$USECASE" == "NRV" ];then
  ./2.NRV_tests.sh
elif [ "$USECASE" == "ELP" ];then
  ./2.NRV_tests.sh
  ./2.ELP_tests.sh
else
  echo "Unknown usecase : $USECASE"
  exit 1
fi

