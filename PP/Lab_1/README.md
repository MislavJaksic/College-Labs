## Lab One

There are N philosophers at a table. Two adjacent philosophers share a fork. A fork can be dirty or it can be
clean. Each philosopher is a process and they have to communicate using messages.

The problem and the solution is very similar to [The Drinking Philosophers Problem](https://dl.acm.org/citation.cfm?id=1804&dl=ACM&coll=DL).

Do (until stopped)
*  think for a random number of milliseconds
*  Do (until you have both forks)
    * ask for a fork
*  eat
  
The solution doesn't let philosophers starve to death. That is, there can be no deadlock. The algorithm is
deceptively simple. Its complexity comes from philosophers being processes and this being a parallel program.
  