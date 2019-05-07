#!/usr/bin/python3
# import logging
from linearProgramming import LinearProgramming

class Simplex():

	def run(self):
		# loggingging.basicConfig(level=# loggingging.INFO, format='%(message)s', filename='# logging', filemode='w')

		rows, columns = map(int,input().strip().split(" "))
		c = list(map(float, input().split()))
		Ab = [list(map(float, input().split())) for row in range(rows)]

		# loggingging.info("%i rows", rows)
		# loggingging.info("%i columns", columns)
		# loggingging.info(c)
		# loggingging.info(Ab)

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