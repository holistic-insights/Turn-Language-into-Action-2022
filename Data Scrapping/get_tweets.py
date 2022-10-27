import pandas as pd
import tweepy
from datetime import datetime
from dateutil.relativedelta import relativedelta

def search_tweets(api, words, date_since, num_tweets):

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

def main():

    consumer_key = "e7n2TeJaCdWHLUYJgWzA32JWN"
    consumer_secret = "N9al7H21S8bScQFXWuQ3idJQaDxwIINssia2XVmQf7bmGtPjv4"
    access_key = "1350230087925424143-l5JyfE5XpzzrMpU131rGJYbf0mdkt4"
    access_secret = "7HhTGZVh4cGanMcQ0uZefbsAjadlFVexoGMZuXv4Cp7gQ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    comp = pd.read_csv('fortune1000_twitter_linkedin.csv')
    
    not_all_scrapped = True

    while not_all_scrapped:

        counter = 0

        try:
            done = pd.read_csv('fortune1000_scraped_tweets.csv')
            already_scrapped = done['target'].unique().tolist()
        except:
            done = None
            already_scrapped = []

        twitter_list = []

        for index, row in comp.iterrows():
            
            user = row['twitter']

            counter += 1

            if user in already_scrapped:
                print(f'{counter}/{len(comp)} - {user} - already scrapped')
                continue

            print(f'{counter}/{len(comp)} - {user}')

            currentTimeDate = datetime.now() - relativedelta(months=6)
            currentTime = currentTimeDate.strftime('%Y-%m--%d')

            try:
                by_user = search_tweets(api, f'from:{user}', currentTime, 250)
                about_user = search_tweets(api, f'{user.lower()}', currentTime, 250)
            except:
                print("# Scrapping broke ... retrying ...")
                break

            by_user['target'] = user
            by_user['tweeted_by_targer'] = True
            about_user['target'] = user
            about_user['tweeted_by_targer'] = False

            twitter_list.append(by_user)
            twitter_list.append(about_user)

        try:
            tweets_df = pd.concat(twitter_list, ignore_index=True)
            if done is not None:
                tweets_df = pd.concat([tweets_df, done], ignore_index=True)
            tweets_df.to_csv('fortune1000_scraped_tweets.csv', index=False)
        except:
            pass

        if counter == len(comp):
            not_all_scrapped = False

if __name__ == '__main__':
    main()