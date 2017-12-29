from Programs.Matrix import Matrix

def SolveTasks(tasks):
  for task in tasks:
    print "Solving task:" + task
    TryToSolveATask(task)
    
def TryToSolveATask(path):
  A, b = CreateMatricies(path)
  
  if (path == "Tasks/Task_6Y.txt"):
    for i in range(0, A.n_rows):
      A._matrix[0][i] /= float(10**9)
      
      A._matrix[2][i] *= float(10**10)
    b._matrix[0][0] /= float(10**9)
    b._matrix[2][0] *= float(10**10)
    print "-.-.- Applied special transformations -.-.-"
    
  try:
    print "-.-.- solveAxbWithLU -.-.-"
    x, y = Matrix.solveAxbWithLU(A, b)
    PrintResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LU"
    print
    
  try:
    print "-.-.- solveAxbWithLUP -.-.-"
    x, y = Matrix.solveAxbWithLUP(A, b)
    PrintResults(x, y)
  except ZeroDivisionError:
    print u"Cannot solve with LUP"
    print
    
def CreateMatricies(path):
  A = Matrix.fromFile(path.replace("Y", "A"))
  b = Matrix.fromFile(path.replace("Y", "b"))
  PrintLoaded(A, b)
  return A, b
  
def PrintLoaded(A, b):
  print "A:"
  print A
  print "b:"
  print b
  
def PrintResults(x, y):
  print "x:"
  print x
  print "y:"
  print y

baseName = "Tasks/Task_XY.txt"
taskNumbers = [6]#2, 3, 4, 5, 6] # <- 
tasks = []

for number in taskNumbers:
  tasks.append(baseName.replace("X", str(number)))

SolveTasks(tasks)
