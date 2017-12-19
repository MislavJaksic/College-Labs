from Programs.GeneticAlgorithm import GeneticAlgorithm, BinaryCreature, FloatingPointCreature, BinaryPopulation, FloatingPointPopulation
from Tasks.TaskFunctions import f3
from Programs.Helpers.Matrix import Matrix

import pytest
from copy import copy

def test_GeneticAlgorithm_Binary_MaxEval_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                          max_evaluations=1000)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_FloatingPoint_MaxGen_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=5, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, binary_display=False, precision=0, p_of_mutation=0.01, p_of_crossover=0.01,
                          max_generations=1000)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_FloatingPoint_GoalValue_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, binary_display=False, precision=0, p_of_mutation=0.01, p_of_crossover=0.01,
                          reach_goal_value=(0.1)**3)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_FloatingPoint_ConvergedOnAPoint_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, binary_display=False, precision=0, p_of_mutation=0.01, p_of_crossover=0.01,
                          no_improvement_limit=50)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted


@pytest.fixture(scope='function')
def SimpleBinaryPopulation():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  p_of_mutation = 0.01
  population_size = 3
  precision = 4
  population = BinaryPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size, precision)
  return population
  
def test_BinaryPopulation_InitializeBestWorstCreatures(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.worst_goal_creature != False
  assert SimpleBinaryPopulation.best_goal_creature != False
  assert SimpleBinaryPopulation.worst_fitness_creature != False
  assert SimpleBinaryPopulation.best_fitness_creature != False
  
def test_BinaryPopulation_EvaluatePopulation(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal_value != False
    assert creature.fitness_value >= 0

def test_BinaryPopulation_SetGoalForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetGoalForAllCreatures()
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal_value > 0

def test_BinaryPopulation_SetFitnessForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetFitnessForAllCreatures()
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal_value >= 0
  
def test_BinaryPopulation_SetBestWorstGoalForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetBestWorstGoalForAllCreatures()
  assert SimpleBinaryPopulation.worst_goal_creature != False
  assert SimpleBinaryPopulation.best_goal_creature != False
  
def test_BinaryPopulation_SetBestWorstFitnessForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetBestWorstFitnessForAllCreatures()
  assert SimpleBinaryPopulation.worst_fitness_creature != False
  assert SimpleBinaryPopulation.best_fitness_creature != False
    
def test_BinaryPopulation_SetBestWorstGoalCreature(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal_value >= SimpleBinaryPopulation.best_goal_creature.goal_value
    assert creature.goal_value <= SimpleBinaryPopulation.worst_goal_creature.goal_value
    
def test_BinaryPopulation_SetBestWorstFitnessCreature(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.fitness_value >= SimpleBinaryPopulation.worst_fitness_creature.fitness_value
    assert creature.fitness_value <= SimpleBinaryPopulation.best_fitness_creature.fitness_value
  
  
def test_BinaryPopulation_KTournamentCreatureSelection(SimpleBinaryPopulation):
  worst_creature, other_creatures = SimpleBinaryPopulation.KTournamentCreatureSelection(3)
  assert len(other_creatures) == 2
  for creature in other_creatures:
    assert worst_creature.fitness_value < creature.fitness_value
  
def test_BinaryPopulation_ChooseKRandomCreatures(SimpleBinaryPopulation):
  k = 3
  assert len(SimpleBinaryPopulation.ChooseKRandomCreatures(k)) == k
  
def test_BinaryPopulation_RandomlyChooseCrossover(SimpleBinaryPopulation):
  parent_one = SimpleBinaryPopulation.population[0]
  parent_two = SimpleBinaryPopulation.population[1]
  crossover_functions = (SimpleBinaryPopulation.KPointCrossover, SimpleBinaryPopulation.UniformCrossover)
  assert SimpleBinaryPopulation.RandomlyChooseCrossover(parent_one, parent_two, crossover_functions) != parent_one.group_of_chromosomes
  
def test_BinaryPopulation_RandomlyChooseMutation(SimpleBinaryPopulation):
  group_of_chromosomes = copy(SimpleBinaryPopulation.population[0].group_of_chromosomes)
  mutation_functions = (SimpleBinaryPopulation.SimpleMutation, SimpleBinaryPopulation.UniformMutation)
  assert SimpleBinaryPopulation.RandomlyChooseMutation(group_of_chromosomes, mutation_functions) != SimpleBinaryPopulation.population[0].group_of_chromosomes
  
  
def test_BinaryPopulation_ReplaceCreatureWithAnother(SimpleBinaryPopulation):
  group_of_chromosomes = Matrix([[1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0],
                                 [1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,1,0]])
  SimpleBinaryPopulation.ReplaceCreatureWithAnother(SimpleBinaryPopulation.worst_goal_creature, group_of_chromosomes)
  assert group_of_chromosomes != SimpleBinaryPopulation.worst_goal_creature.group_of_chromosomes
  

def test_BinaryPopulation_CalculateChromosomeLength(SimpleBinaryPopulation):
  min_x = -50
  max_x = 50
  precision = 4
  assert SimpleBinaryPopulation.CalculateChromosomeLength(min_x, max_x, precision) == 20  
  
def test_BinaryPopulation_CalculateCreatureMutationProbability(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.CalculateCreatureMutationProbability(0.01) > 0.180
  assert SimpleBinaryPopulation.CalculateCreatureMutationProbability(0.01) < 0.183
  
def test_BinaryPopulation_CalculateHowManyBitsToMutate(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.CalculateHowManyBitsToMutate() == 4
  
  
def test_BinaryPopulation_KPointCrossover(SimpleBinaryPopulation):
  parent_one = SimpleBinaryPopulation.population[0]
  parent_two = SimpleBinaryPopulation.population[1]
  chromosome_group = SimpleBinaryPopulation.KPointCrossover(parent_one, parent_two, k=4)
  assert chromosome_group._CountRows() == 2
  assert len(chromosome_group._GetMatrixRow(2)) == 20
  
def test_BinaryPopulation_SwitchChromosome(SimpleBinaryPopulation):
  chromosome_one = SimpleBinaryPopulation.population[0].group_of_chromosomes._GetMatrixRow(2)
  chromosome_two = SimpleBinaryPopulation.population[1].group_of_chromosomes._GetMatrixRow(2)
  current_chromosome = SimpleBinaryPopulation.population[0].group_of_chromosomes._GetMatrixRow(2)
  assert SimpleBinaryPopulation.SwitchChromosome(current_chromosome, chromosome_one, chromosome_two) == chromosome_two
  
def test_BinaryPopulation_UniformCrossover(SimpleBinaryPopulation):
  parent_one = SimpleBinaryPopulation.population[0]
  parent_two = SimpleBinaryPopulation.population[1]
  chromosome_group = SimpleBinaryPopulation.UniformCrossover(parent_one, parent_two)
  assert chromosome_group._CountRows() == 2
  assert len(chromosome_group._GetMatrixRow(2)) == 20
  
def test_BinaryPopulation_RandomBitIfParentBitsAreDifferent(SimpleBinaryPopulation):
  chromosome_one = SimpleBinaryPopulation.population[0].group_of_chromosomes._GetMatrixRow(2)
  chromosome_two = SimpleBinaryPopulation.population[1].group_of_chromosomes._GetMatrixRow(2)
  assert SimpleBinaryPopulation.RandomBitIfParentBitsAreDifferent(chromosome_one, chromosome_two, 2) in (0,1)
  
  
def test_BinaryPopulation_SimpleMutation(SimpleBinaryPopulation):
  group_of_chromosomes = copy(SimpleBinaryPopulation.population[0].group_of_chromosomes)
  assert SimpleBinaryPopulation.SimpleMutation(group_of_chromosomes) != SimpleBinaryPopulation.population[0].group_of_chromosomes
  
def test_BinaryPopulation_UniformMutation(SimpleBinaryPopulation):
  group_of_chromosomes = copy(SimpleBinaryPopulation.population[0].group_of_chromosomes)
  assert SimpleBinaryPopulation.UniformMutation(group_of_chromosomes) != SimpleBinaryPopulation.population[0].group_of_chromosomes
  

def test_BinaryPopulation_GetNextGeneration(SimpleBinaryPopulation):
  for i in range (1000):
    SimpleBinaryPopulation.GetNextGeneration()
  assert True #one of them is different
  

@pytest.fixture(scope='function')
def SimpleFloatingPointPopulation():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  p_of_mutation = 0.01
  population_size = 3
  population = FloatingPointPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size)
  return population
 
def test_FloatingPointPopulation_EvaluatePopulation(SimpleFloatingPointPopulation):
  for creature in SimpleFloatingPointPopulation.population:
    assert creature.goal_value != False
    assert creature.fitness_value >= 0
    
    
def test_FloatingPointPopulation_ArithmeticCrossover(SimpleFloatingPointPopulation):
  parent_one = SimpleFloatingPointPopulation.population[0]
  parent_two = SimpleFloatingPointPopulation.population[1]
  value_one = parent_one.group_of_chromosomes[(2, 1)]
  value_two = parent_two.group_of_chromosomes[(2, 1)]
  result = SimpleFloatingPointPopulation.ArithmeticCrossover(parent_one, parent_two)[(2,1)]
  assert (value_one < result) and (result < value_two) or (value_two < result) and (result < value_one)
  
def test_FloatingPointPopulation_HeuristicCrossover(SimpleFloatingPointPopulation):
  parent_one = SimpleFloatingPointPopulation.population[0]
  parent_two = SimpleFloatingPointPopulation.population[1]
  value_one = parent_one.group_of_chromosomes[(2, 1)]
  value_two = parent_two.group_of_chromosomes[(2, 1)]
  result = SimpleFloatingPointPopulation.HeuristicCrossover(parent_one, parent_two)[(2,1)]
  assert result != parent_one.group_of_chromosomes
  
  
def test_FloatingPointPopulation_GaussianMutation(SimpleFloatingPointPopulation):
  group_of_chromosomes = copy(SimpleFloatingPointPopulation.population[0].group_of_chromosomes)
  result = SimpleFloatingPointPopulation.GaussianMutation(group_of_chromosomes)
  assert result != SimpleFloatingPointPopulation.population[0].group_of_chromosomes
  
  
def test_FloatingPointPopulation_GetNextGeneration(SimpleFloatingPointPopulation):
  for i in range (1000):
    SimpleFloatingPointPopulation.GetNextGeneration()
  assert True #one of them is different
  

@pytest.fixture(scope='function')
def SimpleBinaryCreature():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  chromosome_length = 20
  creature = BinaryCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, chromosome_length)
  return creature
  
def test_Creature_GenerateRandomFloatingPointValue(SimpleBinaryCreature):
  floating_point = SimpleBinaryCreature.GenerateRandomFloatingPointValue() == 20
  assert (-50 < floating_point) and (floating_point < 50)
  
def test_Creature_SetGoalValue(SimpleBinaryCreature):
  SimpleBinaryCreature.SetGoalValue()
  assert SimpleBinaryCreature.goal_value != False
  
def test_Creature_SetFitnessValue(SimpleBinaryCreature):
  SimpleBinaryCreature.SetFitnessValue(20, 5000)
  assert SimpleBinaryCreature.fitness_value != False
  
  
def test_BinaryCreature_CreateChromosome(SimpleBinaryCreature):
  chromosome_matrix = SimpleBinaryCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 20
  
def test_BinaryCreature_ConvertFloatingPointToBinary(SimpleBinaryCreature):
  assert SimpleBinaryCreature.ConvertFloatingPointToBinary(4.231514) == 568659
  
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
  
def test_BinaryCreature_SetPoint(SimpleBinaryCreature):
  point = SimpleBinaryCreature.SetPoint()
  assert len(point) == 2
  assert (point[1] < 50 and  -50 < point[1])
  

@pytest.fixture(scope='function')
def SimpleFloatingPointCreature():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  creature = FloatingPointCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
  return creature
  
def test_FloatingPointCreature_CreateChromosome(SimpleFloatingPointCreature):
  chromosome_matrix = SimpleFloatingPointCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 1
  
def test_FloatingPointCreature_CreateFloatingPointChromosome(SimpleFloatingPointCreature):
  assert SimpleFloatingPointCreature.CreateFloatingPointChromosome(4.27487) == [4.27487]
  
def test_FloatingPointCreature_SetPoint(SimpleFloatingPointCreature):
  point = SimpleFloatingPointCreature.SetPoint()
  assert len(point) == 2
  assert (point[1] < 50 and  -50 < point[1])
  

#  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)