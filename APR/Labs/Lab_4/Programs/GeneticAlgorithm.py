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
                     fitness_bounds=(0,1), population_size=100, binary_display=True, precision=2, mutation_probability=0.1, crossover_probability=0.1,
                     maximum_evaluations=1000):
    self.goal_function = goal_function #!= as the fitness_function
    self.dimensions = dimensions
    self.lower_problem_bound = problem_bounds[0] #== dg
    self.upper_problem_bound = problem_bounds[1] #== gg
    
    self.lower_fitness_bound = fitness_bounds[0] #== a
    self.upper_fitness_bound = fitness_bounds[1] #== b
    self.population_size = population_size
    self.binary_display = binary_display
    self.precision = precision
    self.mutation_probability = mutation_probability
    self.crossover_probability = crossover_probability
    
    self.maximum_evaluations = maximum_evaluations
  
  def _MapGoalToFitness(self, goal_value):
    """
    Windowing:
    Fi = a + (b - a) * ((fi - f_worst) / (f_best - f_worst))
    """
    fitness_inteval_length = self.upper_fitness_bound - self.lower_fitness_bound
    goal_value_minus_worst_goal_value = goal_value - self.worst_goal_value
    best_minus_worst_goal_value = self.best_goal_value - self.worst_goal_value
    return self.lower_fitness_bound + fitness_inteval_length * goal_value_minus_worst_goal_value / best_minus_worst_goal_value
    
  def CreatePopulation(self):
    population = Population(self.goal_function, self.dimensions, self.lower_problem_bound, self.upper_problem_bound,
                            self.binary_display, self.precision)
  
  
class Population(object):
  def __init__(self, goal_function, dimensions, lower_problem_bound, upper_problem_bound,
               ):
    self.goal_function = goal_function
    self.dimensions = dimensions
    self.lower_problem_bound = lower_problem_bound
    self.upper_problem_bound = upper_problem_bound
    
    self.worst_goal_value_creature = None
    self.best_goal_value_creature = None
    
    self.worst_fitness_value_creature = None
    self.best_fitness_value_creature = None
  
  def CreatePopulation(self):
    """
    #repeat:
    #  create a creature with a random state within bounds
    #until there are enough creatures
    """
    current_population_size = 0
    population = []
    while (self.population_size > current_population_size):
      creature = Creature(self.goal_function, self.dimensions, self.lower_problem_bound, self.upper_problem_bound)
      population.append(creature)
      current_population_size += 1
      
  
class Creature(object):
  def __init__(self, goal_function, dimensions, lower_problem_bound, upper_problem_bound):
    self.goal_function = goal_function
    self.dimensions = dimensions
    self.lower_problem_bound = lower_problem_bound
    self.upper_problem_bound = upper_problem_bound
    
    self.goal_value = None
    self.fitness_value = None
    self.chromosome = None
    
  def GenerateRandomFloatingPointValue(self):
    floating_point = random.uniform(self.lower_problem_bound, self.upper_problem_bound)
    return floating_point
   
   
class BinaryCreature(Creature):
  def __init__(self, goal_function, dimensions, lower_problem_bound, upper_problem_bound, precision):
    super(BinaryCreature, self).__init__(goal_function, dimensions, lower_problem_bound, upper_problem_bound)
    
    self.precision = precision
    self.chromosome_length = self.CalculateChromosomeLength()
    
    self.chromosome = self.CreateChromosome()

  def CalculateChromosomeLength(self):
    interval_length = self.upper_problem_bound - self.lower_problem_bound
    log_10_of_floating_point_interval = math.log10(1 + interval_length * (10**self.precision))
    log10_of_2 = math.log10(2)
    chromosome_length = math.ceil(log_10_of_floating_point_interval / log10_of_2)
    return int(chromosome_length)
    
  def CreateChromosome(self):
    chromosome_group = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloatingPointValue()
      print random_number
      random_binary_number = self.ConvertFloatingPointToBinary(random_number)
      print random_binary_number
      
      chromosome = self.CreateBinaryChromosome(random_binary_number)
      print chromosome
      chromosome_group.append(chromosome)
      
    return Matrix(chromosome_group)
  
  def ConvertFloatingPointToBinary(self, floating_point):
    interval_length = self.upper_problem_bound - self.lower_problem_bound
    binary_value = (floating_point - self.lower_problem_bound) / interval_length * (2**self.chromosome_length)
    return int(binary_value)
    
  def CreateBinaryChromosome(self, binary_value):
    binary_chromosome = []
    dividend = binary_value
    divisor = 2
    while (dividend > 0):
      remainder = dividend % divisor
      binary_chromosome.append(remainder)
      dividend = dividend / divisor
      
    binary_chromosome = self.AddLeadingZeroesToList(binary_chromosome, self.chromosome_length)
    binary_chromosome = self.ReverseList(binary_chromosome)
    
    return binary_chromosome
      
  def ReverseList(self, list):
    reverse_list = []
    for i in range(len(list)):
      element = list[(-1)*i - 1]
      reverse_list.append(element)
      
    return reverse_list
      
  def AddLeadingZeroesToList(self, list, max_length):
    for i in range(max_length - len(list)):
      list.append(0)
      
    return list
    
class FloatingPointCreature(Creature):
  def __init__(self):
    pass
  