import streamlit as st
import pandas as pd
import pandas as pd
#from traitlets import default
import tweepy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import API scripts
import linkedinAPI 
import expertaiAPI


st.title("ESG Glassdoor")

st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")


col1, col2, col3 = st.columns(3)
with col1:
    #company_name = st.text_input("Company name", value="Walmart")
    company_name = st.selectbox("Company", (list(linkedinAPI.getPosts().company.unique())), index=3)

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
    raw_posts = linkedinAPI.getPosts()
    raw_comments = linkedinAPI.getComments()

    # Do ESG & Sentiment Analysis
    posts, comments = expertaiAPI.magic(raw_posts, raw_comments)
    company_posts = posts[posts.company == company_name.lower()]
    company_comments = comments[comments.company == company_name.lower()]

    st.write("---")
    
    # Summary Estatistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='text-align: center;'>{company_name}</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4 style='text-align: center;'>LinkedIn Top 10</h4>", unsafe_allow_html=True)
    # Scores
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
    # posts and comments
    col3, col4, col5, col6 = st.columns(4)
    style = "style='text-align: center; background: #F0F8FF; padding-top: 25px; padding-bottom: 25px;'"
    with col3:
        st.markdown(f"<h3 {style}>{len(company_posts.post_urn)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Posts</p>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<h3 {style}>{round(company_posts.numComments.mean())}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Comments (Avg)</p>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<h3 {style}>{len(posts.post_urn)}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Posts</p>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<h3 {style}>{round(posts.numComments.mean())}</h3", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Comments (Avg)</p>", unsafe_allow_html=True)

    st.write("---")

    # Show Raw Posts
    if show_posts:
        st.write("Raw Posts Data")
        st.write(raw_posts)

    # Show Analysed Posts  
    if show_analysis:
        st.write("Analysed Posts Data")
        st.write(company_posts)

    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='text-align: center;'>ESG x Sentiment</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.scatter(x=company_posts["Sentiment"], y=company_posts["ESG"], cmap='veridis')
        try:
            z = np.polyfit(company_posts["Sentiment"], company_posts["ESG"], 1)
            p = np.poly1d(z)
            ax.plot(company_posts["Sentiment"], p(company_posts["Sentiment"]),"r--")
        except:
            pass
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
