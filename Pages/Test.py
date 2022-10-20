import streamlit as st
import pandas as pd
import pandas as pd
import tweepy
import numpy as np

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

@st.cache
def search_tweets(user, date_since, num_tweets):

    consumer_key = "e7n2TeJaCdWHLUYJgWzA32JWN"
    consumer_secret = "N9al7H21S8bScQFXWuQ3idJQaDxwIINssia2XVmQf7bmGtPjv4"
    access_key = "1350230087925424143-l5JyfE5XpzzrMpU131rGJYbf0mdkt4"
    access_secret = "7HhTGZVh4cGanMcQ0uZefbsAjadlFVexoGMZuXv4Cp7gQ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    words = f'{user.lower()}'

    df = pd.DataFrame(columns=['username', 'date', 'retweet_count', 'text'])

    tweets = tweepy.Cursor(api.search_tweets, words, lang="en", since_id=date_since, tweet_mode='extended').items(num_tweets)

    list_tweets = [tweet for tweet in tweets]

    for tweet in list_tweets:
        
        username = tweet.user.screen_name
        retweetcount = tweet.retweet_count
        date = tweet.created_at
        hashtags = tweet.entities['hashtags']

        try:
                text = tweet.retweeted_status.full_text
        except AttributeError:
                text = tweet.full_text
                
        ith_tweet = [username, date, retweetcount, text]
        df.loc[len(df)] = ith_tweet

    return df

st.title("ESG Glassdoor")

st.write("Raising transparency on companies' attitude towards ESG and compare their position with public perception.")

col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Company name", value="Tesla")
with col2:
    twitter_user = st.text_input("Company Twitter username", value="Tesla")
with col3:
    linkedin_user = st.text_input("Company LinkedIn username", value="Tesla")

col1, col2, col3 = st.columns(3)
with col1:
    since_date = st.text_input("Get posts since", value="YYYY-MM-DD")
with col2:
    twitter_count = st.slider( "Number of Twitter posts", min_value=100, max_value=1000, step=10, value=0)
with col3:
    linkedin_count = st.slider("Number of LinkedIn posts", min_value=100, max_value=1000, step=10, value=0)

since_date = since_date[:7] + '--' + since_date[8:]

show_raw = st.checkbox('Show raw data')

submit = st.button('Submit')
if submit:

    data = search_tweets(twitter_user, since_date, twitter_count)

    if show_raw:
        st.subheader('Raw data')
        st.write(data)

    data['date'] = pd.to_datetime(data['date'])
    data = data.rename(columns={'date': 'datetime'})
    data['date'] = data['datetime'].apply(lambda x: x.date())
    data['date'] = data['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))

    data_gb = data.groupby('date').count().reset_index()
    data_gb = data_gb.drop(columns=['username', 'datetime', 'retweet_count']).rename(columns={'text': 'num_tweets'})
    data_gb['date'] = pd.to_datetime(data_gb['date'])
    data_gb.head()

    st.subheader('Number of tweets per minute')
    st.line_chart(data=data_gb, x='date', y='num_tweets', width=0, height=0, use_container_width=True)
    
    # hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    # st.bar_chart(hist_values)

    # # Some number in the range 0-23
    # hour_to_filter = st.slider('hour', 0, 23, 17)
    # filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    # st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    # st.map(filtered_data)