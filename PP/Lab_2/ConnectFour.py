class ConnectFourGrid(object):
  def __init__(self):
    self.width = 7
    
    self.tallest_column = 0
    self.grid = self.CreateGrid()
    
    self.move_history = []
    
  def CreateGrid(self):
    list_of_lists = []
    for number in range(self.width):
      list = []
      list_of_lists.append(list)
    
    return list_of_lists
    
  def AddTokenToColumn(self, token, column):
    self.grid[column].append(token)
    
    self.UpdateColumnHeight()
    self.UpdateMoveHistory(token, column)
    
  def UpdateColumnHeight(self):
    for column in range(self.width):
      height = len(self.grid[column])
      
      if (height > self.tallest_column):
        self.tallest_column = height
    
  def UpdateMoveHistory(self, token, column):
    move = (token, column)
    self.move_history.append(move)
    
    
    
  def CheckVictory(self):
    move_row, move_column, token = self.CalculateLastMovePosition()
    
    self.CheckVertical(move_row, move_column, token)
    self.CheckHorizontal(move_row, move_column, token)
    self.CheckMainDiagonal(move_row, move_column, token)
    self.CheckSecondDiagonal(move_row, move_column, token)
    
    
  def CalculateLastMovePosition(self):
    last_move = self.move_history[-1]
    column = last_move[0]
    token = last_move[1]
    column_height = len(self.grid[column])
    row = column_height
    
    return row, column, token
    
  def CheckVertical(self, move_row, move_column, token):
    #check only those beneath
    start_row = move_row
    end_row = move_row - 3
    
    if end_row < 0:
      return False
      
    column = self.grid[move_column][-4:-1]
    for row_token in column:
      if token != row_token:
        return False
        
    return True
    
  def CheckHorizontal(self, move_row, move_column, token):
    #check the whole row
    consecutive_tokens = 0
    
    for column in range():
      for row in range():
        
    
    if consecutive_tokens >= 4:
      return True
      
    return False
    
    
    
  def Print(self):
    string_list = []
    
    top = "| | | | | | | |"
    string_list.append(top)
    
    grid_strings = self.ConstructGridStrings()
    string_list.extend(grid_strings)
    
    dividing_line = ".-.-.-.-.-.-.-."
    bottom = " 0 1 2 3 4 5 6 "
    string_list.append(dividing_line)
    string_list.append(bottom)
    
    list_length = len(string_list)
    
    for string in string_list:
      print string
      
  def ConstructGridStrings(self):
    string_list = []
    for grid_row in range(self.tallest_column):
      string = "|"
      for grid_column in range(self.width):
      
        if (grid_row < len(self.grid[grid_column])):
          token = self.grid[grid_column][grid_row]
        else:
          token = " "
        string += token + "|"
        
      string_list.append(string)
      
    string_list = reversed(string_list)
    return string_list
    
    
    
grid = ConnectFourGrid()
grid.AddTokenToColumn("P", 3)
grid.AddTokenToColumn("C", 3)
grid.AddTokenToColumn("T", 3)
grid.AddTokenToColumn("C", 6)
grid.Print()