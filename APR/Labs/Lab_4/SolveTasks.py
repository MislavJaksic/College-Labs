from Programs.GeneticAlgorithm import GeneticAlgorithm

from Tasks.TaskFunctions import *

from copy import copy

def TaskOne():
  #f1, dim=2, best_values: pop=100, mut=0.01
  
  
  #f3, dim=5, best_values: pop=4, mut=0.01
  iterations = 11
  desired_goal_value = (0.1)**6
  results = []
  for i in range(iterations):
    GA = GeneticAlgorithm(goal_function=f3, dimensions=5, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=4, binary_display=False, precision=8, p_of_mutation=0.01, p_of_crossover=0.01,
                          max_evaluations=10000, reach_goal_value=(0.1)**6)
    point, goal_value = GA.SolveProblem()
    results.append(goal_value)

  results.sort()
  count = 0
  for result in results:
    if result < desired_goal_value:
      count += 1
  print "reached desired goal value:",
  print count
  print "median_goal_value:",
  print results[iterations/2]
  
def ParamOpti():
  desired_goal_value = (0.1)**6
  iterations = 11
  population_values = [20,50,100] #[4,10,20,50,100]
  mutation_values = [0.01,0.05,0.1,0.2,0.5] #[0.01,0.05,0.1,0.2,0.5]
  for pop_value in population_values:
    for mut_value in mutation_values:
      results = []
      for i in range(iterations):
        GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=(-50,150),
                              fitness_bounds=(0,100), population_size=pop_value, binary_display=False, precision=8, p_of_mutation=mut_value, p_of_crossover=0.01,
                              max_evaluations=1000, reach_goal_value=(0.1)**6)
        point, goal_value = GA.SolveProblem()
        results.append(goal_value)
    
    
      results.sort()
      count = 0
      for result in results:
        if result < desired_goal_value:
          count += 1
      print "reached desired goal value:",
      print count
      print "median_goal_value:",
      print results[iterations/2]
      print "min point:",
      print point
      print "population_value:",
      print pop_value
      print "mutation_value:",
      print mut_value
  
def TaskTwo():
  x0 = [-1.9, 2]
  F = f1
  dF = [df1x0, df1x1]
  ddF = [[ddf1x0x0, ddf1x0x1],
         [ddf1x0x1, ddf1x1x1],
        ]
  
  #SolveWithSteepestDescent(x0, F, dF, True)
  #SolveWithNewtonRaphson(x0, F, dF, ddF, True)
  
  #x0 = [0.1, 0.3]
  x0 = [0, 0]
  F = f2
  dF = [df2x0, df2x1]
  ddF = [[ddf2x0x0, ddf2x0x1],
         [ddf2x0x1, ddf2x1x1],
        ]
  
  SolveWithSteepestDescent(x0, F, dF, True)
  #SolveWithNewtonRaphson(x0, F, dF, ddF, True)
  
def TaskThree():
  x0 = [-1.9, 2]
  F = f1
  Inequalities = [constraint1, constraint2]
  Interval = [-100, 100]
  
  #SolveWithBox(x0, F, Inequalities, Interval)
  
  x0 = [0.1, 0.3]
  F = f2
  Inequalities = [constraint1, constraint2]
  Interval = [-100, 100]
  
  SolveWithBox(x0, F, Inequalities, Interval)
  
def TaskFour():
  x0 = [-1.9, 2]
  F = f1
  Inequalities = [constraint1, constraint2]
  
  #SolveWithConstraintOptimization(x0, F, Inequalities, [])
  
  betterx0 = [3, 3]
  
  #SolveWithConstraintOptimization(betterx0, F, Inequalities, [])
  
  x0 = [0.1, 0.3]
  F = f2
  Inequalities = [constraint1, constraint2]
  
  SolveWithConstraintOptimization(x0, F, Inequalities, [])
  
def TaskFive():
  x0 = [0, 0]
  F = f4
  Inequalities = [constraint3, constraint4]
  Equalities = [constraint5]
  
  #SolveWithConstraintOptimization(x0, F, Inequalities, Equalities)
  
  x0 = [5, 5]
  
  SolveWithConstraintOptimization(x0, F, Inequalities, Equalities)
  
def SolveWithSteepestDescent(x0, function, dF, useGolden):
  F = CountInvocations(function)
  newdF = []
  for f in dF:
    newdF.append(CountInvocations(f))
  
  minimum = SteepestDescent(copy(x0), F, newdF, useGolden)
  print "SteepestDescent ",
  PrintMinimumAndInvocations(minimum, F, newdF, [])
  
def SolveWithNewtonRaphson(x0, function, dF, ddF, useGolden):
  F = CountInvocations(function)
  newdF = []
  for f in dF:
    newdF.append(CountInvocations(f))
  
  newddF = []
  for list in ddF:
    newList = []
    for f in list:
      newList.append(CountInvocations(f))
    newddF.append(newList)
    
  minimum = NewtonRaphson(copy(x0), F, newdF, newddF, useGolden=useGolden)
  print "NewtonRaphson ",
  PrintMinimumAndInvocations(minimum, F, newdF, newddF)
  
def SolveWithBox(x0, function, Inequalities, Interval):
  F = CountInvocations(function)
  minimum = Box(copy(x0), F, Inequalities, Interval)
  print "Box ",
  PrintMinimumAndInvocations(minimum, F, [], [])
  
def SolveWithConstraintOptimization(x0, function, Inequalities, Equalities):
  F = CountInvocations(function)
  minimum = ConstraintOptimization(copy(x0), F, Inequalities, Equalities)
  print "ConstraintOptimization ",
  PrintMinimumAndInvocations(minimum, F, [], [])
  
def PrintMinimumAndInvocations(minimum, F, dF, ddF):
  print "minimum:",
  print minimum
  print "Goal function value at minimum:",
  print F(minimum)
  print "Number of goal function invocations:",
  print F.invocations
  
  sum = 0
  for f in dF:
    sum+= f.invocations
  print "Number of first partial function invocations:",
  print sum
  
  sum = 0
  for list in ddF:
    for f in list:
      sum+= f.invocations
  print "Number of second partial function invocations:",
  print sum
  
  print "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-"
  print
  
def CountInvocations(function):
  def interdictor(x):
    interdictor.invocations += 1
    result = function(x)
    return result
    
  interdictor.invocations = 0
  
  return interdictor
  
#ParamOpti()
TaskOne()
#TaskTwo()
#TaskThree()
#TaskFour()
#TaskFive()