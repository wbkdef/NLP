from __future__ import division

import sys
from collections import defaultdict
import random
import operator


class prob:
  def __init__(self, num_english_words,cf={}, cfe={}, smoothing=0):
    assert cfe.keys()==cf.keys()
    assert smoothing>=0
    assert num_english_words>0
    self.cfe=cfe
    self.cf=cf
    if smoothing<0.001:
      smoothing=0.001
    self.smoothing=smoothing

    self.num_english_words=num_english_words
    self.words_from_smoothing=smoothing*num_english_words
  def get_prob(self,f,e):    
    if f not in self.cf:
      return 1/self.num_english_words
    tot_f=self.cf[f]+self.words_from_smoothing
    tot_fe=self.smoothing
    if e in self.cfe[f]:
      tot_fe+=self.cfe[f][e]
    return tot_fe/tot_f
  def print_french_word_info(self,set_english_words,f=None):
    if f==None:
      f_sorted=sorted(self.cf.iteritems(),key=operator.itemgetter(1), reverse=True)[:random.randint(1,12)**3]
      n,(f,c)=random.choice(list(enumerate(f_sorted)))
    print >>sys.stderr, "For french word:",f,"ranked",n
    l=sorted(self.cfe[f].iteritems(),key=operator.itemgetter(1),reverse=True)
    for e, count in l[:5]:
      print >>sys.stderr, "{:<20}{:<20}{:<20}".format(e,count,self.get_prob(f,e))
    print >>sys.stderr, "tot count", sum(x[1] for x in l), "should equal", self.cf[f], "tot prob", sum(self.get_prob(f,e) for e in set_english_words)



def get_new_probabilities(bitext, prob_e_given_f_obj): #The prob_e_given_f_obj is of the class above
  cfe=defaultdict(lambda : defaultdict(float))
  cf=defaultdict(float)
  '''Get Counts'''
  for (n,(f_sent, e_sent)) in enumerate(bitext):
    if n%100==0: sys.stderr.write("-")
    for e in e_sent:
      tot=0
      for f in f_sent:
        tot+=prob_e_given_f_obj.get_prob(f,e)
      for f in f_sent:
        rhs=prob_e_given_f_obj.get_prob(f,e)/tot
        if rhs==0:
          assert False
          print >>sys.stderr, "cfe[f]",cfe[f]
          print >>sys.stderr, "rhs==0"
          print >>sys.stderr, "e",e, "f",f
          print >>sys.stderr, "tot",tot, "prob_e_given_f_obj.get_prob(f,e)",prob_e_given_f_obj.get_prob(f,e)
        cfe[f][e]+=rhs
        cf[f]+=rhs

  return cf, cfe    