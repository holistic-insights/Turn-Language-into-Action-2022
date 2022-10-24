import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

categories = ['Environment', 'Social', 'Governance']
subcategories = ['Climate Impact', 'Biodiversity and Environmental Footprint', 'Waste and Emissions Management ', 'Human Capital ', 'Environmental Opportunities ', 'Waste and Emission Management', 'Diversity and Inclusion', 'Workplace and Product Safety', 'Environmental Crime', 'Legal Compliance', 'Business Ethics and Transparency', 'Product Stewardship']

st.title("ESG meter")
st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")

tab1, tab2 = st.tabs(["Company Scoring", "New Post Scoring"])

with tab1:

    st.subheader("Company Scoring")

    all_data = pd.read_csv('Data/posts_esg_final.csv')
    list_of_companies = tuple(all_data['company'].unique().tolist())

    option = st.selectbox('Search a company', list_of_companies)

    submit = st.button('Submit', key=1)

    if submit:

        st.markdown(f'<h1 style="color:#ff4b4b">{option}</h1>', unsafe_allow_html=True)

        tab11, tab21 = st.tabs(["Overall Analysis", "Comparison with others"])

        with tab11:

            data = all_data.loc[all_data['company'] == option].copy()

            num_esg_pos = data['Positive'].value_counts(dropna=True).sum()
            num_esg_neg = data['Negative'].value_counts(dropna=True).sum()

            cat_counts = dict()
            cat_scores = dict()

            for col in categories:
                cat_counts[col] = data[col].value_counts(dropna=True).sum()
                score = data[col].dropna().mean()
                if pd.isna(score):
                    score = 0
                cat_scores[col] = score

            cat_counts_df = pd.DataFrame({'Category': list(cat_counts.keys()), 'Counts': list(cat_counts.values())})
            cat_scores_df = pd.DataFrame({'Category': list(cat_scores.keys()), 'Scores Sum': list(cat_scores.values())})

            subcat_counts = dict()
            subcat_scores = dict()

            for col in subcategories:
                subcat_counts[col] = data[col].value_counts(dropna=True).sum()
                score = data[col].dropna().mean()
                if pd.isna(score):
                    score = 0
                subcat_scores[col] = score

            subcat_counts_df = pd.DataFrame({'Category': list(subcat_counts.keys()), 'Counts': list(subcat_counts.values())})
            subcat_scores_df = pd.DataFrame({'Category': list(subcat_scores.keys()), 'Scores Sum': list(subcat_scores.values())})

            avg_likes = data['numLikes'].mean()
            avg_comments = data['numComments'].mean()

            st.markdown(f'<p>Average number of likes: <b>{avg_likes:.0f}</b></p>', unsafe_allow_html=True)  
            st.markdown(f'<p>Average number of likes: <b>{avg_comments:.0f}</b></p>', unsafe_allow_html=True)

            labels = ['Posts with positive sentiment', 'Posts with negative sentiment']
            sizes = [num_esg_pos, num_esg_neg]
            explode = (0, 0) 

            st.markdown(f'<h5>ESG sentiment</h5>', unsafe_allow_html=True)
            fig = px.pie(values=sizes, names=labels)

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h4>ESG analysis</h4>', unsafe_allow_html=True)

            only_main = st.checkbox('Only show main categories', value=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<h5>ESG categories counts</h5>', unsafe_allow_html=True)
                st.bar_chart(data=cat_counts_df, x='Category', y='Counts')
            with col2:
                st.markdown(f'<h5>ESG categories scores</h5>', unsafe_allow_html=True)
                st.bar_chart(data=cat_scores_df, x='Category', y='Scores Sum')

            if not only_main:

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f'<h5>ESG subcategories counts</h5>', unsafe_allow_html=True)
                    st.bar_chart(data=subcat_counts_df, x='Category', y='Counts')
                with col2:
                    st.markdown(f'<h5>ESG subcategories scores</h5>', unsafe_allow_html=True)
                    st.bar_chart(data=subcat_scores_df, x='Category', y='Scores Sum')


        with tab21:
            pass

with tab2:
    
    st.subheader("New Post Scoring")


    st.write("Write your post")
    post_text = st.text_area("Write your post", label_visibility='collapsed')

    submit = st.button('Submit', key=2)

    if submit:
        cat = 'Environment'

        col1, col2 = st.columns(2)

        with col1:
            exp1 = st.expander("fff")
            exp1.markdown(f'<h4>ESG Category</h4>', unsafe_allow_html=True)
            exp1.markdown(f'<h2 style="color:#ff4b4b">{cat}</h2>', unsafe_allow_html=True)
        with col2:
            exp2 = st.expander("eee")
            fig = go.Figure(go.Indicator(mode = "gauge+number", value = 13, domain = {'x': [0, 1], 'y': [0, 1]}, title = {'text': "ESG Sentiment"}))
            exp2.plotly_chart(fig, use_container_width=True)

