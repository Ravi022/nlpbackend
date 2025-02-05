# -*- coding: utf-8 -*-
"""reddit_sentiment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z6JTZLw4PEKnezMUakq68eAYwJNeOLm3
"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile /content/drive/MyDrive/init_script.py
# 
# # Import the required packages and install if not already present
# import subprocess
# import sys
# 
# # List of required libraries
# required_libraries = [
# 
#     "vaderSentiment",
#     "praw",
#     "nltk",
#     "contractions",
#     "emoji",
#     "spacy"
# ]
# 
# # Install each library if it is not already installed
# for lib in required_libraries:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
# 
# # Download any additional resources
# subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
#

!python /content/drive/MyDrive/init_script.py

#import packages
import praw
from datetime import date, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from IPython.display import display

g_client_id="2apRvglqzYUqhoC7WTQJRw"
g_client_secret="gz9xZisCzD5Is5yUX8LgqVcsh7KmuQ"
g_user_agent="web scraper"
g_subreddit = "wallstreetbets"
g_num_posts=25

def init_reddit_app():
    reddit = praw.Reddit(
        client_id=g_client_id,
        client_secret=g_client_secret,
        user_agent=g_user_agent,check_for_async=False)
    return reddit

def get_posts(reddit, subreddit,time_span):
    posts = []
    top_posts = reddit.subreddit(subreddit).top(time_filter=time_span, limit=g_num_posts)

    for post in top_posts:
        posts.append(post.id)
    return posts

def get_comments(reddit, posts_id):
    df_comments = pd.DataFrame(columns=['post_id', 'comment_id', 'comment_text'])
    for _id in posts_id:
        submission = reddit.submission(id=_id)
        #print(submission.title, submission.num_comments)
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            try:
                df_comments.loc[len(df_comments.index)] = [comment.submission.id, comment.id, comment.body]
            except AttributeError:
                pass
    return df_comments

def get_threads(reddit,subreddit,time_span):
  df = []



  for post in reddit.subreddit(subreddit).top(time_filter=time_span, limit=g_num_posts):
      df.append([post.title, post.score, post.url, post.num_comments, post.selftext])

  df = pd.DataFrame(df,columns=['title', 'score', 'url', 'num_comments', 'body'])
  return df


def get_data(subreddit,time_span):
    reddit = init_reddit_app()
    postids = get_posts(reddit, subreddit, time_span)
    df = get_comments(reddit, postids)
#   display(df)
    return df

def show_threads(subreddit,timespan):
  reddit=init_reddit_app()
  df_threads=get_threads(reddit,subreddit,timespan)
  #df_threads.to_csv('threads.csv', index=False)
  df_json =df_threads.to_json(orient="records")
  return df_json

show_threads(g_subreddit,"day")



import re
import string
import nltk
import contractions
import emoji
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy



nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")



def expand_contractions(text):
    '''
    Expands contractions in text to full form.

    Example:
    >>> expand_contractions("I can't do this")
        "I cannot do this"
    '''
    return contractions.fix(text)

def replace_emoji(text):
    '''
    Replace Emoji in text with corresponding text description
    '''
    return emoji.demojize(text).replace("_", " ").replace(":", " ")

def lowercase_text(text):
    '''
    Convert text to lowercase.
    '''
    return text.lower()

def remove_punctuation(text):
    '''
    Remove punctuation from text.
    '''
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_numbers(text):
    '''
    Remove numbers from text.
    '''
    return re.sub(r'\d+', '', text)

def remove_special_characters(text):
    '''
    Remove special characters from text
    '''
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def remove_whitespace(text):
    '''
    Remove extra whitespaces from text
    '''
    return text.strip()

def remove_stopwords(text):
    '''
    Remove stopwords from text
    '''
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    return ' '.join([word for word in tokens if word not in stop_words])

"""
def get_wordnet_pos(word):
    '''Map POS tag to first character lemmatize() accepts'''
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_text(text):
    '''
    Lemmatize text considering the part-of-speech of each word.
    '''
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in tokens])
    return lemmatized_output
"""

def lemmatize_text_spacy(text):
    '''
    Lemmatize text using spaCy, considering the part-of-speech and context of each word.
    '''
    doc = nlp(text)
    lemmatized_output = ' '.join([token.lemma_ for token in doc])

    return lemmatized_output

def clean_text(text):
    '''
    Apply all cleaning functions to text
    '''
    #logger.info(f'expand_contractions: {text}')
    text = expand_contractions(text)
    #logger.info(f'replace_emoji: {text}')
    text = replace_emoji(text)
    #logger.info(f'lowercase_text: {text}')
    text = lowercase_text(text)
    #logger.info(f'remove_special_characters: {text}')
    text = remove_special_characters(text)
    #logger.info(f'remove_punctuation: {text}')
    text = remove_punctuation(text)
    #logger.info(f'remove_numbers: {text}')
    text = remove_numbers(text)
    #logger.info(f'remove_whitespace: {text}')
    text = remove_whitespace(text)
    #logger.info(f'remove_stopwords: {text}')
    text = remove_stopwords(text)
    #logger.info(f'lemmatize_text: {text}')
    lemmatized_output = lemmatize_text_spacy(text)
    #logger.info(f'Done, Returning lemmatized_output: {lemmatized_output}')
    return lemmatized_output

!cp /content/drive/MyDrive/nlp-reddit/preprocess.py  /content

import preprocess

def sentiment_analyser_score(df):
    analyser = SentimentIntensityAnalyzer()
    df_sentiment = pd.DataFrame(columns=["comment_id", "comp_score", "sentiment"])
    #   values = list(df.comment_text.values.flatten())
    values = list(df.comment_text.values)
    for row in values:
        row_nf= preprocess.clean_text(row)
        score = analyser.polarity_scores(row_nf)
        if score["compound"] > 0.5:
            sentiment = "positive"
        elif score["compound"] < -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        df_sentiment.loc[len(df_sentiment.index)] = [df.comment_id.loc[len(df_sentiment.index)], score["compound"], sentiment]
        #      Add sentiment to df
    combined_df = df_sentiment.join(df.set_index("comment_id"), on="comment_id")
    #display(combined_df)

    return combined_df

def score_data(df):
    """
    """
    _df = sentiment_analyser_score(df).sort_values(by='comp_score',ascending=False)
  #  display(_df['comment_text'].head(10))
    return _df

def get_scored_data(time):
    df = score_data(get_data(g_subreddit,time))
    return df

def display_comments(df):
    _df= sentiment_analyser_score(df).sort_values(by='comp_score',ascending=False)
    _df_json=_df.head(10).to_json(orient="records")
    return _df_json




#return _df

def getSentimentValues(df):
  scores=score_data(df)
  df_sen = scores["sentiment"].value_counts()
  df_sen_json=df_sen.to_json(orient="records")
  return df_sen_json

def make_chart(df,time):
    fig, ax = plt.subplots()
    df=df["sentiment"].value_counts().sort_index(axis=0).plot(kind='bar',color=['tab:red','tab:blue','tab:green'])
    plt.title("Sentiment in /r/" + g_subreddit + " comments from past " + time)
    ax.bar_label(ax.containers[0], label_type='edge')
    ax.set_ylabel('# of comments')
    plt.xticks(rotation=0)
    plt.show()

df_day = get_data(g_subreddit,"day")
getSentimentValues(df_day)

display_comments(df_day)