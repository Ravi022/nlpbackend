import json
import praw
from datetime import date, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import contractions
import emoji
import spacy
import re
import string
g_client_id="2apRvglqzYUqhoC7WTQJRw"
g_client_secret="gz9xZisCzD5Is5yUX8LgqVcsh7KmuQ"
g_user_agent="web scraper"
g_subreddit = "wallstreetbets"
g_num_posts=25
# Download necessary NLTK and spaCy resources
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")

# Initialize Reddit app (unchanged)
def init_reddit_app():
    reddit = praw.Reddit(
        client_id=g_client_id,
        client_secret=g_client_secret,
        user_agent=g_user_agent,
        check_for_async=False
    )
    return reddit

# Get threads and save as JSON file
def show_threads(subreddit, timespan):
    reddit = init_reddit_app()
    df_threads = get_threads(reddit, subreddit, timespan)
    df_threads_json = df_threads.to_json(orient="records")
    with open(f"{subreddit}_threads_{timespan}.json", "w") as file:
        json.dump(json.loads(df_threads_json), file, indent=4)
    print(f"Saved threads data to {subreddit}_threads_{timespan}.json")

def get_comments(reddit, posts_id):
    df_comments = pd.DataFrame(columns=['post_id', 'comment_id', 'comment_text'])
    for _id in posts_id:
        submission = reddit.submission(id=_id)
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            try:
                df_comments.loc[len(df_comments.index)] = [comment.submission.id, comment.id, comment.body]
            except AttributeError:
                pass
    return df_comments

# Get comments and save as JSON file
def get_data(subreddit, time_span):
    reddit = init_reddit_app()
    postids = get_posts(reddit, subreddit, time_span)
    df_comments = get_comments(reddit, postids)
    df_comments_json = df_comments.to_json(orient="records")
    with open(f"{subreddit}_comments_{time_span}.json", "w") as file:
        json.dump(json.loads(df_comments_json), file, indent=4)
    print(f"Saved comments data to {subreddit}_comments_{time_span}.json")
    return df_comments

# Sentiment analysis and saving as JSON
def display_comments(df):
    df_sentiment = sentiment_analyser_score(df)
    df_sentiment_json = df_sentiment.head(10).to_json(orient="records")
    with open("sentiment_analysis_top_comments.json", "w") as file:
        json.dump(json.loads(df_sentiment_json), file, indent=4)
    print("Saved sentiment analysis data to sentiment_analysis_top_comments.json")

# Get and save sentiment value counts as JSON
def getSentimentValues(df):
    scores = score_data(df)
    df_sen = scores["sentiment"].value_counts()
    df_sen_json = df_sen.to_json(orient="records")
    with open("sentiment_value_counts.json", "w") as file:
        json.dump(json.loads(df_sen_json), file, indent=4)
    print("Saved sentiment value counts to sentiment_value_counts.json")
    return df_sen_json

# Example calls to save output data
df_day = get_data(g_subreddit, "day")          # Save comments
show_threads(g_subreddit, "day")               # Save threads
getSentimentValues(df_day)                     # Save sentiment value counts
display_comments(df_day)                       # Save top comments' sentiment analysis
# pip install praw vaderSentiment nltk contractions emoji spacy pandas matplotlib
