from copy import deepcopy

BOARD_WIDTH = 7
COMPUTER_VICTORY = 1
PLAYER_VICTORY = -1
NEITHER_WIN = 0

class ConnectFourGrid(object):
  def __init__(self):
    self.width = BOARD_WIDTH
    
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
    
    # print (vertical_victory, horizontal_victory, main_diag_victory, second_diag_victory)
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
    
    
def CalculateTopStateValue(top_state):
  computer_states, player_computer_states = ConstructStates(top_state)
  computer_values, player_values = AssignValuesToStates(computer_states, player_computer_states)
  top_value = PropagateStatesUpwards(top_state, computer_values, player_values)
  
  print top_value
  
  return top_value
  
  
def ConstructStates(top_state):
  computer_states = SimulateComputerMoves(top_state)
  player_computer_states = SimulatePlayerMoves(computer_states)
  
  # for state in player_computer_states:
    # state.Print()
    
  return computer_states, player_computer_states
  
def SimulateComputerMoves(top_state):
  computer_states = []
  for number in range(BOARD_WIDTH):
    state = deepcopy(top_state)
    state.AddTokenToColumn("C", number)
    computer_states.append(state)
    
  return computer_states
  
def SimulatePlayerMoves(computer_states):
  player_computer_states = []
  for computer_state in computer_states:
    for number in range(BOARD_WIDTH):
      state = deepcopy(computer_state)
      state.AddTokenToColumn("P", number)
      player_computer_states.append(state)
      
  return player_computer_states

  
def AssignValuesToStates(computer_states, player_computer_states):
  computer_values = AssignComputerMoveValues(computer_states)
  player_values = AssignPlayerMoveValues(player_computer_states)
  
  return computer_values, player_values
  
def AssignComputerMoveValues(computer_states):
  computer_values = []
  for computer_state in computer_states:
    if computer_state.CheckVictory():
      computer_values.append(COMPUTER_VICTORY)
    else:
      computer_values.append(NEITHER_WIN)
      
  return computer_values
  
def AssignPlayerMoveValues(player_states):
  player_values = []
  for player_state in player_states:
    if player_state.CheckVictory():
      player_values.append(PLAYER_VICTORY)
    else:
      player_values.append(NEITHER_WIN)
      
  return player_values
 
  
def PropagateStatesUpwards(top_state, computer_values, player_values):
  propagated_values = PropagatePlayerValuesUpwards(computer_values, player_values)
  
  # for state in computer_states:
    # state.Print()
  # print propagated_values
  
  top_value = PropagateComputerValuesUpwards(top_state, propagated_values)
  
  return top_value
  
def PropagatePlayerValuesUpwards(computer_values, player_values):
  propagated_values = []
  for number in range(BOARD_WIDTH):
    computer_move_value = computer_values[number]
    
    if computer_move_value == NEITHER_WIN:
      relevant_player_values = player_values[number*BOARD_WIDTH:(number+1)*BOARD_WIDTH]
      value = CalculateUpPropagationValue(relevant_player_values)
      propagated_values.append(value)
    elif computer_move_value == COMPUTER_VICTORY:
      propagated_values.append(computer_move_value)
    else:
      raise Exception("ERROR")
      
  return propagated_values
  
def CalculateUpPropagationValue(player_values):
  value_sum = 0
  for value in player_values:
    if value != PLAYER_VICTORY:
      value_sum += value
    else:
      return PLAYER_VICTORY
      
  return float(value_sum) / BOARD_WIDTH
  
def PropagateComputerValuesUpwards(top_state, propagated_values):
  if top_state.CheckVictory() == True:
    return PLAYER_VICTORY
  
  value_sum = 0  
  for value in propagated_values:
    # if value != COMPUTER_VICTORY:
      # value_sum += value
    # else:
      # return COMPUTER_VICTORY
    value_sum += value
      
      
  return float(value_sum) / BOARD_WIDTH
      
  
 
 
state = ConnectFourGrid()
state.AddTokenToColumn("C", 2)
state.AddTokenToColumn("C", 2)
state.AddTokenToColumn("C", 2)
state.AddTokenToColumn("C", 3)
state.AddTokenToColumn("C", 3)
state.AddTokenToColumn("C", 4)
state.AddTokenToColumn("P", 2)
state.AddTokenToColumn("P", 3)
state.AddTokenToColumn("P", 4)
CalculateTopStateValue(state)
  
  
  
  
  