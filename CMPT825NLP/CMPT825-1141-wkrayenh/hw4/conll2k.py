from nltk import chunk
from nltk.corpus import conll2000

cp = chunk.RegexpParser("NP: {<DT><NN>}")
print chunk.accuracy(cp, conll2000.chunked_sents('test.txt', chunk_types=('NP',)))

gold_tree = conll2000.chunked_sents('train.txt', chunk_types=('NP',))[1]
print gold_tree
print cp.parse(gold_tree.flatten())

