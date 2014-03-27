WHAT I DID

1) I loaded parsed sentences from nltk and converted to chomsky normal form:
	treebank.parsed_sents()
	nltk.treetransforms.chomsky_normal_form(tree)
2) I extracted all rules from this treebank and converted them to the form needed for the grammar file (adding counts to the left of each rule).  I prepended all non-terminals by "gr_", so that there would be no overlap with the S2 rules.
3) For the terminal rules, I 
	a) got rid of all rules that mapped to words outside of the vocabulary.
	b) I added counts of 100 times the number of times each rule occurred to the left of each rule
	c) For all words inside the vocabulary I also added 10 more counts of the tag NLTK prefers for that word (hence all words in the vocabulary could be produced).
	d) The words were initially grouped by Anoop, and those that weren't grouped I grouped using NLTK-generated tags.  I used this to "transfer counts" within these groups as a form of smoothing (to deal with data sparsity).
4) I then determined the set of all acceptable non-terminal rules as follows:
	a) First initialize the set of "acceptable outputs" as the set of left hand sides of the terminal rules.
	b) Initialize the set of "acceptable non terminal rules" as the empty set.
	c) For all non-terminal rules whose children are all "acceptable outputs":
		i) Add those rules' left hand sides to the "acceptable outputs"
		ii) Add those rules to the "acceptable non terminal rules"
	d) Repeat c) until no more rules are added.
5) I added all the terminal rules to the end of the vocabulary file
6) I added all the "acceptable non terminal rules" to the S1 file, deleting the grammar that was already there and connecting S1 to gr_S.
7) I got rid of some '#' symbols in the rules that were messing up the sentence generator.