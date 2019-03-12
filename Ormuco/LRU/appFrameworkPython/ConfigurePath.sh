#!/bin/sh

export PI_APP_FRAMEWORK_PATH="/home/tc-dev/code/lru/appFrameworkPython"
export MY_TEST_APP="/var/lib/my_ormuco"

PATH=${PI_APP_FRAMEWORK_PATH}:${PATH}
PATH=${MY_TEST_APP}:${PATH}
export PATH


