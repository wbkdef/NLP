
import nltk
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.corpus import brown

def default_tag(tagged_sents):
    tag_fd = FreqDist()
    for sent in tagged_sents:
        for word, postag in sent:
            tag_fd.inc(postag)
    return str(tag_fd.max())

def usage(args):
    if len(args) > 1:
        print >>sys.stderr, "unknown args", args[1:]
    print >>sys.stderr, "usage: %s -h -i trainsection -o testsection -m method" % (args[0])
    print >>sys.stderr, """
    -h help
    -i training section ,e.g. 'news' or 'editorial'
    -o test section ,e.g. 'news' or 'editorial'
    -m method, e.g. 'default', 'regexp', 'lookup', 'simple_backoff', 'unigram', 'bigram', 'trigram'

    Do not type in the single quotes at the command line.
    """
    sys.exit(2)

def print_to_file(s):
    with open('brown_output','a') as f:
        f.write(s) 

if __name__ == '__main__':
    import sys
    import getopt

    try:
        (trainsection, testsection, method) = ('news', 'editorial', 'default')
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:", ["help", "train=", "test=", "method="])
    except getopt.GetoptError:
        usage(sys.argv)
    for o, a in opts:
        if o in ('-h', '--help'): 
            usage([sys.argv[0]])
            sys.exit(0)
        if o in ('-i', '--train'): trainsection = a
        if o in ('-o', '--test'): testsection = a
        if o in ('-m', '--method'): method = a

    train_tagged_sents = brown.tagged_sents(categories=trainsection)
    test_tagged_sents = brown.tagged_sents(categories=testsection)
    train_tagged_words = brown.tagged_words(categories=trainsection)
    test_tagged_words = brown.tagged_words(categories=testsection)
    train_words = brown.words(categories=trainsection)

    print_to_file("\n\nmethod = "+method+"\n")    
    default_tag = default_tag(train_sents)
    default_tagger = nltk.DefaultTagger(default_tag)

    if method == 'default':
        # default tagger
        print_to_file("%s:test:%lf" % (method, default_tagger.evaluate(test_sents)))    
        print "%s:test:%lf" % (method, default_tagger.evaluate(test_sents))
    elif method == 'regexp':
        # regexp tagger
        patterns = [(r'.*ing$', 'VBG'), # gerunds
                    (r'.*ed$', 'VBD'), # simple past
                    (r'.*es$', 'VBZ'), # 3rd singular present
                    (r'.*ould$', 'MD'), # modals
                    (r'.*\'s$', 'NN$'), # possessive nouns
                    (r'.*s$', 'NNS'), # plural nouns
                    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'), # cardinal numbers
                    (r'.*', 'NN') # nouns (default)
                    ]
        tagger=nltk.RegexpTagger(patterns)
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test_sents)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test_sents))
    elif method == 'lookup':
        # lookup tagger
        # print_to_file()    
        fd=nltk.FreqDist(train_words)
        # print fd.keys()[:10]
        cfd=nltk.ConditionalFreqDist(train_tagged_words)
        d={k:cfd[k].max() for k in fd.keys()[:1000]}
        print d
        tagger=nltk.UnigramTagger(model=d)
        print "%s:test:%lf" % (method, tagger.evaluate(test_tagged_sents))
    elif method == 'simple_backoff':
        # simple backoff tagger
        fd=nltk.FreqDist(train_words)
        cfd=nltk.ConditionalFreqDist(train_tagged_words)
        d={k:cfd[k].max() for k in fd.keys()[:1000]}
        tagger=nltk.UnigramTagger(model=d,backoff=default_tagger)
        print "%s:test:%lf" % (method, tagger.evaluate(test_tagged_sents))
    elif method == 'unigram':
        # unigram backoff tagger
        tagger=nltk.UnigramTagger(train_tagged_sents,backoff=default_tagger)
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test_sents)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test_sents))
    elif method == 'bigram':
        # bigram backoff tagger
        #COMPLETE THIS!
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test_sents)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test_sents))
    elif method == 'trigram':
        # trigram backoff tagger
        #COMPLETE THIS!
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test_sents)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test_sents))
    else:
        print >>sys.stderr, "unknown method"
        sys.exit(2)

