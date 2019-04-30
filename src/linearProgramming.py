import logging
from pprint import pformat

class LinearProgramming():
	def __init__(self, rows, columns, c, Ab):
		self.__rows = rows
		self.__columns = columns
		c = list(map(lambda x: -x, c))
		self.__make_tableaux(c, Ab)
		self.__add_operation_matrix()
		self.__make_canonical_tableaux()
		logging.info(pformat(self.__tableaux))
		# self.do_pivoting(1,rows)
		# logging.info(pformat(self.__tableaux))
	
	

	def __make_tableaux(self, c, Ab):
		self.__tableaux = c + [0]
		self.__tableaux = [self.__tableaux] + Ab
	
	def __add_operation_matrix(self):
		zeroes = [0]*self.__rows
		self.__tableaux[0] = zeroes + self.__tableaux[0]
		for i in range(self.__rows):
			self.__tableaux[i+1] = zeroes + self.__tableaux[i+1]
			self.__tableaux[i+1][i] = 1

	def __make_canonical_tableaux(self):
		zeroes = [0]*self.__rows
		self.__tableaux[0] = self.__tableaux[0][:-1] + zeroes +self.__tableaux[0][-1:]
		for i in range(self.__rows):
			zeroes = [0]*self.__rows
			zeroes[i] = 1
			self.__tableaux[i+1] = self.__tableaux[i+1][:-1] + zeroes +self.__tableaux[i+1][-1:]
	
	def do_pivoting(self, row, column):
		print(self.__tableaux[row], "PIVO")
		multiplier = 1/self.__tableaux[row][column]
		self.__tableaux[row] = list(map(lambda x: x*multiplier, self.__tableaux[row]))
		for index in (i for j in (range(row), range(row+1, self.__rows+1)) for i in j):
			multiplier = -self.__tableaux[index][column]
			line_multiplier = list(map(lambda x: x*multiplier, self.__tableaux[row]))
			self.__tableaux[index] = list(map(lambda x,y: x+y, self.__tableaux[index], line_multiplier))
