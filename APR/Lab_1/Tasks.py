from Programs.Matrix import Matrix

def Task_2():
  A = Matrix.fromFile("Task_2A.txt")
  print A
  print A.LU()
  print "-.-.-.-"
  print A.LUP()

Task_2()