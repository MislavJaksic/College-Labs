import Programs.SteepestDescent
import Tasks.TaskFunctions

import pytest
  
def test_SteepestDescent_GetGradientNorm():
  gradient = [4, 5]
  result = Programs.SteepestDescent._GetGradientNorm(gradient)
  assert (6.3 < result) and (result < 6.5)
  
def test_SteepestDescent_GetGradientAtPoint():
  dF = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  x = [3, 5]
  assert Programs.SteepestDescent._GetGradientAtPoint(dF, x) == [-2, 24]
    
# def test_SteepestDescent_IsGradientNormSmall:
  # assert Programs.SteepestDescent._IsGradientNormSmall(gradientNorm, epsilon) ==