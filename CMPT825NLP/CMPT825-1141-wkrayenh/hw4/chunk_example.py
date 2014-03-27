
from nltk import chunk
tagged_text = """
The/DT market/NN for/IN system-management/NN software/NN for/IN 
Digital/NNP 's/POS hardware/NN is/VBZ fragmented/JJ enough/RB 
that/IN a/DT giant/NN such/JJ as/IN Computer/NNP Associates/NNPS 
should/MD do/VB well/RB there/RB ./.
"""
input = chunk.tagstr2tree(tagged_text)
print input

cp = chunk.RegexpParser("NP: {<DT><NN>}")
print cp.parse(input)

