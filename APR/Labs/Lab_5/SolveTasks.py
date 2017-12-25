from Programs.NumericalIntegration import TrapezoidalRule, RungeKuttaFour
from Programs.Helpers.Matrix import Matrix

from matplotlib import pyplot

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
  
  xs, time = TrapezoidalRule(A, B, x0, T, interval_length)
  #xs, time = RungeKuttaFour(A, B, x0, T, interval_length)
  DrawGraph(xs, time)
  
def TaskFour():
  A = Matrix([[0,1],[-200,-102]])
  B = 0
  x0 = Matrix([[1],[-2]])
  T = 0.01
  interval_length = 20
  
  xs, time = TrapezoidalRule(A, B, x0, T, interval_length)
  #xs, time = RungeKuttaFour(A, B, x0, T, interval_length)
  DrawGraph(xs, time)
  
def DrawGraph(xs, time):
  pyplot.plot(time, xs[0])
  pyplot.plot(time, xs[1])
  pyplot.xlabel("time")
  pyplot.ylabel("x")
  pyplot.show()

#TaskOne()
TaskTwo()
#TaskThree()
#TaskFour()