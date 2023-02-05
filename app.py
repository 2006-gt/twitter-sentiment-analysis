import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , request



def clean_tweet( tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment( tweet):

        # analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer())
        # if analysis.sentiment.classification == "pos":
        #     return 'positive'
        # elif analysis.sentiment.classification == "neg":
        #     return 'negative'

        analysis = TextBlob(clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

def get_tweets(api, query, count=5):

        count = int(count)
        tweets = []
        try:
            fetched_tweets = tweepy.Cursor(api.search_tweets, q=query, lang ='en', tweet_mode='extended').items(count)

            for tweet in fetched_tweets:

                parsed_tweet = {}

                if 'retweeted_status' in dir(tweet):
                    parsed_tweet['text'] = tweet.retweeted_status.full_text
                else:
                    parsed_tweet['text'] = tweet.full_text

                parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text'])

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepyException as e:
            print("Error : " + str(e))

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")


@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            # query=request.form['query']
            # if query == ' ' or query == '':
            #     return render_template('error.html')
            # count=request.form['num']
            # if count == ' ' or count == '':
            #     count = 5
            #     # return render_template('error.html')
            # fetched_tweets = get_tweets(api,query, count)
            # return render_template('result.html', result=fetched_tweets)
            try:
                query=request.form['query']
                count=request.form['num']
                fetched_tweets = get_tweets(api,query, count)
                return render_template('result.html', result=fetched_tweets)
            except:
                return render_template('error.html')

@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
           text = request.form['txt']

           blob = TextBlob(text)
           if blob.sentiment.polarity > 0:
               text_sentiment = "positive"
           elif blob.sentiment.polarity == 0:
               text_sentiment = "neutral"
           else:
               text_sentiment = "negative"
           return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':

    consumer_key = 'g1hWSfPYf9IeSvYmYT7AgSpMW'
    consumer_secret = 'XR3foE5dyQwViEBs8G324hcyfuIarnX1uj9ZZsUrK7uGVZOT5Y'
    access_token = '1601925959447289856-7ngeCmzYdTpduNsiP7jEzFjNt3QgjD'
    access_token_secret = 'rZqMWOgF2EWOofLjjhDYcAgfawU5FqL9ObhgQ5CrWPa1f'

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    app.debug=True
    app.run(host='localhost')


