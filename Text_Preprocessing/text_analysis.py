#### Libraries #####
import json
import re
import string
from collections import Counter
import pandas as pd
import numpy as np
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

with open("bills_pennsylvania.json") as f:
    pennsylvania_dict = json.load(f)


### Stop Words
extra_stop_words = ["hb", "introduced", "page", "pennsylvania", "texas", 
                    "illinois", "project", "bill", "id", "key", "assembly",
                    "hereby", "allocation", "shall", "act"]

stopwords_fix = stopwords.words("english") + extra_stop_words
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Energy policy related Key words or Ngrams to search for within the texts

KEY_NGRAMS = [("energy",), ("fuel",), ("coal",), ("electric",), ("gas",), ("oil",), 
 ("petroleum",), ("nuclear",), ("renewable",), ("barrel",), ("battery",),
 ("diesel",), ("grid",), ("power",), ("reactor",), ("refinery",), 
 ("pipeline",), ("dam",), ("solar",), ("drill,"), ("hydro",), ("hydra",),
 ("environment",), ("extractive", "industry"), ("climate", "change"), 
 ("global", "warming"), ("greenhouse",), ("carbon",), ("pollution",), 
 ("ozone",), ("acid", "rain"), ("biomass",), ("ethanol",), ("cap", "trade"),
 ("air",), ("wind",), ("capacity",), ("emission",), ("conservation",), 
 ("fume",), ("peak", "load"), ("kerosene",), ("clunker",)]

# Round Mask for Wordcloud
x, y = np.ogrid[:300, :300]
MASK = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
MASK = 255 * MASK.astype(int)


#### filenames ###
# TX_from = "Text_Preprocessing/"
# PA_from = "Text_Preprocessing/bills_pennsylvania.json"

# TX_to_table = "cody_bills/assets/table_texas.txt"
# PA_to_table = "cody_bills/assets/table_pennsylvania.txt"

# TX_to_word = "cody_bills/assets/words_texas"
# PA_to_word = "cody_bills/assets/words_pennsylvania"

# TX_to_bigram = "cody_bills/assets/bigrams_texas"
# PA_to_bigram = "cody_bills/assets/bigrams_pennsylvania"


def file_to_dict(filename):
    with open(filename) as f:
        state_dict = json.load(f)

    return state_dict

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

def count_dict_state(dict_bills, n, lemm_bool, mostcommon = None):
    list_ngrams = []
    for bill in dict_bills.values():
        if "text" not in bill:
            continue
        clean_text = clean_tokenize_regex(bill["text"], lemm_bool)
        list_ngrams += list((ngrams(clean_text, n)))

    dict_1 = dict(Counter(list_ngrams).most_common(mostcommon))
    dict_1 = dict({((" ").join(key),val) for (key,val) in dict_1.items()})
    
    return dict(sorted(dict_1.items(), key=lambda x:x[1], reverse = True))
    


def state_word_cloud(dict_bills, n, filename, lemm_bool, mostcommon = None):
    n_gram_dict = count_dict_state(dict_bills, n, lemm_bool, mostcommon)
    wordcloud = WordCloud(width = 7000, 
                        height = 7000, 
                        background_color="white",
                        contour_color='white',
                        prefer_horizontal = 1.0,
                        mask = MASK).generate_from_frequencies(n_gram_dict)
    plt.imshow(wordcloud)
    plt.axis("off")
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
    
    return (count/len(bill_text_lst))*100

#print(sliding_window_key_word(key_ngrams_ex, list_tokens, 10))

def dict_energy_policy_index(keyngrams, dict_bills, window_size):
    dict_list = []
    for bill in dict_bills.values():
        if "text" not in bill:
            continue
        d = {}
        d["Bill_id"] = bill["id"]
        d["Description"] = bill["title"]
        cleaned_text_lst = clean_tokenize_regex(bill["text"], True)
        d["Energy Policy Index"] = sliding_window_key_word(keyngrams, 
                                                   cleaned_text_lst,
                                                   window_size)
        dict_list.append(d)
    
    return dict_list


# def run_text_analysis():
#     with open(TX_from) as f:
#         texas_dict = json.load(f)

#     with open(PA_from) as f:
#         pennsylvania_dict = json.load(f)
    
#     # Unigrams
#     state_word_cloud(texas_dict, 1, TX_to_word, True, 60)
#     state_word_cloud(pennsylvania_dict, 1, PA_to_word, True, 60)
#     # Bigrams
#     state_word_cloud(texas_dict, 2, TX_to_bigram, True, 60)
#     state_word_cloud(pennsylvania_dict, 2, PA_to_bigram, True, 60)
#     # Tables
#     TX_index_dict = dict_energy_policy_index(KEY_NGRAMS, texas_dict, 20)
#     with open(TX_to_table, "w", encoding="utf-8") as nf:
#         json.dump(TX_index_dict, nf)

#     PA_index_dict = dict_energy_policy_index(KEY_NGRAMS, pennsylvania_dict, 20)
#     with open(PA_to_table, "w", encoding="utf-8") as nf:
#         json.dump(PA_index_dict, nf)

#     return None