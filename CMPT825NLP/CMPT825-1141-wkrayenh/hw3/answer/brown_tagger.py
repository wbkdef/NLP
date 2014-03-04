
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
        if o in ('-h', '--help'): usage([sys.argv[0]])
        if o in ('-i', '--train'): trainsection = a
        if o in ('-o', '--test'): testsection = a
        if o in ('-m', '--method'): method = a

    train = brown.tagged_sents(categories=trainsection)
    test = brown.tagged_sents(categories=testsection)

    print_to_file("\n\nmethod = "+method+"\n")    

    if method == 'default':
        # default tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print_to_file("%s:test:%lf" % (method, default_tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
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
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    elif method == 'lookup':
        # lookup tagger
        print_to_file(str(train))    
        cfd=nltk.ConditionalFreqDist(train)
        print_to_file(cfd)    
        d=[(k,cfd[k].max()) for k in cfd.keys()[:1000]]
        print_to_file(d)    
        tagger=nltk.UnigramTagger(model=d)
        print_to_file(tagger)    
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    elif method == 'simple_backoff':
        # simple backoff tagger
        #COMPLETE THIS!
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)

        cfd=nltk.ConditionalFreqDist(train)
        d=[(k,cfd[k].max()) for k in cfd.keys()[:1000]]
        tagger=nltk.UnigramTagger(model=d,backoff=default_tagger)
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    elif method == 'unigram':
        # unigram backoff tagger
        #COMPLETE THIS!
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    elif method == 'bigram':
        # bigram backoff tagger
        #COMPLETE THIS!
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    elif method == 'trigram':
        # trigram backoff tagger
        #COMPLETE THIS!
        
        print_to_file("%s:test:%lf" % (method, tagger.evaluate(test)))    
        print "%s:test:%lf" % (method, tagger.evaluate(test))
    else:
        print >>sys.stderr, "unknown method"
        sys.exit(2)

