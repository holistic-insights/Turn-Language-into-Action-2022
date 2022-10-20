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
        posts[col] = np.random.randint(1, 100, len(posts.name))

    # run sentiment on comments and 
    posts['Sentiment'] = np.random.randint(1, 100, len(posts.name))

    return posts, raw_comments