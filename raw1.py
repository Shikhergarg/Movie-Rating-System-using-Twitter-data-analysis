import re
import tweepy
import csv
import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tweepy import OAuthHandler
from textblob import TextBlob
 
def document_features(document,word_features):
    document_words = set(document) 
    features = {}
    for word in word_features:
        features[word] = (word in document_words)
    return features

def clean_tweet( tweet):
        stop_words=set(stopwords.words("english"))
        st=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        li=st.split()
        final_string=""
        for w in li:
            if w not in stop_words:
                final_string=final_string+' '+w;

        return final_string
 
def main():
    # creating object of TwitterClient Class
    documents=[]
    with open('classifier.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        words=[]
        for row in reader:
            token=word_tokenize(clean_tweet(row['Tweet']))
            documents.append([token,row['Label']])
            words.append(token)
    all_words=[]

    for w in words:
        for wo in w:
            all_words.append(wo)

    all_words = nltk.FreqDist(all_words)

    print(all_words.most_common(20))
    word_features=[]
    for (d,c) in all_words.most_common(1300):
        word_features.append(d)
    # word_features = list(all_words.keys())[:1300]
    # print(word_features)
    # # word_features=list(all_words.keys())[79000:]
    print (len(word_features))
    del all_words
    doc=documents[95000:105000]
    doc.extend(documents[:20000])
    doc.extend(documents[180000:])
    del documents
    documents=doc
    del doc
    # print(clean_tweet(link ...,,,,))
    featuresets = [(document_features(d,word_features), c) for (d,c) in documents]
    
    print (documents[0])
    test_set =featuresets[:10000]
    classifier = nltk.NaiveBayesClassifier.train(featuresets[10000:])
    print("Accuracy",(nltk.classify.accuracy(classifier,test_set))*100)
    classifier.show_most_informative_features(100)
    print (classifier.classify(document_features("movie was great ",word_features)))

    save_classifier=open("naivebayes.pickle","wb")
    pickle.dump(classifier,save_classifier)
    save_classifier.close()
    
    save_word_features=open("word_features.pickle","wb")
    pickle.dump(word_features,save_word_features)
    save_word_features.close()
 
if __name__ == "__main__":
    # calling main function
    main()