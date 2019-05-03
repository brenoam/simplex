import utils
import logging
from pprint import pformat
import pprint

OP_DECIMAL_PLACES = 10
PRINT_DECIMAL_PLACES = 7

class LinearProgramming():
	def __init__(self, rows, columns, c, Ab, auxiliary=False):
		self.__rows = rows
		self.__columns = columns
		self.__op_matrix_len = rows
		c = list(map(lambda x: -x, c))
		self.__make_tableau(c, Ab)
		self.__add_operation_matrix()
		
		# Set b values to positive
		if(auxiliary):
			logging.info("AUXILIARY")
			neg_entries = self.__get_b_negative_entries_index()
			for i in neg_entries:
				self.__tableau[i] = list(map(lambda x: -x, self.__tableau[i]))
				
		basis = [-1]*self.__rows
		for i in range(1, self.__rows+1):
			for index,val in enumerate(self.__tableau[i][self.__op_matrix_len:-1]):
				if (val == 1):
					just_zeroes = 0
					for k in range(self.__rows+1):
						if(self.__tableau[k][index+self.__op_matrix_len] != 0):
							just_zeroes += 1
					if(just_zeroes == 1):
						basis[i-1] = index+self.__op_matrix_len
		if (not any(x == -1 for x in basis)):
			self.__basis = basis
		else:
			self.__basis = self.__make_canonical_tableau()
		
		# Initialization for auxiliary tableau
		if (auxiliary):
			for index,base in enumerate(self.__basis):
				self.__tableau[0][base] = 1
			for index,base in enumerate(self.__basis):
				self.__do_pivoting(index+1, base)
		
		logging.info("ROWS %i COLS %i"%(rows, columns))
		logging.info("Tableau")
		logging.info(pformat(self.__tableau, width=250))
		logging.info("Basis")
		logging.info(pformat(self.__basis, width = 250))
		logging.info("LP created")
	
	def run(self):
		message = self.solve()
		if(message['status'] == "Feasible"):
			print("otima")
			print(message["optimal_value"])
			print(message["solution"])
			print(message["certificate"])
			
		elif(message['status'] == "Unbounded"):
			print("ilimitada")
			print(message["solution"])
			print(message["certificate"])
			
		elif(message['status'] == "Infeasible"):
			print("inviavel")
			print(message["certificate"])
	
	def solve(self):
		# Auxiliary LP
		neg_entries = self.__get_b_negative_entries_index()
		if (len(neg_entries) > 0):
			logging.info("Auxiliary LP")
			message = self.__solve_aux_lp()
			if(message['status'] == "Infeasible"):
				return message
		
		try:
			while(True):
				col = self.__get_first_c_negative_entry()
				row = self.__choose_new_basis_at_col(col)
				self.__do_pivoting(row, col)
				
		except utils.Feasible:
			logging.info("Feasible")
			message = {
				"status": "Feasible",
				"optimal_value":self.__get_optimal_value(),
				"solution": self.__get_feasible_solution(),
				"certificate": self.__get_optimal_certificate(),
				"basis": self.__get_basis()
			}
		except utils.Unbounded as e:
			col = e.args[0]
			logging.info("Unbounded")
			message = {
				"status": "Unbounded",
				"solution": self.__get_feasible_solution(),
				"certificate": self.__get_unbounded_certificate(col),
				"basis": self.__get_basis()
			}
		finally:
			return message
			
	def __solve_aux_lp(self):
		aux_lp = self.__make_auxiliary_tableau()
		message = aux_lp.solve()
		
		if(message['status'] == "Feasible"):
			if(message['optimal_value'] == 0):
				aux_basis = message['basis']
				for index, base in enumerate(aux_basis):
					if(self.__is_variable_from_original_problem(base)):
						self.__do_pivoting(index+1, base)
			elif (message['optimal_value'] < 0):
				message = {
					"status": "Infeasible",
					"certificate": message['certificate']
				}
		return message

	def __make_tableau(self, c, Ab):
		self.__tableau = c + [0]
		self.__tableau = [self.__tableau] + Ab

	def __add_operation_matrix(self):
		zeroes = [0]*self.__rows
		self.__tableau[0] = zeroes + self.__tableau[0]
		
		for i in range(self.__op_matrix_len):
			self.__tableau[i+1] = zeroes + self.__tableau[i+1]
			self.__tableau[i+1][i] = 1

	def __make_canonical_tableau(self):
		zeroes = [0]*self.__rows
		self.__tableau[0] = self.__tableau[0][:-1] + zeroes +self.__tableau[0][-1:]
		
		for i in range(self.__rows):
			zeroes = [0]*self.__rows
			zeroes[i] = 1
			self.__tableau[i+1] = self.__tableau[i+1][:-1] + zeroes +self.__tableau[i+1][-1:]
		
		basis = [i for i in range(self.__op_matrix_len+self.__columns, self.__op_matrix_len*2+self.__columns)]
		return basis
	
	def __make_auxiliary_tableau(self):
		rows = self.__rows
		columns = self.__columns + self.__rows
		c = [0]*columns
		c = list(map(lambda x: -x, c))
		Ab = [self.__tableau[i][self.__op_matrix_len:] for i in range(1, self.__rows+1)]
		auxiliary = True
		lp = LinearProgramming(rows, columns, c, Ab, auxiliary)
		return lp
		
	def __do_pivoting(self, row, column):
		logging.info("Pivoting at %i %i"%(row, column))
		self.__basis[row-1] = column
		multiplier = 1/self.__tableau[row][column]
		self.__tableau[row] = list(map(lambda x: round(x*multiplier, OP_DECIMAL_PLACES), self.__tableau[row]))
		
		for index in (i for j in (range(row), range(row+1, self.__rows+1)) for i in j):
			multiplier = -self.__tableau[index][column]
			line_multiplier = list(map(lambda x: x*multiplier, self.__tableau[row]))
			self.__tableau[index] = list(map(lambda x,y: round(x+y,OP_DECIMAL_PLACES), self.__tableau[index], line_multiplier))
		
		logging.info("Tableau")
		logging.info(pformat(self.__tableau, width=250))
		logging.info("Basis")
		logging.info(pformat(self.__basis, width = 250))
	
	def __get_first_c_negative_entry(self):
		try:
			logging.info("Choosing c negative entry")
			col = self.__op_matrix_len + self.__tableau[0][self.__op_matrix_len:-1].index(next(filter(lambda x: x<0, self.__tableau[0][self.__op_matrix_len:-1])))
			logging.info(col)
			return col
		
		except StopIteration:
			raise utils.Feasible()

	def __get_b_negative_entries_index(self):
		neg_entries = []
		for i in range(1, self.__rows+1):
			if(self.__tableau[i][-1] < 0):
				neg_entries.append(i)
		return neg_entries

	def __choose_new_basis_at_col(self, col):
		logging.info("Chosing new basis")
		index = -1
		value = float("inf")
		
		for i in range(1,self.__rows+1):
			if (self.__tableau[i][col] > 0):
				temp = self.__tableau[i][-1]/self.__tableau[i][col]
				if(temp < value):
					value = temp
					index = i
		logging.info(index)
		logging.info(value)
		if(index == -1):
			raise utils.Unbounded(col)
		else:
			logging.info(index)
			return index
	
	def __get_optimal_value(self):
		return self.__tableau[0][-1]
	
	def __get_optimal_certificate(self):
		return self.__tableau[0][:self.__op_matrix_len]
	
	def __get_feasible_solution(self):
		solution = [0]*self.__columns
		for index, base in enumerate(self.__basis):
			if(self.__is_variable_from_original_problem(base)):
				solution[base-self.__op_matrix_len] = self.__tableau[index+1][-1]
		return solution
	
	def __get_unbounded_certificate(self, col):
		solution = [0]*self.__columns
		if(self.__is_variable_from_original_problem(col)):
			solution[col] = 1
		for index, base in enumerate(self.__basis):
			if(self.__is_variable_from_original_problem(base)):
				solution[index] = -self.__tableau[index+1][col]
		return solution
		
	def __is_variable_from_original_problem(self, basis):
		return(basis >= self.__op_matrix_len and basis < self.__op_matrix_len+self.__columns)
		
	def __get_basis(self):
		return self.__basis