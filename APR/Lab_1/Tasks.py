from Programs.Matrix import Matrix

def Task_2():
  print
  print "Task_2A.txt"
  TryToSolveATask("Task_2A.txt")
  
def Task_3():
  print
  print "Task_3A.txt"
  TryToSolveATask("Task_3A.txt")
  
def Task_4():
  print
  print "Task_4A.txt"
  TryToSolveATask("Task_4A.txt")
  
def Task_5():
  print
  print "Task_5A.txt"
  TryToSolveATask("Task_5A.txt")
  
def Task_6():
  print
  print "Task_6A.txt"
  A, b = CreateMatricies("Task_6A.txt")
  i = 1
  for j in range(1, A.n_rows+1):
    A[(i, j)] /= float(1000000000)
  i = 3
  for j in range(1, A.n_rows+1):
    A[(i, j)] *= float(10000000000)
  b[(1, 1)] /= float(1000000000)
  b[(3, 1)] *= float(10000000000)
  
  print "New and improved A:"
  print A
    
  try:
    x, y = Matrix.solveAxbWithLU(A, b)
    ShowResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LU"
    print
  try:
    x, y = Matrix.solveAxbWithLUP(A, b)
    ShowResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LUP"
    print

def CreateMatricies(path):
  A = Matrix.fromFile(path)
  b = Matrix.fromFile(path.replace("A", "b"))
  ShowLoaded(A, b)
  return A, b
  
def ShowLoaded(A, b):
  print "A:"
  print A
  print "b:"
  print b
  
def TryToSolveATask(path):
  A, b = CreateMatricies(path)
  
  try:
    x, y = Matrix.solveAxbWithLU(A, b)
    ShowResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LU"
    print
  try:
    x, y = Matrix.solveAxbWithLUP(A, b)
    ShowResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LUP"
    print
  
def ShowResults(x, y):
  print "x:"
  print x
  print "y:"
  print y
    
Task_2()
Task_3()
Task_4()
Task_5()
Task_6()