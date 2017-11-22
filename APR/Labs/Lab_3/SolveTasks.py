from Programs.Box import Box
from Programs.ConstraintOptimization import ConstraintOptimization
from Programs.NewtonRaphson import NewtonRaphson
from Programs.SteepestDescent import SteepestDescent

from Tasks.TaskFunctions import *

from copy import copy

def TaskOne():
  x0 = [0, 0]
  F = f3
  dF = [df3x0, df3x1]
  
  SolveWithSteepestDescent(x0, F, dF, True)
  SolveWithSteepestDescent(x0, F, dF, False)
  
def TaskTwo():
  x0 = [-1.9, 2]
  F = f1
  dF = [df1x0, df1x1]
  ddF = [[ddf1x0x0, ddf1x0x1],
         [ddf1x0x1, ddf1x1x1],
        ]
  
  SolveWithSteepestDescent(x0, F, dF, True)
  #SolveWithNewtonRaphson(x0, F, dF, ddF, True)
  
  x0 = [0.1, 0.3]
  F = f2
  dF = [df2x0, df2x1]
  ddF = [[ddf2x0x0, ddf2x0x1],
         [ddf2x0x1, ddf2x1x1],
        ]
  
  #SolveWithSteepestDescent(x0, F, dF, True)
  #SolveWithNewtonRaphson(x0, F, dF, ddF, True)
  
def TaskThree():
  x0 = [-1.9, 2]
  F = f1
  Inequalities = [constraint1, constraint2]
  Interval = [-100, 100]
  
  #SolveWithBox(x0, F, Inequalities, Interval)
  
  x0 = [0.1, 0.3]
  F = f2
  Inequalities = [constraint1, constraint2]
  Interval = [-100, 100]
  
  SolveWithBox(x0, F, Inequalities, Interval)
  
def TaskFour():
  x0 = [-1.9, 2]
  F = f1
  Inequalities = [constraint1, constraint2]
  
  #SolveWithConstraintOptimization(x0, F, Inequalities, [])
  
  betterx0 = [3, 3]
  
  #SolveWithConstraintOptimization(betterx0, F, Inequalities, [])
  
  x0 = [0.1, 0.3]
  F = f2
  Inequalities = [constraint1, constraint2]
  
  SolveWithConstraintOptimization(x0, F, Inequalities, [])
  
def TaskFive():
  x0 = [0, 0]
  F = f4
  Inequalities = [constraint3, constraint4]
  Equalities = [constraint5]
  
  #SolveWithConstraintOptimization(x0, F, Inequalities, Equalities)
  
  x0 = [5, 5]
  
  SolveWithConstraintOptimization(x0, F, Inequalities, Equalities)
  
def SolveWithSteepestDescent(x0, function, dF, useGolden):
  F = CountInvocations(function)
  newdF = []
  for f in dF:
    newdF.append(CountInvocations(f))
  
  minimum = SteepestDescent(copy(x0), F, newdF, useGolden)
  print "SteepestDescent ",
  PrintMinimumAndInvocations(minimum, F, newdF, [])
  
def SolveWithNewtonRaphson(x0, function, dF, ddF, useGolden):
  F = CountInvocations(function)
  newdF = []
  for f in dF:
    newdF.append(CountInvocations(f))
  
  newddF = []
  for list in ddF:
    newList = []
    for f in list:
      newList.append(CountInvocations(f))
    newddF.append(newList)
    
  minimum = NewtonRaphson(copy(x0), F, newdF, newddF, useGolden=useGolden)
  print "NewtonRaphson ",
  PrintMinimumAndInvocations(minimum, F, newdF, newddF)
  
def SolveWithBox(x0, function, Inequalities, Interval):
  F = CountInvocations(function)
  minimum = Box(copy(x0), F, Inequalities, Interval)
  print "Box ",
  PrintMinimumAndInvocations(minimum, F, [], [])
  
def SolveWithConstraintOptimization(x0, function, Inequalities, Equalities):
  F = CountInvocations(function)
  minimum = ConstraintOptimization(copy(x0), F, Inequalities, Equalities)
  print "ConstraintOptimization ",
  PrintMinimumAndInvocations(minimum, F, [], [])
  
def PrintMinimumAndInvocations(minimum, F, dF, ddF):
  print "minimum:",
  print minimum
  print "Goal function value at minimum:",
  print F(minimum)
  print "Number of goal function invocations:",
  print F.invocations
  
  sum = 0
  for f in dF:
    sum+= f.invocations
  print "Number of first partial function invocations:",
  print sum
  
  sum = 0
  for list in ddF:
    for f in list:
      sum+= f.invocations
  print "Number of second partial function invocations:",
  print sum
  
  print "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-"
  print
  
def CountInvocations(function):
  def interdictor(x):
    interdictor.invocations += 1
    result = function(x)
    return result
    
  interdictor.invocations = 0
  
  return interdictor
  
#TaskOne()
#TaskTwo()
#TaskThree()
#TaskFour()
TaskFive()