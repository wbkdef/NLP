from __future__ import division
from nltk.corpus import brown
from nltk.probability import *
from itertools import islice
from math import pow, exp
from numpy import log2

_NINF = float('-1e300') # log probability value for log2(0.0) = Inf

def crossEntropy(Wt, Pt):
    return -(Pt/Wt)

def perplexity(H):
    try: val = pow(2,H)
    except OverflowError: return 'Inf'
    return "%lf" % (val)

def logsum(values):
    sum = 0.0
    for i in values:
        if i == _NINF: return _NINF
        sum += i
    if sum < _NINF: return _NINF
    return sum

def do_train(tagged_sents):
    Wt = 0.0
    bigramFreq = ConditionalFreqDist()
    p = [(None, None)] # empty token/tag pair 
    for sent in tagged_sents:
        Wt += len(sent) 
        bigrams = zip(p+sent, sent+p)
        for (a,b) in bigrams:
            history = a[1]
            current_tag = b[1]
            bigramFreq[history].inc(current_tag)
    return bigramFreq

def compute_perplexity(bigramProb, tagged_sents):
    Wt = 0
    Pt = []
    p = [(None, None)] # empty token/tag pair 
    for sent in tagged_sents:
        bigrams = zip(p+sent, sent+p)
        for (a,b) in bigrams:
            Wt += 1
            history = a[1]
            current_tag = b[1]
            logprob = None
            if bigramProb[history].prob(current_tag) > 0.0:
                logprob = log2(bigramProb[history].prob(current_tag))
            else:
                logprob = _NINF
            Pt.append(logprob)
    H = crossEntropy(Wt, logsum(Pt))
    print >>sys.stderr, "Wt =", Wt, "Pt =", logsum(Pt), "cross entropy =",  H, "perplexity =", perplexity(H)
    return perplexity(H)

def usage(args):
    if len(args) > 1:
        print >>sys.stderr, "unknown args", args[1:]
    print >>sys.stderr, "usage: %s -h -i trainsection -o testsection -m method" % (args[0])
    print >>sys.stderr, """
    -h help
    -i training section ,e.g. 'news' or 'editorial'
    -o test section ,e.g. 'news' or 'editorial'
    -m method, e.g. 'no_smoothing', 'interpolation', 'add_one'
    -l lambda_vector, e.g. "0.5:0.3:0.2" for values of \lambda_1, \lambda_2 and \lambda_3. 
        It must have 3 elements and sum to 1.0 (only used for interpolation)

    Do not type in the single quotes at the command line.
    """
    sys.exit(2)

if __name__ == '__main__':
    import sys 
    import getopt

    try:
        (trainsection, testsection, method, lambda_vector) = ('news', 'editorial', 'default', [0.5,0.3,0.2])
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:l:", ["help", "train=", "test=", "method=", "lambda_vector="])
    except getopt.GetoptError:
        usage(sys.argv)
    for o, a in opts:
        if o in ('-h', '--help'): usage([sys.argv[0]])
        if o in ('-i', '--train'): trainsection = a 
        if o in ('-o', '--test'): testsection = a 
        if o in ('-m', '--method'): method = a 
        if o in ('-l', '--lambda'): lambda_vector = map(float,a.split(':'))

    if len(lambda_vector) < 3:
        print >>sys.stderr, "error: lambda vector should have three elements"
        sys.exit(2)
    if sum(lambda_vector) != 1.0:
        print >>sys.stderr, "error: lambda vector should sum to one"
        sys.exit(2)
    train = brown.tagged_sents(categories=trainsection)
    test = islice(brown.tagged_sents(categories=testsection), 300)
    #test = brown.tagged_sents(categories=testsection)

    bigramFreq = do_train(train)

    # use the maximum likelihood estimate MLEProbDist to create 
    # a probability distribution from the observed frequencies
    bigram = ConditionalProbDist(bigramFreq, MLEProbDist) 

    if method == 'no_smoothing':
        print "%s:%s:%s" % (method, 'train', compute_perplexity(bigram, train))
        print "%s:%s:%s" % (method, 'test', compute_perplexity(bigram, test))
    elif method == 'interpolation':
        print "%s:%s:%s" % (method, 'train', compute_perplexity(bigram, train))
        print "%s:%s:%s" % (method, 'test', compute_perplexity(bigram, test))
    elif method == 'add_one':
    	bigram = ConditionalProbDist(bigramFreq, LaplaceProbDist)
        print "%s:%s:%s" % (method, 'train', compute_perplexity(bigram, train))
        print "%s:%s:%s" % (method, 'test', compute_perplexity(bigram, test))
    elif method == 'interpolation_add_one':
        print "%s:%s:%s" % (method, 'train', compute_perplexity(bigram, train))
        print "%s:%s:%s" % (method, 'test', compute_perplexity(bigram, test))
    else:
        print >>sys.stderr, "unknown method"
        sys.exit(2)
