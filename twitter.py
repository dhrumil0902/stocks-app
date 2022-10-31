import tweepy
import configparser
import pandas as pd

# read configs
config = configparser.ConfigParser()
config.read('pass')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

##public_tweets = api.home_timeline()

##columns = ['Time', 'User', 'Tweet']
##data = []
##for tweet in public_tweets:
##    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

##df = pd.DataFrame(data, columns=columns)

##df.to_csv('tweets.csv')

##print(df)

keywords = 'happy'
limit=5

tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=100, tweet_mode='extended').items(limit)

# tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

# create DataFrame
columns = ['User', 'Tweet','URL']
data = []

for tweet in tweets:
    hyperlink = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
    data.append([tweet.user.screen_name.encode("utf-8"), tweet.full_text.encode("utf-8"),hyperlink ])

df1 = pd.DataFrame(data, columns=columns)

print(df1)







