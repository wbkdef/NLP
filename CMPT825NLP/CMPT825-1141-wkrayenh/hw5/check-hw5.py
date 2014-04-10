"""
Here each group tests single python program which must be named with the group name plus a .py suffix. These programs are executed with the same python interpreter used to run the check program.

Extra options needed to run check-hw5.py:

	-p DIR/PREFIX   prefix for parallel data, e.g. ../hansards when running from answer directory
	-n NUMBER       number of alignments to print, set to 0 to print only accuracy output, set to 1 to debug alignments

"""

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

def align_ops(opts):
    for opt, value in opts:
        if opt == "-p":
            align_opts.train = value
        elif opt == '-n':
            align_opts.n = int(value)

def grade_align(reference, system, output):
    f_data = "%s.%s" % (align_opts.train, align_opts.french)
    e_data = "%s.%s" % (align_opts.train, align_opts.english)
    (size_a, size_s, size_a_and_s, size_a_and_p) = (0.0,0.0,0.0,0.0)
    for (n, (f, e, g, a)) in enumerate(zip(open(f_data), open(e_data), reference, system)):
      fwords = f.strip().split()
      ewords = e.strip().split()

      # check

      size_f = len(fwords)
      size_e = len(ewords)
      try: 
        alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
        for (i,j) in alignment:
          if (i>=size_f or j>size_e):
            sys.stderr.write("WARNING (%s): Sentence %d, point (%d,%d) is not a valid link\n" % (sys.argv[0],n,i,j))
          pass
      except (Exception):
        sys.stderr.write("ERROR (%s) line %d is not formatted correctly:\n  %s" % (sys.argv[0],n,a))
        sys.stderr.write("Lines can contain only tokens \"i-j\", where i and j are integer indexes into the French and English sentences, respectively.\n")
        sys.exit(1)

      # grade

      sure = set([tuple(map(int, x.split("-"))) for x in filter(lambda x: x.find("-") > -1, g.strip().split())])
      possible = set([tuple(map(int, x.split("?"))) for x in filter(lambda x: x.find("?") > -1, g.strip().split())])
      alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
      size_a += len(alignment)
      size_s += len(sure)
      size_a_and_s += len(alignment & sure)
      size_a_and_p += len(alignment & possible) + len(alignment & sure)
      if (n<align_opts.n):
        output.write("  Alignment %i  KEY: ( ) = guessed, * = sure, ? = possible\n" % n)
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
    print >>sys.stderr, "Precision = %f\nRecall = %f\nAER = %f\n" % (precision, recall, aer)
    return True

checks = {
    "align": { 'stdout': grade_align },
}

check.check_all(checks, extra_ops=('p:n:', align_ops), extra_usage=__doc__.rstrip('\n\r'))

