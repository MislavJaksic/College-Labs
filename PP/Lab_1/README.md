## Lab One

There are N philosophers dining at a table. Two adjacent philosophers share a fork. A fork can be dirty or clean.
Each philosopher is a process and they have to communicate using messages.

The problem and the solution is very similar to [The Drinking Philosophers Problem](https://dl.acm.org/citation.cfm?id=1804&dl=ACM&coll=DL).

Do (until sated)
*  Think for a while
*  Do (until you have both forks)
    * Ask for an adjacent fork
*  Eat
  
The solution doesn't let philosophers starve to death. That is, there are no deadlocks. The algorithm is
deceptively simple. Its complexity comes from philosophers being processes and philosophers having to act
in parallel.
  
