#/usr/bin/bash
# RUN THE EXPERIMENT ENTIRELY FROM SCRATCH

# 1. Setup ciboulai XP
./1.setup_ciboulai.sh
# 2. Build
./2.packbuild.sh
if [ "$?" == "1" ];then
  echo "Build failed: cannot run tests. Exit."
  exit 1
else
  echo "Let's go for the tests !"
# 3. Run tests
  ./3.tests.sh
fi
