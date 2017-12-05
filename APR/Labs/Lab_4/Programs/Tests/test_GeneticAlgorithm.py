from Programs.GeneticAlgorithm import GeneticAlgorithm, BinaryCreature
from Tasks.TaskFunctions import f3

import pytest
from copy import copy
  
def test_BinaryCreature_Create():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 150
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  assert creature.chromosome_length == 21
  
def test_BinaryCreature_CalculateChromosomeLength():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  assert creature.CalculateChromosomeLength() == 20
  
def test_BinaryCreature_ReverseList():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  assert creature.ReverseList([1,2,3,4]) == [4,3,2,1]
  
def test_BinaryCreature_CreateBinaryChromosome():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  assert creature.CreateBinaryChromosome(568658) == [1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0]
  
def test_BinaryCreature_ConvertFloatingPointToBinary():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  assert creature.ConvertFloatingPointToBinary(4.231514) == 568658
  
def test_BinaryCreature_CreateChromosome():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  chromosome_matrix = creature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
#  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)