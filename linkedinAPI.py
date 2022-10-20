from curses import raw
from pickletools import read_bytes1
import streamlit as st
import pandas as pd
import numpy as np

def getPosts(keywords = None, n_posts = 10):
      # Fetch Linkedin Posts in kaggle data, to be replaced with LinkedIn API
    raw_posts_df = pd.read_csv('Data/linkedin_post_data_kaggle.csv') # from https://www.kaggle.com/datasets/shreyasajal/linkedin-company-pages-data
    raw_comments_df = None
    return raw_posts_df, raw_comments_df

def getCompanyPosts(company_name, keywords = None, n_posts = 10):

     # Fetch Linkedin Posts in kaggle data, to be replaced with LinkedIn API
    raw_posts_df = pd.read_csv('Data/linkedin_post_data_kaggle.csv') # from https://www.kaggle.com/datasets/shreyasajal/linkedin-company-pages-data
    raw_posts_df.drop('Unnamed: 0', axis=1, inplace=True)
    raw_posts_df = raw_posts_df[raw_posts_df.name == company_name]

    raw_comments_df = pd.DataFrame()
    return raw_posts_df, raw_comments_df