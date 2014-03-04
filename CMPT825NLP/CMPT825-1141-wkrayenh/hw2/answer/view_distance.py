missing_char="_"

def distance(target, source, insertcost, deletecost, replacecost):
	n = len(target)+1 #i is the index for target
	m = len(source)+1 #j is the index for source
	# set up dist and initialize values
	dist = [ [0 for j in range(m)] for i in range(n) ]
	alignment=[[dict(source="",target="") for j in range(m)] for i in range(n)]
	#alignment=[]
	#for j in range(m):
		#alignment.append([[dict(source="",target="")] for j in range(m)]
	for i in range(1,n):
		dist[i][0] = dist[i-1][0] + insertcost
		alignment[i][0]["target"]+=target[i-1]
		alignment[i][0]["source"]+=missing_char
	for j in range(1,m):
		dist[0][j] = dist[0][j-1] + deletecost
		alignment[0][j]["target"]+=missing_char
		alignment[0][j]["source"]+=source[j-1]
	# align source and target strings
	for j in range(1,m):
		for i in range(1,n): 
			inscost = insertcost + dist[i-1][j]
			insStr = dict(source="",target="")
			insStr["target"]=alignment[i-1][j]["target"]+target[i-1]
			insStr["source"]=alignment[i-1][j]["source"]+missing_char
			
			delcost = deletecost + dist[i][j-1]
			delStr = dict(source="",target="")
			delStr["target"]=alignment[i][j-1]["target"]+missing_char
			delStr["source"]=alignment[i][j-1]["source"]+source[j-1]
			if (source[j-1] == target[i-1]): add = 0
			else: add = replacecost
			substcost = add + dist[i-1][j-1]
			subStr = dict(source="",target="")
			subStr["target"]=alignment[i-1][j-1]["target"]+target[i-1]
			subStr["source"]=alignment[i-1][j-1]["source"]+source[j-1]
			costs=(inscost, delcost, substcost)
			strings=(insStr, delStr, subStr)
			ind=sorted(range(3),key=lambda x: costs[x])
			dist[i][j] = costs[ind[0]]
			alignment[i][j] = strings[ind[0]]
			assert dist[i][j] == min(inscost, delcost, substcost)
	def make_compact(source_string,target_string):
		s=[c for c in source_string]
		t=[c for c in target_string]
		assert len(s)==len(t)
		def get_char(ls):
			assert len(ls)==2
			if ls[0] == '_':
				assert ls[1]!='_'
				return ls[1]
			else:
				assert ls[1]=='_'
				return ls[0]
		def compactify(i):
			assert len(s)>i+1
			if "_" in s[i:i+2] and "_" in t[i:i+2]:
				s[i:i+2] = [get_char(s[i:i+2])]
				t[i:i+2] = [get_char(t[i:i+2])]
		for i in range(len(s)):
			if len(s)>i+1:
				compactify(i)
		assert len(s)==len(t)
		return ''.join(s),''.join(t)
	ss,ts=make_compact(alignment[n-1][m-1]["source"],alignment[n-1][m-1]["target"])
	output("levenshtein distance = " + str(int(dist[n-1][m-1])),'b')
	output(" ".join(ss),'b')
	al=[" "]*len(ss)
	for i in range(len(ss)):
		if ts[i]==ss[i]:
			al[i]="|"
	output(" ".join(al),'b')
	output(" ".join(ts),'b')
	# return min edit distance
	return dist[n-1][m-1]

def output(string,types='f'):
	assert types in ['p','f','b']
	if types in ['p','b']:
		print string
	if types in ['f','b']:
		with open('dist.txt','a') as f:
			f.write(string+'\n')

if __name__=="__main__":
	from sys import argv
	import sys
	output('\n'+''.join('-'*20+'\n'),'f')
	output('argv: '+str(argv)+'\n','f')
	output('\n'+''.join('-'*5+'\n'),'f')
	if len(argv) > 2: 
		ld=distance(argv[1], argv[2], 1.0000001, 1.0000001, 2)
		ld=1
		output("levenshtein distance returned =" + str(ld) + "\n",'f')
