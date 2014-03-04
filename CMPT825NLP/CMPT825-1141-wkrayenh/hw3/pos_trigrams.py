from nltk.corpus import brown
from itertools import islice
p = [(None, None)] # empty token/tag pair
for sent in islice(brown.tagged_sents(categories='news'), 5):
    # print out the pos tag sequence for this sentence
    print " ".join([t[1] for t in sent]) 
    trigrams = zip(p+p+sent, p+sent+p, sent+p+p)
    for (a,b,c) in trigrams:
        history = (a[1], b[1])
        current_tag = c[1]
        print current_tag, history    # print each trigram
    print
