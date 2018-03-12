from multiprocessing import Queue, Process, active_children, current_process, freeze_support
from time import sleep
from Queue import Empty

MISSIONARY_NUMBER = 2
CANNIBAL_NUMBER = 2

WAIT_ANCHORED = 4
BOAT_SEATS = 1

HANDSHAKE_TIME = (WAIT_ANCHORED / float(BOAT_SEATS + 4))

class Message(object):
  def __init__(self, text):
    self.text = text

  def __repr__(self):
    return self.text

  def __str__(self):
    return self.text

def TravelAsMissionary(missionary_queue, confirm_queue, boat_queue):
  WaitForBoatIn(missionary_queue)
  EmbarkMissionary(confirm_queue, boat_queue)
  CrossRiver()

def TravelAsCannibal(cannibal_queue, confirm_queue, boat_queue):
  WaitForBoatIn(cannibal_queue)
  EmbarkCannibal(confirm_queue, boat_queue)
  CrossRiver()

def WaitForBoatIn(queue):
  GetMessageFrom(queue)

def EmbarkMissionary(confirm_queue, boat_queue):
  PutMessageIn("Missionary embarked.", confirm_queue)
  PutMessageIn("Missionary passenger.", boat_queue)

def EmbarkCannibal(confirm_queue, boat_queue):
  PutMessageIn("Cannibal embarked.", confirm_queue)
  PutMessageIn("Cannibal passenger.", boat_queue)

def CrossRiverOnBoat():
  """The process can now be .join-ed"""
  pass



def CreateMissionaries(missionary_queue, confirm_queue, boat_queue):
  for number in range(MISSIONARY_NUMBER):
    missionary = Process(target=TravelAsMissionary, args=(missionary_queue, confirm_queue, boat_queue,))
    missionary.start()

def CreateCannibals(cannibal_queue, confirm_queue, boat_queue):
  for number in range(CANNIBAL_NUMBER):
    missionary = Process(target=TravelAsCannibal, args=(cannibal_queue, confirm_queue, boat_queue,))
    missionary.start()

    
    
def TransportPassengers(missionary_queue, cannibal_queue, confirm_queue, boat_queue):
  while (1):
    seats_empty = [BOAT_SEATS]

    EmbarkMixedPassengers(missionary_queue, cannibal_queue, confirm_queue, seats_empty)
    EmbarkMissionaries(missionary_queue, confirm_queue, seats_empty)
    EmbarkCannibals(cannibal_queue, confirm_queue, seats_empty)
    
    sleep(2 * HANDSHAKE_TIME)
    print("--- Passenger manifest ---")
    CheckPassengersIn(boat_queue)
    print("---                    ---")

    if IsBoatEmpty(seats_empty):
      print("There are no passengers waiting to be rowed across.")
      break

    print("")
    
def EmbarkMixedPassengers(missionary_queue, cannibal_queue, confirm_queue, seats_empty):
  while (IsPassengerWaitingIn(missionary_queue) and IsPassengerWaitingIn(cannibal_queue) and IsNumberOfSeatsEmpty(2, seats_empty)):
    if (HandshakeMissionary(missionary_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)
    else:
      break

    if (HandshakeCannibal(cannibal_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)
    else:
      break

def EmbarkMissionaries(missionary_queue, confirm_queue, seats_empty):
  while (IsPassengerWaitingIn(missionary_queue) and IsNumberOfSeatsEmpty(1, seats_empty)):
    if (HandshakeMissionary(missionary_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)

def EmbarkCannibals(cannibal_queue, confirm_queue, seats_empty):
  if NoMissionariesOnBoat(seats_empty):
    while (IsPassengerWaitingIn(cannibal_queue) and IsNumberOfSeatsEmpty(1, seats_empty)):
      if (HandshakeCannibal(cannibal_queue, confirm_queue)):
        DecreaseEmptySeatNumber(1, seats_empty)

def HandshakeMissionary(missionary_queue, confirm_queue):
  PutMessageIn("A missionary can embark.", missionary_queue)
  try:
    GetMessageFrom(confirm_queue, timeout=HANDSHAKE_TIME)
    return True
  except Empty:
    return False

def HandshakeCannibal(cannibal_queue, confirm_queue):
  PutMessageIn("A cannibal can embark.", cannibal_queue)
  try:
    GetMessageFrom(confirm_queue, timeout=HANDSHAKE_TIME)
    return True
  except Empty:
    return False

def IsPassengerWaitingIn(queue):
  if queue.empty():
    return True
  return False

def IsNumberOfSeatsEmpty(number, seats_empty):
  if (seats_empty[0] >= number):
    return True
  return False

def DecreaseEmptySeatNumber(number, seats_empty):
  seats_empty[0] = seats_empty[0] - number

def NoMissionariesOnBoat(seats_empty):
  if (seats_empty[0] >= (BOAT_SEATS - 1)):
    return True
  return False

def IsBoatEmpty(seats_empty):
  if (seats_empty[0] == BOAT_SEATS):
    return True
  return False

def CheckPassengersIn(queue):
  while (not queue.empty()):
    GetMessageFrom(queue)

    
   
def TerminateFinishedProcesses():
  for child_process in active_children():
    pid = str(child_process.pid)
    child_process.join()
    print("Process " + pid + " joined.")

    
    
def PutMessageIn(text, queue):
  pid = str(current_process().pid)
  message = Message(pid + ": " + text)
  print(pid + " sends - " + text)
  queue.put(message)

def GetMessageFrom(queue, timeout=None):
  pid = str(current_process().pid)
  message = queue.get(timeout=timeout)
  print(pid + " receives - " + str(message))
  
  
  
if __name__ == '__main__':
  freeze_support()
  missionary_queue = Queue(1)
  cannibal_queue = Queue(1)
  confirm_queue = Queue(1)
  boat_queue = Queue(BOAT_SEATS)
  
  CreateMissionaries(missionary_queue, confirm_queue, boat_queue)
  CreateCannibals(cannibal_queue, confirm_queue, boat_queue)
  
  TransportPassengers(missionary_queue, cannibal_queue, confirm_queue, boat_queue)

  TerminateFinishedProcesses()
  