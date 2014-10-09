import pymorphy2
import os

morph = pymorphy2.MorphAnalyzer()

def get_normal_form(word):
    return morph.parse(force_decode(word))[0].normal_form


def force_decode(string, codecs=['utf8', 'cp1251']):
    for i in codecs:
        try:
            return string.decode(i)
        except:
            pass
        
        
def add(indexer, path):
    words = open(path).read().replace('.','').replace(',','').split()
    words = map(get_normal_form, words)
    for word in words:
        if word in indexer:
            indexer[word].add(path)
        else:
            indexer[word] = set([path])


def get_indexer(fname_indexer="indexer.txt"):
    return eval(open(fname_indexer).read())


def create_indexer(dir_docs="docs", fname_indexer="indexer.txt"):
    indexer = {}
    for fname in os.listdir(dir_docs):
        path = dir_docs+"\\"+fname
        add(indexer, path)
    f = open(fname_indexer,"w+")
    f.write(str(indexer))
    f.close()  
    
    
def find(word, indexer):
    word_n = get_normal_form(word)
    return set([]) if word_n not in indexer else indexer[word_n]


def search(query, indexer):
    words = query.split()
    if (query.find("AND")>0 or query.find("and")>0) and (query.find("OR")>0 or query.find("or")>0):
        return "incorrect query"
    if len(words) > 1:
        if words[1] == "or" or words[1] == "OR":
            return search_any([words[2*i] for i in range((len(words)+1)/2)], indexer)
        if words[1] == "and" or words[1] == "AND":
            return search_all([words[2*i] for i in range((len(words)+1)/2)], indexer)
        return "incorrect query"  
    return find(words[0], indexer)


def search_any(words, indexer):
    res = find(words[0], indexer)
    for word in words:
        res |= find(word, indexer)
    return res


def search_all(words, indexer):
    res = find(words[0], indexer)
    for word in words:
        res &= find(word, indexer)
        if len(res) == 0:
            return res
    return res



create_indexer(dir_docs="docs")
indexer = get_indexer()
query = "поиск and информационный"
print search(query, indexer)
