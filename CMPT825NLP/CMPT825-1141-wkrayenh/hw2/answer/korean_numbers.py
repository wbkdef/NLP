import sys

def nums(n,side,hack=False):
	#print "nums(",n,")"
	if not isinstance(n, int):
		raise ValueError("The input to 'num' function should be an integer!")
	elif n == 0:
		return ""
	elif n > 999999999 or n<1:
		raise ValueError('n should be a positive integer between 1 and 999,999,999')
	powers=(8,4,3,2,1)
	names=(" eok "," man "," cheon "," baek "," sib ")
	#print n, side, hack
	for pow,name in zip(powers,names):
		if n>=10**pow:
			if pow == 8 and n%(10**pow)<10**5:
				return nums(int(n/10**pow),"left")+name+nums(n%(10**pow),"right",True)
			else:
				return nums(int(n/10**pow),"left",hack)+name+nums(n%(10**pow),"right")
	assert 0<n<10
	digits=[" il "," i "," sam "," sa "," o "," yuk "," chil "," pal "," gu "]
	if side == "left" and not hack:
		digits[0]=""
	else:
		assert hack or side == "right"
	return digits[n-1]

def num(n):
	return nums(n,"left")

if __name__=="__main__":
	from sys import argv
	#print argv
	if len(argv) == 2: 
		x=int(argv[1])
		#print x
		#print x*2
		A=num(x)
		#print A
		print A.strip().replace('  ',' ')
	else:
		x=int(sys.stdin.read())
		A=num(x)
		#print x
		print A.strip().replace('  ',' ')
	#else:
		#print "usage: provide one input argument that is a positive integer between 1 and 999,999,999"
