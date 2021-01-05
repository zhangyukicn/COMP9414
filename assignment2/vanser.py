import pandas as pd
import csv
import numpy
import re
from sklearn.feature_extraction.text import CountVectorizer
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

data_file_training = sys.argv[1]
data_file_test = sys.argv[2]

df_data_file_training = pd.read_csv(data_file_training, sep = '\t', header=None, names=['number','text','attitude'])
df_data_file_test = pd.read_csv(data_file_test, sep = '\t', header=None, names=['number','text','attitude'])

sentence_to_train = numpy.array(df_data_file_training['text'])
sentence_to_test= numpy.array(df_data_file_test['text'])
test_id = numpy.array(df_data_file_test['number'])
train_attitude = numpy.array(df_data_file_training['attitude'])
test_attitude = numpy.array(df_data_file_test['attitude'])

predict_y=[]
analyser = SentimentIntensityAnalyzer()
for text in sentence_to_test:
    score = analyser.polarity_scores(text)
    if score['compound'] >= 0.05:
        predict_y.append('positive')
    elif score['compound'] <= -0.05:
        predict_y.append('negative')
    else:
        predict_y.append('neutral')

print(classification_report(test_attitude, predict_y))
