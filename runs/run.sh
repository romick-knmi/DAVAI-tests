#/usr/bin/bash

./run_ciboulai_setup.sh
./run_packbuild.sh
if [ "$?" == "1" ];then
  echo "Build failed: cannot run tests. Exit."
  exit 1
else
  echo "Let's go for the tests !"
  ./run_tests.sh
fi
