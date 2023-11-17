from collections.abc import Callable
import time
import copy

type Tower = list[list[int]]
type OpenList = list[tuple[TowersOfHanoi, int, list[tuple[int, int]], list[Tower]]]

# Task 1:
class TowersOfHanoi:
    
    def __init__(self, start_config: Tower) -> None:
        """
        translates the start configuration into a representation chosen by you for solving the search problem
        """
        
        self.towers = start_config
        self.maxDisk = max([max(tower) for tower in self.towers if len(tower) > 0])
    
    def move(self, move: tuple[int, int]) -> None:
        """
        moves the top most disk from the start rod to the target rod
        :param start: int
        :param target: int
        :return: None
        """
        self.towers[move[1]].insert(0, self.towers[move[0]].pop(0))

    def valid_move(self, move: tuple[int, int]) -> bool:
        """
        tests the validity of moving the top most disk between the two rods listed in the tuple from first to second.
        returns true, if the following criteria are met:
        - the rods are existing in the game (/)
        - the start and target rod are not the same (/)
        - there is a disk that can be moved between the two rods in the specified direction
        - the move is valid by the rules of the game
        :param move: tuple
        :return: bool
        """
        
        # cant move from rod to itself
        if(move[0] == move[1]):
            return False
        
        # cant move to nonexistent rod
        if(move[0] > len(self.towers) or move[1] > len(self.towers)):
            return False
        if(move[0] < 0 or move[1] < 0):
            return False
        
        # cant move from empty rod
        if(len(self.towers[move[0]]) == 0):
            return False
        
        # move disk to empty rod or smaller tower
        if(len(self.towers[move[1]]) == 0 or self.towers[move[0]][0] < self.towers[move[1]][0]):
            return True
        
        return False

    def valid_moves(self) -> set[tuple[int, int]]:
        """
        returns the set of all valid moves out of the current TowersOfHanoi state
        :return: the set of valid moves as tuples of int
        """
        list = [(i,j) for i in range(len(self.towers)) for j in range(len(self.towers)) if(self.valid_move((i,j)))]
        return set(list)

    def __eq__(self, other) -> bool:
        """
        This function should compare two instances of TowersOfHanoi, returns true if they are the same.
        :param other: an instance of TowersOfHanoi
        :return: Boolean
        """

        if not isinstance(other, TowersOfHanoi):
            # don't attempt to compare against unrelated types
            return NotImplemented

        # not same number of poles
        if len(self.towers) != len(other.towers):
            return False

        for i in range(len(self.towers)):
            # not same number of disks on pole
            if len(self.towers[i]) != len(other.towers[i]):
                return False
            # not same disks on pole
            for j in range(len(self.towers[i])):
                if self.towers[i][j] != other.towers[i][j]:
                    return False
        return True

    # Task 3 Bonus:
    def draw(self) -> None:
        """
        prints the given TowersOfHanoi problem to the console
        :param state:
        :return:
        """
        #get maxWidth and heights of each pole
        diskWidths = []
        diskHeights = []
        
        for disk in self.towers:
            if(len(disk) == 0):
                diskWidths.append(1) # empty rod
            else:
                diskWidths.append(disk[-1]*2-1) # width of biggest disk * 2 - 1 (for better visual)
            diskHeights.append(len(disk))
        
        #print each level of each pole
        maxHeight = max(diskHeights)
        
        # width * 2 - 1 to make each width uneven (for better visual)
        for height in range(maxHeight):
            for i in range(len(self.towers)):
                if((maxHeight - height) > diskHeights[i]):
                    spaces = diskWidths[i]-1 # -2 = -1 (width of disk) -1 (disk pole)
                    leftSpaces = spaces // 2
                    rightSpaces = spaces - leftSpaces
                    print(" "*leftSpaces, end="")
                    print("|", end="")
                    print(" "*rightSpaces, end=" ")
                else:
                    currentWidth = self.towers[i][height-(maxHeight-diskHeights[i])]*2-1 #adjusting to height of current disk
                    spaces = diskWidths[i] - currentWidth
                    leftSpaces = spaces // 2
                    rightSpaces = spaces - leftSpaces
                    print(" "*leftSpaces, end="")
                    print("#"*currentWidth, end="")
                    print(" "*rightSpaces, end=" ")
            print()        

def finished_heuristic(state: TowersOfHanoi) -> float:
    """
    returns 0 no matter the given state; also known as the "already reached the goal" - heuristics
    :param state:
    :return:
    """
    return .0


# Task 2:
class HeuristicSearch:
    def __init__(self, heuristic: Callable[[TowersOfHanoi], float] = None) -> None:
        """
        initialize all containers that you need for making your search more effective, this includes:
        - closed list
        - open list
        - if necessary: parallel search trees from multiple angles (e.g. for forward + backward search)
        """
        self.L : OpenList = [] # open list (list of tuples (state, heuristic, path, previous moves))
        if not heuristic:
            self.heuristic = finished_heuristic
        else:
            self.heuristic = heuristic
    
    @staticmethod
    def drawPath(path: list[tuple[int, int]], start: TowersOfHanoi) -> None:
        """
        draws the path of the solution to the console

        Args:
            path (list[tuple[int, int]]): path to solution
            start (TowersOfHanoi): start state of solution
        """
        start.draw()
        for move in path:
            print()
            start.move(move)
            start.draw()
    
    def solve(self, state: TowersOfHanoi, draw = False) -> list[tuple[int, int]]:
        """
        :param: draw => if set to true, will print the solution to the console
        you can also use HeuristicSearch.drawPath(path ,startState) to draw the solution
        finds a solution to the given problem state
        :return: the sequence of valid moves as described in the readme.md

        If a solution has been found, clear the state variables of the HeuristicSearch
        e.g. clean the open list and the closed list and any other stateful variables
        """
        #BTHC
        start = TowersOfHanoi(copy.deepcopy(state.towers))# save for later drawing the solution
        
        self.L.append((state, self.heuristic(state), [], [])) # start state = startconfiguration, its heuristic; no paths or previous moves yet
        while len(self.L) > 0:
            current = self.L.pop(0) # get first element of open list
            if(self.heuristic(current[0]) == 0):
                # found solution -> draw path, clean up and return solution
                self.L.clear()
                if(draw):
                    self.drawPath(current[2], start)
                return current[2]
            
            children: OpenList = []  # list of children of current state
            for move in current[0].valid_moves(): # generate new children
                newState: TowersOfHanoi = TowersOfHanoi(copy.deepcopy(current[0].towers))
                newState.move(move) # new state after move
                newPath = current[2].copy()
                newPath.append(move) # old path + new move = new path
                previousMoves = current[3].copy()
                previousMoves.append(current[0]) # last previous moves + last state = new previous moves
                if(newState in previousMoves): # check if state has already been visited
                    continue
                children.append((newState, self.heuristic(newState), newPath, previousMoves))
            
            children.sort(key=lambda x: x[1])
            self.L = children + self.L # add children to the start of the open list
        return None


def my_heuristic(state: TowersOfHanoi) -> float:
    """
    :param state: a state of the TowersOfHanoi problem
    :return: the cumulated estimated cost of the path from the state to the goal state

    costs: (length of last Peg + constant) e O(n)
    """
    lastPeg = state.towers[-1]
    if(len(lastPeg) == state.maxDisk):
        return 0 # already solved
    numOfLargeDisks = len(lastPeg) 
    for i in range(len(lastPeg)): # check how many of the largest disks are on the last peg
        if(lastPeg[-i-1] != state.maxDisk-i):
            numOfLargeDisks = i
            break
    movesLastDisk =  (len(lastPeg)-numOfLargeDisks)*2 # 2 moves to get them off the last peg and later on again
    movesOtherDisks = state.maxDisk - len(lastPeg) # move all other disks to the last peg at least once
    return movesLastDisk + movesOtherDisks


if __name__ == '__main__':
    game1 = TowersOfHanoi([[1, 2, 3, 4, 5, 6, 7], [], []])
    game2 = TowersOfHanoi([[2], [3], [4, 5, 6, 7], [8, 9], [1]])
    game3 = TowersOfHanoi([[15], [], [], [], [], [], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])

    # Try your heuristic search:
    search = HeuristicSearch(my_heuristic)
    start_time = time.perf_counter()
    solution1 = search.solve(game1)
    print("solved 1 in", len(solution1), " moves")
    duration1 = time.perf_counter()-start_time
    solution2 = search.solve(game2)
    print("solved 2 in", len(solution2), " moves")
    duration2 = time.perf_counter()-start_time-duration1
    solution3 = search.solve(game3)
    print("solved 3 in", len(solution3), " moves")
    duration3 = time.perf_counter()-start_time-duration2-duration1

    print("Solve duration of game 1:", duration1, "\nSolve duration of game 2:", duration2,
          "\nSolve duration of game 3:", duration3)
    # print("Solution of game 1:", solution1, "\nSolution of game 2:", solution2, "\nSolution of game 3:", solution3)
    print("press enter to end process")
    input()

# input:
# output:
