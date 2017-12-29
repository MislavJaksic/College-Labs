def TrapezoidalRule(A, B, current_state, period, interval_length):
  """
  Solve dx = A*x + B with
  x(t+T) = x(t) + T * (dx(t) + dx(t+T)) / 2
  """
  x = current_state
  T = float(period)
  timer = 0.0
  
  xs = []
  time = []
  for i in range(x.n_rows):
    xs.append([])
    
  while (timer < interval_length):
    xs = AppendVector(x, xs)
    time.append(timer)
    
    x = ApproximateTrapezoidal(A, x, T)
    timer += T
    
  return xs, time
  
def ApproximateTrapezoidal(A, x, T):
  m1 = A * (x)
  m2 = A * (x + m1.scale(T/2))
  next_x = x + m2.scale(T)
  return next_x
  
def RungeKuttaFour(A, B, current_state, period, interval_length):
  """
  m1 = A*xk
  m2 = A*(xk + T*m1/2)
  m3 = A*(xk + T*m2/2)
  m4 = A*(xk + T*m3)
  xk+1 = xk + T*(m1 + 2*m2 + 2*m3 + m4)/6
  """
  x = current_state
  T = float(period)
  timer = 0.0
  
  xs = []
  time = []
  for i in range(x.n_rows):
    xs.append([])
    
  while (timer < interval_length):
    xs = AppendVector(x, xs)
    time.append(timer)
    
    x = ApproximateRungeKutta(A, x, T)
    timer += T
    
  return xs, time
    
def ApproximateRungeKutta(A, x, T):
  m1 = A * (x)
  m2 = A * (x + m1.scale(T/2))
  m3 = A * (x + m2.scale(T/2))
  m4 = A * (x + m3.scale(T))
  sum_ms = m1 + m2.scale(2) + m3.scale(2) + m4
  next_x = x + sum_ms.scale(T/6)
  return next_x
  
def AppendVector(vector, vectors):
  for i in range(vector.n_rows):
    vectors[i].append(vector[(i, 1)])
    
  return vectors
  