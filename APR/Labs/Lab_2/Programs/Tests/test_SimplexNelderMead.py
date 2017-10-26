import Programs.SimplexNelderMead
import Tasks.TaskFunctions

import pytest

def test_SimplexNelderMeadCreateSimplex():
  x0 =[0,0,0]
  steps = [1,1,1]
  assert Programs.SimplexNelderMead.CreateSimplex(x0, steps) == [[1,0,0],[0,1,0],[0,0,1]]