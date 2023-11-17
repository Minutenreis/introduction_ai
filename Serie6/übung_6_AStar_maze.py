from dill import load
from collections.abc import Callable
import time


class Maze:
    """
    The given external form of the maze comes as a string, with the following characters:
    '#' stands for a wall tile
    ' ' a space stands for a walkable tile
    'S' stands for the start, this tile exists only once
    'F' stands for a finish, it could exist multiple times or not at all
    The outside of the maze is blocked completely by walls '#'
    The maze is given in multiple lines, spaced by '\n".

    An example generated maze could be:
    #######
    #     #
    # # # #
    #S  # #
    ### # #
    #F  #F#
    #######

    Your representation needs to be suitable to solve the underlying search problem to find the fastest way to
    a finish from the start. After a maze is solved, the solution is returned as a string, replacing the
    empty spaces of the path taken by '*' characters. The optimal solution of the maze problem is one, where
    the amount of '*' characters is minimal, connecting 'S' and one 'F' over tiles that were previously filled with
    spaces ' '. For an unsolvable maze (no 'F' can be reached from the 'S'), no stars should be added!

    The solution for the above example would be:
    #######
    #     #
    # # # #
    #S**# #
    ###*# #
    #F**#F#
    #######


    Task 1: Create an internal representation of your maze (10P)
    Define the maze as a search problem, where the task is to find the shortest path from the start to a finish.
    Encode your search problem as a graph: states are nodes and can be expanded by executing a transition function
    - Define all necessary values for the maze to be representing a search state in the __init__ function,
      this includes also a way to retrieve the path that was taken until here with its costs.
    - Define a transition function, which checks which states are neighboring a given state.
    - Define a solved function, which returns if the maze is solved in its current state
    - Define a function __eq__(other_state) to check efficiently if two search-states are the same!
    - Define a function g() which returns the cost of the path to this state from the start
    - Define a function: to_text() which returns the current state as a text, with the path taken from the 'S'
      replaced by '*' characters
    ====================================================================================================================
    HINT: To reduce unnecessary redundancy between states, feel free to globally store immutable information.
    Also feel free to add additional arguments to your function definitions as seen fit
    ====================================================================================================================
    """
    def __init__(self, data: None) -> None: # TODO: change this method signature
        """
        Stores all required variables for you representation in the state.
        """
        # TODO: implement
        pass

    @classmethod
    def from_string(cls, raw_lab_text: str):
        """
        Sets up a suitable representation of the given maze, given as a string raw_lab_text
        """
        # TODO: implement conversion to your representation
        your_representation = None
        # TODO: Probably store something in a global variable as well
        return cls(your_representation)

    def transition(self) -> list[tuple]:
        """
        returns a list of states that are neighboring the current state with their respective costs to get to from this
        current state
        """
        # TODO: implement
        pass

    def solved(self) -> bool:
        """
        returns true if the state of the maze is solved by reaching a finish 'F' from the start 'S' , else false
        """
        # TODO: implement
        pass

    def __eq__(self, other_state) -> bool:
        """
        returns true if the other_state is equal to this maze state
        """
        # TODO: implement
        pass

    def g(self) -> float:
        """
        returns the costs of the path taken until this state
        """
        # TODO: implement
        pass

    def to_string(self) -> str:
        """
        returns the string representation as given, but with the path taken from the start to the current state
        replaced by '*' characters (-> see example above in class description)
        """
        # TODO: implement
        pass


def a_search(start_state: Maze, heuristics: Callable[[Maze], float]) -> list[tuple]:
    """
    Task 2: Create the A Algorithm with closed and open list. As a reminder, these are the steps: (6P)
    1. Let the open list be the list of start nodes for the problem (first state of the maze after initialization)
    2. If the open list is empty, report a failure by returning an empty list. Otherwise, select the node n from the
       open list for which f(n) = g(n) + h(n) is minimal, g(n) being the costs of the path from start to this node,
       and h(n) the estimated costs from this state to the closest goal state by your heuristic.
    3. If the current node n represents a goal node, report success and return the solution path from the start_state to
       goal as a list of tuples.
    4. Otherwise, remove n from open_list (and add it to the set of already visited nodes) and add all its successor
       nodes to the open_list, if they weren't already. Update the successor nodes with the path to the start node.
    5. Continue with step 2!

    Add any missing necessary attributes and functions to your maze state to effectively execute your a_search
    algorithm as seen fit!

    Question (2P): A becomes A* for an admissible heuristics. Does A* return always the optimal solution first even if
    it won't use a closed list to keep track of all already visited states? Explain your answer!
    """
    # TODO: implement
    pass


def my_heuristic(lab: Maze) -> float:
    """
    Task 3: Write an admissible (zulässig) and monotone heuristic, that is based on the location of the finishes. (2P)
    Assume that each of the finishes (Bernsteinzimmer) can be detected by a scanner, that gives you the distance
    from your current position to said finish. Based on this information and the ability to see down the hallways
    from where you are standing, choose a heuristic which is also efficient to calculate in your representation of the
    maze!
    (If necessary, add the values you need in your representation or as arguments to make this calculation efficient!)
    """
    # TODO: implement
    pass


# Try it out, when it is all put together:
if __name__ == '__main__':
    """
    IMPORTANT: you can change method signatures and input arguments as seen fit, as long as the main function can be
    executed as prepared in this example (for automatically testing your solution).
    """
    with open("maze.dill", "rb") as f:
        generate_random_maze = load(f)

    # This method can produce random mazes, given a random integer seed >= 2
    print(generate_random_maze(16))

    # Let's solve mazes of different difficulty:
    maze1 = generate_random_maze(15)
    maze2 = generate_random_maze(200)
    maze3 = generate_random_maze(16180)
    maze4 = generate_random_maze(31415)

    start_time = time.perf_counter()
    solution1 = a_search(Maze.from_string(maze1), my_heuristic)
    duration1 = time.perf_counter() - start_time
    print(solution1[-1][1].to_string())

    start_time = time.perf_counter()
    solution2 = a_search(Maze.from_string(maze2), my_heuristic)
    duration2 = time.perf_counter() - start_time
    print(solution2[-1][1].to_string())

    start_time = time.perf_counter()
    solution3 = a_search(Maze.from_string(maze3), my_heuristic)
    duration3 = time.perf_counter() - start_time

    start_time = time.perf_counter()
    solution4 = a_search(Maze.from_string(maze4), my_heuristic)
    duration4 = time.perf_counter() - start_time

    print("Solve duration for maze 1:", duration1,
          "\nSolve duration for maze 2:", duration2,
          "\nSolve duration for maze 3:", duration3,
          "\nSolve duration for maze 4:", duration4
          )
    print("press enter to end process")
    input()

