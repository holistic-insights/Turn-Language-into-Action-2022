from operator import ge, index
from os import link
import streamlit as st
import pandas as pd
import pandas as pd
import tweepy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import API scripts
import linkedinAPI 
import expertaiAPI

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

st.title("ESG Glassdoor")

st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")

col1, col2, col3 = st.columns(3)
with col1:
    company_name = st.text_input("Company name", value="Dell Technologies")
with col2:
    since_date = st.text_input("Get posts since", value="YYYY-MM-DD")
with col3:
    linkedin_count = st.slider("Number of LinkedIn posts", min_value=100, max_value=1000, step=10, value=0) 

keywords = st.multiselect(
    'Hashtags',
    ['#sustainability', '#mrketing', '#carbon', '#religion', '#engineering', '#datascience', '#holin'])

since_date = since_date[:7] + '--' + since_date[8:]

col1, col2, col3 = st.columns(3)
with col1:
    show_posts = st.checkbox('Show Post Data')
with col2:
    show_analysis = st.checkbox('Show Analysis Data')
with col3:
    submit = st.button('Submit')

if submit:

    # Scrape LinkedIn
    # Top linkedin posts
    raw_posts, raw_comments = linkedinAPI.getPosts(company_name)
    # Company posts
    raw_company_posts, raw_company_comments = linkedinAPI.getCompanyPosts(company_name)

    # Do ESG & Sentiment Analysis
    posts, comments = expertaiAPI.magic(raw_posts, raw_comments)
    company_posts, company_comments = expertaiAPI.magic(raw_company_posts, raw_company_comments)

    st.write("---")
    
    # Summary Estatistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='text-align: center;'>{company_name}</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4 style='text-align: center;'>LinkedIn Top 10</h4>", unsafe_allow_html=True)

    col3, col4, col5, col6 = st.columns(4)
    style = "style='text-align: center; background: #F0F8FF; padding-top: 25px; padding-bottom: 25px;'"
    with col3:
        st.markdown(f"<h3 {style}>{round(company_posts.ESG.mean(), 2)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>ESG Score</p>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<h3 {style}>{round(company_posts.Sentiment.mean(), 2)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Sentiment Score</p>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<h3 {style}>{round(posts.ESG.mean(), 2)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>ESG Score</p>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<h3 {style}>{round(posts.Sentiment.mean(), 2)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Sentiment Score</p>", unsafe_allow_html=True)

    st.write("---")

    # Show Raw Posts
    if show_posts:
        st.write("Raw Posts Data")
        st.write(raw_company_posts)

    # Show Analysed Posts
    if show_analysis:
        st.write("Analysed Posts Data")
        st.write(company_posts)

    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='text-align: center;'>ESG x Sentiment</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.scatter(x=company_posts["Sentiment"], y=company_posts["ESG"])
        sns.despine(left = True)
        plt.ylabel('ESG Score')
        plt.xlabel('Sentiment Score')
        st.pyplot(fig)

    with col2:
        st.markdown(f"<h4 style='text-align: center;'>ESG Scores</h4>", unsafe_allow_html=True)
        cols = ['Biodiversity', 'Gender_Equality', 'Strategy']
        means = []
        for col in cols:
            means.append(company_posts[col].mean())

        df = pd.DataFrame({'Score' : means,
                            'Type' : ['Environmental', 'Social', 'Governance']},
                            index = cols)
        fig, ax = plt.subplots()

        colors = tuple(np.select([df["Type"] == 'Environmental',df["Type"] == 'Social',df["Type"] == 'Governance'], ['palegreen', 'plum', 'gainsboro']))

        ax.barh(width=df.Score, y=df.index, align='center', color = colors)
        sns.despine(left = True)

        st.pyplot(fig)

st.write("Secret Email:", st.secrets["EAI_USERNAME"])
