Roadmap for CNN based IA:
=========================

1. Constraints:
---------------

- no extensive dataset
- no extensive computational power

2. choices mades:
-----------------

Use ML only to score the board and to use it inside the expectimax algorithm.

Board => CNN => score (Int)

3. data set:
------------

The idea is to compute a dataset from human played games traces. We will save:
- the board
- the direction choosen by the player
- the current score

How to get board scores from these data ?
let be B a board, B.u, B.d B.l & B.r the boards obtained respectively, after an up, down, left & right move

The direction choosen by the human player gives us a partial order between the boards:
if the player choose left direction we have: B.l > (B.u, B.d, D.r)

We can represent this with a DAG graph: each edge from A to B means A > B

We can now take all these boards and build a giant graph with it, the score of each board will be the "depth" of the board in the graph.

4. data cleaning:
-----------------

As we will have only a small data amount, we need to make similar board have the same signature.
Here are the similitudes we want to avoid:
- orientation similitude: usually players play to put the highest tile in a corner, the idea is to rotate/flip the board to avoid this.
- scale similitude: the idea is that the values of the tiles doesn't impact directly the decision, only the differences between those is important. The idea to avoid this is to replace the value of the tile by it's ratio to the highest tile on the board ( put the link of the outube video about it)

5. graph building:
------------------

the graph created need to be acyclic, so we need to remove all cycles first, a simple rule to do this is to remove all vertices that are part of a oriented cycle.

6. score computing:
-------------------

the best situations will be the node with no incoming edge (meaning there is no better board known)
each node will be scored as follow:
1. compute the shortest path to all "best situation"
2. compute the weight associated to each "best situation": it will be the number of nodes in the largest covering tree
3. the score is the weighted sum of the distances computed in the step 1

