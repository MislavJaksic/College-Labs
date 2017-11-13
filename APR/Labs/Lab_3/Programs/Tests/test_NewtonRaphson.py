import Programs.NewtonRaphson
import Tasks.TaskFunctions
from Programs.Helpers.Matrix import Matrix

import pytest
  
def test_NewtonRaphson_GetGradientMatrixAtPoint():
  dF = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  x = [3, 5]
  result = Matrix([[-2],
                   [24],
                  ])
  assert Programs.NewtonRaphson._GetGradientMatrixAtPoint(dF, x) == result
  
def test_NewtonRaphson_GetInverseHessianMatrixAtPoint():
  ddF = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
         [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
        ]
  x = [3, 5]
  result = Matrix([[0.5, 0    ],
                   [0,   0.125],
                  ])
  assert Programs.NewtonRaphson._GetInverseHessianMatrixAtPoint(ddF, x) == result
  
# def test_NewtonRaphson_GetDescentDirection():
  # gradient = [-8, -16]
  # result = Programs.NewtonRaphson._GetDescentDirection(gradient)
  # assert (0.4 < result[0]) and (result[0] < 0.5) and (0.8 < result[1]) and (result[1] < 0.9)
  
# def test_NewtonRaphsonGolden():
  # startingPoint = [0, 0]
  # GoalFunction = Tasks.TaskFunctions.f2
  # PartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  # result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, PartialDerivativeFunctions)
  # assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)
  
# def test_NewtonRaphsonNoGolden():
  # startingPoint = [0, 0]
  # GoalFunction = Tasks.TaskFunctions.f2
  # PartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  # result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=False)
  # assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)