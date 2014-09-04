"""
A file for defining ILOC grammer
"""
grammer_dict = {"one_op" : r"(\s*output\s+\d+\s*)",
		"two_op" : r"(\s*(load|store)\s+r\d+\s*=>\s*r\d*\s*)",
		"special_two_op" : r"(\s*loadI\s+\d+\s*=>\s*r\d*\s*)",
		"three_op" : r"(\s*(add|sub|mult|lshift|rshift)\s+r\d+\s*,\s*r\d+\s*=>\s*r\d*\s*)",\
		"comment" : r"(\s*//)",
		"whitespace" : r"(\s*)"
		}

GRAMMER_RE = "" 
for operation in grammer_dict:
	GRAMMER_RE += grammer_dict.get(operation) + "|"

GRAMMER_RE = GRAMMER_RE[ : -1]
# print GRAMMER_RE