"""

"""
class Instruction(object):
	"""represent an instruction"""
	def __init__(self, index, opcode, instruction_type, op_one = None, op_two = None, op_three = None, next_op = None):
		super(Instruction, self).__init__()
		self.index = index
		self.type = instruction_type
		self.opcode = opcode
		self.op_one = {"source" : op_one, "virtual" : None, "physical" : None, "nexttuse" : None}
		self.op_two = {"source" : op_two, "virtual" : None, "physical" : None, "nextuse": None}
		self.op_three = {"source" : op_three, "virtual" : None, "physical" : None, "nextuse": None}
		#no need for next_op as there's no flow control instruction
		#self.next_op = next_op
	def __str__(self, str_type = "virtual"):
		if self.type == InstructionType.three_op:
			return "%(opcode)s %(op_one)s, %(op_two)s => %(op_three)s" % {
									"opcode" : self.opcode,
									"op_one" : self.op_one[str_type], 
									"op_two" : self.op_two[str_type],
									"op_three" : self.op_three[str_type]}
		if self.type == InstructionType.two_op:
			return "%(opcode)s %(op_one)s => %(op_three)s" % {
									"opcode" : self.opcode,
									"op_one" : self.op_one[str_type], 
									"op_three" : self.op_three[str_type]}
		if self.type == InstructionType.store:
			return "%(opcode)s %(op_one)s => %(op_two)s" % {
									"opcode" : self.opcode,
									"op_one" : self.op_one[str_type], 
									"op_two" : self.op_two[str_type]}
		if self.type == InstructionType.one_op:
			return "%(opcode)s %(op_one)s" % {
							"opcode" : self.opcode,
							"op_one" : self.op_one[str_type]}
		if self.type == InstructionType.none_op:
			return "%(opcode)s" % {"opcode" : self.opcode}
		print self.type

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