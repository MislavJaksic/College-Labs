import random, math

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
                     fitness_bounds=(0,100), population_size=100, binary_display=True, precision=2, p_of_mutation=0.1, crossover_probability=0.1,
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
    self.p_of_crossover = p_of_crossover
    
    self.max_evaluations = maximum_evaluations
  
  def _MapGoalToFitness(self, goal_value):
    """
    Windowing:
    Fi = a + (b - a) * ((fi - f_worst) / (f_best - f_worst))
    """
    fitness_inteval_length = self.max_fitness - self.min_fitness
    goal_value_minus_worst_goal_value = goal_value - self.worst_goal_value
    best_minus_worst_goal_value = self.best_goal_value - self.worst_goal_value
    return self.min_fitness + fitness_inteval_length * goal_value_minus_worst_goal_value / best_minus_worst_goal_value
    
  def CreatePopulation(self):
    population = Population(self.goal_function, self.dimensions, self.min_x, self.max_x,
                            self.min_fitness, self.max_fitness,
                            self.binary_display, self.precision)
  
  
class Population(object):
  def __init__(self, goal_function, dimensions, min_x, max_x,
               min_fitness, max_fitness,
               binary_display, precision,
               population_size):
    self.population_size = population_size
    
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    
    self.population = False
    if binary_display == True:
      self.population = self.CreateBinaryPopulation(goal_function, dimensions, min_x, max_x, precision)
    elif binary_display == False:
      self.population = self.CreateFloatingPointPopulation(goal_function, dimensions, min_x, max_x)
    else:
      raise Exception(u"binary_display is neither True nor False. False implies a floating point display.")
    
    self.worst_goal_creature = False
    self.best_goal_creature = False
    
    self.worst_fitness_creature = False
    self.best_fitness_creature = False
    
    self.EvaluatePopulation()
    
  def CreateBinaryPopulation(self, goal_function, dimensions, min_x, max_x, precision):
    """
    #repeat:
    #  create a creature with a random state within bounds
    #until there are enough creatures
    """
    current_population_size = 0
    population = []
    while (self.population_size > current_population_size):
      creature = BinaryCreature(goal_function, dimensions, min_x, max_x, precision)
      population.append(creature)
      current_population_size += 1
      
    return population
      
  def CreateFloatingPointPopulation(self, goal_function, dimensions, min_x, max_x):
    current_population_size = 0
    population = []
    while (self.population_size > current_population_size):
      creature = FloatingPointCreature(goal_function, dimensions, min_x, max_x)
      population.append(creature)
      current_population_size += 1
      
    return population
      
  def EvaluatePopulation(self):
    for creature in self.population:
      creature.SetGoalValue()
      self.SetBestWorstGoalCreature(creature)
      
    for creature in self.population:
      creature.SetFitnessValue(self.best_goal_creature.goal_value, self.worst_goal_creature.goal_value, self.min_fitness, self.max_fitness)
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
  
  
  def KTournamentCreatureSelection(self, k):
    selected_creatures = self.ChooseRandomCreatures(k)
    
    worst_fitness_creature = False
    for i in selected_creatures:
      if self.IsUninitialized(worst_fitness_creature):
        worst_fitness_creature = self.population[i]
      
      if self.IsWorseThen(worst_fitness_creature.fitness_value, self.population[i].fitness_value):
        worst_fitness_creature = self.population[i]
        
    return worst_fitness_creature
    
  def ChooseRandomCreatures(self, k):
    selected_creatures = []
    count = 0
    while (k > count):
      random_int = random.randint(0, len(self.population) - 1)
      if random_int not in selected_creatures:
        selected_creatures.append(random_int)
        count += 1
        
    return selected_creatures
  
  
class Creature(object):
  def __init__(self, goal_function, dimensions, min_x, max_x):
    self.goal_function = goal_function
    self.dimensions = dimensions
    self.min_x = min_x
    self.max_x = max_x
    
    self.chromosome = False
    self.point = False
    
    self.goal_value = False
    self.fitness_value = False
    
  def GenerateRandomFloatingPointValue(self):
    floating_point = random.uniform(self.min_x, self.max_x)
    return floating_point
   
  def SetGoalValue(self):
    goal_value = self.goal_function(self.point)
    self.goal_value = goal_value
    
  def SetFitnessValue(self, best_goal_value, worst_goal_value, min_fitness, max_fitness):
    fitness_interval_length = max_fitness - min_fitness
    goal_value_minus_worst_goal_value = self.goal_value - worst_goal_value
    best_worst_goal_difference = float(best_goal_value - worst_goal_value)
    
    self.fitness_value = min_fitness + (fitness_interval_length * goal_value_minus_worst_goal_value) / best_worst_goal_difference
   
   
class BinaryCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, precision):
    super(BinaryCreature, self).__init__(goal_function, dimensions, min_x, max_x)
    
    self.precision = precision
    self.chromosome_length = self.CalculateChromosomeLength()
    
    self.chromosome = self.CreateChromosome()
    self.point = self.CalculatePoint()

  def CalculateChromosomeLength(self):
    interval_length = self.max_x - self.min_x
    log_10_of_floating_point_interval = math.log10(1 + interval_length * (10**self.precision))
    log10_of_2 = math.log10(2)
    chromosome_length = math.ceil(log_10_of_floating_point_interval / log10_of_2)
    return int(chromosome_length)
    
  def CreateChromosome(self):
    chromosome_group = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloatingPointValue()
      random_binary_number = self.ConvertFloatingPointToBinary(random_number)
      
      chromosome = self.CreateBinaryChromosome(random_binary_number)
      chromosome_group.append(chromosome)
      
    return Matrix(chromosome_group)
  
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
      
    binary_chromosome = self.AddTrailingZeroesToChromosome(binary_chromosome, )
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
    for row in range(1, self.chromosome._CountRows() + 1):
      binary_value = self.ConvertBinaryChromosomeToBinaryValue(self.chromosome._GetMatrixRow(row))
      floating_point = self.ConvertBinaryToFloatingPoint(binary_value)
      point.append(floating_point)
      
    return point
    
    
class FloatingPointCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x):
    super(FloatingPointCreature, self).__init__(goal_function, dimensions, min_x, max_x)
    
    self.chromosome = self.CreateChromosome()
    self.point = self.CalculatePoint()
    
  def CreateChromosome(self):
    chromosome_group = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloatingPointValue()
      
      chromosome = self.CreateFloatingPointChromosome(random_number)
      chromosome_group.append(chromosome)
      
    return Matrix(chromosome_group)
    
  def CreateFloatingPointChromosome(self, floating_point):
    floating_point_chromosome = []
    floating_point_chromosome.append(floating_point)
    
    return floating_point_chromosome
      
  def CalculatePoint(self):
    point = []
    for row in range(1, self.chromosome._CountRows() + 1):
      point.append(self.chromosome._GetMatrixRow(row)[0])
      
    return point
    