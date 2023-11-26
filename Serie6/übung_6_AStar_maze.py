from dill import load
from collections.abc import Callable
import time
import networkx as nx


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
    def __init__(self, data: nx.Graph, current: str, finish: list[str], path: list[str], rows : list[str]):
        """
        Stores all required variables for you representation in the state.
        """
        self.graph = data #potentially global
        self.current = current
        self.finish = finish #potentially global
        self.path = path
        self.rows = rows #potentially global

    @classmethod
    def from_string(cls, raw_lab_text: str):
        """
        Sets up a suitable representation of the given maze, given as a string raw_lab_text
        """
        graph = nx.Graph()
        nodes = []
        edges = []
        rows = raw_lab_text.split("\n")
        xLength = len(rows[0])
        yLength = len(rows)
        start = ""
        finish = []
        for i in range(xLength):
            for j in range(yLength):
                if rows[j][i] == " " or rows[j][i] == "S" or rows[j][i] == "F":
                    nodes.append(str(i) + "x" + str(j) + "y")
                    if(i > 0 and rows[j][i-1] == " "):
                        edges.append((str(i) + "x" + str(j) + "y", str(i-1) + "x" + str(j) + "y"))
                    if(i < xLength-1 and rows[j][i+1] == " "):
                        edges.append((str(i) + "x" + str(j) + "y", str(i+1) + "x" + str(j) + "y"))
                    if(j > 0 and rows[j-1][i] == " "):
                        edges.append((str(i) + "x" + str(j) + "y", str(i) + "x" + str(j-1) + "y"))
                    if(j < yLength-1 and rows[j+1][i] == " "):
                        edges.append((str(i) + "x" + str(j) + "y", str(i) + "x" + str(j+1) + "y"))
                    if(rows[j][i] == "S"):
                        start = str(i) + "x" + str(j) + "y"
                    if(rows[j][i] == "F"):
                        finish.append(str(i) + "x" + str(j) + "y")
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        
        return cls(graph, start, finish, [], rows)

    # returns list[Maze]
    def transition(self):
        """
        returns a list of states that are neighboring the current state with their respective costs to get to from this
        current state
        """
        newStates = [node for node in self.graph.adj[self.current] if node not in self.path]
        return [Maze(self.graph, node, self.finish, self.path + [self.current],self.rows) for node in newStates]

    def solved(self) -> bool:
        """
        returns true if the state of the maze is solved by reaching a finish 'F' from the start 'S' , else false
        """
        if self.current in self.finish:
            return True
        return False

    def __eq__(self, other_state) -> bool:
        """
        returns true if the other_state is equal to this maze state
        """
        
        if not isinstance(other_state, Maze):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.current != other_state.current:
            return False
        
        if self.finish != other_state.finish:
            return False
        
        if (nx.is_isomorphic(self.graph, other_state.graph) == False):
            return False
        
        return True

    def g(self) -> float:
        """
        returns the costs of the path taken until this state
        """
        return len(self.path)

    def to_string(self) -> str:
        """
        returns the string representation as given, but with the path taken from the start to the current state
        replaced by '*' characters (-> see example above in class description)
        """
        if(not self.solved()):
            return "\n".join(self.rows)
        
        tempRows = self.rows.copy()
        
        for elem in self.path[1:]:
            (x,y) = self.getCoord(elem)
            tempRows[y] = tempRows[y][:x] + "*" + tempRows[y][x+1:]
                    
        return "\n".join(tempRows)
    
    @staticmethod
    def getCoord(node):
        return (int(node.split("x")[0]), int(node.split("x")[1].split("y")[0]))

def a_search(start_state: Maze, heuristics: Callable[[Maze], float]) -> Maze:
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
    L = [start_state]
    C = []
    lengths = {}
    G = nx.DiGraph()
    G.add_node(start_state.current)
    while len(L) > 0:
        n = min(L, key=lambda x: x.g() + heuristics(x))
        L.remove(n)
        C.append(n)
        if n.solved():
            return n
        for m in n.transition():
            if m.current not in G.predecessors(n.current):
                if m not in C and m not in L:
                    G.add_node(m.current)
                    lengths[m.current] = m.g()
                    G.add_edge(n.current, m.current)
                    L.append(m)
                else:
                    if m.g() < lengths[m.current]:
                        lengths[m.current] = m.g()
                        oldEdges = G.in_edges(m.current) # only 1
                        G.remove_edge(oldEdges[0][0], oldEdges[0][1])
                        G.add_edge(n.current, m.current)
                        costChange = m.g() - lengths[m.current]
                        for succ in G.successors(m.current):
                            lengths[succ] += costChange
    return None


def my_heuristic(lab: Maze) -> float:
    """
    Task 3: Write an admissible (zulässig) and monotone heuristic, that is based on the location of the finishes. (2P)
    Assume that each of the finishes (Bernsteinzimmer) can be detected by a scanner, that gives you the distance
    from your current position to said finish. Based on this information and the ability to see down the hallways
    from where you are standing, choose a heuristic which is also efficient to calculate in your representation of the
    maze!
    (If necessary, add the values you need in your representation or as arguments to make this calculation efficient!)
    """
    if lab.solved():
        return 0
    (x,y) = Maze.getCoord(lab.current)
    finishes = [Maze.getCoord(finish) for finish in lab.finish]
    minDistance = float("inf")
    for (x1,y1) in finishes:
        distance = abs(x1-x) + abs(y1-y)
        if distance < minDistance:
            minDistance = distance
    return minDistance
    


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
    print(solution1.to_string())

    start_time = time.perf_counter()
    solution2 = a_search(Maze.from_string(maze2), my_heuristic)
    duration2 = time.perf_counter() - start_time
    print(solution2.to_string())

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

