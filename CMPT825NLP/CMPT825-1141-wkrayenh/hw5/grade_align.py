import check
import os
import difflib
import re
import sys

class align_options:
    def __init__(self):
        self.train = "../hansards"
        self.n = sys.maxint
        self.english = 'e'
        self.french = 'f'

align_opts = align_options()

def grade_align(reference, system, output):
    f_data = "%s.%s" % (align_opts.train, align_opts.french)
    e_data = "%s.%s" % (align_opts.train, align_opts.english)
    (size_a, size_s, size_a_and_s, size_a_and_p) = (0.0,0.0,0.0,0.0)
    for (i, (f, e, g, a)) in enumerate(zip(open(f_data), open(e_data), reference, system)):
      fwords = f.strip().split()
      ewords = e.strip().split()
      sure = set([tuple(map(int, x.split("-"))) for x in filter(lambda x: x.find("-") > -1, g.strip().split())])
      possible = set([tuple(map(int, x.split("?"))) for x in filter(lambda x: x.find("?") > -1, g.strip().split())])
      alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
      size_a += len(alignment)
      size_s += len(sure)
      size_a_and_s += len(alignment & sure)
      size_a_and_p += len(alignment & possible) + len(alignment & sure)
      if (i<align_opts.n):
        output.write("  Alignment %i  KEY: ( ) = guessed, * = sure, ? = possible\n" % i)
        output.write("  ")
        for j in ewords:
          output.write("---")
        output.write("\n")
        for (i, f_i) in enumerate(fwords):
          output.write(" |")
          for (j, _) in enumerate(ewords):
            (left,right) = ("(",")") if (i,j) in alignment else (" "," ")
            point = "*" if (i,j) in sure else "?" if (i,j) in possible else " "
            output.write("%s%s%s" % (left,point,right))
          output.write(" | %s\n" % f_i)
        output.write("  ")
        for j in ewords:
          output.write("---")
        output.write("\n")
        for k in range(max(map(len, ewords))):
          output.write("  ")
          for word in ewords:
            letter = word[k] if len(word) > k else " "
            output.write(" %s " % letter)
          output.write("\n")
        output.write("\n")

    precision = size_a_and_p / size_a
    recall = size_a_and_s / size_s
    aer = 1 - ((size_a_and_s + size_a_and_p) / (size_a + size_s))
    output.write("Precision = %f\nRecall = %f\nAER = %f\n" % (precision, recall, aer))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        with open(sys.argv[1], 'r') as a:
            with open(sys.argv[2], 'r') as b:
                grade_align(list(a), list(b), sys.stdout)
    else:
        print >>sys.stderr, "usage: python", sys.argv[0], "gold output"
