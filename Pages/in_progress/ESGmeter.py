import streamlit as st
import pandas as pd
from streamlit_tags import st_tags
import plotly.graph_objects as go


@st.cache
def get_data():

    df = pd.DataFrame()

    return df

@st.cache
def call_models():

    df = pd.DataFrame()

    return df

@st.cache
def analytics():

    df = pd.DataFrame({'post': ['overall', '#1', '#2', '#3'], 'ESG': ['Environment', 'Social', 'Environment', 'Environment'], 'ESG sentiment score': [9.7, 7, 2, 20], 'Number of comments': [230, 40, 90, 100], 'Comments sentiment': [5.7, -5, 20, 2]})

    return df

st.title("ESG Glassdoor")
st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")

data = get_data()
data = call_models()
data = analytics()

tab1, tab2 = st.tabs(["Company Scoring", "New Post Scoring"])

with tab1:
    st.subheader("Company Scoring")

    keywords = st_tags(label='Company', maxtags=2, suggestions=['Tesla', 'Amazon', 'Google'], text='Press enter to add more')

with tab2:
    
    st.subheader("New Post Scoring")


    st.write("Write your post")
    post_text = st.text_area("Write your post", label_visibility='collapsed')

    submit = st.button('Submit')

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

