#!/bin/sh

echo "JOB_BEGIN_AT__"$(date "+%Y.%m.%d-%H.%M.%S")

for lob in "${loblist[@]}"
do

  python /home/andrew_maguire/localDev/codeBase/pmc-analytical-data-mart/nlp/post_parser_google_sentiment.py ${lob} 50 > /home/andrew_maguire/logs/run_nlp_post_parser_google_sentiment_${lob}_LOG_$(date "+%Y.%m.%d-%H.%M.%S").txt  2>&1&

done

echo "JOB_END_AT__"$(date "+%Y.%m.%d-%H.%M.%S")