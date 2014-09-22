"""

"""
class Instruction():
	"""represent an instruction"""
	def __init__(self, index, opcode, instruction_type, op_one = None, op_two = None, op_three = None, next_op = None):
		self.index = index
		self.type = instruction_type
		self.opcode = opcode
		self.op_one = op_one
		self.op_two = op_two
		self.op_three = op_three

	def get_str(self, reg_type = "physical"):
		""""""
		def get_reg_val(op_name, reg_type):
			if isinstance(op_name, dict):
				return op_name[reg_type]
			else:
				return op_name
				
		if self.type == InstructionType.three_op:
			return "%(opcode)s %(op_one)s, %(op_two)s => %(op_three)s" % {
									"opcode" : self.opcode,
									"op_one" : get_reg_val(self.op_one, reg_type), 
									"op_two" : get_reg_val(self.op_two, reg_type),
									"op_three" : get_reg_val(self.op_three, reg_type)}
		if self.type == InstructionType.two_op:
			return "%(opcode)s %(op_one)s => %(op_three)s" % {
									"opcode" : self.opcode,
									"op_one" : get_reg_val(self.op_one, reg_type), 
									"op_three" : get_reg_val(self.op_three, reg_type)}
		if self.type == InstructionType.store:
			return "%(opcode)s %(op_one)s => %(op_two)s" % {
									"opcode" : self.opcode,
									"op_one" : get_reg_val(self.op_one, reg_type), 
									"op_two" : get_reg_val(self.op_two, reg_type)}
		if self.type == InstructionType.one_op:
			return "%(opcode)s %(op_one)s" % {
							"opcode" : self.opcode,
							"op_one" : get_reg_val(self.op_one, reg_type)}
		if self.type == InstructionType.none_op:
			return "%(opcode)s" % {"opcode" : self.opcode}

	def get_index(self):
		""""""
		return self.index

	def set_op_value(self, op_field, value, reg_field = None):
		if not reg_field:
			if op_field == "op_one":
				self.op_one = value
				return
			if op_field == "op_two":
				self.op_two =value
				return
			if op_field == "op_three":
				self.op_three = value
				return
			raise Exception
		else:
			if op_field == "op_one":
				self.op_one[reg_field] = value
				return
			if op_field == "op_two":
				self.op_two[reg_field] =value
				return
			if op_field == "op_three":
				self.op_three[reg_field] = value
				return
			raise Exception

	def get_op(self, op_field, reg_field = None):
		if not reg_field:
			if op_field == "op_one":
				return self.op_one
			if op_field == "op_two":
				return self.op_two
			if op_field == "op_three":
				return self.op_three
			raise Exception
		else:
			if op_field == "op_one":
				return self.op_one[reg_field]
			if op_field == "op_two":
				return self.op_two[reg_field]
			if op_field == "op_three":
				return self.op_three[reg_field]
			raise Exception

#helper function 
#Source: http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
class Enum(set):
	def __getattr__(self, name):
		if name in self:
			return name
		raise AttributeError
		
	def __setattr__(self, name, value):
		raise AttributeError

InstructionType = Enum(["none_op", "one_op", "two_op", "three_op", "store"])