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
    
    vertical_victory = self.CheckVertical(move_row, move_column, token)
    horizontal_victory = self.CheckHorizontal(move_row, move_column, token)
    main_diag_victory = self.CheckMainDiagonal(move_row, move_column, token)
    second_diag_victory = self.CheckSecondDiagonal(move_row, move_column, token)
    
    print (vertical_victory, horizontal_victory, main_diag_victory, second_diag_victory)
    if True in (vertical_victory, horizontal_victory, main_diag_victory, second_diag_victory):
      return True
      
    return False
    
  def CalculateLastMovePosition(self):
    last_move = self.move_history[-1]
    token = last_move[0]
    column = last_move[1]
    column_height = len(self.grid[column]) 
    row = column_height - 1
    
    return row, column, token
    
  def CheckVertical(self, move_row, move_column, token):
    #check only those beneath
    start_row = move_row
    end_row = move_row - 3
    print end_row
    if end_row < 0:
      return False
      
    column = self.grid[move_column][-4:-1]
    print column
    for row_token in column:
      if token != row_token:
        return False
        
    return True
    
  def CheckHorizontal(self, move_row, move_column, token):
    #check the whole row
    consecutive_tokens = 0
    for column in range(self.width):
      try:
        grid_token = self.grid[column][move_row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      except:
        consecutive_tokens = 0
      
      if consecutive_tokens >= 4:
        return True
        
    return False
    
  def CheckMainDiagonal(self, move_row, move_column, token):
    # \ diagonal
    start_row = move_row + 3
    
    start_column = move_column - 3
    end_column = move_column + 3
    
    if start_row < 0:
      start_row = 0
      
    if start_column < 0:
      start_column = 0
    if end_column > 6:
      end_column = 6
      
    column = start_column
    row = start_row
    consecutive_tokens = 0
    while (row >= 0 and column <= end_column):
      try:
        grid_token = self.grid[column][row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      except:
        consecutive_tokens = 0
      
      if consecutive_tokens >= 4:
        return True
        
      row -= 1
      column += 1
      
    return False
    
  def CheckSecondDiagonal(self, move_row, move_column, token):
    # / diagonal
    start_row = move_row - 3
    end_row = move_row + 3
    start_column = move_column - 3
    end_column = move_column + 3
    
    if start_row < 0:
      start_row = 0
      
    if start_column < 0:
      start_column = 0
    if end_column > 6:
      end_column = 6
      
    column = start_column
    row = start_row
    consecutive_tokens = 0
    while (row <= end_row and column <= end_column):
      try:
        grid_token = self.grid[column][row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      except:
        consecutive_tokens = 0
      
      if consecutive_tokens >= 4:
        return True
        
      row += 1
      column += 1
      
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
    
    
def ConstructStates(top_state):