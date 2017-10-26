from copy import copy

def SimplexNelderMead(startingPoint, alpha, beta, gama, GoalFunction, step=[], epsilon=(0.1)**6):
  x0 = startingPoint
  refCoef = alpha
  expCoef = beta
  conCoef = gama
  F = GoalFunction
  if not steps:
    for i in range(len(x0)):
      steps.append(1)
  
  simpleks = CreateSimplex(x0, steps)
  
def CreateSimplex(x0, steps):
  simplex = []
  for i in range(len(x0)):
    simplexPoint = copy(x0)
    simplexPoint[i] += steps[i]
    simplex.append(simplexPoint)
  return simplex
  
  
"""  
  // Ulazne velicine: X0, alfa, beta, gama, epsilon
izracunaj tocke simpleksa X[i], i = 0..n;
ponavljaj
{ odredi indekse h,l : F(X[h]) = max, F(X[l]) = min;
  odredi centroid Xc;
  Xr = Refleksija();
  ako F(Xr)<F(X[l])
  {   Xe = Ekspanzija();
      ako F(Xe)<F(X[l])
            X[h] = Xe;
      inace
            X[h] = Xr;
  }
  inace
  {   ako F(Xr)>F(X[j]) za svaki j=0..n, j!=h
      {     ako F(Xr)<F(X[h])
                  X[h] = Xr;
            Xk = Kontrakcija();
            ako F(Xk)<F(X[h])
                  X[h] = Xk;
            inace
                  pomakni sve tocke prema X[l];
      }
      inace
            X[h] = Xr;
  }
}dok nije zadovoljen uvjet zaustavljanja;
  """