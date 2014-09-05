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
		#normally line number start on 1
		self.line_number = line_number + 1
	def  __str__(self):
		return ILOC_SYNTAX_ERROR % {"filename": self.filename.name, "line_number": self.line_number, "line": self.line}

class ILOCParser():
	"""docstring for Scanner"""
	def __init__(self, source_file):
		self.source_file = source_file
		self.source_line = []
		self.parser_operation_re =  re.compile(GRAMMER_OPERATION_RE)
		self.parser_comment_re =  re.compile(GRAMMER_COMMENT_RE)

	def scan(self):
		source_text = self.source_file.read()
		self.source_line = source_text.split("\n")
		self.source_file.close()
	
	def parse(self):
		# for line_number, a_line in enumerate(self.source_line):
		line_number = 0
		for a_line in self.source_line:
			#we assume code lines are much greater than empty lines
			if self.parser_operation_re.match(a_line):
				self._convert_to_list(a_line)
			elif self.parser_comment_re.match(a_line):
				pass
			else:
				raise ILOCSyntaxError(self.source_file, a_line, line_number)

	def _convert_to_list(self):
		pass
