#/usr/bin/bash
# BUILD EXECUTABLES

# superseding arguments
arg=""
if [ "$1" == "preexisting_pack=True" ] || [ "$1" == "preexisting_pack=False" ];then
    echo "Conf attribute '$1' superseded by commandline argument."
    arg=$1
elif [ "$1" != "" ];then
    echo "Commandline argument '$1' ignored."
fi
# build
export DAVAI_START_BUILD=`python -c "import time; print(time.time())"`
python3 vortex/bin/mkjob.py -j name=packbuild task=build.gmkpack.G2P_CL $arg
# bundle build
#python3 vortex/bin/mkjob.py -j name=packbuild task=build.gmkpack.B2P_CL $arg

# wait & check for build
export MTOOLDIR=/scratch/mtool/$LOGNAME  # needed to find cached expertise output of build
python3 vortex/bin/mkjob.py -j profile=rd name=wait4build task=build.wait4build
ok=$?

# return status of build
if [ "$ok" == "0" ];then
  echo "Build OK: continue"
  exit 0
else
  echo "Build KO ! $ok"
  echo "See log in $MTOOLDIR/<jobid>"
  exit 1
fi
