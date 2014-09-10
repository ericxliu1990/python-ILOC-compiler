"""
"""
import re
from ILOC_grammer import *
from Instruction import *

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
		return ILOC_SYNTAX_ERROR % {"filename": self.filename.name, 
						"line_number": self.line_number, 
						"line": self.line}

class ILOCParser():
	"""docstring for Scanner"""
	def __init__(self, source_file):
		self.source_file = source_file
		self.source_line = []
		self.ir_list = []
		self.parser_operation_re =  re.compile(GRAMMER_OPERATION_RE)
		self.parser_comment_re =  re.compile(GRAMMER_COMMENT_RE)

	def scan(self):
		source_text = self.source_file.read()
		self.source_line = source_text.split("\n")
		self.source_file.close()
	
	def parse(self):
		new_line_number = 0
		for line_number, a_line in enumerate(self.source_line):
			#we assume code lines are much greater than empty lines
			if self.parser_operation_re.match(a_line):
				new_line_number += 1
				self._add_ir_list(new_line_number, a_line, line_number)
			elif self.parser_comment_re.match(a_line):
				pass
			else:
				raise ILOCSyntaxError(self.source_file, a_line, line_number)

	def get_ir_list(self):
		return self.ir_list

	def _add_ir_list(self, new_line_number, a_line, line_number):
		#really slow version of implementation,
		#and not clean way to handle three operator instructions
		a_line = a_line.replace(",", "", 1)
		new_line_list = a_line.split()
		new_line_list_len = len(new_line_list)
		if new_line_list_len == 4:
			self.ir_list.append(Instruction(new_line_number, new_line_list[0], 
				InstructionType.two_op,
				op_one = new_line_list[1], 
				op_three = new_line_list[3]))
		elif new_line_list_len == 5:
			self.ir_list.append(Instruction(new_line_number,new_line_list[0], 
				InstructionType.three_op,
				op_one = new_line_list[1], 
				op_two = new_line_list[2], 
				op_three = new_line_list[4]))
		elif new_line_list_len == 2:
			self.ir_list.append(Instruction(new_line_number,new_line_list[0], 
				InstructionType.one_op,
				op_one = new_line_list[1]))
		elif new_line_list_len ==1:
			self.ir_list.append(Instruction(new_line_number,new_line_list[0])), InstructionType.none_op,
		else:
			print new_line_list
			raise ILOCSyntaxError(self.source_file, a_line, line_number)