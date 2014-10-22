
from collections import namedtuple


Word = namedtuple("Word", ["word", "N", "direction"])


def get_query_words(query):
    tokens = query.split()
    words = []
    N = 1
    direction = "BOTH"
    for token in tokens:
        if token[0] == '/':
            N = abs(int(token[1:]))
            direction = "BOTH"
            if token[1] == '+':
                direction = "RIGHT"
            if token[0] == '-':
                direction = "LEFT"
        else:
            words.append(Word(token, N, direction))
    return words


def find_all_pos(doc_words, word, list_pos=None):
    n = len(doc_words)
    if list_pos is None:
        list_pos = range(len(doc_words))
    res = set()
    for i in list_pos:
        if word.direction != "LEFT":
            for j in range(i+1, min(n, i+word.N+1)):
                if doc_words[j] == word.word:
                    res.add(j)
        if word.direction != "RIGHT":
            for j in range(max(0, i-word.N-1), i):
                if doc_words[j] == word.word:
                    res.add(j)
    return res


def relevant(doc, query):
    doc_words = doc.split()
    query_words = get_query_words(query)
    list_pos = None
    for word in query_words:
        list_pos = find_all_pos(doc_words, word, list_pos)
        if len(list_pos) == 0:
            break
    if len(list_pos) > 0:
        return True
    else:
        return False


def main():
    doc = "big black big jeep"
    query = "black /+3 jeep"

    print(relevant(doc, query))
    print(relevant(doc, "jeep2"))






main()