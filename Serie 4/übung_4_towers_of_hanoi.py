from collections.abc import Callable
import time


# Task 1:
class TowersOfHanoi:
    
    towers: list[list[int]]
    
    def __init__(self, start_config: list[list[int]]) -> None:
        """
        translates the start configuration into a representation chosen by you for solving the search problem
        """
        
        self.towers = start_config

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
        list = [{i,j} for i in range(len(self.towers)) for j in range(len(self.towers)) if(self.valid_move((i,j)))]
        set = set(list)
        return set

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
        if not heuristic:
            self.heuristic = finished_heuristic
        else:
            self.heuristic = heuristic

    def solve(self, state: TowersOfHanoi) -> list[tuple[int, int]]:
        """
        finds a solution to the given problem state
        :return: the sequence of valid moves as described in the readme.md

        If a solution has been found, clear the state variables of the HeuristicSearch
        e.g. clean the open list and the closed list and any other stateful variables
        """
        # TODO: implement
        pass


def my_heuristic(state: TowersOfHanoi) -> float:
    """
    :param state: a state of the TowersOfHanoi problem
    :return: the cumulated estimated cost of the path from the state to the goal state
    """
    # TODO: implement
    pass


if __name__ == '__main__':
    game1 = TowersOfHanoi([[1, 2, 3, 4, 5, 6, 7], [], []])
    game2 = TowersOfHanoi([[2], [3], [4, 5, 6, 7], [8, 9], [1]])
    game3 = TowersOfHanoi([[15], [], [], [], [], [], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])

    game2.draw()
    # Try your heuristic search:
    search = HeuristicSearch(my_heuristic)
    start_time = time.perf_counter()
    solution1 = search.solve(game1)
    duration1 = time.perf_counter()-start_time
    solution2 = search.solve(game2)
    duration2 = time.perf_counter()-start_time-duration1
    solution3 = search.solve(game3)
    duration3 = time.perf_counter()-start_time-duration2-duration1

    print("Solve duration of game 1:", duration1, "\nSolve duration of game 2:", duration2,
          "\nSolve duration of game 3:", duration3)
    print("press enter to end process")
    input()
    # TODO: implement
    pass


# input:
# output:
