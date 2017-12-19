# encoding=utf8
import datetime
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import argparse
import logging

# set logging level
logging.basicConfig(level=logging.WARNING)

# parse args
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script')
    parser.add_argument('lob', choices=['lobA', 'lobB', 'lobC'])
    parser.add_argument('n_posts')
    args = parser.parse_args()
    try:
        # use args
        lob = args.lob
        n_posts = args.n_posts
    except errors.HttpError as e:
        print('Error parsing args')

logging.info(lob)
logging.info(n_posts)
        
# config vars for bq
project_id = 'my-project-name'
private_key = "/location/to/my/key/blahblah.json"

# timestamp for bq target table
bqsuffix = datetime.date.today().strftime('%Y%m%d')

# Instantiates a client
client = language.LanguageServiceClient()

##########################################
## GET DATA
##########################################

qry = """
SELECT
  lob,
  post_date_gmt,
  post_id_domain,
  post_title,
  url as post_url,
  concat(post_title,'. ',post_content_rendered) as post_content_rendered 
FROM
  """+lob+""".post_features
where
  post_content_rendered is not null
  and
  post_id_domain not in (select post_id_domain from nlp.google_sentiment_all group by 1)
order by 
  post_date_gmt desc
LIMIT
  """+n_posts+"""
"""

# get data
df = pd.read_gbq(qry,project_id,private_key=private_key)

##########################################
## DO NLP
##########################################

# loop trough each input                       
for index, row in df.iterrows():

    # get some vars
    text = row['post_content_rendered']
    post_id_domain = row['post_id_domain']
    post_title = row['post_title']
    post_url = row['post_url']
    lob = row['lob']
    post_date_gmt = row['post_date_gmt']
    
    # print info
    logging.info('#' * 25)
    logging.info(post_id_domain)
    logging.info(post_url)
    logging.info('#' * 25)
    
    # create document to parse
    document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
    
    # try parse sentiment
    try:
       sentiment = client.analyze_sentiment(document=document).document_sentiment
    except: 
        pass
    
    # create a df to collect results into
    out_df = pd.DataFrame()
    
    try:
        out_df = out_df.append({'lob': lob,
                                'post_id_domain': post_id_domain,
                                'post_title': post_title,
                                'post_url': post_url,
                                'post_date_gmt': post_date_gmt,
                                'sentiment_magnitude': sentiment.magnitude,
                                'sentiment_score': sentiment.score
                                }, ignore_index=True)                                
    except:
        pass
    
    # if we have data then stream it in
    if out_df.shape[0] > 0:
        # save results to bq
        pd.io.gbq.to_gbq(out_df,'nlp.google_sentiment_raw_'+bqsuffix,project_id,if_exists='append')

