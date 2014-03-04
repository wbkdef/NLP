import sys
from itertools import islice
from nltk.corpus import brown
news_text = brown.words(categories='science_fiction')
max = 50000
count = 0
output = ''
syms = {}
for charList in map(list, news_text):
    charList = map(lambda z: z.lower(), charList)
    charList = filter(lambda z: z.isalpha(), charList)
    charList = map(lambda z: str(ord(z) - 96), charList)
    charList.append(str(27))
    nchars = len(charList)
    if nchars == 0: continue
    for char in charList:
        if not syms.has_key(char): syms[char] = True
    if count == max: break
    if count > 0: output += ' '
    if count + nchars > max:
        output += " ".join(charList[:max - count])
        count += max - count
        break
    else:
        output += " ".join(charList)
        count += nchars

print "T=", count
print output
print >>sys.stderr, "number of symbols = %d" % len(syms.keys())
