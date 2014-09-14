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
MEMERY_STACK_ADD = 2000
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
def save_file(filename, code_list):
	write_file = open(str(filename).split(".")[0] + "_allocated.i", "w")
	for a_instruction in code_list:
		write_file.write(a_instruction.get_str() + "\n")
	write_file.close()

def main():
	arguments = arguments_parse()
	parser = ILOCParser(arguments.filename)
	parser.scan()
	try:
		parser.parse()
	except ILOCSyntaxError, iloc_exception:
		print iloc_exception
		exit()
	allocator = ILOCAllocator(parser.get_instruction_list(), arguments.k)
	allocator.find_live_ranges()
	if arguments.k >2:
		allocator.local_allocate()
	if arguments.k ==2:
		allocator.special_local_allocate(MEMERY_STACK_ADD) 
	allocator.print_instruction()
	# save_file(arguments.filename.name, allocator.instruction_list)

if __name__ == '__main__':
	main()