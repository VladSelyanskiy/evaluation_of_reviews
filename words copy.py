import nltk
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix


reviews = pd.read_table("reviews.txt", header=None, encoding="utf-8")
reviews.head()
reviews.info()
reviews[0].value_counts()


enc = LabelEncoder()
label = enc.fit_transform(reviews[0])

text = reviews[1]

processed = text.str.lower()

nltk.download("stopwords")
stop_words = set(stopwords.words("russian"))

processed = processed.apply(
    lambda x: " ".join(term for term in x.split() if term not in stop_words)
)
ps = nltk.PorterStemmer()
processed = processed.apply(lambda x: " ".join(ps.stem(term) for term in x.split()))


nltk.download("punkt_tab")
all_words = []

for message in processed:
    words = word_tokenize(message)
    for w in words:
        all_words.append(w)

all_words = nltk.FreqDist(all_words)

word_features = [x[0] for x in all_words.most_common(1500)]


def find_features(message):
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = word in words

    return features


features = find_features(processed[0])

messages = list(zip(processed, label))

np.random.shuffle(messages)

feature_set = [(find_features(text), label) for (text, label) in messages]

training, test = train_test_split(
    feature_set, test_size=0.25, random_state=1, shuffle=True
)

print(len(training))
print(len(test))


names = [
    "K Nearest Neighbors",
    "Decision Tree",
    "Random Forest",
    "Logistic Regression",
    "SGD Classifier",
    "Naive Bayes",
    "Support Vector Classifier",
]

classifiers = [
    KNeighborsClassifier(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    LogisticRegression(),
    SGDClassifier(max_iter=100),
    MultinomialNB(),
    SVC(kernel="linear"),
]

models = zip(names, classifiers)

for name, model in models:
    nltk_model = SklearnClassifier(model)
    nltk_model.train(training)
    accuracy = nltk.classify.accuracy(nltk_model, test)
    print("{} model Accuracy: {}".format(name, accuracy))

from sklearn.ensemble import VotingClassifier

models = list(zip(names, classifiers))

nltk_ensemble = SklearnClassifier(
    VotingClassifier(estimators=models, voting="hard", n_jobs=-1)
)
nltk_ensemble.train(training)
accuracy = nltk.classify.accuracy(nltk_ensemble, test)
print("Voting Classifier model Accuracy: {}".format(accuracy))

text_features, labels = zip(*test)
prediction = nltk_ensemble.classify_many(text_features)

print(classification_report(labels, prediction))

print(
    pd.DataFrame(
        confusion_matrix(labels, prediction),
        index=[["actual", "actual"], ["positive", "negative"]],
        columns=[["predicted", "predicted"], ["positive", "negative"]],
    )
)
