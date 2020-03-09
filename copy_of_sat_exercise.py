from pysat.solvers import Minisat22
import itertools
import numpy as np  # we'll need numpy's 2-dim array

n_student = 15
n_day = (n_student-1)//2
n_group = n_student//3

idx2 = 1
varmap2 = dict()
mapback2 = dict()

# if student 𝑖 walks in group 𝑔 on day 𝑑
for d in range(n_day):
    for g in range(n_group):
        for i in range(n_student):
            varmap2[(d, g, i)] = idx2
            mapback2[idx2] = (d, g, i)
            idx2 += 1

# if student pair (𝑖,𝑗) walks in group 𝑔 on day 𝑑
for d in range(n_day):
    for g in range(n_group):
        for (i, j) in itertools.combinations(range(n_student), 2):
            varmap2[(d, g, (i, j))] = idx2
            mapback2[idx2] = (d, g, (i, j))
            idx2 += 1

# to link these two propositional symbols, we add the following constraints:
# if student pair (𝑖,𝑗) walks in group 𝑔 on day 𝑑, then student 𝑖 walks in 
# group 𝑔 on day 𝑑 and student 𝑗 walks in group 𝑔 on day 𝑑; if student 𝑖 and 
# student 𝑗 walk in group 𝑔 on day 𝑑, then student pair (𝑖,𝑗) walks in group 
# 𝑔 on day 𝑑
def link_symbols(solver, ivarmap):
    for d in range(n_day):
        for g in range(n_group):
            for (i, j) in itertools.combinations(range(n_student), 2):
                solver.add_clause([-ivarmap[(d, g, i)], -ivarmap[(d, g, j)], ivarmap[(d, g, (i, j))]])
                solver.add_clause([-ivarmap[(d, g, (i, j))], ivarmap[(d, g, i)]])
                solver.add_clause([-ivarmap[(d, g, (i, j))], ivarmap[(d, g, j)]])

"""**Exercise 4A (report in PDF)** How many propositional symbols does this encoding generate? Explain your answer.

For the two exercises below, please export this Jupyter notebook to a .py file. If you are working on Google Colab, you can download the .py file by doing the following: 

<img src="https://www.cs.cornell.edu/courses/cs4700/2020sp/homeworks/download-py.png" width="300">

**Exercise 4B (report in .py file)** Please complete the encoding by coming up with the constraints. 

*HINT:* First, write your constraints out in English. Then, convert them into the clauses that will be used to compute a solution, similar to what was done for Sudoku.
"""

# def sol_4B():
    # please define such a function in your .py file, as we'll be calling it to check your answer
    # you should return whatever it is in the .get_model()
    # for example:
    # s = Minisat22()
    # ... do whatever ...
    # return s.get_model()
def sol_4B():
  s = Minisat22()

  # Link Symbols
  link_symbols(s, varmap2)

  # Make sure that no two students walk out twice in a group across the seven days
  for (i, j) in itertools.combinations(range(n_student), 2):
    clauses = []
    for d in range(n_day):
      for g in range(n_group):
        clauses.append(varmap2[(d, g, (i, j))])
    for (c1, c2) in itertools.combinations(clauses, 2):
      s.add_clause([-c1, -c2])
  
  # Make sure that every student is assigned and only assigned one group every day
  for i in range(n_day):
    for j in range(n_student):
      groups = [varmap2[(i, g, j)] for g in range(n_group)]
      for (g1, g2) in itertools.combinations(groups, 2):
        s.add_clause([-g1, -g2])
      s.add_clause(groups)
  
  # Make sure that every group has three students every day
  for i in range(n_day):
    for j in range(n_group):
      for (s1, s2, s3) in itertools.combinations(range(n_student), 3):
        c1 = varmap2[(i, j, (s1, s2))]
        c2 = varmap2[(i, j, (s1, s3))]
        c3 = varmap2[(i, j, (s2, s3))]
        s.add_clause([-c1, -c2, c3])
        s.add_clause([-c1, -c3, c2])
        s.add_clause([-c2, -c3, c1])
  
  s.solve()
  return s.get_model()

def print_solution(imodel, imapback):
  sol = np.zeros((7, 15), dtype=int)
  for i in range(525):
    if imodel[i] > 0:
      day, group, student = imapback[i + 1]
      sol[day][student] = group
  print(sol)

model2 = sol_4B()
print_solution(model2, mapback2)

"""**Exercise 4C (report in .py file)** Can you use the SAT solver to come up with ten different schedules? 

*HINT:* There are many ways to do this.  Here is one: think about how to prevent the solver from returning a truth assignment? More specifically, what constraints can you add to prevent that?
"""

# def sol_4C():
    # please define such a function in your .py file, as we'll be calling it to check your answer
    # please return the 10 models you compute in a list
    # for example:
    # res = []
    # for _ in range(10):
    #     # add constraints to your solver
    #     s.add_clause(...)
    #     # append solutions
    #     res.append(s.get_model())
    # return res
def sol_4C():
  s = Minisat22()

  # Link Symbols
  link_symbols(s, varmap2)

  # Make sure that no two students walk out twice in a group across the seven days
  for (i, j) in itertools.combinations(range(n_student), 2):
    clauses = []
    for d in range(n_day):
      for g in range(n_group):
        clauses.append(varmap2[(d, g, (i, j))])
    for (c1, c2) in itertools.combinations(clauses, 2):
      s.add_clause([-c1, -c2])
  
  # Make sure that every student is assigned and only assigned one group every day
  for i in range(n_day):
    for j in range(n_student):
      groups = [varmap2[(i, g, j)] for g in range(n_group)]
      for (g1, g2) in itertools.combinations(groups, 2):
        s.add_clause([-g1, -g2])
      s.add_clause(groups)
  
  # Make sure that every group has three students every day
  for i in range(n_day):
    for j in range(n_group):
      for (s1, s2, s3) in itertools.combinations(range(n_student), 3):
        c1 = varmap2[(i, j, (s1, s2))]
        c2 = varmap2[(i, j, (s1, s3))]
        c3 = varmap2[(i, j, (s2, s3))]
        s.add_clause([-c1, -c2, c3])
        s.add_clause([-c1, -c3, c2])
        s.add_clause([-c2, -c3, c1])

  s.solve()
  res = [s.get_model()]
  for _ in range(9):
    curr = res[-1]
    clause = []
    for i in range(len(curr)):
      clause.append(-curr[i])
    s.add_clause(clause)
    s.solve()
    res.append(s.get_model())
  return res

"""### Some final notes:

*   As the Boolean Satisfiability problem is an NP-hard problem, it is too easy to run into a case where it takes too long to get a solution. If you don't get an answer for a minute, that often means your constraints are too hard.  A rule of thumb is to aim for making clauses with fewer literals!
*   Use print() as much as you can!  If you're stuck, use print() to see what truth assignment the SAT solver returns, inspect what constraints are missing, and then you can add clauses according to those missed constraints (just like we did for the Sudoku problem). Remeber, we have defined a mapping called ``mapback2``; you can use that to translate from a propositional symbol to which student walk in which group on which day.
"""