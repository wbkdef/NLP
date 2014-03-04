
import nltk
from nltk.probability import FreqDist, ConditionalFreqDist, ProbDist


#def default_tag(tagged_sents):
tag_fd = FreqDist()
postags=[3,4,5,3,2,5,6,8,65,5,3,3,5,6,7,3]
for postag in postags:
	tag_fd.inc(postag)
print tag_fd
print ProbDist(tag_fd)




