import sys
import traceback

def norecurse(f):
     def func(*args, **kwargs):
         if len([l[2] for l in traceback.extract_stack() if l[2] == f.func_name]) > 0:
             raise Exception, 'recursion detected'
         return f(*args, **kwargs)
     print >>sys.stderr, "no recursion detected"
     return func

@norecurse
def virahanka(n):
    # change this function to be non-recursive by using a table to store computed results for each n
    vhs=[]
    vhs.append([""])
    vhs.append(["S"])
    for i in range(2,n+1):
        s = ["S" + prosody for prosody in vhs[-1]]
        l = ["L" + prosody for prosody in vhs[-2]]
        vhs.append(s+l)
    if not (n==0 or n==len(vhs)-1):
        raise ValueError("n is "+str(n)+" and len(vhs)-1 is "+ str(len(vhs)-1))
    return vhs[n]

if __name__ == "__main__":
    import sys
    for num in sys.stdin:
        n = int(num)
        print str(virahanka(n))
