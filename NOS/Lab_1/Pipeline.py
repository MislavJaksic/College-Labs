from multiprocessing import Pipe, Process, active_children, current_process, freeze_support
from time import sleep
from copy import copy
from heapq import heappush, heappop

PHILOSOPHER_NUMBER = 3
TIMEOUT =  1 / float(PHILOSOPHER_NUMBER - 1)

class Philosopher(object):
  def __init__(self, ID, pipes):
    self.ID = ID
    self.pipes = pipes
    self.clock = 0
    self.request_queue = []
    self.replies = []

  def ReceiveMessages(self):
    for pipe in self.pipes:
      if pipe == False:
        continue
        
      if (pipe.poll(TIMEOUT)):
        message = pipe.recv()
        self.ActOnMessage(message)
        
  def ActOnMessage(self, message):
    time_stamp, text, sender_ID = message
    self.Say("Recieved " + text + " from " + str(sender_ID))
    
    if (text == "Request"):
      self.SynchroniseClock(time_stamp)
      self.AddRequestToQueue(message)
      self.ReplyToSender(sender_ID)
    elif (text == "Release"):
      removed_request = self.RemoveFromQueue()
    elif (text == "Reply"):
      self.SynchroniseClock(time_stamp)
      self.AddToReplies(message)
      
  def SynchroniseClock(self, time_stamp):
    if (time_stamp >= self.clock):
      self.clock = time_stamp + 1
    else:
      self.IncreaseClock()
      
  def IncreaseClock(self):
    self.clock = self.clock + 1
    
  def ReplyToSender(self, sender_ID):
    reply = self.CreateReply()
    self.Say("Sending " + reply[1] + " to " + str(reply[2]))
    self.pipes[sender_ID].send(reply)
    
  def CreateReply(self):
    time_stamp = self.CreateTimeStamp()
    reply = (time_stamp, "Reply", self.ID)
    return reply

  def RemoveFromQueue(self):
    message = heappop(self.request_queue)
    return message
    
  def AddToReplies(self, reply):
    self.replies.append(reply)


  def SendRequest(self):
    request = self.CreateRequest()
    self.AddRequestToQueue(request)
    self.SendMessageToAll(request)
    
  def CreateRequest(self):
    time_stamp = self.CreateTimeStamp()
    request = (time_stamp, "Request", self.ID)
    return request
    
  def CreateTimeStamp(self):
    time_stamp = self.clock
    return time_stamp
    
  def SendMessageToAll(self, message):
    self.Say("Sending " + message[1] + " to all")
    for pipe in self.pipes:
      if pipe == False:
        continue
      pipe.send(message)


  def WaitForYourTurnToEat(self):
    while (not (self.IsMyRequestFirstInQueue() and self.IsRecievedAllReplies())):
      self.ReceiveMessages()
      
  def IsMyRequestFirstInQueue(self):
    first_request = self.request_queue[0]
    time_stamp, message, ID = first_request
    
    if (ID == self.ID):
      return True
    return False
    
  def IsRecievedAllReplies(self):
    if (len(self.replies) == (PHILOSOPHER_NUMBER - 1)):
      return True
    return False

  def DeleteReplies(self):
    self.replies = []
    
    
  def SendRelease(self):
    message = self.RemoveFromQueue()
    release = self.CreateRelease(message)
    self.SendMessageToAll(release)

  def CreateRelease(self, message):
    release = (message[0], "Release", self.ID)
    return release


  def AddRequestToQueue(self, request):
    heappush(self.request_queue, request)

  def Say(self, text):
    string = ""
    for number in range(self.ID):
      string += "        "

    string += str(self.ID) + ": "

    string += text

    print(string)
  
  def __str__(self):
    string = ""
    string += "Philosopher:" + "\n"
    string += "    " + "ID:" + str(self.ID) + "\n"
    string += "    " + "Pipes:" + str(self.pipes) + "\n"
    string += "    " + "Clock:" + str(self.clock) + "\n"
    string += "    " + "Replies:" + str(self.replies) + "\n"
    return string
      
      
      
def Philosophize(ID, pipes):
  philosopher = Philosopher(ID, pipes)

  #print(philosopher)

  while (True):
    EnjoyConference(philosopher)
    Eat(philosopher)
    EnjoyConference(philosopher)

def EnjoyConference(philosopher):
  philosopher.ReceiveMessages()

def Eat(philosopher):
  philosopher.SendRequest()
  philosopher.WaitForYourTurnToEat()
  philosopher.DeleteReplies()
  philosopher.Say("--- Eating ---")
  sleep(2)
  philosopher.Say("... Done eating ...")
  sleep(1)
  philosopher.SendRelease()
      
      
def CreatePipeMatrix(size):
  matrix = CreateFalseValueMatrix(size)
  
  #Triangle matrix with False on the main diagonal
  for row in range(size):
    for column in range(size - (row + 1)):
      column = column + (row + 1)

      a, b = Pipe()
      matrix[row][column] = a
      matrix[column][row] = b

  return matrix
  
def CreateFalseValueMatrix(size):
  array = []
  for number in range(size):
    array.append(False)

  array_of_arrays = []
  for count in range(size):
    array_of_arrays.append(copy(array))

  return array_of_arrays

  
def CreatePhilosophers(philosophers, pipe_matrix):
  for number in range(philosophers):
    philosopher = Process(target=Philosophize, args=(number, pipe_matrix[number],))
    philosopher.start()
    
    
def WaitUntilTheyAllFinish():
  active_processes = active_children()
  while (active_processes):
    print("Sleeping until they finish philosophizing...")
    sleep(10)
    active_processes = active_children()

    
if __name__ == '__main__':
  freeze_support()

  pipe_matrix = CreatePipeMatrix(PHILOSOPHER_NUMBER)
  CreatePhilosophers(PHILOSOPHER_NUMBER, pipe_matrix)

  WaitUntilTheyAllFinish()