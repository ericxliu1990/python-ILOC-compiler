"""
"""
from Instruction import *

NO_NEXT_USE = -1
PHYSICAL_REG = {"vr_name" : None, "nextuse": None}
MEMERY_STACK_ADD = 1000

class ILOCAllocator():
	"""docstring for Allocator"""

	def __init__(self, instruction_list, source_reg_num):
		self.instruction_list = instruction_list
		self.source_reg_num = source_reg_num
		#used for find live ranges()
		self.sr_to_vr_dict = dict()
		self.last_used_dict = dict()
		self.vr_index = 0
		self.max_live = 0
		#used for local allocating
		self.physical_regs = dict()
		self.free_pr_list = list()
		#used for spilling
		self.address_count = 0
		#used for special spilling
		self.instruction_counter = 0

	def find_live_ranges(self):
		for a_instruction in reversed(self.instruction_list):
			self._update(a_instruction.op_three, a_instruction.index)
			if self._is_register(a_instruction.op_three) and a_instruction.op_three["source"] :
				del self.sr_to_vr_dict[a_instruction.op_three["source"]]
				del self.last_used_dict[a_instruction.op_three["source"]]
			self._update(a_instruction.op_one, a_instruction.index)
			self._update(a_instruction.op_two, a_instruction.index)
			#maintain max_live 
			self.max_live = max(self.max_live, len(self.sr_to_vr_dict))
			# print "sr_to_vr" + str(self.sr_to_vr_dict)
			# print "LU" + str(self.last_used_dict)

	def local_allocate(self):
		self._init_pyhscial_regs()
		for a_instruction in self.instruction_list:
			op_one = a_instruction.op_one
			op_two = a_instruction.op_two
			op_three = a_instruction.op_three

			print "---------------------------------------"
			print a_instruction.get_str( "virtual") 

			if self._is_register(op_one):
				a_instruction.set_op_value("op_one", self._ensure(op_one["virtual"]), "physical")
			if self._is_register(op_two):
				a_instruction.set_op_value("op_two", self._ensure(op_two["virtual"]),  "physical")
			if self._is_register(op_one) and op_one["nextuse"] == NO_NEXT_USE:
				self._free(a_instruction.op_one["physical"])
			if self._is_register(op_two) and op_two["nextuse"] == NO_NEXT_USE:
				self._free(a_instruction.op_two["physical"])
			if self._is_register(op_three):
				a_instruction.set_op_value("op_three", self._allocate(a_instruction.op_three["virtual"]),  "physical")
			if self._is_register(op_one) and op_one["nextuse"]:
				self.physical_regs[op_one["physical"]]["nextuse"] = op_one["nextuse"]
			if self._is_register(op_two) and op_two["nextuse"]:
				self.physical_regs[op_two["physical"]]["nextuse"] = op_two["nextuse"]
			if self._is_register(op_three) and op_three["virtual"]:
				self.physical_regs[a_instruction.op_three["physical"]]["nextuse"] = op_three["nextuse"]

	def special_local_allocate(self):
		SPECIAL_OP_MAP = {"op_one": "pr0", "op_two": "pr1", "op_three" : "pr1"}

		for a_instruction in list(self.instruction_list):
			self.instruction_counter += 1
			for op_type in ["op_one", "op_two", "op_three"]:
				if self._is_register(a_instruction.get_op(op_type)):
					self._special_spill(a_instruction, op_type)
					a_instruction.set_op_value(op_type, SPECIAL_OP_MAP[op_type], "physical")

			print "***********************"
			print a_instruction.get_index(), a_instruction.get_str("virtual")

	def _update(self, operation, index):
		if operation:
			if self._is_immediate(operation):
				return
			if self._is_register(operation):
				if not operation["source"] in self.sr_to_vr_dict:
					self.sr_to_vr_dict[operation["source"]] = "r" + str(self.vr_index)
					self.last_used_dict[operation["source"]] = NO_NEXT_USE
					self.vr_index += 1
				operation["virtual"] = self.sr_to_vr_dict[operation["source"]]
				operation["nextuse"] = self.last_used_dict[operation["source"]]
				self.last_used_dict[operation["source"]] = index
			return Exception

	def _init_pyhscial_regs(self):
		for index in xrange(self.source_reg_num):
			physical_reg_name = "pr" + str(index)
			self.physical_regs[physical_reg_name]  = PHYSICAL_REG
			self.free_pr_list.append(physical_reg_name)

	def _ensure(self, virtual_reg):
		#need linear search, really slow
		for physical_reg_name, physical_reg in self.physical_regs.items():
			if physical_reg["vr_name"] == virtual_reg:
				print "find physical_reg_name", physical_reg_name
				return physical_reg_name
		return  self._allocate(virtual_reg)

	def  _special_spill(self, a_instruction, op_type):
		""""""
		def get_new_reg(physical_value):
			return {"physical" : "r" + str(physical_value)}

		if op_type == "op_one" or op_type == "op_three":
			one_op_three = get_new_reg(0)
		if op_type == "op_two":
			one_op_three = get_new_reg(1)
		virtual_reg = a_instruction.get_op(op_type, "virtual")
		new_instruction_one = Instruction("-", "loadI", InstructionType.two_op, 
						op_one =  self._special_allocate(virtual_reg), 
						op_three = one_op_three)
		print "new instruction 1:" , new_instruction_one.get_str()
		if op_type == "op_one":
			opcode = "load"
			two_op_one = get_new_reg(0)
			two_op_three = get_new_reg(0)
		if op_type =="op_two":
			opcode = "load"
			two_op_one =get_new_reg(1)
			two_op_three = get_new_reg(1)
		if op_type =="op_three":
			opcode  = "store"
			two_op_one =get_new_reg(1)
			two_op_three = get_new_reg(0)
		new_instruction_two = Instruction("-", opcode,  InstructionType.two_op, 
						op_one = two_op_one, 
						op_three = two_op_three)
		print "new instruction 2: ", new_instruction_two.get_str()
		if op_type =="op_one" or op_type =="op_two":
			self.instruction_list.insert(self.instruction_counter -1, new_instruction_one)
			self.instruction_counter += 1
			self.instruction_list.insert(self.instruction_counter -1, new_instruction_two)
			self.instruction_counter += 1
		if op_type =="op_three":
			self.instruction_list.insert(self.instruction_counter, new_instruction_one)
			self.instruction_counter += 1
			self.instruction_list.insert(self.instruction_counter, new_instruction_two)
			self.instruction_counter += 1
		self.print_instruction()

	def _special_allocate(self, virtual_reg):
		for memory_name, memory in self.physical_regs.items():
			if memory["vr_name"] == virtual_reg:
				print "find physical_reg_name", memory_name
				return memory_name

		new_memery = {"vr_name" : virtual_reg}
		new_memery_name = self._get_new_address()
		self.physical_regs[new_memery_name] = new_memery
		print virtual_reg, self.physical_regs
		return new_memery_name

	def _allocate(self, virtual_reg):
		if len(self.free_pr_list) > 0:
			print virtual_reg, self.free_pr_list
			new_physical_reg = {"vr_name" : virtual_reg, "nextuse": None}
			new_physical_reg_name = self.free_pr_list.pop()
			self.physical_regs[new_physical_reg_name] = new_physical_reg
			return new_physical_reg_name
		else:
			physical_reg = self._spill(virtual_reg)

	def _free(self, physical_reg_name):
		print "--->physical_regs:" , self.physical_regs
		self.physical_regs[physical_reg_name] = PHYSICAL_REG
		self.free_pr_list.append(physical_reg_name)
		print "<----physical_regs:" , self.physical_regs

	def _spill(self, virtual_reg):
		print self.physical_regs
		raise Exception

	def _get_new_address(self):
		self.address_count += 1
		return MEMERY_STACK_ADD + 4 * self.address_count

	def _is_register(self, a_register):
		return isinstance(a_register, dict)

	def _is_immediate(self, immediate):
		return isinstance(immediate, basestring)

	def _is_memory(self, memery):
		if not memery:
			return False
		if not menery.find("m") == -1:
			return True
		return False

	def print_instruction(self):
		for a_instruction in self.instruction_list:
			print a_instruction.get_index(), ": ", a_instruction.get_str()