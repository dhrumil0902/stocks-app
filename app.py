import streamlit as st
import yfinance as yf
import pandas as pd
import time
import ticker_list
import datetime as dt
import tweepy
import configparser
import pandas as pd
import requests
import praw
import re
import matplotlib.pyplot as plt
from datetime import date
from PIL import Image
import streamlit.components.v1 as components
import json

#setting up headers and page layout
st.set_page_config(layout = "wide")
tab1, tab2, tab3 = st.tabs(["Stock", "Risk Calculaor",'News'])

#tab1 has general info
with tab1:
    print(len(ticker_list.ticker_ls))
    sorted(ticker_list.ticker_ls)

    fiftyhigh = []
    fifitylow = []
    curr_price = []
    sector = []
    country = []

    ticker_info =yf.Ticker(ticker_list.ticker_ls[0])

    now = dt.datetime.now().strftime('%y')
    
    list1 = ['h','y','r']

    with st.container():
         coll1, coll2, coll3, coll4, coll5 = st.columns(5)
         with coll3:
            result = st.selectbox("Select Stock",ticker_list.ticker_ls)
    
    st.markdown(
    """
    <style>
    [data-testid="select team"][aria-expanded="true"] > div:first-child {
        width: 500px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    with st.container():
        col1, col1c,col1b,col1d, col2,col3,col4 = st.columns([1.5,1,1,1,5,0.5,.5], gap="small")


        if(yf.Ticker(result).info['regularMarketPrice'] != None):
            price =  (yf.Ticker(result).info['currentPrice']  - yf.Ticker(result).info['fiftyTwoWeekHigh'])  / yf.Ticker(result).info['fiftyTwoWeekHigh'] * 100
            price1 =  (yf.Ticker(result).info['currentPrice']  - yf.Ticker(result).info['fiftyTwoWeekLow'])  / yf.Ticker(result).info['fiftyTwoWeekLow'] * 100
            round(price,1)
            round(price1,1)
            col1c.metric("Current Price:",  round(yf.Ticker(result).info['currentPrice'],2)," ")
            col1b.metric("52 Week High", yf.Ticker(result).info['fiftyTwoWeekHigh'], str(round(price,1)) + "%"  )
            col1d.metric('52 Week Low: ',yf.Ticker(result).info['fiftyTwoWeekLow'], str(round(price1,1)) + "%" )
            col1c.metric('Target Price: ',round(yf.Ticker(result).info['targetMedianPrice'],2))
            col1b.metric('Dividend Rate: ',round(yf.Ticker(result).info['dividendRate'],3))
            ##col1d.metric('Revenue Growth: ',(round(yf.Ticker(result).info['revenueGrowth']*100),2))
            
        with col1:
            st.write("Additional Information")
            if(yf.Ticker(result).info['regularMarketPrice'] != None):

                ##print(yf.Ticker(result).info['sector'])
                st.write('Sector: ', yf.Ticker(result).info['sector'])
            
           
            
        with col2:
            st.write('Opening Prices graph')
            today = date.today()
            today_formatted = today.strftime("%Y-%m-%d")


            data = yf.download(result,'2016-01-01', today_formatted)
            print(data)
            print(data.columns)
            #data['Adj Close'].plot()

            #frame = pd.DataFrame(data['Open'], columns = data['Adj Close'])
            st.line_chart( data['Adj Close'])
         
 
       

    tab1a,tab1b,tab1c = st.tabs(["Twitter","Reddit","Yahoo Finance"])

    
    with tab1a:
        "Twitter"
        
        config = configparser.ConfigParser()
        config.read('pass')

        api_key = config['twitter']['api_key']
        api_key_secret = config['twitter']['api_key_secret']

        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']


        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        
        
        keywords = "$" + result
        #display 5 results at max
        limit=5

        tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=100, tweet_mode='extended').items(limit)

  
        columns = ['User', 'Tweet','URL']
        data = []
        
        for tweet in tweets:
            hyperlink = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            link = "https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            data.append([tweet.user.screen_name, tweet.full_text, hyperlink ])

           
            

        df1 = pd.DataFrame(data, columns=columns)

        

        st.dataframe(df1)  # Same as st.write(df)
    
    with tab1b:
        "Reddit"
        client_id = '9mxvBGQC4eEXhU_MskU7BA'
        secret_key = 'GE0cQIbh15OqTvE4xuCy174PRGaq1A'

        auth = requests.auth.HTTPBasicAuth(client_id,secret_key)
        data = {
            'grant_type': 'password',
            'username': 'tester_09',
            'password': 'testing1234'
        }

        headers = {'User Agent': 'MyAPI/0.0.1'}

        reddit = praw.Reddit(client_id='9mxvBGQC4eEXhU_MskU7BA', client_secret='GE0cQIbh15OqTvE4xuCy174PRGaq1A', user_agent='finance')

        posts = []
        ml_subreddit = reddit.subreddit(result)
        for post in ml_subreddit.hot(limit=5):
            #hyperlink = f'<a href="{post.url}">{post.title}</a>'
            hyperlink = 'hello'
            posts.append([ post.url,post.title, post.score, post.id, post.num_comments, post.selftext, post.created])

        posts = pd.DataFrame(posts,columns=['url','title', 'score', 'id', 'num_comments', 'body', 'created'])

        st.dataframe(posts)



        print(posts)


        
with tab2:

    now = dt.datetime.now().strftime('%y')
    
    list1 = ['h','y','r']
    result_duplicate = st.selectbox("risk calculater",ticker_list.ticker_ls)
    lst = [10,100,1000,10000,10000]
    price = st.selectbox('How much u wanna invest bro?',lst)
    st.write("you can buy these many shares with the alloted investment")
    st.write(price / (yf.Ticker(result_duplicate).info['currentPrice']))
    







    

