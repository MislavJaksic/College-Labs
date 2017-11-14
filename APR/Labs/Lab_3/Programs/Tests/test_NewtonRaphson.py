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
  
def test_NewtonRaphson_CreateGradientAtPoint():
  dF = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  x = Programs.NewtonRaphson._CreateColumnMatrix([3, 5])
  result = Matrix([[-2],
                   [24],
                  ])
  assert Programs.NewtonRaphson._CreateGradientAtPoint(dF, x) == result
  
def test_NewtonRaphson_CreateGradientNorm():
  gradientMatrix = Matrix([[3],
                           [4],
                          ])
  assert Programs.NewtonRaphson._CreateGradientNorm(gradientMatrix) == 5
  
def test_NewtonRaphson_CreateInverseHessianAtPoint():
  ddF = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
         [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
        ]
  x = Programs.NewtonRaphson._CreateColumnMatrix([3, 5])
  result = Matrix([[0.5, 0    ],
                   [0,   0.125],
                  ])
  assert Programs.NewtonRaphson._CreateInverseHessianAtPoint(ddF, x) == result
  
def test_NewtonRaphson_CreateDescentDirection():
  inverseHessian = Matrix([[0.5, 0],
                           [0,   0.125],
                          ])
  gradient = Matrix([[6],
                     [0],
                    ])
  result = Programs.NewtonRaphson._CreateDescentDirection(inverseHessian * gradient)
  result = result._GetMatrixColumn(1)
  assert (-1.1 < result[0]) and (result[0] < -0.9) and (-0.1 < result[1]) and (result[1] < 0.1)
  
def test_NewtonRaphsonGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  FirstPartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  HessianPartialDerivativeFunctions = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
                                      [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
                                     ]
  result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=True)
  result = result._GetMatrixColumn(1)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)
  
def test_NewtonRaphsonNoGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  FirstPartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  HessianPartialDerivativeFunctions = [[Tasks.TaskFunctions.ddf2x0x0, Tasks.TaskFunctions.ddf2x0x1],
                                      [Tasks.TaskFunctions.ddf2x0x1, Tasks.TaskFunctions.ddf2x1x1],
                                     ]
  result = Programs.NewtonRaphson.NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=False)
  result = result._GetMatrixColumn(1)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)