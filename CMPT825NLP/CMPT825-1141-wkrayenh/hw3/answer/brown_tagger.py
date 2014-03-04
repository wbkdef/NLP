
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

    if method == 'default':
        # default tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'regexp':
        # regexp tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'lookup':
        # lookup tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'simple_backoff':
        # simple backoff tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'unigram':
        # unigram backoff tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'bigram':
        # bigram backoff tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'trigram':
        # trigram backoff tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    else:
        print >>sys.stderr, "unknown method"
        sys.exit(2)

