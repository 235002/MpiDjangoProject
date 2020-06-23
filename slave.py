from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print('My rank is ', rank)
# https://rabernat.github.io/research_computing/parallel-programming-with-mpi-for-python.html
# https://www.mn.uio.no/astro/english/services/it/help/programming/mpi-linux-clusters.html#python
# https://stackoverflow.com/questions/25585918/mpi-gather-send-data-to-the-master

value = np.array(rank, 'd')
print('Rank is ', rank, 'value is ', value)
# initialize the np arrays that will store the results
valueSum = np.array(0.0, 'd')
valueMax = np.array(0.0, 'd')
# perform the reductions
comm.Reduce(value, valueSum, op=MPI.SUM, root=0)
comm.Reduce(value, valueMax, op=MPI.MAX, root=0)
if rank == 0:
    print('Rank 0, valueSum ', valueSum)
    print('Rank 0, valueMax ', valueMax)
# numDataPerRank = 10
# sendBuf = np.linspace(rank*numDataPerRank+1, (rank+1)*numDataPerRank, numDataPerRank)
# print('Rank is ', rank, 'sendBuf is ', sendBuf)
# # Passing MPI data types explicitly
# recvBuf = None
# if rank == 0:
#     recvBuf = np.empty(numDataPerRank*size, dtype='d')

# if rank == 0:
#     # Read data parameters from a file
#     # numData = 10
#     # comm.send(numData, dest=1)
#     data = np.linspace(1, numDataPerRank*size, numDataPerRank*size)
# recvBuf = np.empty(numDataPerRank, dtype='d')
# comm.Scatter(data, recvBuf, root=0)
#     comm.Send(data, dest=1)
# elif rank == 1:
#     numData = comm.recv(source=0)
#     print('Number of data to receive is ', numData)
#     data = np.empty(numData, dtype='d')
#     comm.Recv(data, source=0)
#     print('Data received is ', data)
# else:
#     numData = None
#
# numData = comm.bcast(numData, root=0)
# if rank != 0:
#     data = np.empty(numData, dtype='d')
#
# comm.Bcast(data, root=0)
# if rank == 0:
#     print('Rank is ', rank, ' data received is ', recvBuf)
