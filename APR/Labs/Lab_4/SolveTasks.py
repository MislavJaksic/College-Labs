from Programs.GeneticAlgorithm import GeneticAlgorithm

from Tasks.TaskFunctions import *

from copy import copy
import cProfile



def TaskOne():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 11
  results = []
  for i in range(iterations):
    # GA = GeneticAlgorithm(goal_function=f1, dimensions=2, problem_bounds=problem_bounds,
                          # fitness_bounds=(0,100), population_size=100, binary_display=False, precision=8, p_of_mutation=0.01, p_of_crossover=0.01,
                          # max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
    
    # GA = GeneticAlgorithm(goal_function=f3, dimensions=5, problem_bounds=problem_bounds,
                          # fitness_bounds=(0,100), population_size=4, binary_display=False, precision=8, p_of_mutation=0.01, p_of_crossover=0.01,
                          # max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
    
    # GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                # fitness_bounds=(0,100), population_size=100, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                # max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
    
    GA = GeneticAlgorithm(goal_function=f7, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=20, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
    
    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
  
def ParamOpti():
  problem_bounds = (-50,150)
  max_evals = 5000
  desired_goal_value = (0.1)**6
  iterations = 11
  population_values = [4,10,20,50] #[4,10,20,50,100]
  mutation_values = [0.01] #[0.01,0.05,0.1,0.2,0.5]
  precision_values = [2,4]
  for pop_value in population_values:
    for mut_value in mutation_values:
      for pre_value in precision_values:
        results = []
        for i in range(iterations):
          GA = GeneticAlgorithm(goal_function=f7, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=pop_value, binary_display=True, precision=pre_value, p_of_mutation=mut_value, p_of_crossover=0.01,
                                max_evaluations=max_evals, reach_goal_value=desired_goal_value)
          point, goal_value = GA.SolveProblem()
          results.append((goal_value, point))
      
      
        results = SortGoalAndPoint(results)
        count = CountSuccesses(results, desired_goal_value)
        PrintResults(results, count, iterations)
        print "population_value:",
        print pop_value
        print "mutation_value:",
        print mut_value
        print "precision_value:",
        print pre_value
  
def TaskTwo():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000
  
  iterations = 3
  dimensions = [1,3,6,10]
  for d in dimensions:
    results = []
    for i in range(iterations):
      GA = GeneticAlgorithm(goal_function=f6, dimensions=d, problem_bounds=problem_bounds,
                                    fitness_bounds=(0,100), population_size=20, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                    max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
        
      # GA = GeneticAlgorithm(goal_function=f7, dimensions=d, problem_bounds=problem_bounds,
                                  # fitness_bounds=(0,100), population_size=20, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                  # max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)

      point, goal_value = GA.SolveProblem()
      results.append((goal_value, point))

    results = SortGoalAndPoint(results)
    count = CountSuccesses(results, desired_goal_value)
    PrintResults(results, count, iterations)
  
def TaskThree():
  problem_bounds = (-50,150)
  max_evals = 100000
  desired_goal_value = (0.1)**6
  divergence_at = 1000
  
  binary_display = False
  d = 6
  
  iterations = 11
  results = []
  for i in range(iterations):
    
    GA = GeneticAlgorithm(goal_function=f6, dimensions=d, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=20, binary_display=binary_display, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
                                
    # GA = GeneticAlgorithm(goal_function=f7, dimensions=d, problem_bounds=problem_bounds,
                                # fitness_bounds=(0,100), population_size=20, binary_display=binary_display, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                # max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
                                
    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
  
def TaskFour():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 11
  
  #population_values = [30, 50, 100, 200] #[30, 50, 100, 200]
  mutation_values = [0.01, 0.03, 0.06, 0.1] #[0.1, 0.3, 0.6, 0.9]
  #for pop_value in population_values:
  for mut_value in mutation_values:
    results = []
    for i in range(iterations):   
      GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                  fitness_bounds=(0,100), population_size=100, binary_display=True, precision=4, p_of_mutation=mut_value, p_of_crossover=0.01,
                                  max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)
      
      point, goal_value = GA.SolveProblem()
      results.append((goal_value, point))
      print goal_value

    results = SortGoalAndPoint(results)
    count = CountSuccesses(results, desired_goal_value)
    PrintResults(results, count, iterations)
  
def TaskFive():
  """
  The tournament size is set at k=3, but it can be increased for testing purposes within the algorithm.
  WARNING: always return the tournmanet size  after testing.
  """
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 11
  results = []
  for i in range(iterations):
    GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=100, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                                max_evaluations=max_evals, reach_goal_value=desired_goal_value, no_improvement_limit=divergence_at)

    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))
    print goal_value

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
  
def SortGoalAndPoint(results):
  results = sorted(results, key=lambda result: result[0])
  return results
  
def CountSuccesses(results, desired_goal_value):
  count = 0
  for result in results:
    if result[0] < desired_goal_value:
      count += 1
      
  return count
  
def PrintResults(results, count, iterations):
  print "reached desired goal value:",
  print count
  print "median_goal_value:",
  print results[iterations/2][0]
  print "point:",
  print results[iterations/2][1]
  

#cProfile.run("ParamOpti()")
#TaskOne()
#TaskTwo()
#TaskThree()
#TaskFour()
TaskFive()