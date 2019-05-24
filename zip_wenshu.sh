time_0=`date`
date_0=`date -d "1 hours ago" +%Y%m%d_%H`
date_1=`date -d "25 hours ago" +%Y%m%d_%H`
date_2=`date -d "+1 hours" +%Y%m%d_%H`
number=`ls data/"$date_0"|wc -l `
echo $time_0 $date_0 $number>> log/log_doc_id_data
zip -r data/"$date_0"_doc.zip data/$date_0
cd data/
rm -rf "$date_1"
mkdir $date_2
