from curses import raw
from pickletools import read_bytes1
import streamlit as st
import pandas as pd
import numpy as np

def magic(raw_posts, raw_comments):

    # Run esg
    cols = ['ESG', 'Environment', 'Social', 'Governance', 'Biodiversity', 'Gender_Equality', 'Strategy']

    posts = raw_posts.copy()
    for col in cols:
        posts[col] = np.random.randint(1, 100, len(posts.company))

    comments = raw_comments.copy()
    comments['Sentiment'] = np.random.randint(1, 100, len(comments.company))

    # Post sentiment as average of comment sentiment
    posts['Sentiment'] = posts['post_urn'].apply(lambda x: comments[comments.post_urn == x]['Sentiment'].mean())

    return posts, comments