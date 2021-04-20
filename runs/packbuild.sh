#/usr/bin/bash

host=$(davai_guess_host)
local_profile="rd-$host-mt"
davai_mkjob_run="python vortex/bin/mkjob.py -j profile=$local_profile"

# build
export DAVAI_START_BUILD=`python -c "import time; print(time.time())"`
$davai_mkjob_run name=packbuild task=build.gmkpack.G2P_CL

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
