from curses import raw
from pickletools import read_bytes1
import streamlit as st
import pandas as pd
import numpy as np
import linkedin_api 
from datetime import datetime
import pandas as pd
import os

def connect():
     return linkedin_api.Linkedin(st.secrets["LINKEDIN_USERNAME"], st.secrets["LINKEDIN_PASSWORD"], refresh_cookies=False)
     
def getPosts(keywords = None, n_posts = 10):
     # Pre-Fetched Linkedin Posts to be replaced with LinkedIn API
     # raw_posts_df = pd.read_csv('Data/linkedin_post_data_kaggle.csv') from https://www.kaggle.com/datasets/shreyasajal/linkedin-company-pages-data
     raw_posts_df = pd.read_csv('Data/posts.csv')
     return raw_posts_df

def getComments(keywords = None, n_posts = 10):
     # Pre-Fetched Linkedin comments to be replaced with LinkedIn API
     raw_comments_df = pd.read_csv('Data/comments.csv')
     return raw_comments_df


def debugLater(api, company, comments_nr):

     #posts_data = pd.read_csv("Data/linkedin_post_data_kaggle.csv")
     #posts_data = posts_data.loc[posts_data.name == company]

     post_urn = "urn:li:activity:6453360792111718400"
     cols = ['comment_urn', 'post_urn', 'ts', 'company', 'author', 'numLikes', 'lang', 'text']

     comments_data = pd.DataFrame(data=[], columns=cols)

     post_urn = str(post_urn)

     # Get Comments
     comments = api.get_post_comments(post_urn, comment_count=comments_nr)
     n_comments = len(comments)
     st.write(f'comments: {n_comments}')


     for j in range(n_comments):

          # urn
          comment_urn = comments[j]['urn'].split(',')[-1][:-1]

          # Author
          try:
               author = comments[j]['commenter']['com.linkedin.voyager.feed.MemberActor']['urn'].split(':')[-1]
          except:
               author = comments[j]['commenter']['com.linkedin.voyager.feed.CompanyActor']['urn'].split(':')[-1]

          # numLikes
          numLikes = comments[j]['socialDetail']['likes']['paging']['total']

          try:
               lang = comments[j]['originalLanguage']
               
          except:
               lang = "Other"

          text = comments[j]['commentV2']['text']

          new_row = {'comment_urn': comment_urn,
                    'post_urn': post_urn,
                    'ts': ts,
                    'company': company,
                    'author': author,
                    'numLikes': numLikes,
                    'lang': lang,
                    'text': text}

          comments_data = comments_data.append(new_row, ignore_index=True)

     comments_data.set_index('comment_urn', inplace=True)
     comments_data.to_csv('Data/company_comments.csv', header='cols', encoding='utf-8')
     return comments_data

     #     if not os.path.isfile('comments.csv'):
     #         comments_data.to_csv('comments.csv', header='cols', encoding='utf-8')

     #     else: # else it exists so append without writing the header
     #         comments_data.to_csv('comments.csv', mode='a', header=False, encoding='utf-8')