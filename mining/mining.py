from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys

def __init__():
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

def read_file(file_path, stopword="stopword.txt"):
    file_article = open(file_path, "r")
    read_article = file_article.read()

    file_stop_list = open(stopword, "r")
    stop_word = file_stop_list.read()

    return read_article, stop_word

def read_stopword(stopword="mining/stopword.txt"):
    file_stop_list = open(stopword, "r")
    stop_word = file_stop_list.read()

    return stop_word

def tokenizing(read_article, stop_word, judul):
    data = read_article.split()
    data_stopword = stop_word.split()
    data_judul = judul.split()

    for i in data_judul:
        data.append(i)
    data_low = [i.lower() for i in data]

    return data_low, data_stopword, data_judul

def textmining(data, data_stopword, data_judul, result, stemmer):
    for i in data:
        word = i
        for ch in ['.',',','!','(',')',';','”','“',']','[',':','?','/','"','-']:
            word = word.replace(ch,"")
            i = word
            
        isPass = "True"
        for j in data_stopword:
            if i == j:
                isPass = "False"
                break
        
        if isPass == "True":
            if stemmer.stem(i) in result:
                result[stemmer.stem(i)] +=1
            else:
                result[stemmer.stem(i)] = 1
        
    return result