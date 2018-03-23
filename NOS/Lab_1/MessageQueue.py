from multiprocessing import Queue, Process, active_children, current_process, freeze_support
from time import sleep
from Queue import Empty

MISSIONARY_NUMBER = 8
CANNIBAL_NUMBER = 10

WAIT_ANCHORED = 4
BOAT_SEATS = 3

HANDSHAKE_TIME = (WAIT_ANCHORED / float(BOAT_SEATS + 4))


def TravelAsMissionary(ID, missionary_queue, confirm_queue, boat_queue):
  WaitForBoatIn(ID, missionary_queue)
  EmbarkMissionary(ID, confirm_queue, boat_queue)
  CrossRiver()

def TravelAsCannibal(ID, cannibal_queue, confirm_queue, boat_queue):
  WaitForBoatIn(ID, cannibal_queue)
  EmbarkCannibal(ID, confirm_queue, boat_queue)
  CrossRiver()

def WaitForBoatIn(ID, queue):
  GetMessageFrom(ID, queue)

def EmbarkMissionary(ID, confirm_queue, boat_queue):
  PutMessageIn(ID, "Missionary embarked.", confirm_queue)
  PutMessageIn(ID, "Missionary passenger.", boat_queue)

def EmbarkCannibal(ID, confirm_queue, boat_queue):
  PutMessageIn(ID, "Cannibal embarked.", confirm_queue)
  PutMessageIn(ID, "Cannibal passenger.", boat_queue)

def CrossRiver():
  """The process can now be .join-ed"""
  pass



def CreateMissionaries(missionary_queue, confirm_queue, boat_queue):
  for number in range(MISSIONARY_NUMBER):
    ID = str(number) + "M"
    missionary = Process(target=TravelAsMissionary, args=(ID, missionary_queue, confirm_queue, boat_queue,))
    missionary.start()

def CreateCannibals(cannibal_queue, confirm_queue, boat_queue):
  for number in range(CANNIBAL_NUMBER):
    ID = str(number) + "C"
    missionary = Process(target=TravelAsCannibal, args=(ID, cannibal_queue, confirm_queue, boat_queue,))
    missionary.start()

    
def TransportPassengers(missionary_queue, cannibal_queue, confirm_queue, boat_queue):
  while (True):
    seats_empty = [BOAT_SEATS]

    EmbarkMixedPassengers(missionary_queue, cannibal_queue, confirm_queue, seats_empty)
    #Possible states after mixed embarking: a)M = C, b)M = C+1, c)C = M+1
    
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
  while IsTwoSeatsEmptyAndBothPassengersWaiting(missionary_queue, cannibal_queue, seats_empty):
    if (HandshakeMissionary(missionary_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)
    else:
      break

    if (HandshakeCannibal(cannibal_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)
    else:
      break
      
def IsTwoSeatsEmptyAndBothPassengersWaiting(missionary_queue, cannibal_queue, seats_empty):
  if (IsPassengerWaitingIn(missionary_queue) and IsPassengerWaitingIn(cannibal_queue) and IsNumberOfSeatsEmpty(2, seats_empty)):
    return True
  return False
  
def EmbarkMissionaries(missionary_queue, confirm_queue, seats_empty):
  while IsEmptySeatAndPassengerWaiting(seats_empty, missionary_queue):
    if (HandshakeMissionary(missionary_queue, confirm_queue)):
      DecreaseEmptySeatNumber(1, seats_empty)

def EmbarkCannibals(cannibal_queue, confirm_queue, seats_empty):
  if NoMissionariesOnBoat(seats_empty):
    while IsEmptySeatAndPassengerWaiting(seats_empty, cannibal_queue):
      if (HandshakeCannibal(cannibal_queue, confirm_queue)):
        DecreaseEmptySeatNumber(1, seats_empty)
        
def IsEmptySeatAndPassengerWaiting(seats_empty, queue):
  if (IsPassengerWaitingIn(queue) and IsNumberOfSeatsEmpty(1, seats_empty)):
    return True
  return False
  
def IsPassengerWaitingIn(queue):
  if IsNoMessagesInQueue(queue):
    return True
  return False
  
def IsNoMessagesInQueue(queue):
  if queue.empty():
    return True
  return False

def IsNumberOfSeatsEmpty(number, seats_empty):
  if (seats_empty[0] >= number):
    return True
  return False

def HandshakeMissionary(missionary_queue, confirm_queue):
  PutMessageIn("Boat", "A missionary can embark.", missionary_queue)
  try:
    GetMessageFrom("Boat", confirm_queue, timeout=HANDSHAKE_TIME)
    return True
  except Empty:
    return False

def HandshakeCannibal(cannibal_queue, confirm_queue):
  PutMessageIn("Boat", "A cannibal can embark.", cannibal_queue)
  try:
    GetMessageFrom("Boat", confirm_queue, timeout=HANDSHAKE_TIME)
    return True
  except Empty:
    return False
    
def DecreaseEmptySeatNumber(number, seats_empty):
  seats_empty[0] = seats_empty[0] - number

def NoMissionariesOnBoat(seats_empty):
  if (seats_empty[0] >= (BOAT_SEATS - 1)):
    return True
  return False

def CheckPassengersIn(queue):
  while (not queue.empty()):
    GetMessageFrom("Boat", queue)

def IsBoatEmpty(seats_empty):
  if (seats_empty[0] == BOAT_SEATS):
    return True
  return False
   
   
def TerminateFinishedProcesses():
  for child_process in active_children():
    pid = str(child_process.pid)
    child_process.join()
    print("Process " + pid + " joined.")

    
def PutMessageIn(ID, text, queue):
  pid = str(current_process().pid)
  message = ID + ": " + text
  print(ID + " sends - " + text)
  queue.put(message)

def GetMessageFrom(ID, queue, timeout=None):
  message = queue.get(timeout=timeout)
  print(ID + " receives - " + message)

  
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
  