from Programs.GeneticAlgorithm import GeneticAlgorithm, BinaryCreature, FloatingPointCreature, Population
from Tasks.TaskFunctions import f3

import pytest
from copy import copy

@pytest.fixture(scope='function')
def SimpleBinaryPopulation():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  binary_display = True
  precision = 4
  lower_fitness_bound = 0
  upper_fitness_bound = 100
  population_size = 5
  population = Population(goal_function, dimensions, lower_problem_bound, upper_problem_bound,
                          lower_fitness_bound, upper_fitness_bound,
                          binary_display, precision,
                          population_size)
  return population
  
def test_BinaryPopulation_EvaluatePopulation(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal_value != False
    assert creature.fitness_value >= 0
  
def test_BinaryPopulation_SetBestWorstGoalCreature(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.worst_goal_creature.goal_value != False
  assert SimpleBinaryPopulation.best_goal_creature.goal_value != False
    
def test_BinaryPopulation_SetBestWorstFitnessCreature(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.worst_fitness_creature.fitness_value == 0.0
  assert SimpleBinaryPopulation.best_fitness_creature.fitness_value == 100.0
  
def test_BinaryPopulation_KTournamentCreatureSelection(SimpleBinaryPopulation):
  creature = SimpleBinaryPopulation.KTournamentCreatureSelection(3)
  assert creature.fitness_value >= 0.0
  
def test_BinaryPopulation_ChooseRandomCreatures(SimpleBinaryPopulation):
  assert len(SimpleBinaryPopulation.ChooseRandomCreatures(3)) == 3
  
  
@pytest.fixture(scope='function')
def SimpleFloatingPointPopulation():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  binary_display = False
  precision = 4
  lower_fitness_bound = 0
  upper_fitness_bound = 100
  population_size = 5
  population = Population(goal_function, dimensions, lower_problem_bound, upper_problem_bound,
                          lower_fitness_bound, upper_fitness_bound,
                          binary_display, precision,
                          population_size)
  return population
 
def test_FloatingPointPopulation_EvaluatePopulation(SimpleFloatingPointPopulation):
  for creature in SimpleFloatingPointPopulation.population:
    assert creature.goal_value != False
    assert creature.fitness_value >= 0
  

@pytest.fixture(scope='function')
def SimpleBinaryCreature():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  precision = 4
  creature = BinaryCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision)
  return creature
  
def test_Creature_GenerateRandomFloatingPointValue(SimpleBinaryCreature):
  floating_point = SimpleBinaryCreature.GenerateRandomFloatingPointValue() == 20
  assert (-50 < floating_point) and (floating_point < 50)
  
def test_Creature_SetGoalValue(SimpleBinaryCreature):
  SimpleBinaryCreature.SetGoalValue()
  assert SimpleBinaryCreature.goal_value != False
  
def test_Creature_SetFitnessValue(SimpleBinaryCreature):
  SimpleBinaryCreature.SetFitnessValue(50, 20, 0, 40)
  assert SimpleBinaryCreature.fitness_value != False
  
  
def test_BinaryCreature_CalculateChromosomeLength(SimpleBinaryCreature):
  assert SimpleBinaryCreature.CalculateChromosomeLength() == 20
  
def test_BinaryCreature_CreateChromosome(SimpleBinaryCreature):
  chromosome_matrix = SimpleBinaryCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 20
  
def test_BinaryCreature_ConvertFloatingPointToBinary(SimpleBinaryCreature):
  assert SimpleBinaryCreature.ConvertFloatingPointToBinary(4.231514) == 568658
  
def test_BinaryCreature_ConvertBinaryToFloatingPoint(SimpleBinaryCreature):
  floating_point = SimpleBinaryCreature.ConvertBinaryToFloatingPoint(568658)
  assert (4.22 < floating_point) and (floating_point < 4.24)
  
def test_BinaryCreature_CreateBinaryChromosome(SimpleBinaryCreature):
  assert SimpleBinaryCreature.CreateBinaryChromosome(568658) == [1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0]
  
def test_BinaryCreature_ReverseList(SimpleBinaryCreature):
  assert SimpleBinaryCreature.ReverseList([1,2,3,4]) == [4,3,2,1]
  
def test_BinaryCreature_AddTrailingZeroesToChromosome(SimpleBinaryCreature):
  assert SimpleBinaryCreature.AddTrailingZeroesToChromosome([1,2,3,4]) == [1,2,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  assert SimpleBinaryCreature.AddTrailingZeroesToChromosome([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,0,0,0,0]) == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,0,0,0,0]
  
def test_BinaryCreature_ConvertBinaryChromosomeToBinaryValue(SimpleBinaryCreature):
  binary_value = SimpleBinaryCreature.ConvertBinaryChromosomeToBinaryValue([1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0])
  assert binary_value == 568658
  
def test_BinaryCreature_CalculatePoint(SimpleBinaryCreature):
  point = SimpleBinaryCreature.CalculatePoint()
  assert len(point) == 2
  assert point[1] < 50
  

@pytest.fixture(scope='function')
def SimpleFloatingPointCreature():
  goal_function = f3
  dimensions = 2
  lower_problem_bound = -50
  upper_problem_bound = 50
  creature = FloatingPointCreature(goal_function, dimensions, lower_problem_bound, upper_problem_bound)
  return creature
  
def test_FloatingPointCreature_CreateChromosome(SimpleFloatingPointCreature):
  chromosome_matrix = SimpleFloatingPointCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 1
  
def test_FloatingPointCreature_CreateFloatingPointChromosome(SimpleFloatingPointCreature):
  assert SimpleFloatingPointCreature.CreateFloatingPointChromosome(4.27487) == [4.27487]
  
def test_FloatingPointCreature_CalculatePoint(SimpleFloatingPointCreature):
  point = SimpleFloatingPointCreature.CalculatePoint()
  assert len(point) == 2
  assert point[1] < 50
  

#  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)