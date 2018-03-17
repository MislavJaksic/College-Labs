from mpi4py import MPI
from random import randint

# http://mpi4py.scipy.org/docs/apiref/index.html
# http://mpi4py.readthedocs.io/en/stable/intro.html

#Run with: mpiexec -n 4 python mpi_lab.py

class Message(object):
  def __init__(self, message_type):
    self.type = message_type

  def __str__(self):
    string = ""
    string += "Message:"
    string += "    " + "Type:" + self.message_type
    return string

class Philosopher(object):
  def __init__(self, communicator, process_rank, number_of_processes):
    self.com = communicator
    self.rank = process_rank
    self.highest_rank = (number_of_processes - 1)
    self.forks = self.AssignForks()
    self.neighbours = self.AssignNeighbours()
    self.request_channels = self.AssignRequestChannels()
    self.requests = []

  def AssignForks(self):
    forks = {}
    if (self.rank == 0):
      forks["left"] = True
      forks["right"] = True
    elif (self.rank < self.highest_rank):
      forks["left"] = False
      forks["right"] = True
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

  def AssignRequestChannels(self):
    channels = {}
    if (self.rank == 0):
      channels["left"] = self.com.irecv(source=self.neighbours["left"])
      channels["right"] = self.com.irecv(source=self.neighbours["right"])
    elif (self.rank < self.highest_rank):
      channels["left"] = self.com.irecv(source=self.neighbours["left"])
      channels["right"] = self.com.irecv(source=self.neighbours["right"])
    elif (self.rank == self.highest_rank):
      channels["left"] = self.com.irecv(source=self.neighbours["left"])
      channels["right"] = self.com.irecv(source=self.neighbours["right"])

    return channels

  def Say(self, text):
    string = ""
    for number in range(self.rank):
      string += "  "

    string += text

    print(string)

  def __str__(self):
    string = ""
    string += "Philosopher:\n"
    string += "    " + "Rank:" + str(self.rank) + "\n"
    string += "    " + "Forks:" + str(self.forks) + "\n"
    string += "    " + "Neighbours:" + str(self.neighbours) + "\n"
    return string

# .Init()
# .Finalize()

# .Get_size()
# .Get_rank()

# .send()
# .recv()

# .isend() # return Request objects
# .irecv()

# .bcast()
# .reduce()

# .scatter()
# .gather()

# Request.test() -> returns: boolean, message
  #possibly need to refresh the Request after it is completed by the .test()
  
# Proces(i)
  #Think()
  #while (not IsHaveBothForks())
    #RequestFork()
		# posalji zahtjev za vilicom;				// ispis: trazim vilicu (i)
		# ponavljaj {
			# cekaj poruku (bilo koju!);
			# ako je poruka odgovor na zahtjev		// dobio vilicu
				# azuriraj vilice; 
			# inace ako je poruka zahtjev			// drugi traze moju vilicu
				# obradi zahtjev (odobri ili zabiljezi);
		# } dok ne dobijes trazenu vilicu;
	# }
	# jedi;								// ispis: jedem
	# odgovori na postojece zahtjeve;					// ako ih je bilo
# }

def Think():
  print("Thinking...")
  
  number_of_thought_cycles = randint(4, 16)
  for interval in range(number_of_thought_cycles):
    # i 'istovremeno' odgovaraj na zahtjeve!			// asinkrono, s povremenom provjerom
    sleep(0.25)
    
def IsHaveBothForks():
  if (IsLeftFork() and IsRightFork()):
    return True
  return False
  
def RequestFork():
  print("I need fork from...")

if __name__ == "__main__":
  communicator = MPI.COMM_WORLD
  process_rank = communicator.Get_rank()
  number_of_processes = communicator.Get_size()

  philosopher = Philosopher(communicator, process_rank, number_of_processes)

  print(philosopher)