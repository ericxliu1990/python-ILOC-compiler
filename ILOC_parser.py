"""
"""
import re
from ILOC_grammer import *

ILOC_SYNTAX_ERROR = """File %(filename)s, in line %(line_number)s:
	%(line)s
ILOCSyntaxError: invalid syntax"""

class ILOCSyntaxError(Exception):
	"""docstring for ILOCSyntaxError"""
	def __init__(self, filename, line, line_number):
		self.filename = filename
		self.line = line
		self.line_number = line_number
	def  __str__(self):
		return ILOC_SYNTAX_ERROR % {"filename": self.filename.name, "line_number": self.line_number, "line": self.line}

class ILOCParser():
	"""docstring for Scanner"""
	def __init__(self, source_file):
		self.source_file = source_file
		self.source_line = []
		self.parser_re = GRAMMER_RE

	def scan(self):
		source_text = self.source_file.read()
		self.source_line = source_text.split("\n")
		self.source_file.close()
	
	def parse(self):
		parser_re = re.compile(self.parser_re)
		for line_number, a_line in enumerate(self.source_line):
			if not parser_re.match(a_line):
				raise ILOCSyntaxError(self.source_file, a_line, line_number)
