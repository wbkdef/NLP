"""
Here each group tests single python program which must be named with the group name plus a .py suffix. These programs are executed with the same python interpreter used to run the check program.
"""

import check
import os
import difflib
import re

def edgews_normalize(*parts):
    def filter(x):
        x = [l.strip() for l in x]
        return [l + '\n' for l in x if l != '']
    return [filter(x) for x in parts]

def diff_almost_exact(a, b, output):
    a, b = edgews_normalize(a, b)
    if a != b:
            output.write("Diff in output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

def diff_almost_exact_uniq(a, b, output):
    return diff_almost_exact(set(a), set(b), output)

def diff_unordered(a, b, output):
    a, b = edgews_normalize(a, b)
    a, b = sorted(a), sorted(b)
    if a != b:
            output.write("Diff in sorted output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

#def diff_report_scores(a, b, output):
#    a, b = edgews_normalize(a, b)
#    for (i,j) in zip(a, b):
#        x = i.rstrip().split(':')
#        y = j.rstrip().split(':')
#        (k1, v1) = (" ".join(x[:-1]), x[-1])
#        (k2, v2) = (" ".join(y[:-1]), y[-1])
#        print "%s: reference:%s yours:%s difference: %lf" % (k1, v1, v2, float(v2)-float(v1))
#    return True

# This is for rechunk and the numeric hw3 problems. It treats the input as a list of key:value pairs,
# validates the input, and compares the input and gold as dictionaries.

def diff_report_scores(a, b, output):
    def makekey(a, b):
        return a + "_" + b
    def parse(lines, source_name, expected_keys):
        pairs = [line.split(':') for line in lines]
        lookup = {}
        for i, pair in enumerate(pairs, 1):
            try:
                if len(pair) != 3: 
                    raise ValueError
                key = makekey(pair[0], pair[1])
                if key in lookup:
                    print >> output, "warning: duplicate key \"%s\" on line %i of %s" % (key, i, source_name)
                lookup[key] = float(pair[2])
            except ValueError, e:
                print >> output, "line %i of %s is does not have the correct format" % (i, source_name)
                raise e
        return [makekey(pair[0], pair[1]) for pair in pairs], lookup

    try:
        a_order, a_lookup = parse(a, "reference", None)
        b_order, b_lookup = parse(b, "output", a_order)
    except ValueError, e:
        return False

    ok = True
    for key in b_order:
        if key not in a_lookup:
            print >> output, "unknown key '%s' in output" % (key)
            ok = False
    if ok:
        for key in a_order:
            if key in b_lookup:
                v1, v2 = a_lookup[key], b_lookup[key]
                print "%s: reference:%s yours:%s difference: %lf" % (key, v1, v2, float(v2)-float(v1))
            else:
                print >> output, "key '%s' is missing from output" % (key)
                ok = False
    return ok

checks = {
#    "emailextract": { 'stdout': diff_almost_exact },
#    "browntags": { 'stdout': diff_almost_exact },
#    "freqnp": { 'stdout': diff_almost_exact },
#    "brown_tagger": { 'stdout': diff_report_scores },
    "smoothing": { 'stdout': diff_report_scores },
#    "hmm_decipher": { 'file_check': ["hmmplot.png", os.path.exists] },
}

check.check_all(checks, extra_usage=__doc__.rstrip('\n\r'))
