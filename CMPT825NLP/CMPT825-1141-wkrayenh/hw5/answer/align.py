#!/usr/bin/env python
from __future__ import division
"""
    python align.py [options]

    options are:

	-p DIR/PREFIX   prefix for parallel data, Defaults: DIR=../ PREFIX=../hansards when running from answer directory
	-n NUMBER       number of training examples to use, Default: n = sys.maxint
"""

import optparse

import sys
import os.path
from collections import defaultdict
import random
import operator
import align_iteration
import itertools as it

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

'''RUN PARAMETERS'''
SMOOTHING=0.01
STARTING_SIZE=50
INCREASE_MULT=1.4
f_word_to_follow='avec'
NUM_FULL_ITERATIONS=2
CONVERT_TO_LOWER_CASE=True

sys.stderr.write("Training with Bruce's Algorithm...\n")
if CONVERT_TO_LOWER_CASE:
  bitext = [[sentence.strip().lower().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
else:
  bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
n=len(bitext)

'''GET SET OF WORDS'''
french_words=set()
english_words=set()
for f,e in bitext:
  french_words|=set(f)
  english_words|=set(e)
ne=len(english_words)
nf=len(french_words)
print >>sys.stderr, "len(french_words)",len(french_words)
print >>sys.stderr, "len(english_words)", len(english_words)

'''LEARN ALIGNMENTS'''
# f -> e, where an f can be aligned with more than one e in a sentence (but not vice versa)


sys.stderr.write("Training initial probabilities")

prob=align_iteration.prob(ne) #Will return uniform probabilities
num_full_its=0
run_size=min(STARTING_SIZE,n)
while num_full_its < NUM_FULL_ITERATIONS:
  if run_size==n:
    bitext_slice=bitext
  else:
    slice_start=random.randint(0,n-run_size-1)
    bitext_slice=it.islice(bitext,slice_start,slice_start+run_size)
  cf,cfe=align_iteration.get_new_probabilities(bitext_slice,prob)
  prob=align_iteration.prob(ne,cf,cfe,SMOOTHING)
  prob.print_french_word_info(english_words)#,f_word_to_follow)
  print >>sys.stderr, "completed run on", run_size, "sentences"
  if run_size < n:
    run_size=min(int(run_size*INCREASE_MULT+1),n)
  else:
    num_full_its+=1
    assert run_size==n
  # break










'''OUTPUT ALIGNMENTS'''
for (f, e) in bitext:
  # sys.stderr.write("\nFRENCH "+str(f))
  # sys.stderr.write("\nENGLISH "+str(e))
  for (i, f_i) in enumerate(f):
    best_prob_so_far=0
    alignment=-1
    for (j, e_j) in enumerate(e):
      p=prob.get_prob(f_i,e_j)
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
