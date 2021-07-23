#/usr/bin/bash

# 1. Setup ciboulai XP
./setup_ciboulai.sh
# 2. Build
./packbuild.sh
if [ "$?" == "1" ];then
  echo "Build failed: cannot run tests. Exit."
  exit 1
else
  echo "Let's go for the tests !"
# 3. Run tests
  ./tests.sh
fi
