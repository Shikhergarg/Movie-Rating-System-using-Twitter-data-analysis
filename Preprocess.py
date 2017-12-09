import re
import tweepy
import csv
import nltk
import random
import pandas as pd
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from tweepy import OAuthHandler
from textblob import TextBlob
 
def clean_tweet(tweet):
    stop_words=set(stopwords.words("english"))
    st=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.lower()).split())
    li=st.split()
    final_string=""
    for w in li:
        if w not in stop_words:
            final_string=final_string+' '+w;

    return final_string
#Defining the path of the file
path = 'classified_tweets.txt'


#Reading the data from the file in the Dataframe Tweets
Tweets = pd.read_fwf(path,colspecs=[[0,1], [1,10000]],names=['Label', 'tweet'])
                

Tweets.Label = Tweets.Label.map({4:1,0:0})

filename = "classifier.csv"
fields = ['Label', 'Tweet']
X = Tweets.tweet
Y = Tweets.Label
print (X)

with open(filename, 'w') as csvfile:
     # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    for x in range(0, 200000):
        tweet=X[x]
        tweet=clean_tweet(tweet)
       	d=[Y[x],tweet]
        csvwriter.writerow(d)

print(X[0])

        

 
