import math
import time
import random
import timeit
from collections import Counter

class ClueCell:
    position = None
    southSum = None
    eastSum = None
    easternValueCells = None
    southernValueCells = None
    eastDomain = None
    southDomain = None

    def __init__(self, i, j, ss, es):
        self.position = (i, j)
        self.southSum, self.eastSum = ss, es
        self.easternValueCells = list()
        self.southernValueCells = list()
        self.eastDomain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.southDomain = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def isViolated(self):
        if self.eastSum != 0:
            # if self.duplicateEast():
            #     return True
            if self.checkEastSum():
                return True

        if self.southSum != 0:
            # if self.duplicateSouth():
            #     return True
            if self.checkSouthSum():
                return True

        return False

    def duplicateEast(self):
        temp = set()
        for cell in self.easternValueCells:
            if cell.value not in temp:
                if cell.value != 0:
                    temp.add(cell.value)
            else:
                return True

        return False

    def checkEastSum(self):
        if self.eastSum == 0:
            return False

        allAssigned = True

        temp1 = 0
        unAssigned = 0
        for cell in self.easternValueCells:
            if temp1 <= self.eastSum:
                if cell.value == 0:
                    unAssigned += 1
                    allAssigned = False
                temp1 += cell.value
            else:
                return True


        if (unAssigned*(unAssigned+1))/2 + temp1 < self.eastSum:
            return True

        if (45 - ((unAssigned-1)*unAssigned)/2) + temp1 > self.eastSum:
            return True
        # temp2 = temp1
        # for i in range(unAssigned):
        #     temp2 += i + 1
        # if temp2 > self.eastSum:
        #     return True
        #
        # temp2 = temp1
        # for i in range(unAssigned):
        #     temp2 += 9 - i
        # if temp2 < self.eastSum:
        #     return True

        if allAssigned and temp1 < self.eastSum:
            return True
        else:
            return False

    def duplicateSouth(self):
        temp = set()
        for cell in self.southernValueCells:
            if cell.value not in temp:
                if cell.value != 0:
                    temp.add(cell.value)
            else:
                return True

        return False

    def checkSouthSum(self):
        if self.southSum == 0:
            return False

        allAssigned = True

        unAssigned = 0
        temp1 = 0
        for cell in self.southernValueCells:
            if temp1 <= self.southSum:
                if cell.value == 0:
                    unAssigned += 1
                    allAssigned = False
                temp1 += cell.value
            else:
                return True

        if unAssigned*(unAssigned+1)/2 + temp1 > self.southSum:
            return True

        if (45 - (unAssigned-1)*unAssigned/2) + temp1 < self.southSum:
            return True

        # temp2 = temp1
        # for i in range(unAssigned):
        #     temp2 += i + 1
        # if temp2 > self.southSum:
        #     return True
        #
        # temp2 = temp1
        # for i in range(unAssigned):
        #     temp2 += 9 - i
        # if temp2 < self.southSum:
        #     return True

        if allAssigned and temp1 < self.southSum:
            return True
        else:
            return False

    def isSatisfied(self):
        if not self.isViolated():
            temp1 = 0
            temp2 = 0
            for cell in self.easternValueCells:
                if temp1 <= self.eastSum:
                    temp1 += cell.value
                else:
                    return False

            for cell in self.southernValueCells:
                if temp2 <= self.southSum:
                    temp2 += cell.value
                else:
                    return False
        else:
            return False

        return temp1 == self.eastSum and temp2 == self.southSum


class ValueCell:
    position = None
    northClue = None
    westClue = None
    value = None
    assigned = None
    kakBoard = None

    def __init__(self, i, j, v):
        self.position = (i, j)
        self.value = v
        self.assigned = False

    def assign(self, value):
        if value not in self.westClue.eastDomain or value not in self.northClue.southDomain or self.assigned:
            return False
        elif value in range(1, 10):
            self.assigned = True
            self.value = value
            self.westClue.eastDomain.remove(value)
            self.northClue.southDomain.remove(value)
            return True

        return False

    def unAssign(self):
        if not self.assigned:
            return False
        else:
            self.westClue.eastDomain.add(self.value)
            self.northClue.southDomain.add(self.value)
            self.value = 0
            self.assigned = False
            return True


class Kakuro:
    board = None
    bestVariables = None

    def __init__(self, m, n, clueSet):
        self.board = self.board_generator(m, n, clueSet)
        self.updateConstraints()
        self.bestVariables = list()

    def updateConstraints(self):
        m = len(self.board)
        n = len(self.board[0])

        for i in range(m):
            for j in range(n):

                current_cell = self.board[i][j]
                if isinstance(current_cell, ClueCell):

                    if current_cell.eastSum != 0:
                        for k in range(current_cell.position[1] + 1, n):
                            candidate = self.board[i][k]
                            if isinstance(candidate, ValueCell):
                                current_cell.easternValueCells.append(candidate)
                                candidate.westClue = current_cell
                            else:
                                break

                    if current_cell.southSum != 0:
                        for k in range(current_cell.position[0] + 1, m):
                            candidate = self.board[k][j]
                            if isinstance(candidate, ValueCell):
                                current_cell.southernValueCells.append(candidate)
                                candidate.northClue = current_cell
                            else:
                                break

        return

    def chooseNextVar(self):
        m = len(self.board)
        n = len(self.board[0])

        for i in range(m):
            for j in range(n):
                current_cell = self.board[i][j]
                if isinstance(current_cell, ValueCell):
                    if not current_cell.assigned:
                        return current_cell

        return None

    def chooseNextVarEnhanced(self):
        m = len(self.board)
        n = len(self.board[0])

        smallestSum = math.inf
        # biggestSum = -math.inf
        bestVar = None
        for i in range(m):
            for j in range(n):
                current_cell = self.board[i][j]
                if isinstance(current_cell, ValueCell):
                    if not current_cell.assigned:
                        tempSmall = math.inf
                        # tempBig = 0
                        if current_cell.westClue is not None:
                            tempSmall = current_cell.westClue.eastSum
                        if current_cell.northClue is not None:
                            if current_cell.northClue.southSum < tempSmall:
                                tempSmall = current_cell.northClue.southSum

                        if tempSmall < smallestSum:
                            smallestSum = tempSmall
                            bestVar = current_cell
        return bestVar

    def isConsistent(self):

        m = len(self.board)
        n = len(self.board[0])
        for i in range(m):
            for j in range(n):
                current_cell = self.board[i][j]
                if isinstance(current_cell, ClueCell):
                    if current_cell.isViolated():
                        return False

        return True

    def isConsistentEnhanced(self, variable):
        if variable.westClue.isViolated() or variable.northClue.isViolated():
            return False
        return True

    def orderValues(self, domain):
        # ########### Random ###########################

        # temp = domain
        # result = list()
        # while len(temp) != 0:
        #     index = random.randint(0, len(temp) - 1)
        #     result.append(temp.pop(index))
        # return result


        # ########### Median ###########################

        # temp = sorted(domain)
        # result = list()
        # while len(temp) != 0:
        #     result.append(temp.pop(int(len(temp)/2)))
        # return result


        # ########### biggest ##########################

        # temp = sorted(domain, reverse=True)
        # return temp


        # ########## smallest ##########################

        temp = sorted(domain)
        return temp

    def isWin(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                current_cell = self.board[i][j]
                if isinstance(current_cell, ClueCell):
                    if not current_cell.isSatisfied():
                        return False

        return True

    def board_generator(self, m, n, clueSet):
        result = []
        for i in range(m):
            result.append([])
            for j in range(n):
                result[i].append(ValueCell(i, j, 0))

        for clue in clueSet:
            if len(clue) == 2:
                result[clue[0]][clue[1]] = ClueCell(clue[0], clue[1], 0, 0)
            else:
                result[clue[0]][clue[1]] = ClueCell(clue[0], clue[1], clue[2], clue[3])

        return result


def backTrackingSearch(csp: Kakuro):
    return recursiveBackTracking(csp)


def recursiveBackTracking(csp: Kakuro):
    if csp.isWin():
        return True

    variable = csp.chooseNextVarEnhanced()

    if variable is None:
        # print_kakuro(csp)
        return csp.isWin()

    temp = csp.orderValues(list(set(variable.northClue.southDomain).intersection(set(variable.westClue.eastDomain))))
    for value in temp:
        if variable.assign(value):
            if csp.isConsistentEnhanced(variable):
                result = recursiveBackTracking(csp)
                if result:
                    return True
                else:
                    variable.unAssign()
            else:
                variable.unAssign()

    return False


def print_kakuro(kak):
    m = len(kak.board)
    n = len(kak.board[0])

    for i in range(m):
        print("\n\n", end="")
        for j in range(n):
            if isinstance(kak.board[i][j], ClueCell):
                y = str(kak.board[i][j].southSum).__add__(",")
                x = str(kak.board[i][j].eastSum)
                t = y.__add__(x)
                print(f"{t:^10}", end="")
            else:
                print(f"{kak.board[i][j].value:^10}", end="")
        print("\n\n", end="")
    print("\n#######################################################################################################\n")


example_1 = {(0, 0), (0, 1), (0, 2, 30, 0), (0, 3, 11, 0), (0, 4), (1, 0), (2, 0, 0, 18), (3, 0, 0, 24), (4, 0),
             (1, 1, 16, 7), (1, 4, 4, 0), (4, 1, 0, 12), (4, 4)}

example_2 = {(0, 0, 0, 0), (0, 1, 0, 0), (0, 2, 0, 0), (0, 3, 4, 0), (0, 4, 24, 0), (0, 5, 30, 0), (0, 6, 0, 0),
             (0, 7, 0, 0), (0, 8, 0, 0), (0, 9, 0, 0), (0, 10, 0, 0), (0, 11, 0, 0), (0, 12, 0, 0),
             (1, 0, 0, 0), (1, 1, 17, 0), (1, 2, 7, 18), (1, 6, 0, 0), (1, 7, 0, 0), (1, 8, 4, 0), (1, 9, 41, 0), (1, 10, 0, 0),
             (1, 11, 0, 0), (1, 12, 0, 0),
             (2, 0, 0, 29), (2, 6, 16, 0), (2, 7, 4, 10), (2, 10, 0, 0), (2, 11, 0, 0), (2, 12, 0, 0),
             (3, 0, 0, 11), (3, 3, 16, 29), (3, 10, 3, 0), (3, 11, 0, 0), (3, 12, 0, 0),
             (4, 0, 0, 0), (4, 1, 0, 8), (4, 4, 28, 19), (4, 8, 24, 5), (4, 11, 4, 0), (4, 12, 17, 0),
             (5, 0, 0, 0), (5, 1, 0, 0), (5, 2, 0, 15), (5, 5, 6, 0), (5, 6, 0, 0), (5, 7, 0, 27),
             (6, 0, 0, 0), (6, 1, 4, 0), (6, 2, 17, 0), (6, 3, 0, 6), (6, 6, 0, 0), (6, 7, 0, 14), (6, 10, 0, 12),
             (7, 0, 0, 12), (7, 3, 16, 3), (7, 6, 0, 0), (7, 7, 0, 15), (7, 10, 4, 0), (7, 11, 0, 0), (7, 12, 0, 0),
             (8, 0, 0, 24), (8, 6, 16, 0), (8, 7, 4, 0), (8, 8, 29, 6), (8, 11, 6, 0), (8, 12, 0, 0),
             (9, 0, 0, 0), (9, 1, 0, 0), (9, 2, 0, 10), (9, 5, 4, 15), (9, 9, 7, 4), (9, 12, 3, 0),
             (10, 0, 0, 0), (10, 1, 0, 0), (10, 2, 0, 0), (10, 3, 0, 32), (10, 10, 17, 3),
             (11, 0, 0, 0), (11, 1, 0, 0), (11, 2, 0, 0), (11, 3, 0, 4), (11, 6, 0, 0), (11, 7, 0, 23),
             (12, 0, 0, 0), (12, 1, 0, 0), (12, 2, 0, 0), (12, 3, 0, 0), (12, 4, 0, 0), (12, 5, 0, 0), (12, 6, 0, 0), (12, 7, 0, 18),
             (12, 11, 0, 0), (12, 12, 0, 0)}

example_3 = {(0, 0, 0, 0), (0, 1, 16, 0), (0, 2, 24, 0), (0, 3, 0, 0), (0, 4, 0, 0), (1, 0, 0, 15), (1, 3, 23, 0),
             (1, 4, 0, 0), (2, 0, 0, 22), (2, 4, 3, 0), (3, 0, 0, 0), (3, 1, 0, 18), (4, 0, 0, 0), (4, 1, 0, 0),
             (4, 2, 0, 11)}

example_4 = {(0, 0, 0, 0), (0, 1, 0, 0), (0, 2, 34, 0), (0, 3, 12, 0), (0, 4, 0, 0), (0, 5, 0, 0), (0, 6, 0, 0),
             (0, 7, 0, 0),
             (1, 0, 0, 0), (1, 1, 8, 16), (1, 4, 8, 0), (1, 5, 0, 0), (1, 6, 0, 0), (1, 7, 0, 0),
             (2, 0, 0, 15), (2, 5, 19, 0), (2, 6, 0, 0), (2, 7, 0, 0),
             (3, 0, 0, 13), (3, 3, 11, 14), (3, 6, 21, 0), (3, 7, 0, 0),
             (4, 0, 0, 0), (4, 1, 0, 13), (4, 4, 0, 8), (4, 7, 0, 0),
             (5, 0, 0, 0), (5, 1, 0, 11), (5, 4, 11, 17), (5, 7, 12, 0),
             (6, 0, 0, 0), (6, 1, 0, 0), (6, 2, 0, 9), (6, 5, 8, 14),
             (7, 0, 0, 0), (7, 1, 0, 0), (7, 2, 0, 0), (7, 3, 0, 13),
             (8, 0, 0, 0), (8, 1, 0, 0), (8, 2, 0, 0), (8, 3, 0, 0), (8, 4, 0, 11), (8, 7, 0, 0)}

# kakuro = Kakuro(5, 5, example_1)
# kakuro = Kakuro(13, 13, example_2)
# kakuro = Kakuro(5, 5, example_3)
# kakuro = Kakuro(9, 8, example_4)


def my_func():
    kakuro = Kakuro(13, 13, example_2)
    backTrackingSearch(kakuro)

my_time = timeit.timeit("my_func()", "from __main__ import my_func", number=10)
print("\n\n\n\n\n\n\n\n\n\n\n\n"
      "\n###########################################################################################################\n")
print("RecursiveBacktracking\n"
      "Consistency Checking: Simple\n"
      "Variable Choosing Order: Enhanced\n"
      "Value Choosing Order: Random\n"
      "Number of Executions: 100\n"
      f"Average time: {my_time / 10}")


# print_kakuro(kakuro)
# time1 = time.time()
# backTrackingSearch(kakuro)
# time2 = time.time()
# print_kakuro(kakuro)
# print("Elapsed time = ", time2 - time1)
