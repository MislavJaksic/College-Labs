from Programs.NumericalIntegration import TrapezoidalRule, RungeKuttaFour
from Programs.Helpers.Matrix import Matrix

from matplotlib import pyplot
import math

def TaskOne():
  A = Matrix([[1,2,3],
              [4,5,6],
              [7,8,9],
             ])
  A.inverse()
  print A
  
def TaskTwo():
  A = Matrix([[4,-5,-2],
              [5,-6,-2],
              [-8,9,3],
             ])
  A.inverse()
  print A
  
def TaskThree():
  A = Matrix([[0,1],[-1,0]])
  B = 0
  x0 = Matrix([[1],[5]])
  T = 0.01
  interval_length = 20
  
  #xs, time = TrapezoidalRule(A, B, x0, T, interval_length)
  #DrawGraph(xs, time)
  xs, time = RungeKuttaFour(A, B, x0, T, interval_length)
  DrawGraph(xs, time)
  
def TaskThreeTrueFunction():
  x0 = [1,5]
  T = 0.01
  interval_length = 20
  timer = 0.0
  time = []
  while (timer < interval_length):
    time.append(timer)
    timer += T
    
  xs = []
  for t in time:
    xs.append(TrueFunction(x0, t))
    
  pyplot.plot(time, xs)
  pyplot.xlabel("time")
  pyplot.ylabel("x")
  pyplot.show()
  
def TaskFour():
  A = Matrix([[0,1],[-200,-102]])
  B = 0
  x0 = Matrix([[1],[-2]])
  T = 0.01
  interval_length = 5
  
  xs, time = TrapezoidalRule(A, B, x0, T, interval_length)
  DrawGraph(xs, time)
  #xs, time = RungeKuttaFour(A, B, x0, T, interval_length)
  #DrawGraph(xs, time)
  
def TrueFunction(x, t):
  return x[0]*math.cos(t) + x[1]*math.sin(t)
  
def DrawGraph(xs, time):
  pyplot.plot(time, xs[0])
  pyplot.plot(time, xs[1])
  pyplot.xlabel("time")
  pyplot.ylabel("x")
  pyplot.show()

#TaskOne()
TaskTwo()
#TaskThree()
#TaskThreeTrueFunction()
#TaskFour()
