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
from PIL import Image
import requests
from plotly.subplots import make_subplots


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


def company_analysis(data):

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

    return num_posts, num_esg_neg, num_esg_pos, avg_likes, avg_comments, cat_counts_df, cat_scores_df, subcat_counts_df, subcat_scores_df

def comments_analysis(data_x):

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

    return data_x, top_ESG_data_x

st.title("SustainaMeter")
st.write("Raising transparency on companies' attitude towards ESG")

tab1, tab2 = st.tabs(["Company Scoring", "New Post Scoring"])

with tab1:

    st.subheader("Company Scoring")

    all_data = pd.read_csv('ESG Models/Data/posts_esg_final.csv')
    list_of_companies = tuple(all_data['company'].unique().tolist())

    companies_info = pd.read_csv("Data Scrapping/linkedin-api/data/fortune1000_twitter_linkedin.csv", encoding = "ISO-8859-1")[['linkedin', 'name', 'logo']]

    list_of_companies_rich = companies_info[companies_info.linkedin.isin(list_of_companies)].name.values

    col1, col2, col3 = st.columns([2,1,3])

    with col1:

        option_name = st.selectbox('Search a company', list_of_companies_rich)

    with col2:

        num_posts = st.selectbox('Number of posts', ['All', 20, 10, 5])

    with col3:
        choose_top_5 = st.selectbox('Compare with top 5 companies based on', ['Number of posts', 'Number of likes', 'Number of comments', 'ESG sentiment'])

    submit = st.button("Go!", key=1)

    if submit:

        option_logo = "https://" + companies_info.loc[companies_info.name == option_name].logo.values[0]
        logo = Image.open(requests.get(option_logo, stream=True).raw)
        option = companies_info.loc[companies_info.name == option_name].linkedin.values[0]

        # blank spaces
        st.markdown("#")

        # logo and company name 
        col1, mid, col2 = st.columns([3,1.5,20])
        with col1:
            st.image(logo, width=100)
        with col2:
            st.markdown(f'<h1 style="color:#ff4b4b, text-align: center">{option_name}</h1>', unsafe_allow_html=True)

        tab11, tab12 = st.tabs(["Overall Analysis", "Comparison with Top 5 Companies"])

        # data display
        with tab11:

            data = all_data.loc[all_data['company'] == option].copy()

            if num_posts == 'All':
                num_posts = len(data)
            
            data = data.sort_values(by='numLikes', ascending=False).iloc[:num_posts].reset_index()

            num_posts, num_esg_neg, num_esg_pos, avg_likes, avg_comments, cat_counts_df, cat_scores_df, subcat_counts_df, subcat_scores_df = company_analysis(data)

            layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=10, #right margin
                    b=0, #bottom margin
                    t=0, #top margin
                )
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                fig = go.Indicator(
                    mode = "number",
                    value = np.round(num_posts),
                    title = {"text": "Number of posts"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            with col2:

                fig = go.Indicator(
                    mode = "number",
                    value = np.round(avg_likes),
                    title = {"text": "Average likes"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            with col3:

                fig = go.Indicator(
                    mode = "number",
                    value = np.round(avg_comments),
                    title = {"text": "Average comments"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h4>ESG analysis</h4>', unsafe_allow_html=True)

            st.markdown(f'<h5>ESG categories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_counts_df.sort_values(by='Category'), x='Category', y='Counts', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG categories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG subcategories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_counts_df.sort_values(by='Category'), x='Category', y='Counts', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)
        
            st.markdown(f'<h5>ESG subcategories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)
            
            labels = ['Positive', 'Negative']
            sizes = [num_esg_pos, num_esg_neg]
            
            st.markdown(f'<h5>Posts ESG sentiment</h5>', unsafe_allow_html=True)
            fig = px.pie(values=sizes, names=labels, color=sizes, color_discrete_sequence=['#00CC96', '#EF553B'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h4>Comments sentiment analysis</h4>', unsafe_allow_html=True)

            data_wcomm = pd.read_csv('ESG Models/Data/comments_sentiment.csv')
            data_esg_final = pd.read_csv('ESG Models/Data/posts_esg_25_10.csv')
            data_esg_final = data_esg_final.rename(columns={'urn':'post_urn'})

            final_df = data_esg_final.merge(data_wcomm, on='post_urn', how='left')
            final_df = final_df.drop_duplicates()
            final_df = final_df.sort_values('sentiment',ascending=False)

            data_x = final_df.loc[final_df['company_x'] == option].copy()

            data_x, top_ESG_data_x = comments_analysis(data_x)

            st.markdown(f'<h5>Distribution of comments for all posts</h5>', unsafe_allow_html=True)

            if data_x['sentiment'].median() > 0:
                color = "#00CC96"
            else:
                color = "#EF553B"

            fig = go.Figure()
            fig.add_trace(go.Box(x=data_x['sentiment'], name=option_name, marker_color = color))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>Distribution of comments for top 5 posts with the highest ESG total score</h5>', unsafe_allow_html=True)

            if top_ESG_data_x['sentiment'].median() > 0:
                color = "#00CC96"
            else:
                color = "#EF553B"

            fig = go.Figure()
            fig.add_trace(go.Box(x=top_ESG_data_x['sentiment'], name=option_name, marker_color = color))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<a href='#esg-meter'>Go to top</a>", unsafe_allow_html=True)

        with tab12:


            if choose_top_5 == 'Number of likes':

                top = all_data[['company', 'numLikes']].groupby('company').mean().reset_index().sort_values(by='numLikes', ascending=False).iloc[:5].reset_index().drop(columns=['index'])
                top_companies = top['company'].tolist()
                top_data = all_data.loc[all_data['company'].isin(top_companies)]
                data = top_data.copy()

                if num_posts == 'All':
                    num_posts = len(data)

                data = data.sort_values(by='numLikes', ascending=False).iloc[:num_posts].reset_index()

            elif choose_top_5 == 'Number of comments':

                top = all_data[['company', 'numComments']].groupby('company').mean().reset_index().sort_values(by='numComments', ascending=False).iloc[:5].reset_index().drop(columns=['index'])
                top_companies = top['company'].tolist()
                top_data = all_data.loc[all_data['company'].isin(top_companies)]
                data = top_data.copy()

                if num_posts == 'All':
                    num_posts = len(data)

                data = data.sort_values(by='numLikes', ascending=False).iloc[:num_posts].reset_index()

            elif choose_top_5 == 'Number of posts':

                top = all_data[['company', 'numLikes']].groupby('company').count().reset_index().sort_values(by='numLikes', ascending=False).iloc[:5].reset_index().drop(columns=['index'])
                top_companies = top['company'].tolist()
                top_data = all_data.loc[all_data['company'].isin(top_companies)]
                data = top_data.copy()

                if num_posts == 'All':
                    num_posts = len(data)

                data = data.sort_values(by='numLikes', ascending=False).iloc[:num_posts].reset_index()
            
            num_posts_top5, num_esg_neg_top5, num_esg_pos_top5, avg_likes_top5, avg_comments_top5, cat_counts_df_top5, cat_scores_df_top5, subcat_counts_df_top5, subcat_scores_df_top5 = company_analysis(data)


            layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=10, #right margin
                    b=0, #bottom margin
                    t=0, #top margin
                )
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                fig = go.Indicator(
                    mode = "number+delta",
                    value = np.round(num_posts),
                    delta = {'position': "top", 'reference': np.round(num_posts_top5)},
                    title = {"text": "Number of posts<br><span style='font-size:0.8em;color:gray'>Difference to top 5</span><br>"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            with col2:

                fig = go.Indicator(
                    mode = "number+delta",
                    value = np.round(avg_likes),
                    delta = {'position': "top", 'reference': np.round(avg_likes_top5)},
                    title = {"text": "Average likes<br><span style='font-size:0.8em;color:gray'>Difference to top 5</span><br>"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            with col3:

                fig = go.Indicator(
                    mode = "number+delta",
                    value = np.round(avg_comments),
                    delta = {'position': "top", 'reference': np.round(avg_likes_top5)},
                    title = {"text": "Average comments<br><span style='font-size:0.8em;color:gray'>Difference to top 5</span><br>"},
                    domain = {'x': [0, 1], 'y': [0, 1]})
                fig = dict(data=[fig], layout=layout)
                st.plotly_chart(fig, use_container_width=True)

            cat_counts_df['Category'] = cat_counts_df['Category'].apply(lambda x: f'{x} ({option_name})')
            cat_counts_df_top5['Category'] = cat_counts_df_top5['Category'].apply(lambda x: f'{x} (Top 5)')

            cat_counts_df['Source'] = option_name
            cat_counts_df['Source'] ='Top 5'

            cat_counts_df_top5['Counts'] = cat_counts_df_top5['Counts'].apply(lambda x: x/5)

            cat_counts_df_all = pd.concat([cat_counts_df, cat_counts_df_top5], ignore_index=True)

            st.markdown(f'<h4>ESG analysis</h4>', unsafe_allow_html=True)

            st.markdown(f'<h5>ESG categories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_counts_df_all.sort_values(by='Category'), x='Category', y='Counts', pattern='Source', color='Category', color_discrete_sequence=['#B6E886', '#B6E886', '#FF6692', '#FF6692', '#19D3F3', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG categories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=cat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>ESG subcategories counts</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_counts_df.sort_values(by='Category'), x='Category', y='Counts', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)
        
            st.markdown(f'<h5>ESG subcategories scores</h5>', unsafe_allow_html=True)
            fig = px.bar(data_frame=subcat_scores_df.sort_values(by='Category'), x='Category', y='Scores Sum', color='Main category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>Posts ESG sentiment</h5>', unsafe_allow_html=True)

            labels = ['Positive', 'Negative']

            fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                                subplot_titles=[option_name, 'Top 5'])
            fig.add_trace(go.Pie(labels=labels, values=[num_esg_pos, num_esg_neg], scalegroup='one',
                                name=option_name), 1, 1)
            fig.add_trace(go.Pie(labels=labels, values=[num_esg_pos_top5, num_esg_neg_top5], scalegroup='one',
                                name='Top 5 companies'), 1, 2)

    
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h4>Comments sentiment analysis</h4>', unsafe_allow_html=True)

            data_wcomm = pd.read_csv('ESG Models/Data/comments_sentiment.csv')
            data_esg_final = pd.read_csv('ESG Models/Data/posts_esg_25_10.csv')
            data_esg_final = data_esg_final.rename(columns={'urn':'post_urn'})

            final_df = data_esg_final.merge(data_wcomm, on='post_urn', how='left')
            final_df = final_df.drop_duplicates()
            final_df = final_df.sort_values('sentiment',ascending=False)

            data_x_top5 = final_df.loc[final_df['company_x'].isin(top_companies)].copy()

            data_x_top5, top_ESG_data_x_top5 = comments_analysis(data_x_top5)

            st.markdown(f'<h5>Distribution of comments for all posts </h5>', unsafe_allow_html=True)

            if data_x['sentiment'].median() > 0:
                color = "#00CC96"
            else:
                color = "#EF553B"

            if data_x_top5['sentiment'].median() > 0:
                color_top5 = "#00CC96"
            else:
                color_top5 = "#EF553B"

            fig = go.Figure()
            fig.add_trace(go.Box(x=data_x['sentiment'], name=option_name, marker_color = color, showlegend=False))
            fig.add_trace(go.Box(x=data_x_top5['sentiment'], name='Top 5', marker_color = color_top5, showlegend=False))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f'<h5>Distribution of comments for top 5 posts with the highest ESG total score</h5>', unsafe_allow_html=True)

            if top_ESG_data_x['sentiment'].median() > 0:
                color = "#00CC96"
            else:
                color = "#EF553B"

            if top_ESG_data_x_top5['sentiment'].median() > 0:
                color_top5 = "#00CC96"
            else:
                color_top5 = "#EF553B"

            fig = go.Figure()
            fig.add_trace(go.Box(x=top_ESG_data_x['sentiment'], name=option_name, marker_color = color, showlegend=False))
            fig.add_trace(go.Box(x=top_ESG_data_x_top5['sentiment'], name='Top 5', marker_color = color_top5, showlegend=False))
            st.plotly_chart(fig, use_container_width=True)

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

        fig = px.bar(data_frame=cats_df.sort_values(by='Category'), x='Category', y='Score', color='Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
        st.plotly_chart(fig, use_container_width=True)

        sub_main_match_df = pd.concat([pd.DataFrame({'Category': subcategories_env, 'Main Category': ['Environment']*len(subcategories_env)}), pd.DataFrame({'Category': subcategories_gov_pos_neg, 'Main Category': ['Governance']*len(subcategories_gov_pos_neg)}), pd.DataFrame({'Category': subcategories_soc, 'Main Category': ['Social']*len(subcategories_soc)})], ignore_index=True)
        subcats_df = subcats_df.merge(sub_main_match_df, on='Category', how='right').replace(np.nan, 0)

        st.markdown(f'<h5>ESG sub categories</h5>', unsafe_allow_html=True)
        fig = px.bar(data_frame=subcats_df.sort_values(by='Main Category'), x='Category', y='Score', color='Main Category', color_discrete_sequence=['#B6E886', '#FF6692', '#19D3F3'])
        st.plotly_chart(fig, use_container_width=True)

        if post_esg_sentiment > 100:
            post_esg_sentiment = 100
        elif post_esg_sentiment < -100:
            post_esg_sentiment = -100

        st.markdown('#')

        st.markdown(f'<h5>Sentiment analysis</h5>', unsafe_allow_html=True)

        layout = go.Layout(
        margin=go.layout.Margin(
                l=10, #left margin
                r=10, #right margin
                b=0, #bottom margin
                t=0, #top margin
            )
        )

        col1, col2 = st.columns(2)

        with col1:        

            if post_esg_sentiment > 0:
                color = "#00CC96"
            elif post_esg_sentiment == 0:
                color = "black"
            else:
                color = "#EF553B"

            fig = go.Indicator(mode = "gauge+number", value = post_esg_sentiment, gauge = {'bar': {'color': color}, 'axis': {'range': [-100, 100], 'visible': False}}, domain = {'x': [0, 1], 'y': [0, 1]}, title = {'text': "ESG Sentiment"})  
            fig = dict(data=[fig], layout=layout)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
    
            loaded_model = load_model('model_autokeras', custom_objects=ak.CUSTOM_OBJECTS)
            predicted_comments_sentiment = loaded_model.predict(tf.expand_dims(np.array([post_text]), -1))

            if predicted_comments_sentiment > 0:
                color = "#00CC96"
            elif predicted_comments_sentiment == 0:
                color = "black"
            else:
                color = "#EF553B"

            fig = go.Indicator(mode = "gauge+number", value = predicted_comments_sentiment.item(), gauge = {'bar': {'color': color}, 'axis': {'range': [-100, 100], 'visible': False}}, domain = {'x': [0, 1], 'y': [0, 1]}, title = {'text': "Predict Comments Sentiment"})   
            fig = dict(data=[fig], layout=layout)
            st.plotly_chart(fig, use_container_width=True)
   