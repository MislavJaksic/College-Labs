import random, math
from copy import copy
from numpy.random import normal

from Helpers.Matrix import Matrix

class GeneticAlgorithm(object):
  """
  #create population
  #evaluate the population
  #repeat:
  #  randomly choose 3 creatures 
  #  kill the worst among them
  #  new_creature = crossover(two surviving creatures)
  #  mutate new_creature with some probability
  #  evaluate the new_creature
  #  add the new_creature to population
  #until(stop condition has been reached)
  """
  def __init__(self, goal_function, dimensions, problem_bounds, fitness_bounds=(0,100),
               population_size=100, display="binary", precision=4, p_of_mutation=0.01, 
               max_generations=False, max_evaluations=False, reach_goal=False, no_improvement_limit=False, time_limit=False):
    self.goal_function = self.CountInvocations(goal_function) #!= as the fitness_function
    self.dimensions = dimensions
    self.min_x = problem_bounds[0]
    self.max_x = problem_bounds[1]
    
    self.min_fitness = fitness_bounds[0]
    self.max_fitness = fitness_bounds[1]
    self.population_size = population_size
    self.display = display
    self.precision = precision
    self.p_of_mutation = p_of_mutation
    
    self.max_generations = max_generations #suggested value is
    self.max_evaluations = max_evaluations #suggested value is 5000
    self.reach_goal = reach_goal #suggested value is (0.1)**6
    self.no_improvement_limit = no_improvement_limit #suggested value is 10% of evaluation limit
    self.time_limit = time_limit #suggested value is
    
    self.no_improvement_counter = 0
    self.last_best_goal = False
  
  def CountInvocations(self, function):
    def interdictor(x):
      interdictor.invocations += 1
      result = function(x)
      return result
      
    interdictor.invocations = 0
    
    return interdictor
    
  def SolveProblem(self):
    population = self.CreatePopulation()
    
    while not (self.IsStoppingConditionReached(population)):
      population.GetNextGeneration()
    
    best_point = population.best_goal_creature.point
    best_goal = population.best_goal_creature.goal
    return best_point, best_goal
      
  def CreatePopulation(self, seed_creatures=[]):
    if self.display == "binary":
      population = BinaryPopulation(self.goal_function, self.dimensions, self.min_x, self.max_x, self.min_fitness, self.max_fitness,
                                    self.population_size, self.precision, self.p_of_mutation, seed_creatures)
    elif self.display == "float":
      population = FloatPopulation(self.goal_function, self.dimensions, self.min_x, self.max_x, self.min_fitness, self.max_fitness,
                                   self.population_size, self.p_of_mutation, seed_creatures)                                      
    else:
      raise Exception("Display can either be 'binary' or 'float'.")
                                           
    self.last_best_goal = population.best_goal_creature.goal
    return population
  
  def IsStoppingConditionReached(self, population):
    """
    Stop once a single condition has been reached.
    """
    if self.IsMaxGenenrations(population):
      return True
        
    if self.IsMaxEvaluations():
      return True
        
    if self.IsGoalValueReached(population):
      return True
    
    if self.last_best_goal > population.best_goal_creature.goal:
      self.last_best_goal = population.best_goal_creature.goal
      self.no_improvement_counter = 0
    else:
      self.no_improvement_counter += 1
          
    if self.IsConvergedAroundASinglePoint():
      return True
        
    if self.time_limit:
      if self.time_limit:
        pass #TODO
      
    return False
    
  def IsMaxGenenrations(self, population):
    if self.max_generations == False:
      return False
    if self.max_generations < population.generation:
      print "Max generation."
      return True
    return False
    
  def IsMaxEvaluations(self):
    if self.max_evaluations == False:
      return False
    if self.max_evaluations < self.goal_function.invocations:
      print "Max evaluations."
      return True
    return False
    
  def IsGoalValueReached(self, population):
    if self.reach_goal == False:
      return False
    if self.reach_goal > population.best_goal_creature.goal:
      print "Reached the desired goal."
      return True
    return False
      
  def IsConvergedAroundASinglePoint(self):
    if self.no_improvement_limit == False:
      return False
    if self.no_improvement_limit < self.no_improvement_counter:
      print "No improvement."
      return True
    return False
    
  def IsTimeToRestartPopulation(self, population):
    if self.IsConvergedAroundASinglePoint():
      return True
    return False
        
  def PrintPopulationData(self, population):
    if (self.goal_function.invocations % 500) == 0:
      self.DisplayData(population)
  
  def DisplayData(self, population):
    print "Goal function invocations:",
    print self.goal_function.invocations
    print "Best goal value:",
    print population.best_goal_creature.goal
    print "Worst goal value:",
    print population.worst_goal_creature.goal
  
  
class Population(object):
  def __init__(self, dimensions, min_fitness, max_fitness, population_size, p_of_mutation):
    self.dimensions = dimensions
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    self.population_size = population_size
    self.p_of_mutation = p_of_mutation
    
    self.generation = 0
    
    self.population = []
    
    self.worst_goal_creature = False
    self.best_goal_creature = False
    
    self.worst_fitness_creature = False
    self.best_fitness_creature = False
  
  def SeedCreatures(self, seed_creatures):
    for creature in seed_creatures:
      self.population.append(creature)
  
  def SetPopulation(self, population):
    for creature in population:
      self.population.append(creature)
  
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
      creature.SetGoal()
      
  def SetFitnessForAllCreatures(self):
    for creature in self.population:
      creature.SetFitness(self.worst_goal_creature.goal)
  
  def SetBestWorstGoalForAllCreatures(self):
    for creature in self.population:
      self.SetBestWorstGoalCreature(creature)
  
  def SetBestWorstFitnessForAllCreatures(self):
    for creature in self.population:
      self.SetBestWorstFitnessCreature(creature)
  
  def SetBestWorstGoalCreature(self, creature):
    if self.IsBetterGoalThen(creature.goal, self.best_goal_creature.goal):
      self.best_goal_creature = creature
      
    elif self.IsWorseGoalThen(creature.goal, self.worst_goal_creature.goal):
      self.worst_goal_creature = creature
      
  def SetBestWorstFitnessCreature(self, creature):
    if self.IsBetterFitnessThen(creature.fitness, self.best_fitness_creature.fitness):
      self.best_fitness_creature = creature
      
    elif self.IsWorseFitnessThen(creature.fitness, self.worst_fitness_creature.fitness):
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
  
  
  def GetNextGeneration(self):
    worst_fitness_creature, other_creatures = self.KTournamentCreatureSelection()
    parent_one = other_creatures[0]
    parent_two = other_creatures[1]
    
    new_chromosomes = self.RandomlyChooseCrossover(parent_one, parent_two, self.crossover_functions)
    
    if self.IsRandomlyMutateCreature():
      new_chromosomes = self.RandomlyChooseMutation(new_chromosomes, self.mutation_functions)
    
    self.ReplaceCreatureWithAnother(worst_fitness_creature, new_chromosomes)
    
    self.generation += 1
  
  def KTournamentCreatureSelection(self, k=3):
    selected_creatures = self.ChooseKRandomCreatures(k)
    
    worst_fitness_creature = self.population[selected_creatures[0]]
    
    other_creatures = []
    for i in selected_creatures[1:]:
      if self.IsWorseFitnessThen(self.population[i].fitness, worst_fitness_creature.fitness):
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
  
  def RandomlyChooseCrossover(self, parent_one, parent_two, crossover_functions):
    random_int = random.randint(0, len(crossover_functions) - 1)
    
    new_chromosomes = crossover_functions[random_int](parent_one, parent_two)
    return new_chromosomes
  
  def RandomlyChooseMutation(self, chromosomes, mutation_functions):
    random_int = random.randint(0, len(mutation_functions) - 1)
    
    new_chromosomes = mutation_functions[random_int](chromosomes)
    return new_chromosomes
  
  def ReplaceCreatureWithAnother(self, creature, new_chromosomes):
    if self.IsReplacingWorstCreature(creature):
      creature.SetChromosomes(new_chromosomes)
      creature.SetGoal()
      self.SetBestWorstGoalForAllCreatures()
      
      self.SetFitnessForAllCreatures()
      self.SetBestWorstFitnessForAllCreatures()
    else:
      creature.SetChromosomes(new_chromosomes)
      creature.SetGoal()
      self.SetBestWorstGoalCreature(creature)
      
      creature.SetFitness(self.worst_goal_creature.goal)
      self.SetBestWorstFitnessCreature(creature)
  
  def IsReplacingWorstCreature(self, creature):
    if creature == self.worst_goal_creature:
      return True
    
    return False
  
  
  def __str__(self):
    pretty_string = ""
    
    pretty_string += "Population size:"
    pretty_string += str(self.population_size)
    pretty_string += "\n"
    
    pretty_string += "Worst goal:"
    pretty_string += str(self.worst_goal_creature.goal)
    pretty_string += "\n"
    
    pretty_string += "Best goal:"
    pretty_string += str(self.best_goal_creature.goal)
    pretty_string += "\n"
    
    pretty_string += "Worst fitness:"
    pretty_string += str(self.worst_goal_creature.fitness)
    pretty_string += "\n"
    
    pretty_string += "Best fitness:"
    pretty_string += str(self.best_goal_creature.fitness)
    pretty_string += "\n"
    
    return pretty_string
  

class BinaryPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness,
               population_size, precision, p_of_mutation, seed_creatures=[]):
    super(BinaryPopulation, self).__init__(dimensions, min_fitness, max_fitness, population_size, p_of_mutation)
    self.crossover_functions = [self.KPointCrossover, self.UniformCrossover]
    self.mutation_functions = [self.SimpleMutation, self.UniformMutation]
    
    self.chromosome_length = self.CalculateChromosomeLength(min_x, max_x, precision)
    
    self.SeedCreatures(seed_creatures)
    
    new_population = self.CreateBinaryPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.SetPopulation(new_population)
    
    self.p_of_creature_mutation = self.CalculateCreatureMutationProbability(p_of_mutation)
    self.mutate_bits = self.CalculateHowManyBitsToMutate()
    
    self.InitializeBestWorstCreatures()
    
    self.EvaluatePopulation()
    
  def CalculateChromosomeLength(self, min_x, max_x, precision):
    interval_length = max_x - min_x
    log_10_of_interval = math.floor(math.log10(1 + interval_length * (10**precision)))
    log10_of_2 = math.log10(2)
    chromosome_length = math.ceil(log_10_of_interval / log10_of_2)
    return int(chromosome_length)
  
  def CalculateCreatureMutationProbability(self, p_of_mutation):
    creature_mutation_p = (1 - (1 - p_of_mutation)**self.chromosome_length)
    return creature_mutation_p
  
  def CalculateHowManyBitsToMutate(self):
    mutation_frequency = 1 / self.p_of_creature_mutation
    return int(self.chromosome_length / math.floor(mutation_frequency))
  
  def CreateBinaryPopulation(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    current_population_size = len(self.population)
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
    
    new_chromosomes = []
    for dimension in range(1, self.dimensions + 1):
      
      new_chromosome = []
      current_chromosome = parent_one.chromosomes._GetMatrixRow(dimension)
      for i in range(self.chromosome_length):
        new_chromosome.append(current_chromosome[i])
        if i in crossover_points:
          chromosome_one = parent_one.chromosomes._GetMatrixRow(dimension)
          chromosome_two = parent_two.chromosomes._GetMatrixRow(dimension)
          current_chromosome = self.SwitchChromosome(current_chromosome, chromosome_one, chromosome_two)
      
      new_chromosomes.append(new_chromosome)
    
    return Matrix(new_chromosomes)
    
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
    new_chromosomes = []
    for dimension in range(1, self.dimensions + 1):
      
      new_chromosome = []
      for i in range(self.chromosome_length):
        chromosome_one = parent_one.chromosomes._GetMatrixRow(dimension)
        chromosome_two = parent_two.chromosomes._GetMatrixRow(dimension)
        bit = self.RandomBitIfParentBitsAreDifferent(chromosome_one, chromosome_two, i)
        new_chromosome.append(bit)
        
      new_chromosomes.append(new_chromosome)
    
    return Matrix(new_chromosomes)
    
  def RandomBitIfParentBitsAreDifferent(self, chromosome_one, chromosome_two, i):
    if chromosome_one[i] == chromosome_two[i]:
      bit = chromosome_one[i]
    else:
      bit = random.randint(0,1)
      
    return bit
    
    
  def SimpleMutation(self, chromosomes):
    """
    Change a few randomly selected bits.
    """
    mutated_chromosomes = copy(chromosomes)
    for i in range(self.mutate_bits):
      mutate_bit = random.randint(1, self.chromosome_length)
      for chromosome in range(1, self.dimensions + 1):
        if mutated_chromosomes[(chromosome, mutate_bit)] == 0:
          mutated_chromosomes[(chromosome, mutate_bit)] = 1
        else:
          mutated_chromosomes[(chromosome, mutate_bit)] = 0
          
    return mutated_chromosomes
    
  def UniformMutation(self, chromosomes):
    """
    Change every single bit in the chromosomes.
    """
    mutated_chromosomes = copy(chromosomes)
    for bit in range(1, self.chromosome_length + 1):
      for chromosome in range(1, self.dimensions + 1):
        if mutated_chromosomes[(chromosome, bit)] == 0:
          mutated_chromosomes[(chromosome, bit)] = 1
        else:
          mutated_chromosomes[(chromosome, bit)] = 0
          
    return mutated_chromosomes
    
  def IsRandomlyMutateCreature(self):
    if (random.random() < self.p_of_creature_mutation):
      return True
    return False
    
    
class FloatPopulation(Population):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness,
               population_size, p_of_mutation, seed_creatures=[]):
    super(FloatPopulation, self).__init__(dimensions, min_fitness, max_fitness, population_size, p_of_mutation)
    self.crossover_functions = [self.ArithmeticCrossover, self.HeuristicCrossover]
    self.mutation_functions = [self.GaussianMutation]
    
    self.SeedCreatures(seed_creatures)
    
    new_population = self.CreateFloatPopulation(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    self.SetPopulation(new_population)
      
    self.InitializeBestWorstCreatures()
    
    self.EvaluatePopulation()
  
  def CreateFloatPopulation(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    current_population_size = len(self.population)
    population = []
    while (self.population_size > current_population_size):
      creature = FloatCreature(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
      population.append(creature)
      current_population_size += 1
      
    return population
    
    
  def ArithmeticCrossover(self, parent_one, parent_two):
    new_chromosomes = []
    a = random.random()

    for chromosome in range(1, self.dimensions + 1):
      new_chromosome = []
      
      value_one = parent_one.chromosomes[(chromosome, 1)]
      value_two = parent_two.chromosomes[(chromosome, 1)]
      
      new_value = a * value_one + (1 - a) * value_two
      new_chromosome.append(new_value)
      
      new_chromosomes.append(new_chromosome)
    
    return Matrix(new_chromosomes)
    
  def HeuristicCrossover(self, parent_one, parent_two):
    new_chromosomes = []
    a = random.random()

    for chromosome in range(1, self.dimensions + 1):
      new_chromosome = []
      
      if parent_one.fitness > parent_two.fitness:
        worse_value = parent_two.chromosomes[(chromosome, 1)]
        better_value = parent_one.chromosomes[(chromosome, 1)]
      else:
        worse_value = parent_one.chromosomes[(chromosome, 1)]
        better_value = parent_two.chromosomes[(chromosome, 1)]
      
      new_value = a * (better_value - worse_value) + better_value
      new_chromosome.append(new_value)
      
      new_chromosomes.append(new_chromosome)
    
    return Matrix(new_chromosomes)
    
    
  def GaussianMutation(self, chromosomes):
    standard_deviation = 1.0
    
    mutated_chromosomes = []
    for chromosome in range(1, self.dimensions + 1):
      mean = chromosomes[(chromosome, 1)]
      mutated_chromosomes.append([normal(mean, standard_deviation)])
      
    return Matrix(mutated_chromosomes)
       
  def IsRandomlyMutateCreature(self):
    if (random.random() < self.p_of_mutation):
      return True
    return False
    
  
class Creature(object):
  """
  A creature has a solution, a solution representation (chromosomes), goal and fitness value.
  """
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    self.goal_function = goal_function
    self.dimensions = dimensions
    self.min_x = min_x
    self.max_x = max_x
    self.min_fitness = min_fitness
    self.max_fitness = max_fitness
    
    self.chromosomes = False
    self.point = False
    
    self.goal = False
    self.fitness = False
    
  def GenerateRandomFloat(self):
    floating = random.uniform(self.min_x, self.max_x)
    return floating
   
  def SetChromosomes(self, chromosomes):
    self.chromosomes = chromosomes
    self.SetPoint()
    return True
   
  def SetGoal(self):
    goal = self.goal_function(self.point)
    self.goal = goal
    return goal
    
  def SetFitness(self, worst_goal):
    fitness = worst_goal - self.goal
    self.fitness = fitness
    return fitness
   
  def SetWindowedFitness(self, best_goal, worst_goal):
    """
    a is minimal fitness value
    b is maximal fitness value
    Windowing:
    Fi = a + (b - a) * ((fi - f_worst) / (f_best - f_worst))
    """
    fitness_interval = self.max_fitness - self.min_fitness
    goal_minus_worst_goal = self.goal - worst_goal
    best_worst_goal_difference = best_goal - worst_goal
    
    fitness = self.min_fitness + (fitness_interval * goal_minus_worst_goal) / best_worst_goal_difference
    self.fitness = fitness
    return fitness
  
  
  def __str__(self):
    pretty_string = ""
    
    problem_bounds = [self.min_x, self.max_x]
    pretty_string += "Problem_bounds: "
    pretty_string += str(problem_bounds)
    pretty_string += "\n"
    
    fitness_bounds = [self.min_fitness, self.max_fitness]
    pretty_string += "Fitness_bounds: "
    pretty_string += str(fitness_bounds)
    pretty_string += "\n"
    
    pretty_string += "Chromosome_length: "
    pretty_string += str(len(self.chromosomes._GetMatrixRow(0)))
    pretty_string += "\n"
    
    pretty_string += "Chromosomes: "
    pretty_string += "\n"
    pretty_string += str(self.chromosomes)
    pretty_string += "\n"
    
    pretty_string += "Points: "
    pretty_string += str(self.point)
    pretty_string += "\n"
    
    pretty_string += "Goal value: "
    pretty_string += str(self.goal)
    pretty_string += "\n"
    
    pretty_string += "Fitness value: "
    pretty_string += str(self.fitness)
    pretty_string += "\n"
    
    return pretty_string

   
class BinaryCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness, chromosome_length):
    super(BinaryCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    self.chromosome_length = chromosome_length
    
    chromosomes = self.CreateChromosome()
    self.SetChromosomes(chromosomes)
    
  def CreateChromosome(self):
    """
    Matrix([[binary],[binary],[binary]])
    """
    chromosomes = []
    for i in range(self.dimensions):
      random_number = self.GenerateRandomFloat()
      random_binary_number = self.ConvertFloatToBinary(random_number)
      
      chromosome = self.CreateBinaryChromosome(random_binary_number)
      chromosomes.append(chromosome)
      
    return Matrix(chromosomes)
  
  def ConvertFloatToBinary(self, floating):
    interval_length = self.max_x - self.min_x
    binary = (floating - self.min_x) / interval_length * (2**self.chromosome_length - 1)
    return int(round(binary))
    
  def ConvertBinaryToFloat(self, binary):
    floating = float(binary)
    interval_length = self.max_x - self.min_x
    floating = self.min_x + floating / (2**self.chromosome_length - 1) * interval_length
    return floating
    
  def CreateBinaryChromosome(self, binary):
    binary_chromosome = []
    dividend = binary
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
    for missing_zero in range(self.chromosome_length - len(chromosome)):
      chromosome.append(0)
      
    return chromosome
    
  def ConvertBinaryChromosomeToBinary(self, binary_chromosome):
    reverse_binary_chromosome = self.ReverseList(binary_chromosome)
    
    bit_position = 0
    binary = 0
    for bit in reverse_binary_chromosome:
      binary += bit * (2**bit_position)
      bit_position += 1
      
    return binary
    
  def SetPoint(self):
    point = []
    for chromosome in range(1, self.dimensions + 1):
      binary = self.ConvertBinaryChromosomeToBinary(self.chromosomes._GetMatrixRow(chromosome))
      floating = self.ConvertBinaryToFloat(binary)
      point.append(floating)
      
    self.point = point
    return point
    
    
class FloatCreature(Creature):
  def __init__(self, goal_function, dimensions, min_x, max_x, min_fitness, max_fitness):
    super(FloatCreature, self).__init__(goal_function, dimensions, min_x, max_x, min_fitness, max_fitness)
    
    chromosomes = self.CreateChromosome()
    self.SetChromosomes(chromosomes)
    
  def CreateChromosome(self):
    """
    Matrix([[floating],[floating],[floating]])
    """
    chromosomes = []
    for d in range(self.dimensions):
      random_float = self.GenerateRandomFloat()
      
      chromosome = self.CreateFloatChromosome(random_float)
      chromosomes.append(chromosome)
      
    return Matrix(chromosomes)
    
  def CreateFloatChromosome(self, floating):
    floating_chromosome = []
    floating_chromosome.append(floating)
    
    return floating_chromosome
     
  def SetPoint(self):
    point = []
    for chromosome in range(1, self.dimensions + 1):
      point.append(self.chromosomes._GetMatrixRow(chromosome)[0])
      
    self.point = point
    return point
    

  

  
""""""