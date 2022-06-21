# Steps:
# We need to accept a zero-sum game (doesn't necessarily ALWAYS need to be a zero-sum game, we could do it with non-zero sum games as well) as a matrix
# We need to store that matrix in some kind of reasonable data structure.
# We need to generate the system of equations that we need to solve to achieve Nash Equilibrium
# I need to remember how simplex works
# We need to write a Simplex implementation
# Pass the system of equations to the Simplex function
# Return the nash equilibrium

# Order of Operations:
# We should probably write the code to accept and store matrices early on, as well as the simplex implementation. That'll let us know what kind of form
# of data we're operating on, which will probably be especially important for creating the system of linear equations and doing a good job of passing it
# to Simplex.

# Simplex - I think the basic idea here is that since the objective function is linear, at any point inside the feasible solution space we can tell which
# direction is 'good' and move that way. Mathematically, this means pivoting on negative variables in the objective funtion. Graphically, this means moving
# from one corner to another along an edge by pivoting. My main issue that's preventing me from understanding everything at the moment is the proof that all
# corners are within the feasible solution space - I seem to recall there being some overlap in graphical representations of the solution space and I still
# haven't gotten my head wrapped around that. I'd like to do so as soon as I can, because at the moment I think I generally understand how the algorithm needs
# to work but without being able to visualize the proof I have a hard time convincing myself of its correctness, and I worry that I'll miss some minor detail.
# I think the best next step here would be to try and derive a proof of the algorithm based on what I know, that should get me familiar enough with it to
# feel confident starting to code. 
