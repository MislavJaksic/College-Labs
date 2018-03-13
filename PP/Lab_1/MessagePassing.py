from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# .Init()
# .Finalize()

# .Get_size()
# .Get_rank()

# .Send()
# .Recv()

# .Bcast()
# .Reduce()

# .Scatter()
# .Gather()

if rank == 0:
  data = {'a': 7, 'b': 3.14}
  comm.send(data, dest=1, tag=11)
  print("Master")
elif rank != 0:
  data = comm.recv(source=0, tag=11)
  print("Slave")