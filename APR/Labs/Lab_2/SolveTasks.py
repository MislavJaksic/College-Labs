from Programs.CoordinateDescent import CoordinateDescent
from Programs.HookeJeeves import HookeJeeves
from Programs.SimplexNelderMead import SimplexNelderMead

from Tasks.TaskFunctions import f1,f2,f3,f4,f6

from copy import copy
from random import randint

def f3Variant(x):
  return (x[0] - 3)**2

def TaskOne():
  startingPoint = [10000.]
  function = f3Variant
  Solve(startingPoint, function)
  
def TaskTwo():
  #function_value_pairs = [([-1.9,2.],f1)]
  #function_value_pairs = [([0.1,0.3],f2)]
  #function_value_pairs = [([0,0,0,0,0],f3)]
  function_value_pairs = [([5.1,1.1],f4)]
  for startingPoint, function in function_value_pairs:
    Solve(startingPoint, function)
  
def TaskThree():
  startingPoint, function = ([5.,5.], f4)
  
  SolveWithSimplex(startingPoint, function)
  SolveWithHookeJeeves(startingPoint, function)
  
def TaskFour():
  #startingPoint, function = ([0.5,0.5],f1)
  startingPoint, function = ([20.,20.],f1)
  
  differentSteps = [[1,1],[5,5],[10,10],[20,20]]
  
  for steps in differentSteps:
    SolveWithSimplex(startingPoint, function, steps=steps)
  
def TaskFive():
  function = f6
  
  startingPoint = [-1,-1]
  print "startingPoint:",
  print startingPoint
  SolveWithSimplex(startingPoint, function)
    
  for i in range(5):
    startingPoint = [randint(-50,50), randint(-50,50)]
    print "startingPoint:",
    print startingPoint
    SolveWithSimplex(startingPoint, function)
  
  
def Solve(startingPoint, function):
  SolveWithDescent(startingPoint, function)
  SolveWithSimplex(startingPoint, function)
  SolveWithHookeJeeves(startingPoint, function)
  
  
def SolveWithDescent(startingPoint, function):
  GoalFunction = CountInvocations(function)
  minimum = CoordinateDescent(copy(startingPoint), GoalFunction)
  print "CoordinateDescent ",
  PrintMinimumAndInvocations(minimum, GoalFunction)
  
def SolveWithSimplex(startingPoint, function, steps=[]):
  GoalFunction = CountInvocations(function)
  minimum = SimplexNelderMead(copy(startingPoint), GoalFunction, steps=steps)
  print "SimplexNelderMead ",
  PrintMinimumAndInvocations(minimum, GoalFunction)
  
def SolveWithHookeJeeves(startingPoint, function):
  GoalFunction = CountInvocations(function)
  minimum = HookeJeeves(copy(startingPoint), GoalFunction)
  print "HookeJeeves ",
  PrintMinimumAndInvocations(minimum, GoalFunction)
  
def PrintMinimumAndInvocations(minimum, GoalFunction):
  print "minimum:",
  print minimum
  print "Number of invocations:",
  print GoalFunction.invocations
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

