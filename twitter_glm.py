import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from joblib import dump

data = pd.read_csv('data/twitter_sentiments.csv')
data.head()

train, test = train_test_split(data, test_size=0.2, stratify=data['label'], random_state=21)

#train.shape, test.shape

# create a TF-IDF vectorizer object
tfidf_vectorizer = TfidfVectorizer(lowercase= True, max_features=1000, stop_words=ENGLISH_STOP_WORDS)

# fit the object with the training data tweets
tfidf_vectorizer.fit(train.tweet)

# transform the train and test data
train_idf = tfidf_vectorizer.transform(train.tweet)
test_idf  = tfidf_vectorizer.transform(test.tweet)

model_LR = LogisticRegression()

# fit the model with the training data
model_LR.fit(train_idf, train.label)

# predict the label on the traning data
predict_train = model_LR.predict(train_idf)

# predict the model on the test data
predict_test = model_LR.predict(test_idf)

# f1 score on train data
f1_score(y_true= train.label, y_pred= predict_train)
## >> 0.4888178913738019

f1_score(y_true= test.label, y_pred= predict_test)
## >> 0.45751633986928114

pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(lowercase=True,
                                                      max_features=1000,
                                                      stop_words= ENGLISH_STOP_WORDS)),
                            ('model', LogisticRegression())])

# fit the pipeline model with the training data
pipeline.fit(train.tweet, train.label)

text = ["Virat Kohli, AB de Villiers set to auction their 'Green Day' kits from 2016 IPL match to raise funds"]

# predict the label using the pipeline
pipeline.predict(text)
## >> array([0])

dump(pipeline, filename="text_classification.joblib")