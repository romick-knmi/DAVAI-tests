#/usr/bin/bash

./setup_ciboulai.sh
./packbuild.sh
if [ "$?" == "1" ];then
  echo "Build failed: cannot run tests. Exit."
  exit 1
else
  echo "Let's go for the tests !"
  ./tests.sh
fi
