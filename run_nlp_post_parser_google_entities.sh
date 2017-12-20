#!/bin/sh

echo "JOB_BEGIN_AT__"$(date "+%Y.%m.%d-%H.%M.%S")

loblist=(lobA lobB lobC)

for lob in "${loblist[@]}"
do

  python post_parser_google_entities.py ${lob} 50 > /logs/run_nlp_post_parser_google_entities_${lob}_LOG_$(date "+%Y.%m.%d-%H.%M.%S").txt  2>&1&

done

echo "JOB_END_AT__"$(date "+%Y.%m.%d-%H.%M.%S")