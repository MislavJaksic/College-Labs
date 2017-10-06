from Programs.Matrix import Matrix

def Task_2():
  A1, A2, b = CreateMatricies("Task_2A.txt")
  print A1
  
  #L, U = A1.LU()
  
  #L, U, P = A2.LUP()
  
  x, y = A2.solveAxbWithLUP(A2, b)
  print x
  print y

def CreateMatricies(path):
  A1 = Matrix.fromFile(path)
  A2 = Matrix.fromFile(path)
  b = Matrix.fromFile(path.replace("A", "b"))
  return A1, A2, b
    
Task_2()