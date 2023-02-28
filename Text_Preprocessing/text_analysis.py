#### Libraries #####
import re
import string
from collections import Counter
import pandas as pd
import networkx as nx
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import urllib.request
from matplotlib import pyplot as plt
import seaborn as sns

import nltk
nltk.download("stopwords")
nltk.download('wordnet')
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.util import ngrams


#### Constants #####
filename1 = "HB11_example.txt"
extra_stop_words = ["hb", "introduced", "page", "california", "texas"]
stopwords_fix = stopwords.words("english") + extra_stop_words
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()
key_ngrams_ex = [("advertising", "licensee"), ("board", ), ("regulation", ), ("electronic", "security")]
KEY_NGRAMS = [("energy",), ("fuel",), ("coal",), ("electric",), ("gas",), ("oil",), 
 ("petroleum",), ("nuclear",), ("renewable",), ("barrel",), ("battery",),
 ("diesel",), ("grid",), ("power",), ("reactor",), ("refinery",), 
 ("pipeline",), ("dam",), ("solar",), ("drill,"), ("hydro",), ("hydra",),
 ("environment",), ("extractive", "industry"), ("climate", "change"), 
 ("global", "warming"), ("greenhouse",), ("carbon",), ("pollution",), 
 ("ozone",), ("acid", "rain"), ("biomass",), ("ethanol",), ("cap", "trade"),
 ("air",), ("wind",), ("capacity",), ("emission",), ("conservation",), 
 ("fume",), ("peak", "load"), ("kerosene",), ("clunker",)]

def file_to_string(filename):
    with open(filename) as file:
        bill_string = file.read().replace('\n',' ')

    return bill_string

#print(file_to_string(filename1))


def clean_tokenize_regex(bill_text, lemm_bool = False):

    cleaned_text = re.sub(r'[^\w\s]', "", bill_text) # punctuation
    cleaned_text = re.sub(r'[0-9]',"", cleaned_text) # digits
    cleaned_text = re.sub(r'\b[a-zA-Z]\b', "", cleaned_text) # single characters
    cleaned_text = re.sub(' +', ' ', cleaned_text) # multiple spaces
    cleaned_text = cleaned_text.lower()
    # Get rid of stopwords
    remove_this = re.compile(r'\b(' + r'|'.join(stopwords.words("english") + 
                                                extra_stop_words) + r')\b\s*')
    cleaned_text = remove_this.sub("", cleaned_text)
    list_clean_text = cleaned_text.split()
    if lemm_bool == True:
        return [lemmatizer.lemmatize(w) for w in list_clean_text]
    return list_clean_text

    #print(lemmatizer.lemmatize("petroleum"), porter.stem("hydroelectric"))
    #print(len(clean_tokenize_regex(file_to_string(filename1), True)))

def count_dict_state(list_bills, n, lemm_bool, mostcommon = None):
    list_ngrams = []
    for bill in list_bills:
        clean_text = clean_tokenize_regex(bill["description"], lemm_bool)
        list_ngrams += list((ngrams(clean_text, n)))

    dict_1 = dict(Counter(list_ngrams).most_common(mostcommon))
    dict_1 = dict({((" ").join(key),val) for (key,val) in dict_1.items()})
    
#return dict(sorted(dict_1.items(), key=lambda x:x[1], reverse = True))
    return dict_1


def state_word_cloud(lst_bills, n, filename, lemm_bool, mostcommon = None):
    n_gram_dict = count_dict_state(lst_bills, n, lemm_bool, mostcommon)
    #print(n_gram_dict)

    wordcloud_CA = WordCloud(width = 1000, 
                        height = 500, 
                        background_color="black",
                        colormap="Paired").generate_from_frequencies(n_gram_dict)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    plt.savefig(filename+".png", bbox_inches='tight')
    plt.close()

    return None

def sliding_window_key_word(keyngrams, bill_text_lst, window_size):
    
    count = 0
    leap = int(window_size/2)
    for i in range(0, len(bill_text_lst), leap):
        window = bill_text_lst[i:i+window_size]
        for kngram in keyngrams:
            if set(kngram).issubset(window):
                count += 1
    
    return count/len(bill_text_lst)

#print(sliding_window_key_word(key_ngrams_ex, list_tokens, 10))

def dict_energy_policy_index(keyngrams, list_bills, window_size):
    dict = {} 
    for bill in list_bills: 
        cleaned_text_lst = bill["description"]
        dict[bill["id"]] = sliding_window_key_word(keyngrams, 
                                                   cleaned_text_lst,
                                                   window_size)
    
    return None
