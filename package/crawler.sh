#!/bin/bash

# echo $PATH
# which python3

pycmd='python3'
mod_id='crawler'
mod_folder="./${mod_id}"

# echo "# starting crawler."

#
# check python executable's version.
#
sval=`${pycmd} --version 2>/dev/null`
if [ $? -ne 0 ]
then
	echo "not found python3."
	exit 1
fi

py_ver=`echo ${sval} | awk '{print $2}'`

echo "#=========================="
echo "# python version : ${py_ver}"
echo "#=========================="
#
# check module exists.
#
if [ ! -d ${mod_folder} ]
then
	echo "not found module folder - ${mod_folder}"
	exit 2
fi

#
# run module with python
#
cmd="${pycmd} -m ${mod_id} $*"
$cmd
exit_code=$?

# echo "#"
# echo "# crawler done.exit code(${exit_code})"
# echo "#"

exit ${exit_code}



