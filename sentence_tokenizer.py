import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords

def sent_tokenizer(sentence): #Parts of Speech Tokenizer
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

def sorting_pos(sentence): #filtering function
    punc_list = ['.','!','?',',']
    stop_words = set(stopwords.words("english") + punc_list)
    words = nltk.word_tokenize(sentence)
    filtered_sent = []
    for w in words:
        if w not in stop_words:
            filtered_sent.append(w)
    return filtered_sent