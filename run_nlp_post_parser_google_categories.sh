#!/bin/sh

echo "JOB_BEGIN_AT__"$(date "+%Y.%m.%d-%H.%M.%S")

loblist=(bgr deadline footwearnews goldderby hollywoodlife indiewire robbreport spy tvline variety wwd)

for lob in "${loblist[@]}"
do

  python /home/andrew_maguire/localDev/codeBase/pmc-analytical-data-mart/nlp/post_parser_google_categories.py ${lob} 50 > /home/andrew_maguire/logs/run_nlp_post_parser_google_categories_${lob}_LOG_$(date "+%Y.%m.%d-%H.%M.%S").txt  2>&1&

done

echo "JOB_END_AT__"$(date "+%Y.%m.%d-%H.%M.%S")