from scrape_linkedin_posts import *

def get_LinkedIn_comments(posts_file, comments_nr):
    
    posts_data = pd.read_csv(posts_file, encoding="utf-8").iloc[811+1615+1095+555:]

    for post_urn, company in tqdm(zip(posts_data.urn, posts_data.company), total=len(posts_data)):

        # Get Comments
        try:
            comments = api.get_post_comments(str(post_urn), comment_count=comments_nr)
            n_comments = len(comments)
        except:
            n_comments = 0
            pass

        for j in range(n_comments):

            # urn
            comment_urn = comments[j]['urn'].split(',')[-1][:-1]

            # Timestamp
            ts = convert_ts(comment_urn)
            
            # Author
            try:
                author = comments[j]['commenter']['com.linkedin.voyager.feed.MemberActor']['urn'].split(':')[-1]
            except:
                author = " "
                pass

            # numLikes
            numLikes = comments[j]['socialDetail']['likes']['paging']['total']

            try:
                lang = comments[j]['originalLanguage']
                
            except:
                lang = "Other"
                pass

            try:
                text = comments[j]['commentV2']['text']
            except:
                text = " "
                pass
                
            new_row = pd.DataFrame({'comment_urn':[comment_urn],
                                                'post_urn': [post_urn],
                                                'ts': [ts],
                                                'company': [company],
                                                'author': [author],
                                                'numLikes': [numLikes],
                                                'lang': [lang],
                                                'text': [text]})

            new_row.to_csv('data/comments.csv', mode='a', header=False, encoding='utf-8')


LINKEDIN_USERNAME = getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = getenv("LINKEDIN_PASSWORD")

api = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)

comments_nr = 100
posts_file = "data/posts2_clean.csv"

get_LinkedIn_comments(posts_file, comments_nr)