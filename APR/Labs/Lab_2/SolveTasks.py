from Programs.CoordinateDescent import CoordinateDescent
from Programs.HookeJeeves import HookeJeeves
from Programs.SimplexNelderMead import SimplexNelderMead

from Tasks.TaskFunctions import f1,f2,f3,f4,f6

from copy import copy

def f3Variant(x):
  return (x[0] - 3)**2

def TaskOne():
  startingPoint = [1000.]
  function = f3Variant
  Solve(startingPoint, function)
  
def Solve(startingPoint, function):
  SolveWithDescent(startingPoint, function)
  SolveWithSimplex(startingPoint, function)
  SolveWithHookeJeeves(startingPoint, function)
  print startingPoint
  
  
def SolveWithDescent(startingPoint, function):
  GoalFunction = CountInvocations(function)
  minimum = CoordinateDescent(copy(startingPoint), GoalFunction)
  print "CoordinateDescent ",
  PrintMinimumAndInvocations(minimum, GoalFunction)
  
def SolveWithSimplex(startingPoint, function):
  GoalFunction = CountInvocations(function)
  minimum = SimplexNelderMead(copy(startingPoint), GoalFunction)
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
  
TaskOne()



