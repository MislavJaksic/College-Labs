## Lab_One

### Message queues

Cannibals and missionaries need to cross a river. They use a boat of a certain capacity to cross it. A boat may
never have more cannibals then missionaries. Missionaries, cannibals and the boat are processes and communicate
using message queues.

When the boat docks, it tells a passanger to board it by "handshaking" either a missionary or cannibal. The
boat leaves the dock when it is at capacity. The complexity of the program comes from passengers being processes
and having to communicate using queues.

### Pipelines

Multiple philosophers are attending a conference. Only a single philosopher can eat at any time. The
philosophers determine who is going to eat by communicating using a pipeline.

Just like message queues, the complicated part of the problem is executing everything in parallel.