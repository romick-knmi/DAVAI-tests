#/usr/bin/bash
# RUN THE EXPERIMENT ENTIRELY FROM SCRATCH

# 0. Setup ciboulai XP
./0.setup_ciboulai.sh
ok=$?
if [ "$ok" != "0" ];then
  echo "Ciboulai setup failed: fix before running tests. Exit."
  exit $ok
else
  echo "Let's go for the build !"
  # 1. Build
  ./1.build.sh
  if [ "$?" == "1" ];then
    echo "Build failed: cannot run tests. Exit."
    exit 1
  else
    echo "Let's go for the tests !"
  # 2. Run tests
    ./2.tests.sh
  fi
fi
