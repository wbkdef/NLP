from nltk.corpus import brown
from itertools import islice
p = [(None, None)] # empty token/tag pair 
for sent in islice(brown.tagged_sents(categories='news'), 5):
    # print out the pos tag sequence for this sentence
    print " ".join([t[1] for t in sent]) 
    bigrams = zip(p+sent, sent+p)
    for (a,b) in bigrams:
        history = a[1]
        current_tag = b[1]
        print current_tag, history    # print each bigram
    print
