# Simplex - I think the basic idea here is that since the objective function is linear, at any point inside the feasible solution space we can tell which
# direction is 'good' and move that way. Mathematically, this means pivoting on negative variables in the objective funtion. Graphically, this means moving
# from one corner to another along an edge by pivoting. My main issue that's preventing me from understanding everything at the moment is the proof that all
# corners are within the feasible solution space - I seem to recall there being some overlap in graphical representations of the solution space and I still
# haven't gotten my head wrapped around that. I'd like to do so as soon as I can, because at the moment I think I generally understand how the algorithm needs
# to work but without being able to visualize the proof I have a hard time convincing myself of its correctness, and I worry that I'll miss some minor detail.
# I think the best next step here would be to try and derive a proof of the algorithm based on what I know, that should get me familiar enough with it to
# feel confident starting to code. 

# TODO:
# - Accept a system of linear equations IN STANDARD FORM — we can handle transitioninng into standard form elsewhere.
# - Write a function to Pivot on a particular column of the matrix
# - Slot that in to a full algorithm to solve a system ASSUMING INITIAL FEASIBLE SOLUTION
# - Write the code to check for/create that feasible solution

import numpy as np

class LinearSystem:
	def __init__(self, A, b, c):
		if (A.shape[0] != b.shape[0] or
			A.shape[1] != c.shape[0] or
			b.shape[1] != 1 or
			c.shape[1] != 1):
			raise DimensionError("Invalid matrix dimensions!")
		self._AInitial = A
		self._bInitial = b
		self._cInitial = c
		self._pivSys = np.append(A.copy(), np.identity(A.shape[0]), axis=1)
		self._pivObjFn = np.append(np.transpose(c), np.zeros((1, A.shape[0])), axis=1)
		self._pivRight = b
		self._pivObjVal = 0

	# Pivots on the specified column by index
	def pivot(self, n):

		print("Starting pivot on column " + str(n))

		# Multiply the nth column by the rhs element-wise, and find the index of the lowest element to determine pivot row
		row = -1
		rVal = np.inf
		for i in range(self._AInitial.shape[0]):
			if (self._pivSys[i,n] > 0 and
				self._pivRight[i,0]/self._pivSys[i,n] < rVal):
				row = i
				rVal = self._pivRight[i,0]/self._pivSys[i,n]
		if (row == -1):
			raise LinearSystemError("Included variable with no nonzero coefficients!")

		# TODO - make this error more robust - it can also proc if there are no non-negative solutions. 


		#print(self._pivSys[:,n]) # TRASH
		#print(self._pivRight[:,0]) # TRASH
		#print(np.divide(self._pivRight[:,0], self._pivSys[:,n])) # TRASH
		print("Row " + str(row) + " was chosen for pivot base.") # TRASH

		# Iterate through array performing pivots
		for i in range(self._A.shape[0]):
			if (i != row):
				coef = self._pivSys[i, n] / self._pivSys[row, n]
				# Subtract pivot row * coef from row i
				self._pivSys[i,:] = np.subtract(self._pivSys[i,:], np.multiply(coef, self._pivSys[row,:]))
				self._pivRight[i,:] = np.subtract(self._pivRight[i,:], np.multiply(coef, self._pivRight[row,:]))
			else:
				coef = 1 / self._pivSys[row, n]
				self._pivSys[i,:] = np.multiply(coef, self._pivSys[row,:])
				self._pivRight[i,:] = np.multiply(coef, self._pivRight[row,:])

		# Pivot for objective function row
		coef = self._pivObjFn[0, n] / self._pivSys[row, n]
		# Subtract pivot row * coef from row i
		self._pivObjFn = np.subtract(self._pivObjFn, np.multiply(coef, self._pivSys[row,:]))
		self._pivObjVal = np.subtract(self._pivObjVal, np.multiply(coef, self._pivRight[row,:]))

		print("Pivot results are:")
		print(self._pivObjFn) # TRASH
		print(self._pivObjVal) # TRASH
		print(self._pivSys) # TRASH
		print(self._pivRight) # TRASH
		print("/n")

	# Return true if the solution represented by the system's currently basic variables is feasible, false otherwise.
	def checkFeasibility(self):
		if (self._pivRight[0, np.argmin(self._pivRight)] < 0):
			return False
		return True

	def addArtificialVariables(self):
		return

	# Find the index of the next column to pivot on (the first negative coefficient in the objective function). If there are no negatives, return None.
	# TODO - is there a better way to isolate one column if there are multiple negatives other than picking the most negative? Preliminary analysis says there
	# isn't a super obvious way, as most heuristics have pretty simple exceptions, but it's possible that one exists with reasonable accuracy. Something to
	# consider to improve runtime once the basic version works.
	# TODO - There is a problem with this - currently, we have no way of dealing with variables that're basic in the original system but that also appear in
	# the objective function. First of all, we want to get rid of those because if we pivot on them we aren't actually changing the rest of the system. Then,
	# after doing that, we need to figure out how to avoid looping.

	# OKAY. So basically, we have two problems here, tangentially related to each other. Firstly, when looking for an initial feasible solution, we end up in
	# a position where we have a complex variable expressed in the objective function. Since we're minimizing w, we're also stuck with a positive coefficient
	# in the objective function. Obviously we can't pivot onto a variable that's already complex, but we CAN subtract it from the objective function to put it
	# in different terms, and then simplify from there. The question is whether we want to do this first or last, and also if that's even relevant - we don't
	# know if it's even possible for that situation to occur outside of minimizing artificial variables. Our OTHER problem is that if we have a dimension that
	# is only expressed in one constraint, that variable is ostensibly basic. The problem is, we still need to add a slack variable, which results in us 
	# having too many complex variables. This represents not being sure where on the line between the two corners we are, and I don't think it's a good thing
	# quite frankly. The solution here is just to not treat the original variable as complex, and treat it as zero. There's nothing wrong with doing that, 
	# but it does break our method of visually inspecting variables to see if they're complex or not. I think the best way to solve this is to create an array
	# of variables that we consider basic? And that way we can make sure we always know what we're doing? I'm going to try and figure out the first problem
	# before this one, I think.

	# OKAY AGAIN. I'm fairly certain that the following is true of handling artificial variables. Firstly, whether we change the terms of one or multiple
	# complex aritifical variables before starting to actually pivot doesn't seem to matter at all. What does matter, however, is whether or not we pivot
	# off of the row including the artificial variable. It seems a lot cleaner if we do? If we don't, we still have that articial variable as one of our
	# complex variables, and we get the corresponding slack variable as a false complex variable. The math still works out, but it's messier. I think ideally,
	# we just make all the artificial variables basic, which means pivoting off of the rows they're present in. But, is that always possible? What if they're
	# higher than other rows and we reintroduce negatives? I'm not sure but I do think it's maybe possible that because the presence of artificial variables
	# belies reversed inequalities, it might be true that the right hand sides of artificial variables must be smallest or tied for the smallest, else there
	# would be no solutions (if two lines want a solution between them, switching the positions of the lines gets rid of all possible solutions). This would
	# be a good thing to prove, I think. So do that.

	def getPivotCol(self):
		val = np.argmin(self._pivObjFn)
		# Need to check the value, not the index.
		if (self._pivObjFn[0,val] < 0):
			return val
		return None

	def getADimensions(self):
		return self._A.shape

	def getObjVal(self):
		return self._pivObjVal

def acceptInput():
	return

# Given a system of linear equations, continue pivoting until the objective function is optimized. Then return that system.
# TODO - this might need to change when we add the initial feasible solution finder.
def simplexCore(linSys):
	n = linSys.getADimensions()[0] + linSys.getADimensions()[1]
	m = linSys.getADimensions()[1]
	bound = int(np.math.factorial(n) / np.multiply(np.math.factorial(m), np.math.factorial(n-m)))
	#print("Bound is: " + str(bound)) # TRASH
	for i in range(bound):
		piv = linSys.getPivotCol()
		if (piv is None):
			return linSys
		linSys.pivot(piv)

		# TODO - is this the best way to do this with setting an upper bound? It's not very accurate, but I figure it's more ideal than
		# a while loop? I could be wrong though.

# Given a system of linear equations, acquire a feasible solution. This is done by, for each negative right hand side, multiplying the entire equation by
# negative one and adding an artificial variable, then creating an objective function that sums all the artificial variables and minimizes that sum.
# TODO - Is it guaranteed that minimizing the sum across all artificial variables results in zero, or is it possible that there are systems for which there
# is no initial feasible solution? Realistically, I'm certain that there are, how do we address that? Can we check for that and raise an exception?
# TODO - Is it ever possible for repeated applications of this operation to result in a feasible solution when a single one would not?
def locateFeasibleSolution(linSys):

