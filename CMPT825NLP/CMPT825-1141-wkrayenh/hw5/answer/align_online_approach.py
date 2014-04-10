#!/usr/bin/env python
from __future__ import division
"""
    python align.py [options]

    options are:

	-p DIR/PREFIX   prefix for parallel data, Defaults: DIR=../ PREFIX=../hansards when running from answer directory
	-n NUMBER       number of training examples to use, Default: n = sys.maxint
"""
#Code Graveyard
            # from nltk.probability import *
            # bigramFreq[history].inc(current_tag)
            # bigram = ConditionalProbDist(bigramFreq, MLEProbDist)
            # unigramFreq = FreqDist((x[1] for x in train_words_tags))
            # unigram = MLEProbDist(unigramFreq)

import optparse

import sys
import os.path
from collections import defaultdict
import random
import operator

optparser = optparse.OptionParser()
optparser.add_option("-p", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

if not ( os.path.isfile(f_data) and os.path.isfile(e_data) ):
    print >>sys.stderr, __doc__.strip('\n\r')
    sys.exit(1)

'''GET DATA'''
sys.stderr.write("Training with Bruce's Algorithm...\n")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]


'''GET SET OF WORDS'''
french_words=set()
english_words=set()
for f,e in bitext:
  french_words|=set(f)
  english_words|=set(e)
ne=len(english_words)
nf=len(french_words)
print "len(french_words)",len(french_words)
print "len(english_words)", len(english_words)
base_num=10.0 #Ten initial counts from each french word to each English word
cf={f:base_num*ne*1.0 for f in french_words}
# cf_decay={f:base_num*ne for f in french_words}
cf_mult_inc_buildup={f:0.0 for f in french_words} #When this exceeds 1, decrement it and increase the new counts added.
cf_add_mult={f:1.0 for f in french_words}
cf_mult_factor=1.01
cfe=defaultdict(lambda : defaultdict(lambda : base_num))
# sys.exit(0)

'''LEARN ALIGNMENTS'''
#Get Vocabulary, and initialize probabilities uniformly?  Or better yet, just add some smoothing in, and then all can be initialized to 0, I think.
# f -> e, where an f can be aligned with more than one e in a sentence (but not vice versa)
random.shuffle(bitext)
for i in xrange(20):
  def prob_e_given_f_fcn(f,e):
    if e not in cfe[f]:
      return base_num/cf[f]
    return cfe[f][e]/cf[f]
  for (n,(f_sent, e_sent)) in enumerate(bitext):
    if n%100==0: sys.stderr.write("-")
    for e in e_sent:
      tot=0
      for f in f_sent:
        tot+=prob_e_given_f_fcn(f,e)
      for f in f_sent:
        rhs=prob_e_given_f_fcn(f,e)/tot
        if rhs==0:
          print >>sys.stderr, "cfe[f]",cfe[f]
          print >>sys.stderr, "rhs==0"
          print >>sys.stderr, "e",e, "f",f
          print >>sys.stderr, "tot",tot, "prob_e_given_f_fcn(f,e)",prob_e_given_f_fcn(f,e)
          assert False
        cfe[f][e]+=rhs*cf_add_mult[f]      
        cf[f]+=rhs*cf_add_mult[f]
        cf_mult_inc_buildup[f]+=rhs
        if cf_mult_inc_buildup[f]>1:
          cf_mult_inc_buildup[f]-=1
          cf_add_mult[f]*=cf_mult_factor

  '''Print Stuff'''
  f_sorted=sorted(cf.iteritems(),key=operator.itemgetter(1), reverse=True)[:100]
  # french_words_to_print=random.choice(f_sorted)[0]
  # print set(x[0] for x in random.sample(f_sorted,10))
  french_words_to_print=set(['de'])#'fait', 'la', ')', 'jeunes', 'scrutin', ',', 'un', 'sont', 'nous', 'sant\xc3\xa9']) #**********************
  for f in french_words_to_print:
    print >> sys.stderr, "For french word:", f
    l=sorted(cfe[f].iteritems(),key=operator.itemgetter(1),reverse=True)
    for e, count in l[:5]:
      print >>sys.stderr, "{:<20}{:<20}{:<20}".format(e,count,prob_e_given_f_fcn(f,e))
    print >>sys.stderr, "tot count", sum(x[1] for x in l), "should be less than", cf[f], "tot prob", sum(prob_e_given_f_fcn(f,e) for e in english_words)

sys.exit(1)
# pfe=defaultdict(lambda : defaultdict(float))
# for f in cfe:
#   for e, prob in cfe[f].iteritems():
#     if cf[f] <= 0:
#       print >>sys.stderr, "The prob is 0 for f", f
#       print >>sys.stderr, "key", key
#       print >>sys.stderr, "cfe", cfe
#       assert False
#     pfe[f][e]=cfe[f][e]/cf[f]





def get_new_probabilities(prob_e_given_f_fcn,french_words_to_print=None): #The prob_e_given_f_fcn takes parameters (f,e)
  cfe=defaultdict(lambda : defaultdict(float))
  cf=defaultdict(float)
  for (n,(f_sent, e_sent)) in enumerate(bitext):
    if n%100==0: sys.stderr.write("-")
    for e in e_sent:
      tot=0
      for f in f_sent:
        tot+=prob_e_given_f_fcn(f,e)
      for f in f_sent:
        rhs=prob_e_given_f_fcn(f,e)/tot
        if rhs==0:
          print >>sys.stderr, "cfe[f]",cfe[f]
          print >>sys.stderr, "rhs==0"
          print >>sys.stderr, "e",e, "f",f
          print >>sys.stderr, "tot",tot, "prob_e_given_f_fcn(f,e)",prob_e_given_f_fcn(f,e)
          assert False
        cfe[f][e]+=rhs
        cf[f]+=rhs
  pfe=defaultdict(lambda : defaultdict(float))
  for f in cfe:
    for e, prob in cfe[f].iteritems():
      if cf[f] <= 0:
        print >>sys.stderr, "The prob is 0 for f", f
        print >>sys.stderr, "key", key
        print >>sys.stderr, "cfe", cfe
        assert False
      pfe[f][e]=cfe[f][e]/cf[f]


  f=french_word_to_print
  print >>sys.stderr, "For french word:",f
  l=sorted(cfe[f].iteritems(),key=operator.itemgetter(1),reverse=True)
  for e, count in l[:5]:
    print >>sys.stderr, "{:<20}{:<20}{:<20}".format(e,count,pfe[f][e])
  print >>sys.stderr, "tot count", sum(x[1] for x in l), "should equal", cf[f], "tot prob", sum(pfe[f][e] for e in pfe[f])
  # print >>sys.stderr, "cfe[f]",cfe[f]
  # print >>sys.stderr, "list(cfe[f].iteritems()).sorted(key=operator.itemgetter(1),reverse=True)",sorted(cfe[f].iteritems(),key=operator.itemgetter(1),reverse=True)
  # print >>sys.stderr, "pfe[f]",pfe[f]  
  return pfe, cf

sys.stderr.write("Training initial probabilities")
pfe,cf=get_new_probabilities(lambda x,y:1)
f_sorted=sorted(cf.iteritems(),key=operator.itemgetter(1), reverse=True)[:100]
f_word_to_follow=random.choice(f_sorted)[0]
# f_word_to_follow='avec' #**********************
def get_prob(f,e):
  return pfe[f][e]
for i in xrange(10):
  sys.stderr.write("Training round "+str(i))
  pfe,cf=get_new_probabilities(get_prob,f_word_to_follow)

sys.exit(1)

'''OUTPUT ALIGNMENTS'''
for (f, e) in bitext:
  # sys.stderr.write("\nFRENCH "+str(f))
  # sys.stderr.write("\nENGLISH "+str(e))
  for (i, f_i) in enumerate(f):
    best_prob_so_far=0
    alignment=-1
    for (j, e_j) in enumerate(e):
      p=pfe[f_i][e_j]
      if p>best_prob_so_far:
        best_prob_so_far=p
        alignment=j
    sys.stdout.write("%i-%i " % (i,alignment))
    # sys.stderr.write("a:{}f:{},e:{}".format(alignment,f_i,e[alignment]))
  # sys.exit(1)
  sys.stdout.write("\n")
  # sys.exit(1)

sys.exit(0)

#Implement Training
  #***Have to figure out which way are translating...



sys.stderr.write("Training with Dice's coefficient...")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
print >>sys.stderr, "hi"
# sys.exit(0)
print 'bitext[0]',bitext[0]
sys.exit(1)
f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count = defaultdict(int)
for (n, (f, e)) in enumerate(bitext):
  for f_i in set(f):
    f_count[f_i] += 1
    for e_j in set(e):
      fe_count[(f_i,e_j)] += 1
  for e_j in set(e):
    e_count[e_j] += 1
  if n % 500 == 0:
    sys.stderr.write(".")

dice = defaultdict(int)
for (k, (f_i, e_j)) in enumerate(fe_count.keys()):
  dice[(f_i,e_j)] = 2.0 * fe_count[(f_i, e_j)] / (f_count[f_i] + e_count[e_j])
  if k % 5000 == 0:
    sys.stderr.write(".")
sys.stderr.write("\n")

for (f, e) in bitext:
  for (i, f_i) in enumerate(f): 
    for (j, e_j) in enumerate(e):
      if dice[(f_i,e_j)] >= opts.threshold:
        sys.stdout.write("%i-%i " % (i,j))
  sys.stdout.write("\n")
