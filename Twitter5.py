import re
import tweepy
import csv
import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
   
    def __init__(self):
        
        # keys and tokens from the Twitter Dev Console

        consumer_key = 'VTY1Zq9d3ygUg5tiNx4XH00UO'
        consumer_secret = 'GLCr9rJIBoxIzqSzlgbOw0vi7TFgIUEq9971GkgOeTqM5SXWzP'
        access_token = '885997710691639296-O2UBW6rpSNaNu59zCuLGxoBrWyeZQKY'
        access_token_secret = 'MIDEiRvDWUrsX5LPjXynRtWk4PbxaOwNBauh652piuU9h'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def bag_of_word(self,documents):
        word_features_file=open("word_features.pickle","rb")
        word_features=pickle.load(word_features_file)
        word_features_file.close()
        return word_features

    def Training_classifier(self):
        classifier_file=open("naivebayes.pickle","rb")
        classifier=pickle.load(classifier_file)
        classifier_file.close();
        return classifier

    def find_features(self,document,word_features):
        words=set(document)
        features={}
        for w in word_features:
            features[w]= (w in words)
        return features


 
    def clean_tweet(self, tweet):
        stop_words=set(stopwords.words("english"))
        st=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.lower()).split())
        li=st.split()
        final_string=""
        for w in li:
            if w not in stop_words:
                final_string=final_string+' '+w;

        return final_string
 
    def get_tweet_sentiment(self, tweet,tw):

        tw.append(self.clean_tweet(tweet))

        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, totalcount):
        '''
        Main function to fetch tweets and parse them.
        '''
        
        filename = "tweet.csv"
        fields = ['Tweet', 'Pre Processed Tweet']



        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = []
            
            fetched_tweets = fetched_tweets + self.api.search(q = query, count = 100)

            oldest = fetched_tweets[-1].id;

            while True :
                fetched_tweets = fetched_tweets + self.api.search(q = query, count = 100,max_id =oldest)
                
                oldest = oldest = fetched_tweets[-1].id - 1

                totalcount=totalcount-100
                if totalcount < 0:
                    break


            
            final=[]
            # parsing tweets one by one

            for tweet in fetched_tweets:
                
                tw=[]
                tw.append(tweet.text);

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                #print (tweet.text)
                # saving text of tweet
                
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text,tw)
                parsed_tweet['text'] = tw[1]
                parsed_tweet['actual_text'] = tw[0]

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                if(tw not in final):
                    final.append(tw);


            with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(fields)
     
                # writing the data rows
                #print (final)
                cnt=0;
                for row in final:
                    try:
                        csvwriter.writerow(row)
                    except:
                        # print error (if any)
                        cnt=cnt+1
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            a=0;
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    documents = [(list(movie_reviews.words(fileid)), category)for category in movie_reviews.categories()for fileid in movie_reviews.fileids(category)]
    
    word_features=api.bag_of_word(documents)
    classifier=api.Training_classifier()
    
    # calling function to get tweets
    Movie=input("Enter Movie Name-")
    tweet_count=int(input("Number of tweets-")) 

    tweets = api.get_tweets(query = Movie, totalcount = tweet_count)
    # picking positive tweets from tweets
    a=0;b=0;
    for tweet in tweets:
        tweet['sentiment']=classifier.classify(api.find_features(tweet['text'],word_features))

    # print (api.find_features("It was Suprising incredible. I loved it",word_features))
    print (classifier.classify(api.find_features("It was Suprising incredible. I loved it",word_features)))
        

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == '1']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == '0']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['actual_text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['actual_text'])
 
if __name__ == "__main__":
    # calling main function
    main()