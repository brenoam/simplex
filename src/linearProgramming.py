import utils
import logging
from pprint import pformat

class LinearProgramming():
	def __init__(self, rows, columns, c, Ab):
		self.__rows = rows
		self.__columns = columns
		self.__op_matrix_len = rows
		c = list(map(lambda x: -x, c))
		self.__make_tableau(c, Ab)
		self.__add_operation_matrix()
		self.__basis = self.__make_canonical_tableau()
		logging.info(pformat(self.__tableau))
		logging.info("basis")
		logging.info(pformat(self.__basis))
	
	def solve(self):
		try:
			while(True):
				logging.info("Choosing c negative entry")
				col = self.__get_first_c_negative_entry()
				logging.info("Chosing new basis")
				row = self.__choose_new_basis_at_col(col)
				self.__do_pivoting(row, col)
		except utils.Feasible:
			print ("otima")
			print(self.__get_optimal_value())
			print(self.__get_feasible_solution())
			print(self.__get_optimal_certificate())
			

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
	
	def __do_pivoting(self, row, column):
		multiplier = 1/self.__tableau[row][column]
		self.__tableau[row] = list(map(lambda x: x*multiplier, self.__tableau[row]))
		
		for index in (i for j in (range(row), range(row+1, self.__rows+1)) for i in j):
			multiplier = -self.__tableau[index][column]
			line_multiplier = list(map(lambda x: x*multiplier, self.__tableau[row]))
			self.__tableau[index] = list(map(lambda x,y: x+y, self.__tableau[index], line_multiplier))
	
	def __get_first_c_negative_entry(self):
		try:
			col = self.__tableau[0].index(next(filter(lambda x: x<0, self.__tableau[0][self.__op_matrix_len:-1])))
			logging.info(col)
			return col
		
		except StopIteration:
			raise utils.Feasible

	def __choose_new_basis_at_col(self, col):
		index = -1
		value = float("inf")
		
		for i in range(1,self.__rows+1):
			logging.info(self.__tableau[i][col]/self.__tableau[i][-1])
			logging.info(value)
			if (self.__tableau[i][col] > 0):
				if(self.__tableau[i][col]/self.__tableau[i][-1] < value):
					value = self.__tableau[i][col]/self.__tableau[i][-1]
					index = i
					
		if(index == -1):
			raise Exception("Unbounded")
		else:
			logging.info(index)
			return index
	
	def __get_optimal_value(self):
		return self.__tableau[0][-1]
	
	def __get_optimal_certificate(self):
		return self.__tableau[0][:self.__op_matrix_len]
	
	def __get_feasible_solution(self):
		solution = [0]*self.__rows
		for j in self.__basis:
			for i in range(1, self.__rows+1):
				if(self.__tableau[i][j] == 1):
					solution[i-1] = self.__tableau[i][-1]
		return solution