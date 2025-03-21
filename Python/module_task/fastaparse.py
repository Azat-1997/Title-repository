#!/usr/bin/python

default_mass_table = {'G':57.021464,'A':71.037114,'S':87.032028,
'P':97.052764,'V':99.068414,'T':101.047678,'C':103.009184,
'I':113.084064,'L':113.084064,'N':114.042927,
'D':115.026943,'Q':128.058578,'K':128.094963,
'E':129.042593,'M':131.040485,'H':137.058912,
'F':147.068414,'R':156.101111,'Y':163.063329,
'W':186.079313}

rna_codon_standart = {frozenset(["GGU", "GGC", "GGA", "GGG"]):"G",
                frozenset(["GCU", "GCC", "GCA", "GCG"]):"A",
                frozenset(["GUU", "GUC", "GUA", "GUG"]):"V",
                frozenset(["AUU", "AUC", "AUA"]):"I",
                frozenset(["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"]):"L",
                frozenset(["CCU", "CCC", "CCA", "CCG"]):"P",
                frozenset(["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"]):"S",
                frozenset(["ACU", "ACC", "ACA", "ACG"]):"T",
                frozenset(["UGU", "UGC"]):"C",
                frozenset(["AUG"]):"M",
                frozenset(["GAU", "GAC"]):"D",
                frozenset(["AAU", "AAC"]):"N",
                frozenset(["GAA", "GAG"]):"E",
                frozenset(["CAA", "CAG"]):"Q",
                frozenset(["AAA", "AAG"]):"K",
                frozenset(["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"]):"R",
                frozenset(["CAU", "CAC"]):"H",
                frozenset(["UUU", "UUC"]):"F",
                frozenset(["UAU", "UAC"]):"Y",
                frozenset(["UGG"]):"W",
    frozenset(["UAA","UAG","UGA"]):"-"}


def dna2rna(dna_seq:str) -> str:
# This  extra-function for symplifying work with dna and rna strings
	
	rna = []
	for nucleotide in dna_seq.upper():
		if nucleotide == "T":
			rna.append("U")
		else:
			rna.append(nucleotide)

	return "".join(rna)


def orf(rna_seq:str,start="AUG",end={"UAA","UGA","UAG"},too_short=0) -> list:
# too_short is treshold for filtration by length
	lst_orfs = []
# This function returns all possible orfs.
# In some cases several stop-codons read as aminoacid-coding (selenocysteine or tryptophane)
	size = len(rna_seq)
	for shift in range(3):
		# We can have start from index which don't divide by 3
		# So we note possible shifts: 0, 1 and 2 nucleotides 
		for i in range(shift,size,3):
			if rna_seq[i:i+3] == start:
				orf_seq = [rna_seq[i:i+3]]
				#  Search start-codon and start aggregate codons
				# initialize orf_seq as list for one orf
				for j in range(i+3,size,3):
					orf_seq.append(rna_seq[j:j+3])	
					if rna_seq[j:j+3] in end:
						final = "".join(orf_seq)
						# join triplets in one entire string
						lst_orfs.append(final)
						break
						# break the inner cycle but keep going the outer cycle.
						# It's needs to take all possible orfs from this rna.
	if too_short:
	# if too_short equals to zero we just skip that step in other case make a filtration
		return filter(lambda x: len(x) > too_short, lst_orfs)

	return lst_orfs				



def parse(filename) -> dict:

	fasta_dict = dict()

# return key - Name of sequence (strings with '>')
# The value is sequence itself
	with open(filename) as file:

		for line in file:
			if line[0] == '>':
			# if we get new string with '>', we change key
				key = line.strip()
				if line not in fasta_dict.keys():
					fasta_dict[key] = []
				else:
					raise KeyError("ID should be uniqe")
			else:
				fasta_dict[key].append(line.strip())

	for ID, sequnce in fasta_dict.items():
		# replace list to full-string in value
		fasta_dict[ID] = "".join(sequnce)

	return fasta_dict


def translate(rna_seq:str,codon_table=rna_codon_standart) -> str:
# This function just translate. Be careful: it doesn't search orf before
# You should make orf before, if you want relevant result
# Additionally, you can change codon_table: it's probably needs to work with non-standart genetic codes
# E.g. selenocysteine, pyrolisine and genome of mitochondria or plastids
	prot = []
	size = len(rna_seq)   

	for i in range(0,size,3):

		for key,value in codon_table.items():

			if rna_seq[i:i+3].upper() in key:

				prot.append(value)
	return "".join(prot)
    

def calc_mass(prot_seq:str,mass_table=default_mass_table) -> float:
# You can change mass_table by another if you want.
	mass = 0

	for sym in prot_seq.upper():

		mass += mass_table[sym]

	return mass



