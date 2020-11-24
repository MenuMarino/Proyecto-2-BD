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
import os

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

def create_tweets_index(filename):

    tweets = read_json(filename)
    tweets.sort()    
   

    ids = []
    texts = []
    for i in tweets:        
        ids.append("{:<40}".format(i[0]))
        texts.append("{:<600}".format(i[1]))


    tsize = open("tsize.txt","w")
    tsize.write(str(len(ids)-1))
    tsize.close()
  
   
    tindex = open("tindex.txt","w")  
    for i in range(0, len(ids)-1):
        tindex.write(ids[i])
        tindex.write(texts[i])
    tindex.write(ids[len(ids)-1])
    tindex.write(texts[len(ids)-1])
    tindex.close()

def buscar_tweet(x):
    regs = open("tsize.txt","r")
    cantregs = regs.readline()
    regs.close()
    cantregs = int(cantregs)

    file = open("tindex.txt", 'r')
    low = 0
    high = cantregs

    tweet = ""

    while low <= high: 
  
        mid = (high + low) // 2

        file.seek(mid*640)
        aux = file.read(640)
        docid = aux[0:40]
        docid = docid.replace(" ", "")
        docid = int(docid)
        tweet = aux[30:640]
       # print(termino)
        if docid < x: 
            low = mid + 1
  
        elif docid > x: 
            high = mid - 1
  
        elif docid == x: 
            break
        else:
            tweet = ""
  
    if(tweet != "" and docid == x):
        # print(tweet.strip())
        return ( tweet.strip(), len(limpiar_texto(tweet.strip())) )
    else:
        return ()
        print("no encontrado")

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

def read_json(filename):
    
    df = pd.read_json(filename)
    ids =[]
    texts = []
    pares = []
    tam = len(df['id'])

    for i in range(0,tam):
        if(df['retweeted'][i] == False):
            
            ids.append(df['id'][i])
        
            encoded_string = df['text'][i].encode("ascii", "ignore")
            decode_string = encoded_string.decode()
            texts.append(decode_string)

        
    for i in range(0,len(texts)):
        aux = []
        aux.append(ids[i])
        aux.append(texts[i])
        pares.append(aux)    
    return pares

def create_complete_tweets_index(filename):
    df = pd.read_json(filename)
    ids = []
    dates = []
    texts = []
    user_ids = []
    user_names = []
    locations = []
    retweeted = []
    maxi =0

    tam = len(df['id'])
    
    for i in range(0,tam):
        if(df['retweeted'][i] == False):
            ids.append("{:<40}".format(str(df['id'][i])))
            
            dates.append("{:<40}".format(str(df['date'][i])))

            encoded_string = df['text'][i].encode("ascii", "ignore")
            decode_string = encoded_string.decode()
            texts.append("{:<600}".format(decode_string))

            user_ids.append("{:<40}".format(str(df['user_id'][i])))

            user_names.append("{:<40}".format(str(df['user_name'][i])))

            retweeted.append("{:<6}".format(str(df['retweeted'][i])))

    
    index = open("full_tindex.txt","w")

    for i in range(0,len(ids)-1):
          index.write(ids[i])
          index.write(dates[i])
          index.write(texts[i])
          index.write(user_ids[i])
          index.write(user_names[i])
          index.write(retweeted[i])
          
    index.write(ids[len(ids)-1])
    index.write(dates[len(ids)-1])
    index.write(texts[len(ids)-1])
    index.write(user_ids[len(ids)-1])
    index.write(user_names[len(ids)-1])
    index.write(retweeted[len(ids)-1])

    index.close()
    
def buscar_tweet_completo(x):
    
    regs = open("tsize.txt","r")
    cantregs = regs.readline()
    regs.close()
    cantregs = int(cantregs)

    file = open("full_tindex.txt", 'r')
    low = 0
    high = cantregs

    pos = -1
    

    while low <= high: 
  
        mid = (high + low) // 2

        file.seek(mid*766)
        aux = file.read(766)
        docid = aux[0:40]
        docid = docid.replace(" ", "")
        docid = int(docid)
       # print(termino)
        if docid < x: 
            low = mid + 1
  
        elif docid > x: 
            high = mid - 1
  
        elif docid == x: 
            break
        else:
            pos = -1

    if(docid == x):

        a = aux[0:40]
        a = a.strip()
        a = int(a)

        b = aux[40:80]
        b = b.strip()

        c = aux[80:680]
        c = c.strip()

        d = aux[680:720]
        d = d.strip()
        d = int(d)

        e = aux[720:760]
        e = e.strip()

        a1 = aux[760:766]
        a1 = a1.strip()
        f = False
        if(a1 == "true"):
            f = True
            
        my_dict = {'id': a, 'date': b, 'text': c, 'user_id': d, 'user_name': e, 'retweet': f}
        
        print(my_dict['id'])
        print(my_dict['date'])
        print(my_dict['text'])
        print(my_dict['user_id'])
        print(my_dict['user_name'])
        print(my_dict['retweet'])
        return ( my_dict, len(limpiar_texto(my_dict['text'])) )
    else:
        print("no encontrado")

def create_index(filename):

    xd = read_json(filename)
    stopwords_adicionales = ['«', '»', 'º', ';', '-', ',', '.', '.', ':', '"', 'la', 'el', '', '(', ')', '``', '111º']
    stopwords_adicionales += ['!', '@', '#', '$']
    stop= stopwords.words("spanish") + stopwords_adicionales
    stoplist = stop
    

    texto_limpio = []

    for i in xd:
        texto = limpiar_texto(i[1])
        i[1] = texto
        i[1].sort()
        texto_limpio = texto_limpio + i[1]
    
    N = len(xd)
    texto_limpio.sort()

    final = list(set(texto_limpio)) 

    final.sort()

    xd.sort()
    tokens = []
    for token in final:
         aux1 = "{:<30}".format(token)
         tokens.append(aux1)
         #print(aux1)
   
    index = open("index1.txt", "w")
    posis =[]
    for token in final: 
        aux2 = "{:<10}".format(index.tell())
        posis.append(aux2)
        index.write(token)
        index.write(':')
        docs = []
        occ = []
        cont = 0
        
        for i in xd:   
            if token in i[1]:
                cont = cont+1
                docs.append(str(i[0]))
                occ.append(i[1].count(token))
                
        escribir = []
        
        for i in range(0,len(docs)):
            escribir.append("[")
            escribir.append(docs[i])
            escribir.append("|")
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
    
    table = open("indice.txt","w")
    for i in range(0,len(posis)-1):
           table.write(tokens[i])
           table.write(posis[i])
    table.write(tokens[len(posis)-1])
    table.write(posis[len(posis)-1])
    table.close()
    
    regs = open("registros.txt","w")
    regs.write(str(len(posis)-1))
    regs.close()

def buscar(x):
    # 'x' tiene que ser una sola palabra
    x = limpiar_texto(x)[0]
    regs = open("registros.txt","r")
    cantregs = regs.readline()
    regs.close()
    cantregs = int(cantregs)

    file = open("indice.txt", 'r')
    low = 0
    high = cantregs

    pos = -1

    while low <= high: 
  
        mid = (high + low) // 2

        file.seek(mid*40)
        aux = file.read(40)
        termino = aux[0:30]
        termino = termino.replace(" ", "")
        pos = int(aux[30:40])
       # print(termino)
        if termino < x: 
            low = mid + 1
  
        elif termino > x: 
            high = mid - 1
  
        elif termino == x: 
            break
        else:
            pos = -1
  
    if(pos >-1 and termino == x):
        index = open("index1.txt","r")
        index.seek(pos)
        aux = index.readline()
        # print(aux)
        return aux
    else:
        return ""

def formatear(string):
    result = []
    if string == "":
        return result
    lista = string.split(':')[1].split(',')
    for i in range(0, len(lista)-1):
        par = lista[i][1:-1].split('|')
        result.append( ( int(par[0]), float(par[1]) ) )
    par = lista[len(lista)-1].rstrip()[1:-1].split('|')
    result.append( ( int(par[0]), float(par[1]) ) )
    # for tupla in result:
    #     print(tupla)
    return result

# recibe el query y el documento
def cosine(q, doc):
    # TODO: agarrar la interseccion de terminos entre 'q' y 'doc'
    return np.dot(q, doc) / (np.linalg.norm(q) * np.linalg.norm(doc))

# OJO: query_text = ['candidatura', 'presidencial', 'peru', '2021']
def tf_idf(query_text, query):
    # tf = veces que aparece el termino en el documento
    # df = (1), ya que el unico 'documento' que tenemos, es el query
    # idf = N/df
    query_text = np.array(query_text)
    unique, counts = np.unique(query_text, return_counts=True)
    dic = dict(zip(unique, counts))
    return math.log10(1 + dic[query]) * math.log10(query_text.shape[0])

def retrieval_cosine(query_text, k):
    query_terms = limpiar_texto(query_text)
    query_terms_len = len(query_terms)
    # terms_tf_idf = np.array([])
    terms_tf_idf = {}
    for term in query_terms:
        # terms_tf_idf = np.append(terms_tf_idf, tf_idf(query_terms, term))
        terms_tf_idf[term] = tf_idf(query_terms, term)

    # query_text = ['candidatura', 'presidencial', 'peru', '2021'] (no steameado)
    # query_terms = ['candidatur', 'presidencial', 'peru', '2021'] (stemeado)
    # terms_tf_idf = [0.2, 0.1, 0.3, 0.6]
    # terms_tf_idf = {
    #   'candidatur': 0.2,
    #   'presidencial': 0.1,
    #   'peru': 0.3
    #   '2021': 0.6
    # }

    result = []

    collection = {}

    #  "candidatur urrest eleccion congresal 2020"

    for term in query_terms: # iterar por cada termino del query
        docs = formatear(buscar(term)) # todos los documentos que contienen a 'query'
        for par in docs:
            # par[0]: tweetId
            # par[1]: tf-idf entre tweetId y query
            
            tweetId = par[0]
            term_tweet_tf_idf = par[1]

            if tweetId in collection:
                collection[tweetId] += term_tweet_tf_idf * terms_tf_idf[term]
            else: 
                collection[tweetId] = term_tweet_tf_idf * terms_tf_idf[term]

    for tweetId, numerador in collection.items():
        tweet_correspondiente = buscar_tweet_completo(tweetId)
        collection[tweetId] = collection[tweetId] / ( tweet_correspondiente[1] * query_terms_len )
        result.append( ( tweet_correspondiente[0], collection[tweetId] ) )

    result.sort(key = lambda tup: tup[1], reverse=True)
    # result[:k]
    tweets = []
    ist = []
    if k != -1:
        ist = result[:k]
    else:
        ist = result
    for tupla in ist:
        tweets.append( tupla[0] )
    return tweets

filename = "tweets1.json"

# create_index(filename)
# create_tweets_index(filename)
# create_complete_tweets_index(filename)

# results = retrieval_cosine("JorgeMunozAP Jorge", 3)

# for result in results:
#     print(result)