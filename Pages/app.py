import streamlit as st
import pandas as pd
from streamlit_tags import st_tags

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

st.write("LinkedIn user")
user = st.text_input("LinkedIn user", label_visibility='collapsed')
keywords = st_tags(label='Keywords', text='Press enter to add more')

submit = st.button('Submit')
if submit:

    st.markdown(f'<h1 style="color:#ff4b4b">{user}</h1>', unsafe_allow_html=True)

    data = get_data()
    data = call_models()
    data = analytics()

    tab1, tab2, tab3, tab4 = st.tabs(["Overall", "Post #1", "Post #2", "Post #3"])

    with tab1:
        st.subheader("Overall")
        st.write(data.loc[data['post'] == 'overall'])

    with tab2:
        st.subheader("Post #1")
        st.write(data.loc[data['post'] == '#1'])

    with tab3:
        st.subheader("Post #2")
        st.write(data.loc[data['post'] == '#2'])

    with tab4:
        st.subheader("Post #3")
        st.write(data.loc[data['post'] == '#3'])