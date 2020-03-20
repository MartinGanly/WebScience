from database import mongoController
import matplotlib.pyplot as pyplot
from pandas import DataFrame
from sklearn.cluster import KMeans
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk as nltk
from nltk.stem.snowball import SnowballStemmer

class kmeans():

    def __init__(self):
        self.y_max_value = 4000
        self.n_clusters = 20

    # Gets all tweets and pre-processes each, then runs TF-IDF on each tweet in the corpus of all tweets
    # Then assigns a group to each tweet and inserts the group into the database for later reference
    def kmeans(self):
        print("PROCESSING GROUPS")
        database = mongoController.mongoController()
        # get all tweets
        documents, ids = self.process()

        # turn tweets into TD-IDF representation
        vectorizer = TfidfVectorizer(stop_words=nltk.corpus.stopwords.words('english'))
        X = vectorizer.fit_transform(documents)

        model = KMeans(n_clusters=self.n_clusters, init='k-means++', max_iter=10000, n_init=1)
        model.fit(X)

        print("Top terms per cluster:")
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()

        # Assign groups to each tweet and insert into database
        for i in range(len(documents)):
            print("Processing Kmeans for tweet " + str(i) + "/" + str(len(documents)))
            Y = vectorizer.transform([documents[i]])
            prediction = model.predict(Y)
            database.tweets.insert_group_to_tweet(ids[i], prediction[0])

    # Get all tweets and pre-process them by tokenizing and stemming
    # Removes all words less than 3 characters long and remove urls.
    def process(self):
        database = mongoController.mongoController()
        tweets = database.tweets.get_all_tweets()
        documents = []
        ids = []
        for tweet in tweets:
            for ind_tweet in tweet['tweets']:
                new_string = ' '.join([w for w in ind_tweet['text'].split() if len(w)>3])
                new_string = re.sub(r'http\S+', '', new_string)
                documents.append(new_string)
                ids.append(ind_tweet['idd'])
        return documents, ids

    # Default tokenize and stem SKLearn function
    def tokenize_and_stem(self, text):
        stemmer = SnowballStemmer("english")
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    # Default tokenize SKLearn function
    def tokenize(self, text):
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens
