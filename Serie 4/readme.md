# Search: Towers of Hanoi 

In the previous exercise you were tasked with examining the inner workings of Towers of Hanoi.
Towers of Hanoi can not only be played with 3 rods and 3 disks, but with `n` disks and `k` rods.

The goal of the game is to move all `n` disks from the first of the `k` rods to the last one (rod 1 to rod k). All other
rods can also be used intermediary deposits of disks. Each configuration needs to abide the rules of the game, where 
only smaller disks can lay on larger ones. The size is represented by a natural number (e.g. 1 is the smallest disk, and
the disk of size `n` is the largest).

Towers of Hanoi is a an example, where search is not even close to the optimal solution. This stems from the underlying
structure of the problem exploding exponentially with the amount of disks, while being easy to solve algorithmically
with the frame steward algorithm.

However, your task is to write a search algorithm that solves Towers of Hanoi for arbitrary start configurations (not 
all disks have to be on the first rod). The evaluation of your assignment will regard the following aspects:
1. Find a good modelling of the generalized towers of hanoi as a search problem (4P):
    - represent the disks and rods in a ways, that they comply with the rules of the game
    - write a function, that tests the validity of a move between two rods
    - write a function, that calculates all valid moves for a given Towers of Hanoi state
    - write the compare function __eq__ to compare two instances of the TowersOfHanoi and see if they are the same
2. Program a heuristic search algorithm of your choice (e.g. BTHC, SHC, BS applied on your modelling of the towers of
hanoi (6P):
    - return the solution of your searches in the defined output format
    - compare the time difference between the given 3 input examples based on your algorithm with a chosen heuristic
3. Bonus: Write a function to print a towers of hanoi state in the console similar to the visualization example! (2P)

Input Format: a list of lists of integer, where the integer represents the size of the disk. E.g. the disk 1 is the 
smallest disk

### Input Example A
```python
game1 = [
    [1,2,3,4,5,6,7], # Rod 1
    [], # Rod 2
    [] # Rod 3
]
```

### Input Example B
```python
game2 = [
    [2], # Rod 1
    [3], # ...
    [4, 5, 6, 7],
    [8, 9],
    [1]
]
```

### Input Example C

```python
game3 = [
   [15],
   [],
   [],
   [],
   [],
   [],
   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
]
```

Output Format: a list of ordered pairs (tuples) of integers, where the first entry of is the origin rod and the second 
entry is the target rod of one disk movement. 

### Output Example:
```python
[(1, 2), (1, 3), (2, 3)]
```

In Towers of Hanoi only the most upper disk can be moved. In this example, the most upper disk of rod 1 is moved to rod 2. 
Then the now most upper disk is moved from rod 1 to rod 3. Lastly, the previously moved disk on rod 2 is moved to rod 3.

Visualisation of the example:
```
  #      |        |        
 ###     |        |    
#####    |        |
```

```
  |      |        |        
 ###     |        |    
#####    #        |
```

```
  |      |        |        
  |      |        |    
#####    #       ###
```

```
  |      |        |        
  |      |        #    
#####    |       ###
```

The execution of the output sequence has to abide by the rules of the game. Hence, leading to _the_ valid target 
configuration (where all disks are on the last rod, in correct order).
