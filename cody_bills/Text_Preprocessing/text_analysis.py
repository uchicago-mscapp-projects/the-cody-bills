#######################################################
##  This script takes the bills scraped              ##
##  by Manuel, clean and tokenize their text         ##
##  and with it generates wordclouds as PNG files    ##
##  and json files with The Normalized Energy        ##
##  Policy Index (calculated using a sliding window  ##
##  algorithm)                                       ##
##                                                   ##
##  Author: Santiago Satizabal                       ##
##  email: ssatizabal@uchicago.edu                   ##
#######################################################

## TEXT PROCESSING ANALYSIS ##

#### Libraries #####
import json
import re
from collections import Counter
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import plotly.express as px

import nltk
nltk.download("stopwords")
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.util import ngrams


#### Constants #####

### Stop Words
extra_stop_words = ["hb", "introduced", "page", "pennsylvania", "texas", 
                    "illinois", "project", "bill", "bills", "id", "key", 
                    "assembly", "hereby", "allocation", "shall", "act", 
                    "state", "states", "may","section", "subsection", 
                    "sections", "subsections","commonwealth", "general", 
                    "law","code", "person", "chapter", "chapters", "contingency",
                    "contingencies", "read", "amended", "take", "takes" 
                    "legislature", "enacted", "date", "version","text","follows", 
                    "government", "take", "effect", "year","years", "district", 
                    "districts", "department", "departments", "thesame", "topic", 
                    "see"]

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
TX_from = "cody_bills/Text_Preprocessing/bills_texas.json"
PA_from = "cody_bills/Text_Preprocessing/bills_pennsylvania.json"

TX_to_table = "cody_bills/assets/table_texas.json"
PA_to_table = "cody_bills/assets/table_pennsylvania.json"

TX_to_word = "cody_bills/assets/words_texas"
PA_to_word = "cody_bills/assets/words_pennsylvania"

TX_to_bigram = "cody_bills/assets/bigrams_texas"
PA_to_bigram = "cody_bills/assets/bigrams_pennsylvania"

def clean_tokenize_regex(bill_text, lemm_bool = False):
    """
    Takes the extracted text of the bills (string) and cleans it removing
    punctuation, digits, single characters, etc. The function tokenizes
    the strings and optionally lemmatize them to ease the analysis.
    Inputs: bill_text: text of the bill (str)
            lemm_bool: lemmatizes the tokens if True (bool)
    Returns: list of cleaned lowercased, (lemmatized) tokens
    """

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
        return [lemmatizer.lemmatize(w) for w in list_clean_text if len(w)>2]
    return list_clean_text


def count_dict_state(dict_bills, n, lemm_bool, mostcommon = None):
    """
    Creates a dictionary that maps an ngram to the number of times it appears
    in a set of bills. 
    Inputs: dict_bills: nested dictionary that contains all the extracted 
                        bills of a given state with the information of 
                        the bills
            n: integer that represents the number of words we want the 
               ngrams to have
            lemm_bool: lemmatizes the tokens if True (bool)
            mostcommon: the top mostcommon ngrams we want the dictionary to 
                        show (int)
    Returns: Dictionary that maps each kgram found in the set of bills of 
             the state
             to the number of times it appears in the whole corpus
    """
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
    """
    Plots a wordcloud of the most common ngrams from the scraped dictionary 
    of bills.  
    Inputs: dict_bills: nested dictionary that contains all the extracted 
                        bills of a given state with the information of the 
                        bills
            n: integer that represents the number of words we want the ngrams
            to have
            filename: the name of the filename or path we will save the word 
            cloud plot in.
            lemm_bool: lemmatizes the tokens if True (bool)
            mostcommon: the top mostcommon ngrams we want the dictionary to 
            show (int)
    Returns: None. Saves the wordcloud plot in the specified filename
    """

    n_gram_dict = count_dict_state(dict_bills, n, lemm_bool, mostcommon)
    wordcloud = WordCloud(width = 7000, 
                        height = 7000, 
                        background_color="white",
                        contour_color="black",
                        prefer_horizontal = 1.0,
                        mask = MASK).generate_from_frequencies(n_gram_dict)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(filename+".png", bbox_inches='tight')
    plt.close()

    return None

def sliding_window_key_word(keyngrams, bill_text_lst, window_size):
    """
    From the tokenized text of a bill (list), returns an indicator calculated
    following a sliding window algorithm. The algorithm takes a slice of 
    the list of tokens of a given size (window_size) and searches for the 
    elements of a list of key-ngrams in the window. Each time a key-ngram 
    appears in the window the count augments in 1. The window leaps in a 
    fourth of its size (arbitrarily chose that size but can easily be changed), 
    and repeat the process. The final count is divided by the number of 
    tokens in the bill. 
    Inputs: keyngrams: list of key-ngrams related to energy policy 
                       (list of tuples)
            bill_text_lst: list of the tokens that make up the text of a bill
            window_size: integer that represents the size of the slice.
    Returns: A float that is the ratio between the final count and the length 
             of the bill times 100. In this case it is the Energy policy index
    """

    count = 0
    leap = window_size//4
    for i in range(0, len(bill_text_lst), leap):
        window = bill_text_lst[i:i+window_size]
        for kngram in keyngrams:
            if set(kngram).issubset(window):
                count += 1
    
    return (count/len(bill_text_lst))*100


def dict_energy_policy_index(keyngrams, dict_bills, window_size):
    """
    From a scraped dictionary of bills, change the name of some keys and 
    creates a whose value is the score given when searching for the keywords using 
    the sliding window method, the Energy Policy Index in oru case.
    Inputs: keyngrams: list of key-ngrams related to energy policy (list of tuples)
            dict_bills: nested dictionary that contains all the extracted 
                        bills of a given state with the information of the bills
            window_size: integer that represents the size of the slice.
    """

    dict_list = []
    for bill in dict_bills.values():
        if "text" not in bill:
            continue
        d = {}
        d["Bill ID"] = bill["id"]
        d["Description"] = bill["title"]
        d["Chamber"] = bill["chamber"]
        d["Created date"] = bill["created_date"] 
        cleaned_text_lst = clean_tokenize_regex(bill["text"], True)
        d["Energy Policy Index"] = sliding_window_key_word(keyngrams, 
                                                   cleaned_text_lst,
                                                   window_size)
        d["State"] = bill["state"]
        d["url"] = bill["link"]
        dict_list.append(d)
    
    return dict_list

def append_and_normalize_index(dict_lst_TX, dict_lst_PA):
    """
    Takes the dictionaries of Texas and Pennsylvania that have the 
    Energy Policy Index, append them, normalize the index between 
    1 and 0 using feature scaling (x - Min(X))/(Max(X) - Min(X))
    and divide the database into two lists of dictionaries again. 
    Inputs: dict_lst_TX, dict_lst_PA: lists of dictionaries with non-normalized
                                      energy policy index
    Returns: Tuple with the complete (2-state) dataframe, and each state's list
             of dictionaries updated with the normalized index. 
    """

    df_TX = pd.DataFrame.from_dict(dict_lst_TX, orient='columns')
    df_PA = pd.DataFrame.from_dict(dict_lst_PA, orient='columns')
    df_both_states = pd.concat([df_PA,df_TX])
    min_epol_index = min(df_both_states["Energy Policy Index"])
    max_epol_index = max(df_both_states["Energy Policy Index"])
    df_both_states["Norm_EPol_Index"] = ((df_both_states["Energy Policy Index"] - 
                                          min_epol_index)/(max_epol_index - min_epol_index))
    texas_norm_list = df_both_states.loc[df_both_states["State"] == \
                                         "Texas"].to_dict("records")
    pennsylvania_norm_list = \
                            df_both_states.loc[df_both_states["State"] == \
                            "Pennsylvania"].to_dict("records")

    return (df_both_states, pennsylvania_norm_list, texas_norm_list)

def run_word_clouds():
    """
    Generates the wordclouds for both states. Each state windsup with
    a bigram and unigram wordcloud saved using the filenames defined 
    as constants at the begining of the code.
    """
    with open(TX_from) as f:
        texas_dict = json.load(f)

    with open(PA_from) as f:
        pennsylvania_dict = json.load(f)
    
    # Unigrams
    print("Saving unigram wordclouds")
    state_word_cloud(texas_dict, 1, TX_to_word, True, 60)
    state_word_cloud(pennsylvania_dict, 1, PA_to_word, True, 60)
    # Bigrams
    print("Saving bigram wordclouds")
    state_word_cloud(texas_dict, 2, TX_to_bigram, True, 60)
    state_word_cloud(pennsylvania_dict, 2, PA_to_bigram, True, 60)
    

def run_norm_index_tables():
    """
    Generates the tables (lists of dictionaries) for both states to be 
    used in the dashboard. Again it uses the filenames defined in the 
    "Constants" section at the beginning of the code.
    """

    with open(TX_from) as f:
        texas_dict = json.load(f)

    with open(PA_from) as f:
        pennsylvania_dict = json.load(f)
    
    # normalized Tables
    TX_index_dict = dict_energy_policy_index(KEY_NGRAMS, texas_dict, 20)
    PA_index_dict = dict_energy_policy_index(KEY_NGRAMS, pennsylvania_dict, 20)
    _, pennsylvania_norm, texas_norm = append_and_normalize_index(TX_index_dict, 
                                                                  PA_index_dict)

    print("Saving Table for Pennsylvania")
    with open(PA_to_table, "w", encoding="utf-8") as nf:
        json.dump(pennsylvania_norm, nf, indent=1)
    print("Saving Table for Texas")
    with open(TX_to_table, "w", encoding="utf-8") as nf:
        json.dump(texas_norm, nf, indent=1)

    return None

if __name__ == "__main__":
    run_norm_index_tables()
    run_word_clouds()
