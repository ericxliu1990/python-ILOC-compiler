"""
"""
class ILOCAllocator():
	"""docstring for Allocator"""
	def __init__(self, ir_list, source_reg_num):
		self.ir_list = ir_list
		self.source_reg_num = source_reg_num
		self.sr_to_vr_dict = dict()
		self.last_used_dict = dict()
		self.vr_name = 0
		self.max_live = 0

	def find_live_ranges(self):
		for a_instruction in reversed(self.ir_list):
			self._update(a_instruction.op_three, a_instruction.index)
			if a_instruction.op_three["source"] :
				del self.sr_to_vr_dict[a_instruction.op_three["source"]]
				del self.last_used_dict[a_instruction.op_three["source"]]
			self._update(a_instruction.op_one, a_instruction.index)
			self._update(a_instruction.op_two, a_instruction.index)
			self.max_live = max(self.max_live, len(self.vr_name))
			print "sr_to_vr" + str(self.sr_to_vr_dict)
			print "LU" + str(self.last_used_dict)
			print self.max_live

	def local_allocate(self):
		pass

	def _update(self, operation, index):
		if operation["source"] :
			if operation["source"].isdigit():
				operation["virtual"] = operation["source"]
				return
			if not operation["source"] in self.sr_to_vr_dict:
				self.sr_to_vr_dict[operation["source"]] = "vr" + str(self.vr_name)
				self.last_used_dict[operation["source"]] = None
				self.vr_name += 1
			operation["virtual"] = self.sr_to_vr_dict[operation["source"]]
			operation["nexttuse"] = self.last_used_dict[operation["source"]]
			self.last_used_dict[operation["source"]] = index
			


			