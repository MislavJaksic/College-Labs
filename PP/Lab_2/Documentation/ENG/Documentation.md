## Documentation

Four in a row, player versus computer.
Dimensions: infinite height, 7 in width.
Gravity on. Tokens fall to the bottom of the columns.

Brute force search all the possible states until the desired depth is reached.
1 for victory, -1 for defeat, 0 for neither or a value calculated through recursion.
After performing the brute force search, recursively ascend the tree.

State: a grid configuration.
Data structure: upright grid.

Labor division: the smallest possible task is to calculate a single move, be it player or computer move. In order to complete a task, the processor only needs to know the top state from which it will make all other moves. 
Communication: every task needs to know from whom it is going to receive a task (the supervisor) and to who it has to send the propagated value (again, the supervisor).
Agglomeration: every task is going to make at least one player and one computer move, however it can calculate more then that depending on the desired depth.
Assignment: the tasks will be distributed by a supervisor to the workers. If there is only one processor then it will become the only worker instead of a supervisor.

Measurements:
| Processors | Time | Efficiency | Speedup |
| -- | -- | -- | -- |
| 1 | 25,02 | 1 | 1 |
| 2 | 26,46 | 0,47 | 0,95 |
| 3 | 15,21 | 0,55 | 1,64 |
| 4 | 10,23 | 0,61 | 2,45 |
| 5 | 7,32 | 0,68 | 3,42 |
| 6 | 5,88 | 0,71 | 4,26 |
| 7 | 5,37 | 0,67 | 4,66 |
| 8 | 4,11 | 0,76 | 6,09 |