from mpi4py import MPI
from random import randint
from time import sleep

# Installing relevant packages: Anaconda 2.x; conda install mpi4py; works on linux

# http://mpi4py.scipy.org/docs/apiref/index.html
# http://mpi4py.readthedocs.io/en/stable/intro.html

#Run with: mpiexec -n 2 python NPhilosophers.py

class Fork(object):
  def __init__(self, rank, filthy):
    self.rank = rank
    self.filthy = filthy

  def __str__(self):
    string = ""
    string += "    " + "Rank:" + str(self.rank)
    string += "    " + "Filthy:" + str(self.filthy)
    return string

class Philosopher(object):
  def __init__(self, communicator, process_rank, number_of_processes):
    self.com = communicator
    self.rank = process_rank
    self.highest_rank = (number_of_processes - 1)
    self.forks = self.AssignForks()
    self.neighbours = self.AssignNeighbours()
    self.com_tags = self.AssignCommunicationTags()
    self.message_channels = self.AssignRequestChannels()
    self.requests = []

  def AssignForks(self):
    forks = {}
    if (self.rank == 0):
      forks["left"] = Fork(self.highest_rank, True)
      forks["right"] = Fork(0, True)
    elif (self.rank < self.highest_rank):
      forks["left"] = False
      forks["right"] = Fork(self.rank, True)
    elif (self.rank == self.highest_rank):
      forks["left"] = False
      forks["right"] = False

    return forks

  def AssignNeighbours(self):
    neighbours = {}
    if (self.rank == 0):
      neighbours["left"] = self.highest_rank
      neighbours["right"] = self.rank + 1
    elif (self.rank < self.highest_rank):
      neighbours["left"] = self.rank - 1
      neighbours["right"] = self.rank + 1
    elif (self.rank == self.highest_rank):
      neighbours["left"] = self.rank - 1
      neighbours["right"] = 0

    return neighbours

  def AssignCommunicationTags(self):
    tags = {}
    if (self.rank == 0):
      tags["left"] = self.highest_rank
      tags["right"] = self.rank
    elif (self.rank < self.highest_rank):
      tags["left"] = (self.rank - 1)
      tags["right"] = self.rank
    elif (self.rank == self.highest_rank):
      tags["left"] = (self.rank - 1)
      tags["right"] = self.rank

    return tags

  def AssignRequestChannels(self):
    channels = {}
    channels["left"] = self.com.irecv(source=self.neighbours["left"], tag=self.com_tags["left"])
    channels["right"] = self.com.irecv(source=self.neighbours["right"], tag=self.com_tags["right"])

    return channels

    
    
  def Think(self):
    self.Say("Thinking")
  
    number_of_thought_cycles = randint(4, 16)
    for interval in range(number_of_thought_cycles):
      self.Communicate()
      sleep(0.25)
     
  def Communicate(self):
    self.ReadMessages()
    self.FulfillRequests()
      
  def ReadMessages(self):
    for side in ["right", "left"]:
      message_exists, message = self.ReceiveMessage(side)
      if message_exists:
        self.ActOnMessage(message, side)
        
  def ReceiveMessage(self, side):
    message_exists, message = self.message_channels[side].test()
    return message_exists, message
    
  def ActOnMessage(self, message, side):
    if (message == "Answer"):
      self.ReceiveCleanFork(side)
      self.RefreshMessageChannel(side)
    elif (message == "Request"):
      self.AddRequest(side)
      self.RefreshMessageChannel(side)
      
  def ReceiveCleanFork(self, side):
    #self.Say("Received " + side + " clean fork from " + str(self.neighbours[side]))
    self.forks[side] = Fork(self.neighbours[side], False)
    
  def AddRequest(self, side):
    if side not in self.requests:
      #self.Say("Adding " + side + " to request array of " + str(self.rank))
      self.requests.append(side)
    
  def RefreshMessageChannel(self, side):
    self.message_channels[side] = self.com.irecv(source=self.neighbours[side], tag=self.com_tags[side])

    
  def FulfillRequests(self):
    unfulfilled_requests = []
    for request_side in self.requests:
      if self.IsForkDirtyAndHasFork(request_side):
        self.Say("Give to " + str(self.neighbours[request_side]))
        self.com.isend("Answer", dest=self.neighbours[request_side], tag=self.com_tags[request_side])
        self.RemoveFork(request_side)
      else:
        unfulfilled_requests.append(request_side)

    self.requests = unfulfilled_requests

  def IsForkDirtyAndHasFork(self, side):
    if self.IsHasFork(side) and self.IsForkDirty(side):
      return True
    return False

  def IsForkDirty(self, side):
    if (self.forks[side].filthy == True):
      return True
    return False

  def RemoveFork(self, side):
    self.forks[side] = False

  def IsHaveBothForks(self):
    if (self.IsHasFork("left") and self.IsHasFork("right")):
      return True
    return False

  def RequestSingleFork(self):
    if (not self.IsHasFork("left")):
      self.RequestFork("left")
      return "left"
    elif (not self.IsHasFork("right")):
      self.RequestFork("right")
      return "right"

  def IsHasFork(self, side):
    if (self.forks[side] != False):
      return True
    return False

  def RequestFork(self, side):
    self.Say("Ask " + str(self.neighbours[side]))
    self.com.isend("Request", dest=self.neighbours[side], tag=self.com_tags[side])

    
  def Eat(self):
    self.Say("Eating")
    self.MakeForksFilthy()
      
  def MakeForksFilthy(self):
    self.forks["left"].filthy = True
    self.forks["right"].filthy = True
  
  
  def Say(self, text):
    string = ""
    for number in range(self.rank):
      string += "        "

    string += str(self.rank) + ": "

    string += text

    print(string)

  def __str__(self):
    string = ""
    string += "Philosopher:\n"
    string += "    " + "Rank:" + str(self.rank) + "\n"
    string += "    " + "Neighbours:" + str(self.neighbours) + "\n"
    string += "    " + "Forks:" + "\n"
    string += "    " + "    " + "Left: " + str(self.forks["left"]) + "\n"
    string += "    " + "    " + "Right: " + str(self.forks["right"]) + "\n"
    return string
  

if __name__ == "__main__":
  communicator = MPI.COMM_WORLD
  process_rank = communicator.Get_rank()
  number_of_processes = communicator.Get_size()

  philosopher = Philosopher(communicator, process_rank, number_of_processes)

  #print(philosopher)
  
  while True:
    philosopher.Think()
    while (not philosopher.IsHaveBothForks()):
      requested_fork = philosopher.RequestSingleFork()
      while (not philosopher.IsHasFork(requested_fork)):
        philosopher.Communicate()

    philosopher.Eat()
    philosopher.Communicate()