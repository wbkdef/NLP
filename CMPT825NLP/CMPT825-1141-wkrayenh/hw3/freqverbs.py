from nltk.corpus import brown
from nltk.probability import FreqDist
fd = FreqDist()
for sent in brown.tagged_sents():
    for word, tag in sent:
        if tag[:2] == 'VB':
            fd.inc(word+"/"+tag)
print fd.keys()[:20]
