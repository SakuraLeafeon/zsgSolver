import unittest
import simplex
import numpy as np

class TestSimplexMethods(unittest.TestCase):

	def test_fullPivot(self):
		A = np.array([[0.5, 0.25],[1, 1],[0.5, 0]])
		b = np.array([[20],[60],[15]])
		c = np.array([[-1], [-1]])

		system = simplex.LinearSystem(A, b, c)
		solvedSystem = simplex.simplexCore(system)
		self.assertEqual(solvedSystem.getObjVal(), 60)

	#def test_smallPivot(self):



if __name__ == '__main__':
	unittest.main()