import nltk
from nltk.corpus import ppattach
import sys

def get_feats(ppa):
    # print ppa
    try:
        feats={('V','N1','P','N2'):(ppa.verb,ppa.noun1,ppa.prep,ppa.noun2)}
    except:
    	print ppa
    	return None
    for i in range(4):
        for key in feats.keys(): #Make a copy of keys, b/c adding new elements to the dictionary!
            value=feats[key]
            lk=list(key)
            lk[i]=""
            tk=tuple(lk)
            lv=list(value)
            lv[i]=""
            tv=tuple(lv)
            assert tk not in feats
            feats[tk]=tv
    return feats
def get_list_of_feats_lables(data):
#     data_tuples=[(ppa,ppa.attachment) for ppa in data]
#     feat_lable_tuples=nltk.classify.apply_features(get_feats,data)
    feat_lable_tuples=[(get_feats(ppa),ppa.attachment) for ppa in data]
    return feat_lable_tuples

# print "Train"
train_set = [ (get_feats(item), item.attachment) for item in ppattach.attachments('training') ]
# print "Dev"
dev_set = [ (get_feats(item), item.attachment) for item in ppattach.attachments('devset') ]
# print "Test"
test_set = [ (get_feats(item), item.attachment) for item in ppattach.attachments('test') ]
# print "Done"

# train_feats_labels=get_list_of_feats_lables(train_set)
# dev_feats_labels=get_list_of_feats_lables(dev_set)
# test_feats_labels=get_list_of_feats_lables(test_set)

classifier=nltk.NaiveBayesClassifier.train(train_set) #Not sure how to smooth this!

devacc = nltk.classify.accuracy(classifier, dev_set)
testacc = nltk.classify.accuracy(classifier, test_set)

# print train[0]
# print train_feats_labels[0]
# nltk.classify.accuracy(classifier,dev_feats_labels)

print "all:dev:%lf" % (devacc)
print "all:test:%lf" % (testacc)