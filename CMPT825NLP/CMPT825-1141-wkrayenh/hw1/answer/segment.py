import math
import sys, codecs
import random

OOV_score=-20 #Represents a log probability
digit_bonus=0 #Represents a log probability bonus for numbers
smoothing_constant=1
longest_word=6

class candidate_split:
	def __init__(self,string_to_split):
		self.string_to_split=string_to_split
		self.split_points=[0]
	def factory_copy_and_add_split(old_candidate_split,new_split_point):
		new_cand_split=candidate_split(old_candidate_split.string_to_split)
		new_cand_split.split_points=old_candidate_split.split_points[:] #Make a copy
		assert new_split_point>new_cand_split.split_points[-1]
		new_cand_split.split_points.append(new_split_point)
		return new_cand_split
	def get_last_split_point(self):
		return self.split_points[-1]
	def get_words(self):
		return [self.string_to_split[self.split_points[i]:self.split_points[i+1]] for i in range(len(self.split_points)-1)]
	def get_log_prob(self):
		score=0
		for word in self.get_words():
			if word in log_prob_dict:
				score+=log_prob_dict[word]
			else:
				score+=OOV_score*len(word)-1
				if word.isdigit():
					score+=digit_bonus*len(word)
					pass
		return score
	def get_string(self):
		return " ".join(self.get_words())

def print_cand_split_list(csl,title):
	print title
	for cs in csl:
		#print "{:<25} log-likelihood: {}".format(cs.get_string(), cs.get_log_prob())
		print cs.get_string(),"log-likelihood:", cs.get_log_prob()

def get_best_split(string):
	#print "STARTING get_best_split"
	csl=[candidate_split(string)]
	for i in range(1,len(string)+1):
		#print "i =", i,"start"
		cs_new_candidates=[]
		best_score=-1000000
		best_new_cand_ind=-1
		for cs in csl[-longest_word:]:
			#print cs.get_string(), cs.get_log_prob(log_prob_dict)
			cs_new_candidates.append(cs.factory_copy_and_add_split(i))
			if cs_new_candidates[-1].get_log_prob()>best_score:
				best_score=cs_new_candidates[-1].get_log_prob()
				best_new_cand_ind=len(cs_new_candidates)-1
				#print "best_in_now",best_new_cand_ind
		assert best_new_cand_ind >-1
		csl.append(cs_new_candidates[best_new_cand_ind])
		#print_cand_split_list(cs_new_candidates,"New Candidates")
		#print "chosen candidate: ", cs_new_candidates[best_new_cand_ind].get_string()
		#print_cand_split_list(csl,"Dynamic Programming Table")
		#print "i =", i,"end"
	#print "ENDING get_best_split"
	return csl[-1]
			

if __name__ == '__main__':
	if len(sys.argv) > 1:
		old = sys.stdout
		sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
		with open(sys.argv[1]) as f:
			freq_dict={}
			tot_words=0
			for line in f:
				line = line[:-1]
				utf8line = unicode(line, 'utf-8')
				#print utf8line
				splt=utf8line.split()
				freq_dict[splt[1]]=int(splt[0])
				#dict_name[key]=value
				tot_words+=int(splt[0])+smoothing_constant
				#print splt[1]
				#if random.random()<.001:break
		#print "freq dict:", random.sample(freq_dict,50)
		log_prob_dict={}
		#print tot_words
		log_tot_words=math.log(tot_words)
		for key,value in freq_dict.iteritems():
			log_prob_dict[key]=math.log(value)-log_tot_words 
			#print log_prob_dict[key],
		#log_prob_dict={key:math.log(value/tot_words) for key,value in freq_dict.iteritems()}
		for line in sys.stdin:
				line = line[:-1]
				utf8line = unicode(line, 'utf-8')
				best_split=get_best_split(utf8line)
				print best_split.get_string()
				#print "THE ANSWER FOR",utf8line,"IS:",best_split.get_string()
		sys.stdout = old
	else:
		print >>sys.stderr, "usage: python", sys.argv[0], "frequencies < inputfile"

