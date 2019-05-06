#!/usr/bin/python3
import logging
from linearProgramming import LinearProgramming

class Simplex():
		
	def run(self):
		logging.basicConfig(level=logging.INFO, format='%(message)s', filename='log', filemode='w')
		logger = logging.getLogger(__name__)
		
		rows, columns = map(int,input().strip().split(" "))
		c = list(map(int, input().split()))
		Ab = [list(map(int, input().split())) for row in range(rows)]
		
		logger.info("%i rows", rows)
		logger.info("%i columns", columns)
		logger.info(c)
		logger.info(Ab)
		
		lp = LinearProgramming(rows, columns, c, Ab)
		message = lp.solve()
		if(message['status'] == "Feasible"):
			print("otima")
			print("%.8f"%message["optimal_value"])
			for i in message["solution"]: print("%.8f "%i, end="")
			print()
			for i in message["certificate"]: print("%.8f "%i, end="")
			print()
			
		elif(message['status'] == "Unbounded"):
			print("ilimitada")
			for i in message["solution"]: print("%.8f "%i, end="")
			print()
			for i in message["certificate"]: print("%.8f "%i, end="")
			print()
			
		elif(message['status'] == "Infeasible"):
			print("inviavel")
			for i in message["certificate"]: print("%.8f "%i, end="")
			print()

if (__name__ == '__main__'):
		simplex = Simplex()
		simplex.run()