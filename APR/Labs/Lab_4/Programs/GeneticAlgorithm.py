import random, math
from numpy.random import normal

from Helpers.Matrix import Matrix

class GeneticAlgorithm(object):
  """
  #create population
  #eval population
  #repeat:
  #  randomly choose 3 creatures 
  #  kill the worst among them
  #  new_creature = crossover(two creatures among other)
  #  mutate new_creature with probability p_M
  #  eval new_creature
  #  add new_creature to population
  #until(stop condition)
  """
  def __init__(self, goal_function, dimensions, problem_bounds,
                     fitness_bounds=(0,100), population_size=100, binary_display=True, precision=4, p_of_mutation=0.01, p_of_crossover=0.01,
                     max_generations=False, max_evaluations=False, reach_goal_value=False, no_improvement_limit=False, time_limit=False):
    self.goal_function = self.CountInvocations(goal_function) #!= as the fitness_function
    self.dimensions = dimensions
    self.min_x = problem_bounds[0] #== dg
    self.max_x = problem_bounds[1] #== gg
    
    self.min_fitness = fitness_bounds[0] #== a
    self.max_fitness = fitness_bounds[1] #== b
    self.population_size = population_size
    self.binary_display = binary_display
    self.precision = precision
    self.p_of_mutation = p_of_mutation
    self.p_of_crossover = p_of_crossover #== not used due to tournament selection
    
    self.max_generations = max_generations #suggested value is 1000
    self.max_evaluations = max_evaluations #suggested value is 5000
    self.reach_goal_value = reach_goal_value #suggested value is (0.1)**6
    self.no_improvement_limit = no_improvement_limit #suggested value is 500
    self.no_improvement_counter = 0
    self.last_best_goal = False
    self.time_limit = time_limit #suggested value is 10000
  
  def CountInvocations(self, function):
    def interdictor(x):
      interdictor.invocations += 1
      result = function(x)
      return result
      
    interdictor.invocations = 0
    
    return interdictor
    
  def SolveProblem(self):
    population = self.CreatePopulation()
    
    while (self.StoppingConditionHasNotBeenReached(population)):
      population.GetNextGeneration()
      
      self.IsPrintPopulationData(population) #change during param optimization
    
    #print "-.-.-.-.-.-.-.-.-.-.-"
    best_point = population.best_goal_creature.point
    best_goal = population.best_goal_creature.goal_value
    return best_point, best_goal
      
  def CreatePopulation(self):
    if self.binary_display == True:
      population = BinaryPopulation(self.goal_function, self.dimensions, self.min_x, self.max_x,
                                    self.min_fitness, self.max_fitness, self.p_of_mutation,
                                    self.population_size, self.precision)
    elif self.binary_display == False:
      population = FloatingPointPopulation(self.goal_function, self.dimensions, self.min_x, self.max_x,
                                           self.min_fitness, self.max_fitness, self.p_of_mutation,
                                           self.population_size)
                                           
    self.last_best_goal = population.best_goal_creature.goal_value
    return population
  
  def StoppingConditionHasNotBeenReached(self, population):
    """
    Stop once a single condition has been reached.
    """
    if self.max_generations:
      if self.max_generations < population.generation:
        print "Max gen."
        return False
        
    if self.max_evaluations:
      if self.max_evaluations < self.goal_function.invocations:
        print "Max evaluations."
        return False
        
    if self.reach_goal_value:
      if self.reach_goal_value > population.best_goal_creature.goal_value:
        print "Reached the desired goal."
        return False
        
    if (population.worst_goal_creature.goal_value == population.best_goal_creature.goal_value):
      print "Prevented division by zero."
      return False
    
    if self.last_best_goal > population.best_goal_creature.goal_value:
      self.last_best_goal = population.best_goal_creature.goal_value
      self.no_improvement_counter = 0
    else:
      self.no_improvement_counter += 1
          
    if self.no_improvement_limit:
      if self.no_improvement_limit < self.no_improvement_counter:
        print "No improvement."
        return False
        
    if self.time_limit:
      if self.time_limit:
        pass
      
    return True
  
  def IsPrintPopulationData(self, population):
    if (self.goal_function.invocations % 500) == 0:
    #if (population.generation % 500 == 0):
      self.PrintPopulationData(population)
  
  def PrintPopulationData(self, population):
    print "Generation:",
    print population.generation
    print "Goal function invocations:",
    print self.goal_function.invocations
    print "Best goal value:",
    print population.best_goal_creature.goal_value
    print "Worst goal value:",
    print population.worst_goal_creature.goal_value
  
  
class Population(object):
  def __init__(self, dimensions, min_fitness, max_fitness, p_of_mutation, population_size):
    self.dimensions = dimensions
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    self.p_of_mutation = p_of_mutation
    self.population_size = population_size
    
    self.generation = 0
    
    self.worst_goal_creature = False
    self.best_goal_creature = False
    
    self.worst_fitness_creature = False
    self.best_fitness_creature = False
      
  def InitializeBestWorstCreatures(self):
    if self.IsUninitialized(self.best_goal_creature):
      self.best_goal_creature = self.population[0]
    if self.IsUninitialized(self.worst_goal_creature):
      self.worst_goal_creature = self.population[0]
      
    if self.IsUninitialized(self.best_fitness_creature):
      self.best_fitness_creature = self.population[0]
    if self.IsUninitialized(self.worst_fitness_creature):
      self.worst_fitness_creature = self.population[0]
  
  def EvaluatePopulation(self):
    self.SetGoalForAllCreatures()
    self.SetBestWorstGoalForAllCreatures()
    self.SetFitnessForAllCreatures()
    self.SetBestWorstFitnessForAllCreatures()
    
  def SetGoalForAllCreatures(self):
    for creature in self.population:
      creature.SetGoalValue()
      
  def SetFitnessForAllCreatures(self):
    for creature in self.population:
      creature.SetFitnessValue(self.best_goal_creature.goal_value, self.worst_goal_creature.goal_value)
  
  def SetBestWorstGoalForAllCreatures(self):
    for creature in self.population:
      self.SetBestWorstGoalCreature(creature)
  
  def SetBestWorstFitnessForAllCreatures(self):
    for creature in self.population:
      self.SetBestWorstFitnessCreature(creature)
  
  def SetBestWorstGoalCreature(self, creature):
    if self.IsBetterGoalThen(creature.goal_value, self.best_goal_creature.goal_value):
      self.best_goal_creature = creature
      
    elif self.IsWorseGoalThen(creature.goal_value, self.worst_goal_creature.goal_value):
      self.worst_goal_creature = creature
      
  def SetBestWorstFitnessCreature(self, creature):
    if self.IsBetterFitnessThen(creature.fitness_value, self.best_fitness_creature.fitness_value):
      self.best_fitness_creature = creature
      
    elif self.IsWorseFitnessThen(creature.fitness_value, self.worst_fitness_creature.fitness_value):
      self.worst_fitness_creature = creature
      
  def IsUninitialized(self, variable):
    if variable == False:
      return True
    return False
  
  def IsBetterGoalThen(self, value_one, value_two):
    if value_one < value_two:
      return True
    return False
    
  def IsWorseGoalThen(self, value_one, value_two):
    if value_one > value_two:
      return True
    return False
    
  def IsBetterFitnessThen(self, value_one, value_two):
    if value_one > value_two:
      return True
    return False
    
  def IsWorseFitnessThen(self, value_one, value_two):
    if value_one < value_two:
      return True
    return False
  
  
  def KTournamentCreatureSelection(self, k=3):
    selected_creatures = self.ChooseKRandomCreatures(k)
    
    worst_fitness_creature = self.population[selected_creatures[0]]
    #print "at first worst fitness_value",
    #print self.population[selected_creatures[0]].fitness_value
    other_creatures = []
    for i in selected_creatures[1:]:
      if self.IsWorseFitnessThen(self.population[i].fitness_value, worst_fitness_creature.fitness_value):
        #print "new worst fitness_value",
        #print self.population[i].fitness_value
        other_creatures.append(worst_fitness_creature)
        worst_fitness_creature = self.population[i]  
        #print "other creatures",
        #print worst_fitness_creature.fitness_value
      else:
        other_creatures.append(self.population[i])
        #print "other creatures",
        #print self.population[i].fitness_value
        
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
  
  def RandomlyChooseCrossover(self, parent_one, parent_two, crossover_functions):
    random_int = random.randint(0, len(crossover_functions) - 1)
    
    new_group_of_chromosomes = crossover_functions[random_int](parent_one, parent_two)
    return new_group_of_chromosomes
  
  def RandomlyChooseMutation(self, group_of_chromosomes, mutation_functions):
    random_int = random.randint(0, len(mutation_functions) - 1)
    
    new_group_of_chromosomes = mutation_functions[random_int](group_of_chromosomes)
    return new_group_of_chromosomes
  
  
  def ReplaceCreatureWithAnother(self, creature, new_group_of_chromosomes):
    creature.group_of_chromosomes = new_group_of_chromosomes
    creature.SetPoint()
    
    creature.SetGoalValue()
    
    self.SetBestWorstGoalForAllCreatures()
    if not self.IsBestWorstTheSame():
      self.SetFitnessForAllCreatures()
      self.SetBestWorstFitnessForAllCreatures()
  
  def IsDuplicate(self, new_group_of_chromosomes):
    for creature in self.population:
      if (creature.group_of_chromosomes == new_group_of_chromosomes):
        return True
    return False
  
  def IsBestWorstTheSame(self):
    if (self.worst_goal_creature.goal_value == self.best_goal_creature.goal_value):
      return True
    return False
  

class BinaryPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size, precision):
    super(BinaryPopulation, self).__init__(dimensions, min_fitness, max_fitness, p_of_mutation, population_size)
    
    self.chromosome_length = self.CalculateChromosomeLength(min_x, max_x, precision)
    
    self.population = self.CreateBinaryPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.p_of_creature_mutation = self.CalculateCreatureMutationProbability(p_of_mutation)
    self.mutate_bits = self.CalculateHowManyBitsToMutate()
    self.InitializeBestWorstCreatures()
    
    self.EvaluatePopulation()
    
  def CalculateChromosomeLength(self, min_x, max_x, precision):
    interval_length = max_x - min_x
    log_10_of_floating_point_interval = math.log10(1 + interval_length * (10**precision))
    log10_of_2 = math.log10(2)
    chromosome_length = math.ceil(log_10_of_floating_point_interval / log10_of_2)
    return int(chromosome_length)
  
  def CalculateCreatureMutationProbability(self, p_of_mutation):
    creature_mutation_p = (1 - (1 - p_of_mutation)**self.chromosome_length)
    return creature_mutation_p
  
  def CalculateHowManyBitsToMutate(self):
    mutation_frequency = 1 / self.p_of_creature_mutation
    return int(self.chromosome_length / math.floor(mutation_frequency))
  
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
      crossover_points.append(random.randint(1, self.chromosome_length - 2))
    crossover_points.sort()
    
    new_group_of_chromosomes = []
    for dimension in range(1, self.dimensions + 1):
      
      new_chromosome = []
      current_chromosome = parent_one.group_of_chromosomes._GetMatrixRow(dimension)
      for i in range(self.chromosome_length):
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
    for dimension in range(1, self.dimensions + 1):
      
      new_chromosome = []
      for i in range(self.chromosome_length):
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
    for row in range(1, self.dimensions + 1):
      for column in range(1, self.chromosome_length + 1):
        random_float = random.random()
        if random_float < self.p_of_mutation:
          group_of_chromosomes[(row, column)] = (1 - group_of_chromosomes[(row, column)])
    # for i in range(self.mutate_bits):
      # mutate_column = random.randint(1, self.chromosome_length)
      # for row in range(1, self.dimensions + 1):
        # if group_of_chromosomes[(row, mutate_column)] == 0:
          # group_of_chromosomes[(row, mutate_column)] = 1
        # else:
          # group_of_chromosomes[(row, mutate_column)] = 0
          
    return group_of_chromosomes
    
  def UniformMutation(self, group_of_chromosomes):
    for column in range(1, self.chromosome_length + 1):
      for row in range(1, self.dimensions + 1):
        if group_of_chromosomes[(row, column)] == 0:
          group_of_chromosomes[(row, column)] = 1
        else:
          group_of_chromosomes[(row, column)] = 0
          
    return group_of_chromosomes
    
    
  def GetNextGeneration(self):
    worst_fitness_creature, other_creatures = self.KTournamentCreatureSelection(k=3)
    parent_one = other_creatures[0]
    parent_two = other_creatures[1]
    
    crossover_functions = [self.KPointCrossover, self.UniformCrossover]
    new_group_of_chromosomes = self.RandomlyChooseCrossover(parent_one, parent_two, crossover_functions)
    
    mutation_functions = [self.SimpleMutation, self.UniformMutation]
    if self.IsRandomlyMutate():
      new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
    
    while self.IsDuplicate(new_group_of_chromosomes):
      new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
    
    self.ReplaceCreatureWithAnother(worst_fitness_creature, new_group_of_chromosomes)
    
    self.generation += 1
    
  def IsRandomlyMutate(self):
    if (random.random() < self.p_of_creature_mutation):
      return True
    return False
    
    
class FloatingPointPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, p_of_mutation, population_size):
    super(FloatingPointPopulation, self).__init__(dimensions, min_fitness, max_fitness, p_of_mutation, population_size)
    
    self.population = self.CreateFloatingPointPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.InitializeBestWorstCreatures()
    
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

    for dimension in range(1, self.dimensions + 1):
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

    for dimension in range(1, self.dimensions + 1):
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
    for row in range(1, self.dimensions + 1):
      group_of_chromosomes[(row, 1)] = normal(group_of_chromosomes[(row, 1)], 1.0)
      # if (random.randint(0,1) == 1):
        # group_of_chromosomes[(row, 1)] += (0.1)**8
      # else:
        # group_of_chromosomes[(row, 1)] -= (0.1)**8
      
    return group_of_chromosomes
    
    
  def GetNextGeneration(self):
    worst_fitness_creature, other_creatures = self.KTournamentCreatureSelection(k=3)
    parent_one = other_creatures[0]
    parent_two = other_creatures[1]
    
    crossover_functions = [self.ArithmeticCrossover, self.HeuristicCrossover]
    new_group_of_chromosomes = self.RandomlyChooseCrossover(parent_one, parent_two, crossover_functions)
    
    mutation_functions = [self.GaussianMutation]
    if self.IsRandomlyMutate():
      new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
    # elif self.IsWorstBestSimilar():
      # new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
    # elif (parent_one.group_of_chromosomes == parent_two.group_of_chromosomes):
      # new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
      
    while self.IsDuplicate(new_group_of_chromosomes):
      new_group_of_chromosomes = self.RandomlyChooseMutation(new_group_of_chromosomes, mutation_functions)
      
    self.ReplaceCreatureWithAnother(worst_fitness_creature, new_group_of_chromosomes)
    
    self.generation += 1
    
  def IsRandomlyMutate(self):
    if (random.randint(1, int(1 / self.p_of_mutation)) == 1):
      return True
    return False
    
  
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
    return goal_value
    
  def SetFitnessValue(self, best_goal_value, worst_goal_value):
    """
    Windowing:
    Fi = a + (b - a) * ((fi - f_worst) / (f_best - f_worst))
    """
    fitness_interval_length = self.max_fitness - self.min_fitness
    goal_value_minus_worst_goal_value = self.goal_value - worst_goal_value
    best_worst_goal_difference = best_goal_value - worst_goal_value
    
    fitness = self.min_fitness + (fitness_interval_length * goal_value_minus_worst_goal_value) / best_worst_goal_difference
    self.fitness_value = fitness
    return fitness
   
   
class BinaryCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, chromosome_length):
    super(BinaryCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    self.chromosome_length = chromosome_length
    
    self.group_of_chromosomes = self.CreateChromosome()
    self.SetPoint()
    
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
    return int(round(binary_value))
    
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
    
  def SetPoint(self):
    point = []
    for row in range(1, self.dimensions + 1):
      binary_value = self.ConvertBinaryChromosomeToBinaryValue(self.group_of_chromosomes._GetMatrixRow(row))
      floating_point = self.ConvertBinaryToFloatingPoint(binary_value)
      point.append(floating_point)
      
    self.point = point
    return point
    
    
class FloatingPointCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    super(FloatingPointCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    self.group_of_chromosomes = self.CreateChromosome()
    self.SetPoint()
    
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
      
  def SetPoint(self):
    point = []
    for row in range(1, self.dimensions + 1):
      point.append(self.group_of_chromosomes._GetMatrixRow(row)[0])
      
    self.point = point
    return point
    