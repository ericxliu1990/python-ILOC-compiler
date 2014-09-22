"""
"""
from Instruction import *
from itertools import count
NO_NEXT_USE = -1
NO_REMAT = -1

class ILOCAllocator():
	"""docstring for Allocator"""

	def __init__(self, instruction_list, physcial_reg_num):
		self.instruction_list = instruction_list
		self.physcial_reg_num = physcial_reg_num
		self.instruction_counter = 0
		self.need_spill = None
		self.spill_reg = physcial_reg_num - 1
		self.rematerializable_value = False

	def find_live_ranges(self):
		""""""
		sr_to_vr_dict = dict()
		last_used_dict = dict()
		vr_index = list()
		def update(operation, index):
			if operation:
				if self._is_immediate(operation):
					return
				if self._is_register(operation):
					if not operation["source"] in sr_to_vr_dict:
						sr_to_vr_dict[operation["source"]] = "vr" + str(len(vr_index))
						last_used_dict[operation["source"]] = NO_NEXT_USE
						vr_index.append(None)
					operation["virtual"] = sr_to_vr_dict[operation["source"]]
					operation["nextuse"] = last_used_dict[operation["source"]]
					last_used_dict[operation["source"]] = index
				return Exception

		max_live = 0
		for an_instruction in reversed(self.instruction_list):
			update(an_instruction.op_three, an_instruction.index)
			if self._is_register(an_instruction.op_three) and an_instruction.op_three["source"] :
				del sr_to_vr_dict[an_instruction.op_three["source"]]
				del last_used_dict[an_instruction.op_three["source"]]
			update(an_instruction.op_one, an_instruction.index)
			update(an_instruction.op_two, an_instruction.index)
			#maintain max_live 
			max_live = max(max_live, len(sr_to_vr_dict))
			if max_live > self.physcial_reg_num:
				self.need_spill = True
			else:
				self.need_spill =False
			# print "sr_to_vr" + str(sr_to_vr_dict)
			# print "LU" + str(last_used_dict)

	def local_allocate(self, memory_address):
		""""""
		physical_regs = dict()
		virtual_to_physical = dict()
		virtual_to_memory = dict()
		virtual_to_remat = dict()
		free_pr_list = list()
		address_counter = list()
		
		def get_new_address():
			""""""
			address_counter.append(None)
			return str(memory_address + 4 * len(address_counter))

		def get_new_physical_reg(virtual_reg = None):
			""""""
			return {"vr_name" : virtual_reg, "nextuse": None}

		def init_pyhscial_regs():
			""""""
			if self.need_spill ==  False:
				physical_reg_num = self.physcial_reg_num
			else:
				physical_reg_num = self.physcial_reg_num - 1
			for index in reversed(xrange(physical_reg_num)):
				physical_reg_name = "r" + str(index)
				physical_regs[physical_reg_name]  = get_new_physical_reg()
				free_pr_list.append(physical_reg_name)

		def insert_spill_instructions(insert_type, physical_reg, memory_name):
			""""""
			def get_new_reg(physical_value):
				""""""
				if isinstance(physical_value, basestring):
					return {"physical" : physical_value}
				else:
					return {"physical" : "r" + str(physical_value)}

			if insert_type == "spill" or insert_type == "restore":
				if insert_type == "spill" :
					opcode = "store"
					two_op_one = get_new_reg(physical_reg)
					one_op_three = two_op_three = get_new_reg(self.spill_reg)
				elif insert_type == "restore":
					opcode = "load"
					two_op_one = one_op_three = get_new_reg(self.spill_reg)
					two_op_three =  get_new_reg(physical_reg)
				else:
					raise Exception

				new_instruction_one = Instruction("-", "loadI", InstructionType.two_op, 
								op_one =  memory_name, 
								op_three = one_op_three)
				new_instruction_two = Instruction("-", opcode,  InstructionType.two_op, 
							op_one = two_op_one, 
							op_three = two_op_three)
				self._instruction_list_insert(self.instruction_counter -1, new_instruction_one)
				self._instruction_list_insert(self.instruction_counter -1, new_instruction_two)
			if insert_type == "remat_restore":
				one_op_three =  get_new_reg(physical_reg)
				new_instruction_one = Instruction("-", "loadI", InstructionType.two_op, 
								op_one =  memory_name, 
								op_three = one_op_three)
				self._instruction_list_insert(self.instruction_counter -1, new_instruction_one)

		def ensure(virtual_reg):
			""""""
			if virtual_reg in virtual_to_physical:
				return virtual_to_physical[virtual_reg]

			# if virtual_reg in virtual_to_remat:
			# 	if not virtual_to_remat[virtual_reg] == NO_REMAT:
			# 		physical_reg = allocate(virtual_reg)
			# 		insert_spill_instructions("remat_restore", physical_reg, virtual_to_remat[virtual_reg])
			# 		return physical_reg
					
			if virtual_reg in virtual_to_memory:
				physical_reg = allocate(virtual_reg)
				insert_spill_instructions("restore", physical_reg, virtual_to_memory[virtual_reg])
				return physical_reg

			return  allocate(virtual_reg)

		def allocate(virtual_reg):
			""""""
			# print "physical_regs: ", physical_regs, free_pr_list
			# print "memory_to_virtual: ", memory_to_virtual
			# if not self.rematerializable_value ==NO_REMAT:
			# 	virtual_to_remat[virtual_reg] =  self.rematerializable_value
			# 	print "//", virtual_to_remat

			if len(free_pr_list) == 0:
				new_physical_reg_name = spill(virtual_reg)
			new_physical_reg_name = free_pr_list.pop()
			physical_regs[new_physical_reg_name] = get_new_physical_reg(virtual_reg)
			virtual_to_physical[virtual_reg] = new_physical_reg_name
			return new_physical_reg_name

		def free(physical_reg_name):
			""""""
			del virtual_to_physical[physical_regs[physical_reg_name]["vr_name"]]
			physical_regs[physical_reg_name] = get_new_physical_reg()
			free_pr_list.append(physical_reg_name)

		def spill(virtual_reg):
			""""""
			def get_max_next_use():
				""""""
				# a really slow implementatiom
				max_next_use = 0
				max_physical_reg_name = None
				max_virtual_reg_name = None
				for physical_reg_name, a_physical_reg in physical_regs.items():
					if a_physical_reg["nextuse"] > max_next_use:
						max_next_use = a_physical_reg["nextuse"]
						max_physical_reg_name = physical_reg_name
						max_virtual_reg_name = a_physical_reg["vr_name"]
				return max_physical_reg_name, max_virtual_reg_name

			def is_clean_value(virtual_reg):
				""""""
				return virtual_reg in virtual_to_memory

			if self.need_spill == False:
				raise Exception
			#can be changed to a clever way
			max_physical_reg_name, max_virtual_reg_name = get_max_next_use()
			free(max_physical_reg_name)
			new_memory_name = get_new_address()

			if not is_clean_value(max_virtual_reg_name): # and self.rematerializable_value == NO_REMAT:
				# if max_virtual_reg_name in virtual_to_remat:
				# 	del virtual_to_remat[max_virtual_reg_name]
				# 	print "// in spill :", virtual_to_remat
				virtual_to_memory[max_virtual_reg_name] = new_memory_name
				insert_spill_instructions("spill", max_physical_reg_name, new_memory_name)
			# print "not enough physical_regs spill %(max_next_use)s to memory_to_virtual %(new_memory_name)s" % {
			# 									"max_next_use" : max_physical_reg_name, 
			# 									"new_memory_name" : new_memory_name}
			# print physical_regs

		init_pyhscial_regs()
		for an_instruction in list(self.instruction_list):
			self.instruction_counter += 1
			op_one = an_instruction.op_one
			op_two = an_instruction.op_two
			op_three = an_instruction.op_three

			# print "---------------------------------------"
			# print an_instruction.get_str( "virtual") 
			self.rematerializable_value = self._rematerialization_check(an_instruction)
			if self._is_register(op_one):
				an_instruction.set_op_value("op_one", ensure(op_one["virtual"]), "physical")
			if self._is_register(op_two):
				an_instruction.set_op_value("op_two", ensure(op_two["virtual"]),  "physical")
			if self._is_register(op_one) and op_one["nextuse"] == NO_NEXT_USE:
				free(an_instruction.op_one["physical"])
			if self._is_register(op_two) and op_two["nextuse"] == NO_NEXT_USE:
				free(an_instruction.op_two["physical"])
			if self._is_register(op_three):
				an_instruction.set_op_value("op_three", allocate(an_instruction.op_three["virtual"]),  "physical")
			if self._is_register(op_one) and op_one["nextuse"]:
				physical_regs[op_one["physical"]]["nextuse"] = op_one["nextuse"]
			if self._is_register(op_two) and op_two["nextuse"]:
				physical_regs[op_two["physical"]]["nextuse"] = op_two["nextuse"]
			if self._is_register(op_three) and op_three["virtual"]:
				physical_regs[an_instruction.op_three["physical"]]["nextuse"] = op_three["nextuse"]

	def special_local_allocate(self, memory_address):
		""""""
		SPECIAL_OP_MAP = {"op_one": "r0", "op_two": "r1", "op_three" : "r1"}
		memory_to_virtual = dict()
		virtual_to_memory = dict()
		virtual_to_remat = dict()
		address_counter = list()
		
		def get_new_address():
			""""""
			address_counter.append(None)
			return memory_address + 4 * len(address_counter)

		def special_allocate(virtual_reg):
			""""""
			if virtual_reg in virtual_to_memory:
				return virtual_to_memory[virtual_reg]

			# if virtual_reg in virtual_to_remat:
			# 	return virtual_to_remat[virtual_reg]
			new_memory_name = get_new_address()
			virtual_to_memory[virtual_reg] = new_memory_name
			#print virtual_reg, a_memory
			return new_memory_name

		def special_spill(an_instruction, op_type):
			""""""
			def get_new_reg(physical_value):
				""""""
				return {"physical" : "r" + str(physical_value)}

			if op_type == "op_one" or op_type == "op_three":
				one_op_three = get_new_reg(0)
			if op_type == "op_two":
				one_op_three = get_new_reg(1)
			virtual_reg = an_instruction.get_op(op_type, "virtual")
			new_instruction_one = Instruction("-", "loadI", InstructionType.two_op, 
							op_one =  special_allocate(virtual_reg), 
							op_three = one_op_three)
			#print "new instruction 1:" , new_instruction_one.get_str()
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
			# print "new instruction 2: ", new_instruction_two.get_str()
			if op_type =="op_one" or op_type =="op_two":
				self._instruction_list_insert(self.instruction_counter -1, new_instruction_one)
				self._instruction_list_insert(self.instruction_counter -1, new_instruction_two)

			if op_type =="op_three":
				self._instruction_list_insert(self.instruction_counter, new_instruction_one)
				self._instruction_list_insert(self.instruction_counter, new_instruction_two)
			# self.print_instruction()
			if op_type =="op_three":
				if virtual_reg in virtual_to_remat:
					del virtual_to_remat[virtual_reg]
					# print "// in spill: ", virtual_to_remat

		for an_instruction in list(self.instruction_list):
			self.instruction_counter += 1
			# self.rematerializable_value = self._rematerialization_check(an_instruction)
			# if not self.rematerializable_value == NO_REMAT:
			# 	virtual_to_remat[an_instruction.op_three["virtual"]] = self.rematerializable_value
				# print "//", virtual_to_remat
			for op_type in ["op_one", "op_two", "op_three"]:
				if self._is_register(an_instruction.get_op(op_type)):
					# if self.rematerializable_value == NO_REMAT:
					special_spill(an_instruction, op_type)
					an_instruction.set_op_value(op_type, SPECIAL_OP_MAP[op_type], "physical")

			# print "***********************"
			# print an_instruction.get_index(), an_instruction.get_str("virtual")

	def _rematerialization_check(self, an_instruction):
			""""""
			if an_instruction.opcode == "loadI":
				return an_instruction.op_one
			else:
				return NO_REMAT

	def _instruction_list_insert(self, position, new_instruction):
		self.instruction_list.insert(position, new_instruction)
		self.instruction_counter += 1

	def _is_register(self, a_register):
		""""""
		return isinstance(a_register, dict)

	def _is_immediate(self, immediate):
		""""""
		return isinstance(immediate, basestring)

	def print_instruction(self):
		for an_instruction in self.instruction_list:
			print an_instruction.get_str()