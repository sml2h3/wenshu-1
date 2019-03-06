date_0=$1
date_1=$2
cat json/$date_0 |python seg_data.py $date_0 >> log/log_doc_id_data
zip -r doc_id_data/"$date_0"_doc.zip doc_id_data/$date_0
cd doc_id_data/
rm -rf "$date_1"
