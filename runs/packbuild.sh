#/usr/bin/bash

local_profile="rd-`davai guess_host`-mt"

# build
export DAVAI_START_BUILD=`python -c "import time; print(time.time())"`
python vortex/bin/mkjob.py -j profile=$local_profile name=packbuild task=build.gmkpack.G2P_CL
# wait for build
export MTOOLDIR=/scratch/mtool/$LOGNAME
python vortex/bin/mkjob.py -j profile=void name=wait4build task=build.wait4build
python wait4build.py
ok=$?
rm -f wait4build.py
if [ "$ok" == "0" ];then
  echo "Build OK: continue"
  exit 0
else
  echo "Build KO ! $ok"
  exit 1
fi
