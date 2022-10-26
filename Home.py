import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from expertaiAPI import ExpertAPI
import seaborn as sns
import autokeras as ak
from tensorflow.keras.models import load_model
import tensorflow as tf

categories = ['Environment', 'Social', 'Governance']

subcategories_env_pos = ['Climate Impact', 'Biodiversity and Environmental Footprint', 'Waste and Emission Management', 'Environmental Opportunities ','Waste and Emissions Management ']
subcategories_env_neg = ['Greenwashing','Environmental Crime', 'Biodiversity and Environmental Footprint','Climate Impact','Waste and Emission Management','Waste and Emissions Management ']
subcategories_env = subcategories_env_pos + subcategories_env_neg
subcategories_env = list(dict.fromkeys(subcategories_env))

subcategories_soc_pos = ['Human Capital ','Workplace and Product Safety','Cybersecurity','Diversity and Inclusion','Public Relations','Community Opportunities']
subcategories_soc_neg = ['Human Capital ','Workplace and Product Safety','Cybersecurity','Discrimination','Controversial Profile']
subcategories_soc = subcategories_soc_pos + subcategories_soc_neg
subcategories_soc = list(dict.fromkeys(subcategories_soc))

subcategories_gov_pos_neg = ['Business Ethics and Transparency','Board Engagement','Legal Compliance','Product Stewardship']

subcategories = ['Climate Impact', 'Biodiversity and Environmental Footprint', 'Waste and Emission Management', 'Human Capital ', 'Environmental Opportunities ', 'Waste and Emissions Management ', 'Diversity and Inclusion', 'Workplace and Product Safety', 'Environmental Crime', 'Legal Compliance', 'Business Ethics and Transparency', 'Product Stewardship']
st.title("ESG meter")
st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")

tab1, tab2 = st.tabs(["Company Scoring", "New Post Scoring"])

with tab1:

    st.subheader("Company Scoring")

    all_data = pd.read_csv('Data/posts_esg_final.csv')
    list_of_companies = tuple(all_data['company'].unique().tolist())

    col1, col2 = st.columns(2)

    with col1:

        option = st.selectbox('Search a company', list_of_companies)

    with col2:

        num_posts = st.selectbox('Number of posts', [5, 10, 20, 'All'])

    submit = st.button('Submit', key=1)

    if submit:

        st.markdown(f'<h1 style="color:#ff4b4b">{option}</h1>', unsafe_allow_html=True)

        tab11, tab21 = st.tabs(["Overall Analysis", "Comparison with top 5 companies"])

        with tab11:

            data = all_data.loc[all_data['company'] == option].copy()

            if num_posts == 'All':
                num_posts = len(data)
            
            data = data.sort_values(by='numLikes', ascending=False).iloc[:num_posts].reset_index()

            num_posts = len(data)

            num_esg_pos = data['Positive'].value_counts(dropna=True).sum()
            num_esg_neg = data['Negative'].value_counts(dropna=True).sum()

            cat_counts = dict()
            cat_scores = dict()

            data['Environmental subcategories'] = 0 
            data['Social subcategories'] = 0 
            data['Governance subcategories'] = 0 


            score_env=0
            score_soc=0
            score_gov=0

            for index, col in enumerate(data):
                if index < (len(data)-1):
                    if pd.isna(data.at[index, col]):
                        continue 
                    else:
                        if col in subcategories_env:
                            score_env += data.at[index, col] 
                        elif col in subcategories_soc:
                            score_soc += data.at[index, col]
                        elif col in subcategories_gov_pos_neg:
                            score_gov += data.at[index, col]
                        
                        data.at[index, 'Environmental subcategories'] = score_env
                        data.at[index, 'Social subcategories'] = score_soc
                        data.at[index,'Governance subcategories'] = score_gov
                else: 
                    break

            for col in categories:
                cat_counts[col] = data[col].value_counts(dropna=True).sum()
                score = data[col].dropna().mean()
                if pd.isna(score):
                    score = 0
                cat_scores[col] = score

            cat_counts_df = pd.DataFrame({'Category': list(cat_counts.keys()), 'Counts': list(cat_counts.values())})
            cat_scores_df = pd.DataFrame({'Category': list(cat_scores.keys()), 'Scores Sum': list(cat_scores.values())})

            cat_scores_df = pd.DataFrame({'Category': list(cat_scores.keys()), 'Scores Sum': list(cat_scores.values())})
            cat_scores_df = pd.DataFrame({'Category': list(cat_scores.keys()), 'Scores Sum': list(cat_scores.values())})


            subcat_counts = dict()
            subcat_scores = dict()
            subcat_cat = []

            for col in subcategories:
                subcat_counts[col] = data[col].value_counts(dropna=True).sum()
                score = data[col].dropna().mean()
                if pd.isna(score):
                    score = 0
                subcat_scores[col] = score

            for col in subcat_counts:
                if col in subcategories_env:
                    subcat_cat.append('Environment')
                elif col in subcategories_soc:
                    subcat_cat.append('Social')
                elif col in subcategories_gov_pos_neg:
                    subcat_cat.append('Governance')  
                    
            cat_individual_scores = dict()

            data['ESG total score'] = data[categories].sum(axis=1)

            subcat_counts_df = pd.DataFrame({'Category': list(subcat_counts.keys()), 'Counts': list(subcat_counts.values()), 'Main category': subcat_cat})
            subcat_scores_df = pd.DataFrame({'Category': list(subcat_scores.keys()), 'Scores Sum': list(subcat_scores.values()),'Main category': subcat_cat})

            subcat_counts_df = subcat_counts_df.sort_values(by='Main category')
            subcat_scores_df = subcat_scores_df.sort_values(by='Main category')

            avg_likes = data['numLikes'].mean()
            avg_comments = data['numComments'].mean()

            st.markdown(f'<h5>Overall</h5>', unsafe_allow_html=True)
            st.markdown(f'<p>Number of posts: <b>{num_posts}</b></p>', unsafe_allow_html=True)  
            st.markdown(f'<p>Average number of likes: <b>{avg_likes:.0f}</b></p>', unsafe_allow_html=True)  
            st.markdown(f'<p>Average number of comments: <b>{avg_comments:.0f}</b></p>', unsafe_allow_html=True)

            st.markdown(f'<h4>ESG analysis</h4>', unsafe_allow_html=True)

            st.markdown(f'<h5>ESG categories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_counts_df.sort_values(by='Category'), x='Category', y='Counts', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG categories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG categories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_counts_df.sort_values(by='Category'), x='Category', y='Counts', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)
        
            st.markdown(f'<h5>ESG categories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)
            
            labels = ['Posts with positive sentiment', 'Posts with negative sentiment']
            sizes = [num_esg_pos, num_esg_neg]
            
            st.markdown(f'<h5>ESG sentiment</h5>', unsafe_allow_html=True)
            fig = px.pie(values=sizes, names=labels, color=sizes, color_discrete_sequence=['#00CC96', '#EF553B'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h4>Comments sentiment</h4>', unsafe_allow_html=True)

            data_wcomm = pd.read_csv('Data/comments_sentiment.csv')
            data_esg_final = pd.read_csv('Data/posts_esg_25_10.csv')
            data_esg_final = data_esg_final.rename(columns={'urn':'post_urn'})

            final_df = data_esg_final.merge(data_wcomm, on='post_urn', how='left')
            final_df = final_df.drop_duplicates()
            final_df = final_df.sort_values('sentiment',ascending=False)

            data_x = final_df.loc[final_df['company_x'] == option].copy()

            #top 5 based on ESG total score and  highest total sentiment
            data_x['ESG total score'] = data_x[categories].sum(axis=1)

            total_sentiment = []
            mean_sentiment = []

            total_sentiment = data_x.groupby(by='post_urn')['sentiment'].sum()
            mean_sentiment = data_x.groupby(by='post_urn')['sentiment'].mean()

            frame = {'Total sentiment score': total_sentiment, 'Mean sentiment score': mean_sentiment}
            df_sentiment = pd.DataFrame(frame)

            data_x = data_x.merge(df_sentiment, on='post_urn', how='left')

            top_ESG_data_x = data_x.sort_values('ESG total score',ascending=False).drop_duplicates('post_urn')[0:4]
            top_total_sentiment_data_x = data_x.sort_values('Total sentiment score',ascending=False).drop_duplicates('post_urn')[0:4]
            top_mean_sentiment_data_x = data_x.sort_values('Mean sentiment score',ascending=False).drop_duplicates('post_urn')[0:4]

            data_x_sorted_by_ESG = data_x.sort_values('ESG total score',ascending=False).drop_duplicates('post_urn')
            data_x_sorted_by_total_sentiment = data_x.sort_values('Total sentiment score',ascending=False).drop_duplicates('post_urn')
            data_x_sorted_by_mean_sentiment = data_x.sort_values('Mean sentiment score',ascending=False).drop_duplicates('post_urn')

            st.markdown(f'<h5>Distribution of comments for all posts by a company</h5>', unsafe_allow_html=True)
            fig = px.box(data_frame=data_x , x='sentiment')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>Distribution of comments for top 5 posts with the highest ESG total score</h5>', unsafe_allow_html=True)
            fig = px.box(data_frame=top_ESG_data_x , x='sentiment')
            st.plotly_chart(fig, use_container_width=True)

        with tab21:
            pass

with tab2:
    
    st.subheader("New Post Scoring")

    st.write("Write your post")
    post_text = st.text_area("Write your post", label_visibility='collapsed')

    submit = st.button('Submit', key=2)

    if submit:

        exp = ExpertAPI()
        results_df = exp.esg_detection(pd.DataFrame({'text': [post_text]}))

        all_cat = categories + subcategories + ['Negative', 'Positive']

        for cat in [c for c in all_cat if c not in results_df.columns]:
            results_df[cat] = 0

        if results_df['Positive'].item() > 0:
            post_esg_sentiment = results_df['Positive'].item()
        else:
            post_esg_sentiment = -results_df['Negative'].item()

        cats_df = results_df[categories].transpose().reset_index().rename(columns={'index': 'Category', 0: 'Score'})
        subcats_df = results_df[subcategories].transpose().reset_index().rename(columns={'index': 'Category', 0: 'Score'})

        st.markdown(f'<h5>ESG main categories</h5>', unsafe_allow_html=True)
        st.bar_chart(data=cats_df, x='Category', y='Score')

        st.markdown(f'<h5>ESG sub categories</h5>', unsafe_allow_html=True)
        st.bar_chart(data=subcats_df, x='Category', y='Score')

        fig = go.Figure(go.Indicator(mode = "gauge+number", value = post_esg_sentiment, domain = {'x': [0, 1], 'y': [0, 1]}, title = {'text': "ESG Sentiment"}))
        st.plotly_chart(fig, use_container_width=True)

        x = np.array([post_text])
        
        loaded_model = load_model('model_autokeras', custom_objects=ak.CUSTOM_OBJECTS)
        y_pred = loaded_model.predict(tf.expand_dims(x, -1))
