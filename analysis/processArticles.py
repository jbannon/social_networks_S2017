import numpy as np
import nltk 
from nltk import *
import pandas as pd
import sklearn
from numpy import *
import curses 
import sys
from curses.ascii import isdigit 
import nltk
from nltk.corpus import cmudict 
from sklearn.cross_validation import permutation_test_score
import sklearn
import json
d = cmudict.dict() 



#def nsyl(word): 
# return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]] 



def lexical_diversity(text):
    return (len(set(text)) / len(text)) # scale values

def syll_count(wordlist):
    ## needs improving
    if len(wordlist)==0:
        print('error')
        sys.exit(0)
    csum = 0
    vowels = list('aeiou')
    for w in wordlist:
        l = w.lower()
        for char in l:
            if char in vowels:
                csum = csum+1
    return csum
    
def flesch_kincaid_g(text):
    words = nltk.word_tokenize(text)
    sents = nltk.sent_tokenize(text)
    n_words = len(words)
    n_sents = len(sents)
    nsyll = syll_count(words)
    fkgscore = 0.39*(n_words/n_sents) + 11.8*(nsyll/n_words)-15.59
    return np.floor(fkgscore)

def flesch_kincaid_e(text):
    print("hi")

def stringListMerge(L, sep):
    #print(L)
    return [sep.join(L)]

def processJSONFile(fname):
    import sys
    """if 'json' not in sys.modules or 'pandas' not in sys.modules or 'pd' not in sys.modules:
        print("error: you must import the 'json' module and the 'pandas' module")
        print("add 'import json' and 'import pandas as pd' to the code.")
        print("Exiting...")        
        sys.exit(0)"""
    id_num = 0
    inFile = open(fname,"r")
    jsons_list = inFile.readlines()
    inFile.close()
    #return jsons_list
    df_result = pd.DataFrame()
    for js in jsons_list:
        if js=='\n':
            continue
        #print('loading article with id '+str(id_num))
        json_dict = json.loads(js)
        #print(json_dict.keys())
        #print(json_dict['title'])
        #print("before function call json_dict is: ")
        #print(json_dict)
        json_dict = textProcessDict(json_dict,id_num)
        #print("after function call json_dict is: ")
        #print(json_dict)        
        non_con_dict = dict((key, json_dict[key]) for key  in json_dict.keys() if key!='content')
        #print("non_con_dict is: ")
        #print(non_con_dict) 
        df_temp = pd.DataFrame(non_con_dict)
        #print("temp df is:")
        #print(df_temp)
        df_result = df_result.append(df_temp,ignore_index=True)
        #print(df_result)
        id_num+=1
    newcols =['Article_ID', 'title','category', 'FK_Grade', 'Lex_Div', 'Title_Lex_Div', 'Title_FK_Grade','authors','date','fact','main','url']
    df_result= df_result.ix[:,newcols]
    df_result.to_csv("processed_articles.csv")
    return df_result
        
def textProcessDict(dct,id_num):
    """
        dct must have a:
            - key called 'content' which has article text.
            - key called 'title' which has the article title.
            - key called 'authors' which has 0 or more authors.
    """
    try:
        #print("in textProcess with id " + str(id_num))
        sepr = ", "
        text = dct['content']
        title_text = dct['title']
        dct['Article_ID'] = id_num
        dct['Lex_Div'] = lexical_diversity(text)
        dct['FK_Grade'] = flesch_kincaid_g(text)
        dct['Title_Lex_Div'] = lexical_diversity(title_text)
        dct['Title_FK_Grade'] = flesch_kincaid_g(title_text)
        if len(dct['authors'])==0:
            dct['authors'] = ['Unknown']
        elif len(dct['authors'])>1:
            dct['authors'] = stringListMerge(dct['authors'], sepr)
        return dct
    except KeyError:
        print('I got a KeyError - reason "%s"' % str(e))
        print("""
                    The dictionary passed must have a key called 'content' which 
                        has the article text.
                        and a key called 'title' which has
                        the article title.
                        One of those is missing. 
                        Exiting...
              """)
        sys.exit(0)
    

#vec_fkg = np.vectorize(flesch_kincaid_g)
#vec_fke = np.vectorize(flesch_kincaid_e)
#vec_ld = np.vectorize(lexical_diversity)


"""
todo: more metrics 


"""


src_file_name = 'articles.txt'
df_articles = processJSONFile(src_file_name)

