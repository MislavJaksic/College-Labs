from Programs.Box import Box
from Programs.ConstraintOptimization import ConstraintOptimization
from Programs.NewtonRaphson import NewtonRaphson
from Programs.SteepestDescent import SteepestDescent

from Tasks.TaskFunctions import *

def TaskOne():
  startingPoint = [0, 0]
  GoalFunction = f3
  PartialDerivativeFunctions = [df3x0, df3x1]
  
  print SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=True)
  print SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=False)
  
def TaskTwo():
  Box(startingPoint, GoalFunction, Inequalities, Interval)
  
def TaskThree():
  ConstraintOptimization(startingPoint, GoalFunction, Inequalities, Equalities)
  
def TaskFour():
  NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=True)
  
def TaskFive():
  pass
  
TaskOne()

