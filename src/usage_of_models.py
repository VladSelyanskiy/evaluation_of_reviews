import dill
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

snowball = SnowballStemmer(language="russian")
russian_stop_words = stopwords.words("russian")

vectorizer = TfidfVectorizer(
    tokenizer=lambda x: tokenize_sentence(x, remove_stop_words=True), token_pattern=None
)

classes = {0: "negative", 1: "positive"}

with open(r"src\models\logistic_regression_classifier.pickle", "rb") as file:
    logreg_model = dill.load(file)["model"]

with open(r"src\models\naive_bayes_classifier.pickle", "rb") as file:
    nb_model = dill.load(file)["model"]


def tokenize_sentence(sentence: str, remove_stop_words: bool = True):
    tokens = word_tokenize(sentence, language="russian")
    tokens = [i for i in tokens if i not in string.punctuation]
    if remove_stop_words:
        tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens


def use_model_nb(text):

    return classes[nb_model.predict([text])[0]]


def use_model_lr(text):
    return classes[logreg_model.predict([text])[0]]
