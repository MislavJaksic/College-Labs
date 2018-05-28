from mpi4py import MPI
from copy import deepcopy

# Installing relevant packages: Anaconda 2.x; conda install mpi4py; works on linux

# http://mpi4py.scipy.org/docs/apiref/index.html
# http://mpi4py.readthedocs.io/en/stable/intro.html

#Run with: mpiexec -n 2 python ConnectFour.py

BOARD_WIDTH = 7
COMPUTER_VICTORY = 1
PLAYER_VICTORY = -1
NEITHER_WIN = 0

NUMBER_OF_COMPUTER_MOVES = 3 # >3 can take a huge amount of time!

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
  all_state_tiers = CreateStatesToDesiredDepth(top_state)
  # for tier in all_state_tiers:
    # print len(tier)
  all_state_values = AssignValuesToStates(all_state_tiers)
  # for values in all_state_values:
    # print len(values)
  top_value = PropagateStatesUpwards(top_state, all_state_values)
  
  print top_value
  
  return top_value
  
  
def CreateStatesToDesiredDepth(top_state):
  branching_states = [top_state]
  all_states =[]
  for depth in range(NUMBER_OF_COMPUTER_MOVES - 1):
  
    computer_tier = []
    player_tier = []
    for branching_state in branching_states:
      computer_states, player_after_computer_states = ConstructStates(branching_state)
      computer_tier.extend(computer_states)
      player_tier.extend(player_after_computer_states)
    
    all_states.append(computer_tier)
    all_states.append(player_tier)
    
    branching_states = player_tier
    
  #all_states = reversed(all_states)
  return all_states
  
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

  
def AssignValuesToStates(all_state_tiers):
  all_state_values = []
  for depth in range(NUMBER_OF_COMPUTER_MOVES - 1):
    computer_states = all_state_tiers[depth*2]
    player_after_computer_states = all_state_tiers[depth*2 + 1]
    
    computer_values = AssignComputerMoveValues(computer_states)
    player_values = AssignPlayerMoveValues(player_after_computer_states)
    
    all_state_values.append(computer_values)
    all_state_values.append(player_values)
  
  return all_state_values
  
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
 
  
def PropagateStatesUpwards(top_state, all_state_values):
  all_state_values.reverse()
  
  player_values = all_state_values[0]
  computer_values = all_state_values[1]
  propagated_computer_values = PropagatePlayerValuesUpwards(computer_values, player_values)
  
  for depth in range(1, NUMBER_OF_COMPUTER_MOVES - 1):
    player_values = all_state_values[depth*2]
    computer_values = all_state_values[depth*2 + 1]
    
    propagated_player_values = PropagateComputerValuesUpwards(propagated_computer_values, player_values)
    propagated_computer_values = PropagatePlayerValuesUpwards(computer_values, propagated_player_values)
    
  player_values = [top_state.CheckVictory()]
  top_value = PropagateComputerValuesUpwards(propagated_computer_values, player_values)
  
  return top_value
  
def PropagatePlayerValuesUpwards(computer_values, player_values):
  propagated_values = []
  for number in range(len(computer_values)):
    computer_move_value = computer_values[number]
    
    if computer_move_value == NEITHER_WIN:
      relevant_player_values = player_values[number*BOARD_WIDTH:(number+1)*BOARD_WIDTH]
      value = CalculateComputerUpPropagationValue(relevant_player_values)
      propagated_values.append(value)
    elif computer_move_value == COMPUTER_VICTORY:
      propagated_values.append(computer_move_value)
    else:
      raise Exception("ERROR")
      
  return propagated_values
  
def CalculateComputerUpPropagationValue(player_values):
  value_sum = 0
  for value in player_values:
    if value != PLAYER_VICTORY:
      value_sum += value
    else:
      return PLAYER_VICTORY
      
  return float(value_sum) / BOARD_WIDTH
  
def PropagateComputerValuesUpwards(computer_values, player_values):
  propagated_values = []
  for number in range(len(player_values)):
    player_move_value = player_values[number]
    
    if player_move_value == NEITHER_WIN:
      relevant_computer_values = computer_values[number*BOARD_WIDTH:(number+1)*BOARD_WIDTH]
      value = CalculatePlayerUpPropagationValue(relevant_computer_values)
      propagated_values.append(value)
    elif player_move_value == PLAYER_VICTORY:
      propagated_values.append(player_move_value)
    else:
      raise Exception("ERROR")
      
  return propagated_values
      
def CalculatePlayerUpPropagationValue(computer_values):
  value_sum = 0
  for value in computer_values:
    if value != COMPUTER_VICTORY:
      value_sum += value
    else:
      return COMPUTER_VICTORY
      
  return float(value_sum) / BOARD_WIDTH
      

      
def ComputerThinks(communicator, current_state):
  computer_states, player_computer_states = ConstructStates(current_state)
  tasks = player_computer_states
  
  results = DistributeTasksAndRecieveResults(tasks)

  



def DistributeTasksAndRecieveResults(task_tier):
  for state in task_tier:
    pass
  #communicator.send(message, dest=)

      
# state = ConnectFourGrid()
# state.AddTokenToColumn("C", 0)
# state.AddTokenToColumn("C", 1)
# state.AddTokenToColumn("P", 5)
# state.AddTokenToColumn("P", 6)
# CalculateTopStateValue(state)
      
      
# if __name__ == "__main__":
  # communicator = MPI.COMM_WORLD
  # process_rank = communicator.Get_rank()
  # number_of_processes = communicator.Get_size()
  
  # if process_rank == 0:
    # current_state = ConnectFourGrid()
    # ComputerThinks(communicator, current_state)
  # else:
    # pass
  
  #computer thinks
  #computer makes a move
  #player makes a move

  #computer think
    #create states until the desired depth
    #send tasks to be completed
    #recieve results
    #use results and create other tasks
    #do so until the top

  
  

  
  
  
  
  