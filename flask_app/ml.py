import nltk
import pickle
import pandas as pd

from nltk.corpus import wordnet
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer


# Model configs
MAX_RES = 10
MAX_NB_WORDS = 99999
MAX_SEQUENCE_LENGTH = 200


class Model(object):
    def __init__(self, version_name):
        super().__init__()
        self.load_model(version_name)


    def load_model(self, version_name):
        self.tokenizer = pickle.load(open('static/ml_models/{}_tokenizer.pkl'.format(version_name), 'rb'))
        self.le = pickle.load(open('static/ml_models/{}_label_encoder.pkl'.format(version_name), 'rb'))
        self.model = keras.models.load_model('static/ml_models/{}_model.h5'.format(version_name))

    def get_words(self, meaning):
        if self.model is None:
            raise ValueError('Model not initialized')
        clean_mean = self.process_sentence(meaning)
        X = pd.DataFrame(pad_sequences(self.tokenizer.texts_to_sequences([clean_mean]), maxlen=MAX_SEQUENCE_LENGTH))
        return self.le.inverse_transform(self.model.predict(X)[0].argsort()[::-1][:MAX_RES])

    # function to convert nltk tag to wordnet tag
    def nltk_tag_to_wordnet_tag(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:          
            return None

    def get_wordnet_pos(self, tag):
        tags = {
            "a": "adj",
            "s": "adj", 
            "n": "noun",
            "v": "verb",
            "r": "adv",
        }
        try:
            return tags[tag]
        except KeyError:
            return "unknown"
    
    def process_sentence(self, sentence):
        # Removes stopwords, punctuations, and lemmatizes the sentence
        # Input: She sells sea shells by the sea shore!
        # Output: She sell sea shell sea shore
        processed = []
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        STOP_WORDS = set(stopwords.words('english'))

        tokens = tokenizer.tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)

        for word, pos_tag in pos_tags:
            wn_tag = self.nltk_tag_to_wordnet_tag(pos_tag)
            if word in STOP_WORDS: 
                pass
            elif wn_tag is None:
                processed.append(wordnet_lemmatizer.lemmatize(word))
            else:
                processed.append(wordnet_lemmatizer.lemmatize(word, wn_tag))

        return " ".join(processed)

    def get_meanings(self, words):
        result = []
        for word in words:
            meanings = []
            for syn in wordnet.synsets(word):
                meanings.append((self.get_wordnet_pos(syn.pos()), syn.definition(),))
            result.append((word, meanings))
        return result
