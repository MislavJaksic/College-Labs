## Lab Four

Genetic algorithm:
  create population
  evaluate the population
  repeat:
    randomly choose 3 creatures 
    kill the worst among them
    new_creature = crossover(two surviving creatures)
    mutate new_creature with some probability
    evaluate the new_creature
    add the new_creature to population
  until(stop condition has been reached)
  
