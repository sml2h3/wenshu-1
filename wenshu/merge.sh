#!/bin/bash
path=$1
out_file=$2
if [ -e $out_file ]
then
    rm -f $out_file
fi
touch ${out_file}
#echo  > ${out_file}
for f in `ls ${path}`;
do
    echo "${f}" >> ${out_file}
    cat ${path}/${f} >> ${out_file}
    echo "" >> ${out_file}
done
