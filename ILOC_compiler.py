#!/usr/bin/python
import argparse
from ILOC_parser import *
from ILOC_register_allocator import *

COMPILER_DESCRIPTION = """
A ILOC compiler for COMP 412 Lab1.
"""
K_HELP = """
a integer k specifies the number of registers that the allocator should assume 
are available on the target machine, starting from r0.
"""
FILENAME_HELP = """
This argument specifies	 the name of he input file. It is a valid Linux pathname 
elative to the current working directory.
"""
FILENAME_ERROR = """
usage: ILOC_compiler.py [-h] k filename
ILOC_compiler.py: %s
"""
def arguments_parse():
	argument_parser = argparse.ArgumentParser(description = COMPILER_DESCRIPTION)
	argument_parser.add_argument("k", help = K_HELP, type = int)
	argument_parser.add_argument("filename", help = FILENAME_HELP, type = file)
	try:
		arguments = argument_parser.parse_args()
	except Exception, IOError:
		print  FILENAME_ERROR % IOError
		exit() 
	# print arguments.k, arguments.filename
	return arguments

def main():
	arguments = arguments_parse()
	parser = ILOCParser(arguments.filename)
	parser.scan()
	try:
		parser.parse()
	except ILOCSyntaxError, iloc_exception:
		print iloc_exception
		exit()
	#except Exception, other_exception:
	#	raise other_exception
	allocator = ILOCAllocator(parser.ir_list, arguments.k)
	allocator.find_live_ranges()
	print map(str, parser.ir_list)

if __name__ == '__main__':
	main()