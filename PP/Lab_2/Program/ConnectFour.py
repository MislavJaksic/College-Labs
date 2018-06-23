from mpi4py import MPI
from copy import deepcopy
from time import time

# Installing relevant packages: Anaconda 2.x; conda install mpi4py; works on linux

# http://mpi4py.scipy.org/docs/apiref/index.html
# http://mpi4py.readthedocs.io/en/stable/intro.html

#Run with: mpiexec -n 2 python ConnectFour.py

BOARD_WIDTH = 7
COMPUTER_VICTORY = 1
PLAYER_VICTORY = -1
UNDECIDED = 0

NUMBER_OF_COMPUTER_MOVES = 2 # >3 can take a huge amount of time!

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
      
      if (self.IsColumnHighEnough(column, move_row)):
        grid_token = self.grid[column][move_row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      else:
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
    if end_column > (BOARD_WIDTH - 1):
      end_column = (BOARD_WIDTH - 1)
      
    column = start_column
    row = start_row
    consecutive_tokens = 0
    while (row >= 0 and column <= end_column):
    
      if (self.IsColumnHighEnough(column, row)):
        grid_token = self.grid[column][row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      else:
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
    if end_column > (BOARD_WIDTH - 1):
      end_column = (BOARD_WIDTH - 1)
      
    column = start_column
    row = start_row
    consecutive_tokens = 0
    while (row <= end_row and column <= end_column):
    
      if (self.IsColumnHighEnough(column, row)):
        grid_token = self.grid[column][row]
        if grid_token == token:
          consecutive_tokens += 1
        else:
          consecutive_tokens = 0
          
      else:
        consecutive_tokens = 0
      
      if consecutive_tokens >= 4:
        return True
        
      row += 1
      column += 1
      
    return False
    
  def IsColumnHighEnough(self, column_number, length):
    column = self.grid[column_number]
    if (len(column) > length):
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
    
    
    
def CalculateTopStateValue(top_state):
  all_state_tiers = CreateStatesToDesiredDepth(top_state)
  all_state_values = AssignValuesToStates(all_state_tiers)
  top_value, propagated_computer_values = PropagateStatesUpwards(top_state, all_state_values)
  
  return top_value, propagated_computer_values
  
  
def CreateStatesToDesiredDepth(top_state):
  branching_states = [top_state]
  all_states =[]
  for depth in range(NUMBER_OF_COMPUTER_MOVES - 1):
  
    computer_tier = []
    player_tier = []
    for branching_state in branching_states:
      computer_states, player_after_computer_states = ConstructComputerPlayerStates(branching_state)
      computer_tier.extend(computer_states)
      player_tier.extend(player_after_computer_states)
    
    all_states.append(computer_tier)
    all_states.append(player_tier)
    
    branching_states = player_tier
    
  return all_states
  
def ConstructComputerPlayerStates(root_state):
  states_after_computer_move = SimulateComputerMoves(root_state)
  states_after_computer_and_then_player_move = SimulatePlayerMoves(states_after_computer_move)
    
  return states_after_computer_move, states_after_computer_and_then_player_move
  
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
    
    computer_values = AssignValuesToComputerStates(computer_states)
    player_values = AssignValuesToPlayerStates(player_after_computer_states)
    
    all_state_values.append(computer_values)
    all_state_values.append(player_values)
  
  return all_state_values
  
def AssignValuesToComputerStates(computer_states):
  computer_values = []
  for computer_state in computer_states:
    if computer_state.CheckVictory():
      computer_values.append(COMPUTER_VICTORY)
    else:
      computer_values.append(UNDECIDED)
      
  return computer_values
  
def AssignValuesToPlayerStates(player_states):
  player_values = []
  for player_state in player_states:
    if player_state.CheckVictory():
      player_values.append(PLAYER_VICTORY)
    else:
      player_values.append(UNDECIDED)
      
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
  
  return top_value[0], propagated_computer_values
  
def PropagatePlayerValuesUpwards(computer_values, player_values):
  propagated_values = []
  for number in range(len(computer_values)):
    computer_move_value = computer_values[number]
    
    if computer_move_value == UNDECIDED:
      relevant_player_values = player_values[number*BOARD_WIDTH:(number+1)*BOARD_WIDTH]
      value = CalculateComputerUpPropagationValue(relevant_player_values)
      propagated_values.append(value)
    else:
      propagated_values.append(computer_move_value)
      
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
    
    if player_move_value == UNDECIDED:
      relevant_computer_values = computer_values[number*BOARD_WIDTH:(number+1)*BOARD_WIDTH]
      value = CalculatePlayerUpPropagationValue(relevant_computer_values)
      propagated_values.append(value)
    else:
      propagated_values.append(player_move_value)
      
  return propagated_values
      
def CalculatePlayerUpPropagationValue(computer_values):
  value_sum = 0
  for value in computer_values:
    if value != COMPUTER_VICTORY:
      value_sum += value
    else:
      return COMPUTER_VICTORY
      
  return float(value_sum) / BOARD_WIDTH
     
     
     
def CreateInterestingState(current_state):
  current_state.AddTokenToColumn("C", 0)
  current_state.AddTokenToColumn("C", 0)
  current_state.AddTokenToColumn("C", 0)
  current_state.AddTokenToColumn("P", 0)
  
  current_state.AddTokenToColumn("C", 1)
  
  current_state.AddTokenToColumn("P", 2)
  current_state.AddTokenToColumn("P", 2)
  current_state.AddTokenToColumn("C", 2)
  
  current_state.AddTokenToColumn("C", 3)
  
  current_state.AddTokenToColumn("P", 5)
  current_state.AddTokenToColumn("P", 5)
  current_state.AddTokenToColumn("C", 5)
   
  current_state.AddTokenToColumn("P", 6)
  
  return current_state
     
      
def CalculateBestMove(communicator, number_of_processes, current_state):
  computer_states, player_states = ConstructComputerPlayerStates(current_state)
  tasks = player_states
  
  if number_of_processes != 1:
    results = DistributeTasksAndRecieveResults(communicator, number_of_processes, tasks)
  else:
    results = DoItAllAlone(tasks)
  
  values_of_computer_states = AssignValuesToComputerStates(computer_states)
  propagated_computer_values = PropagatePlayerValuesUpwards(values_of_computer_states, results)
  print propagated_computer_values
  
  column_number = FindHighestValueIndex(propagated_computer_values)
  return column_number
  
def DistributeTasksAndRecieveResults(communicator, number_of_processes, tasks): #delicate, needs refactoring
  task_counter = 0
  distribution_counter = 0
  results = []
  while True:

    for process in range(1, number_of_processes):
      task = tasks[task_counter]
      communicator.send(task, dest=process)
      
      #print "Master sent task " + str(task_counter) + " to process " + str(process)
      task_counter += 1
      distribution_counter += 1
      if task_counter >= len(tasks):
        break
      
    for process in range(1, number_of_processes):
      distribution_counter -= 1
      if distribution_counter < 0:
        break
      
      result = communicator.recv(source=process)
      results.append(result)
      #print "Master recieved " + str(result) + " from process " + str(process)
      
    if distribution_counter < 0:
      break
    if task_counter >= len(tasks):
      break
  
  return results
    
def FindHighestValueIndex(list):
  highest_value = max(list)
  length = len(list)
  for index in range(length):
    value = list[index]
    if (value == highest_value):
      return index
    
    
def DoItAllAlone(tasks):
  results = []
  for task in tasks:
    result, propagated_computer_values = CalculateTopStateValue(task)
    results.append(result)
  return results
    
    
def ComputerMakesAMove(communicator, number_of_processes, current_state):
  #start_time = time()
  move_to_make = CalculateBestMove(communicator, number_of_processes, current_state)
  #end_time = time()
  #print "Time:" + str(end_time - start_time)
  
  current_state.AddTokenToColumn("C", move_to_make)
  current_state.Print()
  
def PlayerMakesAMove(current_state):
  print "The Player may now make a move or surrender: [0,1,2,3,4,5,6] / -1"
  player_move = raw_input(":::")
  player_move = int(player_move)
  
  if IsPlayerSurrender(player_move):
    return player_move
    
  current_state.AddTokenToColumn("P", player_move)
  current_state.Print()
  
  return player_move
  
def IsComputerVictorious(current_state):
  if current_state.CheckVictory():
    return True
  return False
  
def IsPlayerSurrender(player_move):
  if (player_move == -1):
    return True
  return False
  
def IfPlayerVictorious(current_state):
  if current_state.CheckVictory():
    return True
  return False
  
def StopAllWorkers(communicator, number_of_processes):
  for process in range(1, number_of_processes):
    communicator.send(0, dest=process)
    
  
def DoWork(communicator):
  while True:
    state = communicator.recv(source=0)
    if (state == 0):
      break
      
    result, propagated_computer_values = CalculateTopStateValue(state)
    communicator.send(result, dest=0)
    
      
      
if __name__ == "__main__":
  communicator = MPI.COMM_WORLD
  process_rank = communicator.Get_rank()
  number_of_processes = communicator.Get_size()
  
  if process_rank == 0:
    print "Supervisor rank: " + str(process_rank)
    
    current_state = ConnectFourGrid()
    current_state = CreateInterestingState(current_state)
    
    while True:
      ComputerMakesAMove(communicator, number_of_processes, current_state)
      if IsComputerVictorious(current_state):
        print "Computer has won"
        break
      
      player_move = PlayerMakesAMove(current_state)
      if IsPlayerSurrender(player_move):
        print "Player has surrendered"
        break
      if IfPlayerVictorious(current_state):
        print "Player has won"
        break
        
    StopAllWorkers(communicator, number_of_processes)
    
  else:
    print "Worker rank: " + str(process_rank)
    DoWork(communicator)

    
    
    
    