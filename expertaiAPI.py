import os
import streamlit as st
from expertai.nlapi.cloud.client import ExpertAiClient


class ExpertAPI(object):

    def __init__(self):
        super().__init__()
        os.environ['EAI_USERNAME'] = st.secrets['EAI_USERNAME']
        os.environ['EAI_PASSWORD'] = st.secrets['EAI_PASSWORD']

        # Instantiate client to use the Natural Language API
        self.client = ExpertAiClient()

        self.language = 'en'
        self.detector = 'esg-sentiment'

    def esg_detection(self, posts):

        posts.reset_index(drop=True, inplace=True)

        for i, text in enumerate(posts.text):

            try:
                output = self.client.detection(
                    body={'document': {'text': text}},
                    params={'detector': self.detector, 'language': self.language}
                )

                for category in output.categories:
                    posts.loc[i, category.label] = category.score

            except:
                print('ESG Detection Failed')
                continue

        return posts

    def sentiment_analysis(self, comments):

        comments.reset_index(drop=True, inplace=True)

        for i, text in enumerate(comments.text):

            try:
                output = self.client.specific_resource_analysis(
                    body={'document': {'text': text}},
                    params={'resource': 'sentiment', 'language': self.language}
                )
                # overall sentiment ranges from -100 (extremely negative) to 100 (extremely positive)
                comments.loc[i, 'sentiment'] = output.sentiment.overall
                
            except:
                print('Sentiment Analysis Failed')
                continue

        return comments
