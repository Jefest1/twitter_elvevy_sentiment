import tweepy
import pandas as pd
import config  # import the config file

# Replace these with your actual keys and tokens
api_key = config.api_key
api_key_secret = config.api_key_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Define a function to get tweets


def get_elevy_tweets():
    query = "e-levy"
    max_tweets = 10
    tweets = []

    for tweet in tweepy.Cursor(api.search, q=query, lang="en", tweet_mode="extended").items(max_tweets):
        tweet_details = {
            "username": tweet.user.screen_name,
            "created_at": tweet.created_at.strftime('%d-%m-%Y'),
            "content": tweet.full_text,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count
        }
        tweets.append(tweet_details)

    return tweets


# Fetch tweets and print them
elevy_tweets = get_elevy_tweets()


df = pd.DataFrame(elevy_tweets, columns=elevy_tweets.index)
