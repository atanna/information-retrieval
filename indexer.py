from collections import defaultdict
from collections import namedtuple
import pymorphy2
import os



Word = namedtuple("Word", ["word", "N", "direction"])
morph = pymorphy2.MorphAnalyzer()


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


def add(indexer, path):
    words = open(path).read().replace('.','').replace(',','').split()
    words = list(map(get_normal_form, words))
    n = len(words)
    for i in range(n):
        word = words[i]
        if path in indexer[word]:
            indexer[word][path].add(i)
        else:
            indexer[word][path] = set([i])


def get_indexer(fname_indexer="indexer.txt"):
    return defaultdict(dict, eval(open(fname_indexer).read()))


def get_query(path="query.txt"):
    return open(path).read()


def create_indexer(dir_docs="docs", fname_indexer="indexer.txt"):
    indexer = defaultdict(dict)
    for fname in os.listdir(dir_docs):
        path = dir_docs+"\\"+fname
        add(indexer, path)
    try:
        f = open(fname_indexer, "w")
        f.write(repr(dict(indexer)))
        f.close()
    except:
        print("we have a trouble")


def find(word, indexer):
    word_n = get_normal_form(word)
    return {} if word_n not in indexer else indexer[word_n]


def find_doc(word, indexer):
    return find(word, indexer).keys()


def search(query, indexer):
    query_ = query.lower()
    pos, n = 0, len(query_)
    res = None
    pos_and = query_[pos:].find('and')
    if pos_and > -1:
        while pos < n:
            if pos_and == -1:
                pos_and = n
            if res is None:
                res = relevant(query_[pos: pos_and], indexer)
            else:
                res = relevant(query_[pos: pos_and], indexer, dict.fromkeys(res, None))
            if len(res) == 0:
                return res
            pos = pos_and + 3
            pos_and = query_.find('and', pos)

    if pos > 0:
        return res

    while pos < n:
        pos_or = query_.find('or', pos)
        if pos_or == -1:
            pos_or = n
        res_ = relevant(query_[pos: pos_or], indexer)
        if res is None:
            res = res_
        else:
            res |= res_
        pos = pos_or + 2
    return res


def get_query_words(query):
    tokens = query.split()
    words = []
    direction, N = "BOTH", 1
    for token in tokens:
        if token[0] == '/':
            N = abs(int(token[1:]))
            direction = "BOTH"
            if token[1] == '+':
                direction = "RIGHT"
            if token[0] == '-':
                direction = "LEFT"
        else:
            words.append(Word(get_normal_form(token), N, direction))
    return words


def find_all_pos(indexer, word, list_pos=None):
    if list_pos is None:
        list_pos = dict.fromkeys(indexer[word.word].keys(), None)
    d = indexer[word.word]
    res = {}
    for path in list_pos:
        if path not in d:
            continue
        if path not in res:
            res[path] = set()
        for j in d[path]:
            if list_pos[path] is None:
                res[path].add(j)
                continue
            if word.direction != "LEFT":
                for i in list_pos[path]:
                    if i < j <= i+word.N:
                        res[path].add(j)
            if word.direction != "RIGHT":
                for i in list_pos[path]:
                    if i-word.N <= j < i:
                        res[path].add(j)

    return res


def relevant(query, indexer, list_pos=None):
    query_words = get_query_words(query)
    for word in query_words:
        list_pos = find_all_pos(indexer, word, list_pos)
        if len(list_pos) == 0:
            break
    return set(list_pos.keys())


def main():
    create_indexer(dir_docs="docs")
    indexer = get_indexer()
    query = get_query(path="query.txt")
    print(search(query, indexer))

main()