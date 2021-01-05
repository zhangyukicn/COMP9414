import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('dataset.tsv', sep='\t', header=None, quoting=csv.QUOTE_NONE)
'''
topic_id = np.array(data[2])
sentiment = np.array(data[3])


# plot the distribution of topic_id
topic_id_dict = {}
for i in topic_id:
    if i not in topic_id_dict:
        topic_id_dict[i] = 1
    else:
        topic_id_dict[i] += 1

topic_classes = sorted(topic_id_dict.keys())
topic_classes_number = []
for c in topic_classes:
    topic_classes_number.append(topic_id_dict[c])
print(topic_classes)
print(topic_classes_number)
x = np.arange(len(topic_classes))

plt.xlabel('topic_id')
plt.ylabel('number')
plt.title('The occurrence of number of every topic_id')
plt.bar(x, topic_classes_number)
plt.xticks(x, topic_classes, size='xx-small')
for a, b in zip(x, topic_classes_number):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('topic_id.png')
plt.show()
'''

# plot the distribution of sentiment
sentiment_dict = {}
sentiment = np.array(data[2])
for i in sentiment:
    if i not in sentiment_dict:
        sentiment_dict[i] = 1
    else:
        sentiment_dict[i] += 1

sentiment_classes = sorted(sentiment_dict.keys())
sentiment_classes_number = []
for c in sentiment_classes:
    sentiment_classes_number.append(sentiment_dict[c])
print(sentiment_classes)
print(sentiment_classes_number)
x = np.arange(len(sentiment_classes))

plt.xlabel('3 types sentiments')
plt.ylabel('number')
plt.title('The occurrence of number of 3 types sentiment')
plt.bar(x, sentiment_classes_number)
plt.xticks(x, sentiment_classes, size='large')
for a, b in zip(x, sentiment_classes_number):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('sentiment.png')
plt.show()
