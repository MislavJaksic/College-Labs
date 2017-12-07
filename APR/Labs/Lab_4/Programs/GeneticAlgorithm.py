import random, math
from numpy.random import normal

from Helpers.Matrix import Matrix

class GeneticAlgorithm(object):
  """
  #create population
  #eval population
  #repeat:
  #  randomly choose 3 creatures 
  #  kill the worst among the them
  #  new_creature = crossover(other two creatures)
  #  mutate new_creature with probability p_M
  #  eval new_creature
  #  add new_creature to population
  #until(stop condition)
  """
  def __init__(self, goal_function, dimensions, problem_bounds,
                     fitness_bounds=(0,100), population_size=100, binary_display=True, precision=2, p_of_mutation=0.01, p_of_crossover=0.1,
                     max_evaluations=1000):
    self.goal_function = goal_function #!= as the fitness_function
    self.dimensions = dimensions
    self.min_x = problem_bounds[0] #== dg
    self.max_x = problem_bounds[1] #== gg
    
    self.min_fitness = fitness_bounds[0] #== a
    self.max_fitness = fitness_bounds[1] #== b
    self.population_size = population_size
    self.binary_display = binary_display
    self.precision = precision
    self.p_of_mutation = p_of_mutation
    self.p_of_crossover = p_of_crossover #== not used
    
    self.max_evaluations = maximum_evaluations
      
  def CreatePopulation(self):
    population = BinaryPopulation(self.goal_function, self.dimensions, self.min_x, self.max_x,
                            self.min_fitness, self.max_fitness,
                            self.binary_display, self.precision)
  
  
class Population(object):
  def __init__(self, min_fitness, max_fitness, population_size):
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    self.population_size = population_size
    
    self.worst_goal_creature = False
    self.best_goal_creature = False
    
    self.worst_fitness_creature = False
    self.best_fitness_creature = False
      
  def EvaluatePopulation(self):
    for creature in self.population:
      creature.SetGoalValue()
      self.SetBestWorstGoalCreature(creature)
      
    for creature in self.population:
      creature.SetFitnessValue(self.best_goal_creature.goal_value, self.worst_goal_creature.goal_value)
      self.SetBestWorstFitnessCreature(creature)
    
  def SetBestWorstGoalCreature(self, creature):
    if self.IsUninitialized(self.best_goal_creature):
      self.best_goal_creature = creature
      
    if self.IsUninitialized(self.worst_goal_creature):
      self.worst_goal_creature = creature
    
    if self.IsBetterThen(creature.goal_value, self.best_goal_creature.goal_value):
      self.best_goal_creature = creature
      
    if self.IsWorseThen(creature.goal_value, self.worst_goal_creature.goal_value):
      self.worst_goal_creature = creature
      
  def SetBestWorstFitnessCreature(self, creature):
    if self.IsUninitialized(self.best_fitness_creature):
      self.best_fitness_creature = creature
      
    if self.IsUninitialized(self.worst_fitness_creature):
      self.worst_fitness_creature = creature
    
    if self.IsBetterThen(self.best_fitness_creature.fitness_value, creature.fitness_value):
      self.best_fitness_creature = creature
      
    if self.IsWorseThen(self.worst_fitness_creature.fitness_value, creature.fitness_value):
      self.worst_fitness_creature = creature
      
  def IsUninitialized(self, variable):
    if variable == False:
      return True
    return False
  
  def IsBetterThen(self, value_one, value_two):
    if value_one < value_two:
      return True
    return False
    
  def IsWorseThen(self, value_one, value_two):
    if value_one > value_two:
      return True
    return False
  
  
  def KTournamentCreatureSelection(self, k=3):
    selected_creatures = self.ChooseKRandomCreatures(k)
    
    worst_fitness_creature = False
    other_creatures = []
    for i in selected_creatures:
      if self.IsUninitialized(worst_fitness_creature):
        worst_fitness_creature = self.population[i]
      
      elif self.IsWorseThen(worst_fitness_creature.fitness_value, self.population[i].fitness_value):
        other_creatures.append(worst_fitness_creature)
        worst_fitness_creature = self.population[i]
        
      else:
        other_creatures.append(self.population[i])
        
    return worst_fitness_creature, other_creatures
    
  def ChooseKRandomCreatures(self, k):
    selected_creatures = []
    count = 0
    while (k > count):
      random_int = random.randint(0, len(self.population) - 1)
      if random_int not in selected_creatures:
        selected_creatures.append(random_int)
        count += 1
        
    return selected_creatures
  
  def ReplaceCreatureWithAnother(self, creature, new_group_of_chromosomes):
    pass
  

class BinaryPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size, precision):
    super(BinaryPopulation, self).__init__(min_fitness, max_fitness, population_size)
    
    self.chromosome_length = self.CalculateChromosomeLength(min_x, max_x, precision)
    
    self.population = self.CreateBinaryPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.mutate_bits = self.CalculateHowManyBitsToMutate(p_of_mutation)
    
    self.EvaluatePopulation()
    
  def CalculateChromosomeLength(self, min_x, max_x, precision):
    interval_length = max_x - min_x
    log_10_of_floating_point_interval = math.log10(1 + interval_length * (10**precision))
    log10_of_2 = math.log10(2)
    chromosome_length = math.ceil(log_10_of_floating_point_interval / log10_of_2)
    return int(chromosome_length)
    
  def CalculateHowManyBitsToMutate(self, p_of_mutation):
    mutation_frequency = 1 / float(1 - (1 - p_of_mutation)**self.population[0].chromosome_length)
    return int(self.population[0].chromosome_length / math.floor(mutation_frequency))
  
  def CreateBinaryPopulation(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    current_population_size = 0
    population = []
    while (self.population_size > current_population_size):
      creature = BinaryCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, self.chromosome_length)
      population.append(creature)
      current_population_size += 1
      
    return population
    
    
  def KPointCrossover(self, parent_one, parent_two, k=1):
    """
    C1: 0011 0000 <- copy from it until crossover bit
    C2: 1101 1010 <- then continue by copying from here
    crossover point at 3 (k=1)
    -------------
    N:  0011 1010
    """
    crossover_points = []
    for i in range(k):
      crossover_points.append(random.randint(1, parent_one.chromosome_length - 2))
    crossover_points.sort()
    
    new_group_of_chromosomes = []
    for dimension in range(1, parent_one.dimensions + 1):
      
      new_chromosome = []
      current_chromosome = parent_one.group_of_chromosomes._GetMatrixRow(dimension)
      for i in range(parent_one.chromosome_length):
        new_chromosome.append(current_chromosome[i])
        if i in crossover_points:
          chromosome_one = parent_one.group_of_chromosomes._GetMatrixRow(dimension)
          chromosome_two = parent_two.group_of_chromosomes._GetMatrixRow(dimension)
          current_chromosome = self.SwitchChromosome(current_chromosome, chromosome_one, chromosome_two)
      
      new_group_of_chromosomes.append(new_chromosome)
    
    return Matrix(new_group_of_chromosomes)
    
  def SwitchChromosome(self, current_chromosome, chromosome_one, chromosome_two):
    if current_chromosome == chromosome_one:
      current_chromosome = chromosome_two
    else:
      current_chromosome = chromosome_one
    
    return current_chromosome

  def UniformCrossover(self, parent_one, parent_two):
    """
    C1: 0000 1101 <- copy if C1 and C2 are the same
    C2: 0011 1100
    R:  0101 0011 <- if not, copy it from a random one
    -------------
    N:  0001 1101
    """
    new_group_of_chromosomes = []
    for dimension in range(1, parent_one.dimensions + 1):
      
      new_chromosome = []
      for i in range(parent_one.chromosome_length):
        chromosome_one = parent_one.group_of_chromosomes._GetMatrixRow(dimension)
        chromosome_two = parent_two.group_of_chromosomes._GetMatrixRow(dimension)
        bit = self.RandomBitIfParentBitsAreDifferent(chromosome_one, chromosome_two, i)
        new_chromosome.append(bit)
        
      new_group_of_chromosomes.append(new_chromosome)
    
    return Matrix(new_group_of_chromosomes)
    
  def RandomBitIfParentBitsAreDifferent(self, chromosome_one, chromosome_two, i):
    if chromosome_one[i] == chromosome_two[i]:
      bit = chromosome_one[i]
    else:
      bit = random.randint(0,1)
      
    return bit
    
    
  def SimpleMutation(self, group_of_chromosomes):
    for i in range(self.mutate_bits):
      mutate_column = random.randint(1, self.population[0].chromosome_length)
      for row in range(1, self.population[0].dimensions + 1):
        if group_of_chromosomes[(row, mutate_column)] == 0:
          group_of_chromosomes[(row, mutate_column)] = 1
        else:
          group_of_chromosomes[(row, mutate_column)] = 0
          
    return group_of_chromosomes
    
  def UniformMutation(self, group_of_chromosomes):
    for column in range(1, self.population[0].chromosome_length + 1):
      for row in range(1, self.population[0].dimensions + 1):
        if group_of_chromosomes[(row, column)] == 0:
          group_of_chromosomes[(row, column)] = 1
        else:
          group_of_chromosomes[(row, column)] = 0
          
    return group_of_chromosomes
    
    
  def GetNextGeneration(self):
    worst_fitness_creature, other_creatures = self.KTournamentCreatureSelection(k=3)
    parent_one = other_creatures[0]
    parent_two = other_creatures[1]
    
    
    UniformCrossover()
    
class FloatingPointPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size):
    super(FloatingPointPopulation, self).__init__(min_fitness, max_fitness, population_size)
    
    self.population = self.CreateFloatingPointPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.EvaluatePopulation()
  
  def CreateFloatingPointPopulation(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    current_population_size = 0
    population = []
    while (self.population_size > current_population_size):
      creature = FloatingPointCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
      population.append(creature)
      current_population_size += 1
      
    return population
    
    
  def ArithmeticCrossover(self, parent_one, parent_two):
    new_group_of_chromosomes = []
    a = random.random()
    for dimension in range(1, parent_one.dimensions + 1):
      new_chromosome = []
      
      value_one = parent_one.group_of_chromosomes[(dimension, 1)]
      value_two = parent_two.group_of_chromosomes[(dimension, 1)]
      
      new_value = a * value_one + (1 - a) * value_two
      new_chromosome.append(new_value)
      
      new_group_of_chromosomes.append(new_chromosome)
    
    return Matrix(new_group_of_chromosomes)
    
  def HeuristicCrossover(self, parent_one, parent_two):
    new_group_of_chromosomes = []
    a = random.random()
    for dimension in range(1, parent_one.dimensions + 1):
      new_chromosome = []
      
      if parent_one.fitness_value > parent_two.fitness_value:
        value_one = parent_two.group_of_chromosomes[(dimension, 1)]
        value_two = parent_one.group_of_chromosomes[(dimension, 1)]
      else:
        value_one = parent_one.group_of_chromosomes[(dimension, 1)]
        value_two = parent_two.group_of_chromosomes[(dimension, 1)]
      
      new_value = a * (value_two - value_one) + value_two
      new_chromosome.append(new_value)
      
      new_group_of_chromosomes.append(new_chromosome)
    
    return Matrix(new_group_of_chromosomes)
    
    
  def GaussianMutation(self, group_of_chromosomes):
    for row in range(1, self.population[0].dimensions + 1):
      group_of_chromosomes[(row, 1)] = normal(group_of_chromosomes[(row, 1)], 1.0)
      
    return group_of_chromosomes
    
  
class Creature(object):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    self.goal_function = goal_function
    self.dimensions = dimensions
    self.min_x = min_x
    self.max_x = max_x
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    
    self.group_of_chromosomes = False
    self.point = False
    
    self.goal_value = False
    self.fitness_value = False
    
  def GenerateRandomFloatingPointValue(self):
    floating_point = random.uniform(self.min_x, self.max_x)
    return floating_point
   
  def SetGoalValue(self):
    goal_value = self.goal_function(self.point)
    self.goal_value = goal_value
    
  def SetFitnessValue(self, best_goal_value, worst_goal_value):
    """
    Windowing:
    Fi = a + (b - a) * ((fi - f_worst) / (f_best - f_worst))
    """
    fitness_interval_length = self.max_fitness - self.min_fitness
    goal_value_minus_worst_goal_value = self.goal_value - worst_goal_value
    best_worst_goal_difference = float(best_goal_value - worst_goal_value)
    
    self.fitness_value = self.min_fitness + (fitness_interval_length * goal_value_minus_worst_goal_value) / best_worst_goal_difference
   
   
class BinaryCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, chromosome_length):
    super(BinaryCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    self.chromosome_length = chromosome_length
    
    self.group_of_chromosomes = self.CreateChromosome()
    self.point = self.CalculatePoint()
    
  def CreateChromosome(self):
    group_of_chromosomes = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloatingPointValue()
      random_binary_number = self.ConvertFloatingPointToBinary(random_number)
      
      chromosome = self.CreateBinaryChromosome(random_binary_number)
      group_of_chromosomes.append(chromosome)
      
    return Matrix(group_of_chromosomes)
  
  def ConvertFloatingPointToBinary(self, floating_point):
    interval_length = self.max_x - self.min_x
    binary_value = (floating_point - self.min_x) / interval_length * (2**self.chromosome_length)
    return int(binary_value)
    
  def ConvertBinaryToFloatingPoint(self, binary_value):
    floating_binary_value = float(binary_value)
    interval_length = self.max_x - self.min_x
    floating_point = self.min_x + floating_binary_value / (2**self.chromosome_length) * interval_length
    return floating_point
    
  def CreateBinaryChromosome(self, binary_value):
    binary_chromosome = []
    dividend = binary_value
    divisor = 2
    while (dividend > 0):
      remainder = dividend % divisor
      binary_chromosome.append(remainder)
      dividend = dividend / divisor
      
    binary_chromosome = self.AddTrailingZeroesToChromosome(binary_chromosome)
    binary_chromosome = self.ReverseList(binary_chromosome)
    
    return binary_chromosome
      
  def ReverseList(self, list):
    reverse_list = []
    for i in range(len(list)):
      element = list[(-1)*i - 1]
      reverse_list.append(element)
      
    return reverse_list
      
  def AddTrailingZeroesToChromosome(self, chromosome):
    for i in range(self.chromosome_length - len(chromosome)):
      chromosome.append(0)
      
    return chromosome
    
  def ConvertBinaryChromosomeToBinaryValue(self, binary_chromosome):
    reverse_binary_chromosome = self.ReverseList(binary_chromosome)
    
    bit_position = 0
    binary_value = 0
    for bit in reverse_binary_chromosome:
      binary_value += bit * (2**bit_position)
      bit_position += 1
      
    return binary_value
    
  def CalculatePoint(self):
    point = []
    for row in range(1, self.dimensions + 1):
      binary_value = self.ConvertBinaryChromosomeToBinaryValue(self.group_of_chromosomes._GetMatrixRow(row))
      floating_point = self.ConvertBinaryToFloatingPoint(binary_value)
      point.append(floating_point)
      
    return point
    
    
class FloatingPointCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    super(FloatingPointCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    self.group_of_chromosomes = self.CreateChromosome()
    self.point = self.CalculatePoint()
    
  def CreateChromosome(self):
    group_of_chromosomes = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloatingPointValue()
      
      chromosome = self.CreateFloatingPointChromosome(random_number)
      group_of_chromosomes.append(chromosome)
      
    return Matrix(group_of_chromosomes)
    
  def CreateFloatingPointChromosome(self, floating_point):
    floating_point_chromosome = []
    floating_point_chromosome.append(floating_point)
    
    return floating_point_chromosome
      
  def CalculatePoint(self):
    point = []
    for row in range(1, self.dimensions + 1):
      point.append(self.group_of_chromosomes._GetMatrixRow(row)[0])
      
    return point
    