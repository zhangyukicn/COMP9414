import sys
import pandas
import numpy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report


data_file_training = sys.argv[1]
data_file_test = sys.argv[2]


df_data_file_training = pandas.read_csv(data_file_training, sep = '\t', header=None, names=['number','text','attitude'])
#print(df_data_file_training)
df_data_file_test = pandas.read_csv(data_file_test, sep = '\t', header=None, names=['number','text','attitude'])
#print(df_data_file_test)

sentence_to_train = numpy.array(df_data_file_training['text'])
sentence_to_test= numpy.array(df_data_file_test['text'])
test_id = numpy.array(df_data_file_test['number'])
train_attitude = numpy.array(df_data_file_training['attitude'])
test_attitude = numpy.array(df_data_file_test['attitude'])

#print(sentence_to_train)



#url_link = re.compile(r'^(http[s]?|ftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+(\.[a-zA-Z0-9-]+)+(/[\w-]+)*/[\w-]+\.(gif|png|jpg)$')
url_link = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
word_pattern = re.compile(r'[^#@_$%\sa-zA-Z\d]')


satisfy_sentence =[]
satisfy_word= []
#satisfy_word = None
satisfy_test_sentence =[]
#satisfy_test_word = None
satisfy_test_word = []



#training
for modify_url in sentence_to_train:
    match = url_link.search(modify_url)
    if match:
        c_modify_url = re.sub(url_link,' ',modify_url)
        satisfy_sentence.append(c_modify_url)
    else:
        satisfy_sentence.append(modify_url)
satisfy_sentence_ =numpy.array(satisfy_sentence)
#print(satisfy_sentence_)

for modify_word in satisfy_sentence_:
    match = word_pattern.search(modify_word)
    if match:
        modify_word = re.sub(word_pattern,'',modify_word)
        satisfy_word.append(modify_word)
    else:
        satisfy_word.append(modify_word)
satisfy_word = numpy.array(satisfy_word)


##test
for modify_url in sentence_to_test:
    match = url_link.search(modify_url)
    if match:
        modify_url = re.sub(url_link,' ',modify_url)
        satisfy_test_sentence.append(modify_url)
    else:
        satisfy_test_sentence.append(modify_url)
satisfy_test_sentence =numpy.array(satisfy_test_sentence)
#print(len(satisfy_test_word))
for modify_word in satisfy_test_sentence:
    match = word_pattern.search(modify_word)
    if match:
        modify_word = re.sub(word_pattern,'',modify_word)
        satisfy_test_word.append(modify_word)
    else:
        satisfy_test_word.append(modify_word)
satisfy_test_word = numpy.array(satisfy_test_word)
#print(satisfy_word)
#(len(satisfy_test_word))
# for sen in satisfy_test_word:
#     print(sen)


#training
#count = CountVectorizer(lowercase=False, token_pattern='[#@_$%\w\d]{2,}',max_features=1000)
count = CountVectorizer(lowercase=False,token_pattern='[#@_$%\w\d]{2,}')
X_train_bag_of_words = count.fit_transform(satisfy_word)
#print(satisfy_word)
#print(count.vocabulary_)
#print(X_train_bag_of_words)

#test
X_test_bag_of_words = count.transform(satisfy_test_word)

#modle function
def predict_and_test(model, X_test_bag_of_words):
    predicted_y = model.predict(X_test_bag_of_words)
    #print(classification_report(test_attitude, predicted_y,zero_division=0))
    for i in range(0,len(sentence_to_test)):
        print(test_id[i], predicted_y[i])


clf = MultinomialNB()
model = clf.fit(X_train_bag_of_words, train_attitude)
predict_and_test(model, X_test_bag_of_words)
