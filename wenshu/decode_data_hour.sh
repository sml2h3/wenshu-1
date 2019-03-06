date_0=`date -d "1 hours ago" +%H`
date_1=`date -d "1 hours ago" +%Y%m%d_%H`
date_2=`date -d "+1 hours" +%H`
date_3=`date -d "2 hours ago" +%Y%m%d_%H`
date_4=`date -d "25 hours ago" +%Y%m%d_%H`

cd data/
rm -rf $date_2
mkdir $date_2
cd ../

sh decode_data.sh data/$date_0 json/tmp_data json/$date_1
zip json/"$date_1".zip json/$date_1

cd json/
rm -f $date_4
cd ../
sh seg_data.sh $date_1 $date_4
#echo $date_0
#echo $date_1
#echo $date_2
#echo $date_3
#echo $date_4
#echo `ls data/$date_2/`
#echo $date_2
