from Programs.GeneticAlgorithm import GeneticAlgorithm, BinaryCreature, FloatCreature, BinaryPopulation, FloatPopulation
from Tasks.TaskFunctions import f3
from Programs.Helpers.Matrix import Matrix

import pytest
from copy import copy

def test_GeneticAlgorithm_Binary_MaxEval_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, display="binary", precision=0, p_of_mutation=0.01, 
                          max_evaluations=1000)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_Float_MaxGen_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=5, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, display="float", precision=0, p_of_mutation=0.01, 
                          max_generations=1000)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_Float_GoalValue_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, display="float", precision=0, p_of_mutation=0.01, 
                          reach_goal=(0.1)**3)
  result = algo.SolveProblem()
  assert True #the result cannot be interpreted
  
def test_GeneticAlgorithm_Float_ConvergedOnAPoint_f3():
  algo = GeneticAlgorithm(goal_function=f3, dimensions=2, problem_bounds=(-50,150),
                          fitness_bounds=(0,100), population_size=100, display="float", precision=0, p_of_mutation=0.01, 
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
  population = BinaryPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, population_size, precision, p_of_mutation)
  return population
  
def test_BinaryPopulation_InitializeBestWorstCreatures(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.worst_goal_creature != False
  assert SimpleBinaryPopulation.best_goal_creature != False
  assert SimpleBinaryPopulation.worst_fitness_creature != False
  assert SimpleBinaryPopulation.best_fitness_creature != False
  
def test_BinaryPopulation_EvaluatePopulation(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal != False
    assert creature.fitness >= 0

def test_BinaryPopulation_SetGoalForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetGoalForAllCreatures()
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal > 0

def test_BinaryPopulation_SetFitnessForAllCreatures(SimpleBinaryPopulation):
  SimpleBinaryPopulation.SetFitnessForAllCreatures()
  for creature in SimpleBinaryPopulation.population:
    assert creature.goal >= 0
  
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
    assert creature.goal >= SimpleBinaryPopulation.best_goal_creature.goal
    assert creature.goal <= SimpleBinaryPopulation.worst_goal_creature.goal
    
def test_BinaryPopulation_SetBestWorstFitnessCreature(SimpleBinaryPopulation):
  for creature in SimpleBinaryPopulation.population:
    assert creature.fitness >= SimpleBinaryPopulation.worst_fitness_creature.fitness
    assert creature.fitness <= SimpleBinaryPopulation.best_fitness_creature.fitness
  
  
def test_BinaryPopulation_KTournamentCreatureSelection(SimpleBinaryPopulation):
  worst_creature, other_creatures = SimpleBinaryPopulation.KTournamentCreatureSelection(3)
  assert len(other_creatures) == 2
  for creature in other_creatures:
    assert worst_creature.fitness < creature.fitness
  
def test_BinaryPopulation_ChooseKRandomCreatures(SimpleBinaryPopulation):
  k = 3
  assert len(SimpleBinaryPopulation.ChooseKRandomCreatures(k)) == k
  
def test_BinaryPopulation_RandomlyChooseCrossover(SimpleBinaryPopulation):
  parent_one = SimpleBinaryPopulation.population[0]
  parent_two = SimpleBinaryPopulation.population[1]
  crossover_functions = (SimpleBinaryPopulation.KPointCrossover, SimpleBinaryPopulation.UniformCrossover)
  assert SimpleBinaryPopulation.RandomlyChooseCrossover(parent_one, parent_two, crossover_functions) != parent_one.chromosomes
  
def test_BinaryPopulation_RandomlyChooseMutation(SimpleBinaryPopulation):
  chromosomes = copy(SimpleBinaryPopulation.population[0].chromosomes)
  mutation_functions = (SimpleBinaryPopulation.SimpleMutation, SimpleBinaryPopulation.UniformMutation)
  assert SimpleBinaryPopulation.RandomlyChooseMutation(chromosomes, mutation_functions) != SimpleBinaryPopulation.population[0].chromosomes
  
def test_BinaryPopulation_ReplaceCreatureWithAnother(SimpleBinaryPopulation):
  chromosomes = Matrix([[1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0],
                        [1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,1,0]])
  SimpleBinaryPopulation.ReplaceCreatureWithAnother(SimpleBinaryPopulation.worst_goal_creature, chromosomes)
  assert chromosomes != SimpleBinaryPopulation.worst_goal_creature.chromosomes
  
def test_BinaryPopulation_IsReplacingWorstCreature(SimpleBinaryPopulation):
  assert SimpleBinaryPopulation.IsReplacingWorstCreature(SimpleBinaryPopulation.worst_goal_creature)
  
def test_BinaryPopulation__str__(SimpleBinaryPopulation):
  result = str(SimpleBinaryPopulation)
  assert result[:15] == "Population size"
  

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
  chromosome_one = SimpleBinaryPopulation.population[0].chromosomes._GetMatrixRow(2)
  chromosome_two = SimpleBinaryPopulation.population[1].chromosomes._GetMatrixRow(2)
  current_chromosome = SimpleBinaryPopulation.population[0].chromosomes._GetMatrixRow(2)
  assert SimpleBinaryPopulation.SwitchChromosome(current_chromosome, chromosome_one, chromosome_two) == chromosome_two
  
def test_BinaryPopulation_UniformCrossover(SimpleBinaryPopulation):
  parent_one = SimpleBinaryPopulation.population[0]
  parent_two = SimpleBinaryPopulation.population[1]
  chromosome_group = SimpleBinaryPopulation.UniformCrossover(parent_one, parent_two)
  assert chromosome_group._CountRows() == 2
  assert len(chromosome_group._GetMatrixRow(2)) == 20
  
def test_BinaryPopulation_RandomBitIfParentBitsAreDifferent(SimpleBinaryPopulation):
  chromosome_one = SimpleBinaryPopulation.population[0].chromosomes._GetMatrixRow(2)
  chromosome_two = SimpleBinaryPopulation.population[1].chromosomes._GetMatrixRow(2)
  assert SimpleBinaryPopulation.RandomBitIfParentBitsAreDifferent(chromosome_one, chromosome_two, 2) in (0,1)
  
  
def test_BinaryPopulation_SimpleMutation(SimpleBinaryPopulation):
  chromosomes = copy(SimpleBinaryPopulation.population[0].chromosomes)
  assert SimpleBinaryPopulation.SimpleMutation(chromosomes) != SimpleBinaryPopulation.population[0].chromosomes
  
def test_BinaryPopulation_UniformMutation(SimpleBinaryPopulation):
  chromosomes = copy(SimpleBinaryPopulation.population[0].chromosomes)
  assert SimpleBinaryPopulation.UniformMutation(chromosomes) != SimpleBinaryPopulation.population[0].chromosomes
  

def test_BinaryPopulation_GetNextGeneration(SimpleBinaryPopulation):
  for i in range (5000):
    SimpleBinaryPopulation.GetNextGeneration()
  assert True #to make sure the algorithm doesn't malfunction
  

@pytest.fixture(scope='function')
def SimpleFloatPopulation():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  p_of_mutation = 0.01
  population_size = 3
  population = FloatPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, population_size, p_of_mutation)
  return population
 
def test_FloatPopulation_EvaluatePopulation(SimpleFloatPopulation):
  for creature in SimpleFloatPopulation.population:
    assert creature.goal != False
    assert creature.fitness >= 0
    
    
def test_FloatPopulation_ArithmeticCrossover(SimpleFloatPopulation):
  parent_one = SimpleFloatPopulation.population[0]
  parent_two = SimpleFloatPopulation.population[1]
  value_one = parent_one.chromosomes[(2, 1)]
  value_two = parent_two.chromosomes[(2, 1)]
  result = SimpleFloatPopulation.ArithmeticCrossover(parent_one, parent_two)[(2,1)]
  assert (value_one < result) and (result < value_two) or (value_two < result) and (result < value_one)
  
def test_FloatPopulation_HeuristicCrossover(SimpleFloatPopulation):
  parent_one = SimpleFloatPopulation.population[0]
  parent_two = SimpleFloatPopulation.population[1]
  value_one = parent_one.chromosomes[(2, 1)]
  value_two = parent_two.chromosomes[(2, 1)]
  result = SimpleFloatPopulation.HeuristicCrossover(parent_one, parent_two)[(2,1)]
  assert (value_one < result) and (value_two < result) or (value_one > result) and (value_two > result)
  
def test_FloatPopulation_GaussianMutation(SimpleFloatPopulation):
  sample_chromosomes = SimpleFloatPopulation.population[0].chromosomes
  mutated_chromosomes = SimpleFloatPopulation.GaussianMutation(sample_chromosomes)
  assert mutated_chromosomes != sample_chromosomes
  
  
def test_FloatPopulation_GetNextGeneration(SimpleFloatPopulation):
  for i in range (5000):
    SimpleFloatPopulation.GetNextGeneration()
  assert True #to make sure the algorithm doesn't malfunction
  
def test_FloatPopulation_IsRandomlyMutateCreature(SimpleFloatPopulation):
  assert SimpleFloatPopulation.IsRandomlyMutateCreature() in (True, False)
  

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
  
def test_Creature_GenerateRandomFloat(SimpleBinaryCreature):
  floating = SimpleBinaryCreature.GenerateRandomFloat()
  assert (SimpleBinaryCreature.min_x < floating) and (floating < SimpleBinaryCreature.max_x)
  
def test_Creature_SetChromosomes(SimpleBinaryCreature):
  assert SimpleBinaryCreature.SetChromosomes(Matrix([[1],[0]]))
  
def test_Creature_SetGoal(SimpleBinaryCreature):
  SimpleBinaryCreature.SetGoal()
  assert SimpleBinaryCreature.goal != False
  
def test_Creature_SetFitness(SimpleBinaryCreature):
  worst_goal = 5000
  SimpleBinaryCreature.SetFitness(worst_goal)
  assert SimpleBinaryCreature.fitness != False
  
def test_Creature_SetWindowedFitness(SimpleBinaryCreature):
  best_goal = 0
  worst_goal = 100
  SimpleBinaryCreature.SetWindowedFitness(best_goal, worst_goal)
  assert SimpleBinaryCreature.fitness == 100
  
def test_BinaryCreature__str__(SimpleBinaryCreature):
  result = str(SimpleBinaryCreature)
  assert result[:15] == "Problem_bounds:"
  
  
def test_BinaryCreature_CreateChromosome(SimpleBinaryCreature):
  chromosome_matrix = SimpleBinaryCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 20
  
def test_BinaryCreature_ConvertFloatToBinary(SimpleBinaryCreature):
  assert SimpleBinaryCreature.ConvertFloatToBinary(4.231514) == 568658
  
def test_BinaryCreature_ConvertBinaryToFloat(SimpleBinaryCreature):
  floating = SimpleBinaryCreature.ConvertBinaryToFloat(568658)
  assert (4.22 < floating) and (floating < 4.24)
  
def test_BinaryCreature_CreateBinaryChromosome(SimpleBinaryCreature):
  assert SimpleBinaryCreature.CreateBinaryChromosome(568658) == [1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0]
  
def test_BinaryCreature_ReverseList(SimpleBinaryCreature):
  assert SimpleBinaryCreature.ReverseList([1,2,3,4]) == [4,3,2,1]
  
def test_BinaryCreature_AddTrailingZeroesToChromosome(SimpleBinaryCreature):
  insufficiently_long_chromosome = [1,2,3,4]
  sufficiently_long_chromosome = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,0,0,0,0]
  assert SimpleBinaryCreature.AddTrailingZeroesToChromosome(insufficiently_long_chromosome) == [1,2,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  assert SimpleBinaryCreature.AddTrailingZeroesToChromosome(sufficiently_long_chromosome) == sufficiently_long_chromosome
  
def test_BinaryCreature_ConvertBinaryChromosomeToBinary(SimpleBinaryCreature):
  binary = SimpleBinaryCreature.ConvertBinaryChromosomeToBinary([1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0])
  assert binary == 568658
  
def test_BinaryCreature_SetPoint(SimpleBinaryCreature):
  point = SimpleBinaryCreature.SetPoint()
  assert len(point) == 2
  assert (point[1] < SimpleBinaryCreature.max_x) and (SimpleBinaryCreature.min_x < point[1])
   

@pytest.fixture(scope='function')
def SimpleFloatCreature():
  goal_function = f3
  dimensions = 2
  min_x = -50
  max_x = 50
  min_fitness = 0
  max_fitness = 100
  creature = FloatCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
  return creature
  
def test_FloatCreature_CreateChromosome(SimpleFloatCreature):
  chromosome_matrix = SimpleFloatCreature.CreateChromosome()
  assert chromosome_matrix._CountRows() == 2
  assert chromosome_matrix._CountColumns() == 1
  
def test_FloatCreature_CreateFloatChromosome(SimpleFloatCreature):
  random_float = 4.27487
  assert SimpleFloatCreature.CreateFloatChromosome(random_float) == [random_float]
  
def test_FloatCreature_SetPoint(SimpleFloatCreature):
  point = SimpleFloatCreature.SetPoint()
  assert len(point) == 2
  assert (point[1] < SimpleFloatCreature.max_x) and (SimpleFloatCreature.min_x < point[1])


  
  
  
""""""