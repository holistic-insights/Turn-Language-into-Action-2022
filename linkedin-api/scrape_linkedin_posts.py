from linkedin_api import Linkedin
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from os import getenv
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")


# trick to convert urn code into timestamp
def convert_ts(urn):
    unix_ts = int(str(int(bin(int(urn))[2:43], 2))[:-3])
    
    return datetime.utcfromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M:%S')

# receive json with scrapped data, transform relevant post information into dataframe
def get_LinkedIn_posts(posts):
    
    cols = ['urn', 'ts', 'company', 'numLikes', 'numComments', 'text']

    posts_data = pd.DataFrame(data=[], columns=cols)

    for i in range(len(posts)):
        # urn
        urn = posts[i]['urn'].split(':')[-1]

        # Timestamp
        ts = convert_ts(urn)
                  
        # Company
        try:
            company = posts[i]['value']['com.linkedin.voyager.feed.render.UpdateV2']['actor']['name']['attributes'][0]['miniCompany']['universalName']
        except:
            company = ""
            pass

        # numLikes
        numLikes = posts[i]['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['numLikes']

        # numComments
        numComments = posts[i]['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['numComments']

        # Text
        try:
            text = posts[i]['value']['com.linkedin.voyager.feed.render.UpdateV2']['commentary']['text']['text']
        except:
            text = ""
            pass
        
        new_row = {'urn': str(urn),
                   'ts': ts,
                   'company': company,
                   'numLikes': numLikes,
                   'numComments': numComments,
                   'text': text}

        posts_data = posts_data.append(new_row, ignore_index=True)

    posts_data.set_index('urn', inplace=True)
    
    return posts_data


if __name__ == "__main__":

    # Load env
    load_dotenv()

    LINKEDIN_USERNAME = getenv("LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD = getenv("LINKEDIN_PASSWORD")

    api = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)

    posts_nr = 100

    linkedin_accounts = pd.read_csv("data/fortune1000_twitter_linkedin.csv")[['linkedin']]

    # look for posts from each company in the list
    for company in tqdm(linkedin_accounts.values):
        C = company[0]
        posts = api.get_company_updates(public_id=C, max_results=posts_nr)
        posts_data = get_LinkedIn_posts(posts)
        posts_data.to_csv('data/posts.csv', mode='a', header=False, encoding='utf-8')