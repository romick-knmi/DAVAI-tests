#/usr/bin/bash

# find appropriate mkjob profile in config file, and prepare commandline
vapp=$(basename $(dirname $PWD))
vconf=$(basename $PWD)
local_profile=`grep mkjob_profile conf/${vapp}_${vconf}.ini | awk -F "=" '{print $2}'`
DAVAI_MKJOB_RUN="python vortex/bin/mkjob.py -j profile=$local_profile"

# build
export DAVAI_START_BUILD=`python -c "import time; print(time.time())"`
$DAVAI_MKJOB_RUN name=packbuild task=build.gmkpack.G2P_CL

# wait & check for build
export MTOOLDIR=/scratch/mtool/$LOGNAME  # needed to find cached expertise output of build
python vortex/bin/mkjob.py -j profile=void name=wait4build task=build.wait4build
# TODO: move to rd-void (and then remove exec+rm)
python wait4build.py
ok=$?
rm -f wait4build.py

# return status of build
if [ "$ok" == "0" ];then
  echo "Build OK: continue"
  exit 0
else
  echo "Build KO ! $ok"
  exit 1
fi
