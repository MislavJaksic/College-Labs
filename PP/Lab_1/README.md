## Lab One

There are N philosophers dining at a table. Two adjacent philosophers share a fork. A fork can be dirty or it
can be clean. Each philosopher is a process and they have to communicate using messages.

The problem and the solution is very similar to [The Drinking Philosophers Problem](https://dl.acm.org/citation.cfm?id=1804&dl=ACM&coll=DL).

Do (until stopped)
*  Think for a random number of milliseconds
*  Do (until you have both forks)
    * Ask for a fork
*  Eat
  
The solution doesn't let philosophers starve to death. That is, there are no deadlock. The algorithm is
deceptively simple. Its complexity comes from philosophers being processes and it being a parallel algorithm.
  