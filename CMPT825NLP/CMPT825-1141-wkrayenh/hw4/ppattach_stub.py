import nltk
from nltk.corpus import ppattach
import sys

class DefaultClassifier(nltk.classify.ClassifierI):
    default_label = 'N'
    def classify(self, featureset):
        return self.default_label

def default_feature(item):
    return {'None': None}

train_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('training') ]
dev_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('devset') ]
test_set = [ (default_feature(item), item.attachment) for item in ppattach.attachments('test') ]
classifier = DefaultClassifier()
devacc = nltk.classify.accuracy(classifier, dev_set)
testacc = nltk.classify.accuracy(classifier, test_set)
print "prep:dev:%lf" % (devacc)
print "prep:test:%lf" % (testacc)
