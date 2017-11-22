import Programs.NewtonRaphson
import Tasks.TaskFunctions
from Programs.Helpers.Matrix import Matrix

import pytest
from copy import copy
  
def test_NewtonRaphson_CreateColumnMatrix():
  list = [3, 5]
  result = Matrix([[3],
                   [5],
                  ])
  assert Programs.NewtonRaphson._CreateColumnMatrix(list) == result
  
def test_NewtonRaphson_CalculateGradientAtPoint():
  dF = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  x = Programs.NewtonRaphson._CreateColumnMatrix([3, 5])
  result = Matrix([[-2],
                   [24],
                  ])
  assert Programs.NewtonRaphson._CalculateGradientAtPoint(dF, x) == result
  
def test_NewtonRaphson_CalculateVectorNorm():
  gradientMatrix = Matrix([[3],
                           [4],
                          ])
  assert Programs.NewtonRaphson._CalculateVectorNorm(gradientMatrix) == 5
  
def test_NewtonRaphson_CalculateInverseHessianAtPoint():
  ddF = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
         [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
        ]
  x = Programs.NewtonRaphson._CreateColumnMatrix([3, 5])
  result = Matrix([[0.5, 0    ],
                   [0,   0.125],
                  ])
  assert Programs.NewtonRaphson._CalculateInverseHessianAtPoint(ddF, x) == result
  
def test_NewtonRaphson_CalculateMoveDirection():
  inverseHessian = Matrix([[0.5, 0],
                           [0,   0.125],
                          ])
  gradient = Matrix([[6],
                     [0],
                    ])
  useGolden = True
  result = Programs.NewtonRaphson._CalculateMoveDirection(inverseHessian * gradient, useGolden)
  result = result._GetMatrixColumn(1)
  assert (0.9 < result[0]) and (result[0] < 1.1) and (-0.1 < result[1]) and (result[1] < 0.1)
  
def test_NewtonRaphsonGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  FirstPartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  HessianPartialDerivativeFunctions = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
                                      [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
                                     ]
  result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=True)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)
  
def test_NewtonRaphsonNoGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  FirstPartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  HessianPartialDerivativeFunctions = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
                                      [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
                                     ]
  result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=False)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)