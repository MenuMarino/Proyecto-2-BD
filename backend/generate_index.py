
from __future__ import division
from nltk import word_tokenize as nltkword_tokenize
from os import system as ossystem
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter
import pandas as pd
import numpy as np
import json
import ijson
import math
__filename = "index.txt"
stoplist = []
stemmer = SnowballStemmer("spanish")
def limpiar_texto(texto):
    tokens = nltkword_tokenize(texto)
    cleaned_tokens = []
    for token in tokens:
        if token.lower() not in stoplist:
            cleaned_tokens.append(token)

    super_cleaned_tokens = []
    for token in cleaned_tokens:
        super_cleaned_tokens.append(stemmer.stem(token))
    return super_cleaned_tokens

def extraer_texto(filename):
    sw = open(filename, 'r')
    data = sw.read().replace('\n', ' ')
    sw.close()
    return data

def read_json(filename):
    
    df = pd.read_json(filename)
    ids =[]
    texts = []
    pares = []
    for i in df['id']:
        ids.append(i)

    for i in df['text']:
        encoded_string = i.encode("ascii", "ignore")
        decode_string = encoded_string.decode()
        texts.append(decode_string)
        
    for i in range(0,len(texts)):
        aux = []
        aux.append(ids[i])
        aux.append(texts[i])
        pares.append(aux)    
    return pares



def L(term):
    index = open(__filename, "r")
    line = index.readline()
    while (line[0:len(term)] != term):
        line = index.readline()
    if (line[0:len(term)] == term):
        return line[len(term)+1:].split(',')[:-1]
        index.close()
    else:
        index.close()
    

def AND(pubs1, pubs2):
    return list(set(pubs1).intersection(set(pubs2)))

def OR(pubs1, pubs2):
    return list(set((pubs1+pubs2)))

def AND_NOT(pubs1, pubs2):
    return list(set(pubs1).difference(set(pubs2)))



def create_index(filename):

    xd = read_json(filename)
    stopwords_adicionales = ['«', '»', 'º', ';', '-', ',', '.', '.', ':', '"', 'la', 'el', '', '(', ')', '``', '111º']
    stop= stopwords.words("spanish") + stopwords_adicionales
    stoplist = stop
    

    texto_limpio = []

    for i in xd:
        texto = limpiar_texto(i[1])
        i[1] = texto
        i[1].sort()
        texto_limpio = texto_limpio + i[1]

    '''
    for i in xd:
        print(i[1])
    '''

    N = len(xd)




    texto_limpio.sort()

    final = list(set(texto_limpio)) 

    final.sort()

    '''
    for token in final:
        print(token)
    '''

    xd.sort()


    index = open("index1.txt", "w")
    for token in final:
        
        index.write(token)
        index.write(':')
        cont = 0
        docs = []
        occ = []
        for i in xd:   
            
           # print(i[1])
            if token in i[1]:
                
                cont = cont+1
                docs.append(str(i[0]))
                #print(occurrences)
                occ.append(i[1].count(token))
                
        escribir = []
        
        for i in range(0,len(docs)):
            escribir.append("[")
            escribir.append(docs[i])
            escribir.append(",")
            weight = math.log10( 1 + occ[i] ) * math.log10( (N/cont))
            #print(math.log10( 1 + occ[i] ))
            escribir.append(str(weight))
            escribir.append("]")
            escribir.append(",")

        escribir.pop()

        for i in escribir:
            index.write(i)
            
        #print(cont)
        index.write('\n')
        

    index.close()


def recovery(docs):
    files = []
    for num in docs:
        filename = f"libro{num}.txt".format(num)
        files.append(filename)
    return files



create_index("tweets1.json")
