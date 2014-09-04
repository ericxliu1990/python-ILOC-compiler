#!/usr/bin/python
import argparse

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
if __name__ == "__main__":
	argument_parser = argparse.ArgumentParser(description = COMPILER_DESCRIPTION)
	argument_parser.add_argument("k", help = K_HELP)
	argument_parser.add_argument("filename" help = FILENAME_HELP)
	argument_parser.parse_args()
