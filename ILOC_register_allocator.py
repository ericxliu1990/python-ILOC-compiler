"""
"""
NO_NEXT_USE = -1
PHYSICAL_REG = {"vr_name" : None, "nextuse": None}

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
		#used for local allocate
		self.physical_reg_stack = dict()
		self.free_pr_list = list()
	def find_live_ranges(self):
		for a_instruction in reversed(self.instruction_list):
			self._update(a_instruction.op_three, a_instruction.index)
			if a_instruction.op_three["source"] :
				del self.sr_to_vr_dict[a_instruction.op_three["source"]]
				del self.last_used_dict[a_instruction.op_three["source"]]
			self._update(a_instruction.op_one, a_instruction.index)
			self._update(a_instruction.op_two, a_instruction.index)
			#maintain max_live 
			self.max_live = max(self.max_live, len(self.sr_to_vr_dict))
			# print "sr_to_vr" + str(self.sr_to_vr_dict)
			# print "LU" + str(self.last_used_dict)

	def local_allocate(self):
		self._init_pyhscial_reg_stack()
		for a_instruction in self.instruction_list:
			op_one = a_instruction.op_one
			op_two = a_instruction.op_two
			op_three = a_instruction.op_three

			print "---------------------------------------"
			print a_instruction #, op_one["nextuse"], op_two["nextuse"], op_three["nextuse"]
			if self._is_register(op_one["virtual"]):
				a_instruction.op_one["physical"] = self._ensure(op_one["virtual"])
				print "**", a_instruction.op_one["physical"]
			if self._is_register(op_two["virtual"]):
				a_instruction.op_two["physical"] = self._ensure(op_two["virtual"])
			if op_one["nextuse"] == NO_NEXT_USE:
				self._free(a_instruction.op_one["physical"])
			if op_two["nextuse"] == NO_NEXT_USE:
				self._free(a_instruction.op_two["physical"])
			if self._is_register(op_three["virtual"]):
				a_instruction.op_three["physical"] = self._allocate(a_instruction.op_three["virtual"])
			if op_one["nextuse"]:
				self.physical_reg_stack[op_one["physical"]]["nextuse"] = op_one["nextuse"]
			if op_two["nextuse"]:
				self.physical_reg_stack[op_two["physical"]]["nextuse"] = op_two["nextuse"]
			if op_three["virtual"]:
				self.physical_reg_stack[a_instruction.op_three["physical"]]["nextuse"] = op_three["nextuse"]

	def _update(self, operation, index):
		if operation["source"] :
			if operation["source"].isdigit():
				operation["virtual"] = operation["source"]
				return
			if not operation["source"] in self.sr_to_vr_dict:
				self.sr_to_vr_dict[operation["source"]] = "vr" + str(self.vr_index)
				self.last_used_dict[operation["source"]] = NO_NEXT_USE
				self.vr_index += 1
			operation["virtual"] = self.sr_to_vr_dict[operation["source"]]
			operation["nextuse"] = self.last_used_dict[operation["source"]]
			self.last_used_dict[operation["source"]] = index

	def _init_pyhscial_reg_stack(self):
		for index in xrange(self.source_reg_num):
			physical_reg_name = "pr" + str(index)
			self.physical_reg_stack[physical_reg_name]  = PHYSICAL_REG
			self.free_pr_list.append(physical_reg_name)

	def _ensure(self, virtual_reg):
		#need linear search, really slow
		for physical_reg_name, physical_reg in self.physical_reg_stack.items():
			if physical_reg["vr_name"] == virtual_reg:
				print "find physical_reg_name", physical_reg_name
				return physical_reg_name
		return  self._allocate(virtual_reg)

	def _allocate(self, virtual_reg):
		if len(self.free_pr_list) > 0:
			print virtual_reg, self.free_pr_list
			new_physical_reg = {"vr_name" : virtual_reg, "nextuse": None}
			new_physical_reg_name = self.free_pr_list.pop()
			self.physical_reg_stack[new_physical_reg_name] = new_physical_reg
			return new_physical_reg_name
		else:
			physical_reg = self._spill()

	def _free(self, physical_reg_name):
		print "--->physical_reg_stack:" , self.physical_reg_stack
		self.physical_reg_stack[physical_reg_name] = PHYSICAL_REG
		self.free_pr_list.append(physical_reg_name)
		print "<----physical_reg_stack:" , self.physical_reg_stack

	def _spill(self):
		raise Exception
	def _is_register(self, a_register):
		if not a_register:
			return False
		if not a_register.find("r") == -1:
			return True
		return False