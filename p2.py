# Ghazal Sadeghian- 9533054
# AI- First Project
# Q2- A* algorithm
from itertools import permutations

import numpy as np


def findMoves(rows, cols):
    def getMoves(table, row, col):
        moves = []

        for x in range(row):
            if "#" in table[x]:
                targetRow = x
                targetCol = table[x].index("#")

        def swap(roww, coll):
            import copy
            s = copy.deepcopy(table)
            s[targetRow][targetCol], s[roww][coll] = s[roww][coll], s[targetRow][targetCol]
            return s

        # moving up
        if targetRow > 0:
            moves.append(swap(targetRow - 1, targetCol))
        # moving right
        if targetCol < cols - 1:
            moves.append(swap(targetRow, targetCol + 1))
        # moving down
        if targetRow < rows - 1:
            moves.append(swap(targetRow + 1, targetCol))
        # moving left
        if targetCol > 0:
            moves.append(swap(targetRow, targetCol - 1))

        return moves

    return getMoves


def manhattanDistance(puzzle, unknown, row, col):
    distances = []
    for table in findGoals(puzzle, row, col):
        distance = 0
        x = np.array(list(table))
        for i in range(row):
            for j in range(col):
                y = np.where(x == unknown[i][j])
                grow = int((y[0])[0])
                gcol = int((y[1])[0])
                distance += abs(i - grow) + abs(j - gcol)
        distances.append(distance)

    return min(distances)


def key(s):
    num, letters = re.match(r'(\d*)(.*)', s).groups()
    return float(num or 'inf'), letters


def findGoals(table, row, col):
    listOfLists = [[] for i in range(row)]
    sortedLists = []
    for i in range(row):
        for j in range(col):
            if len(re.split('\d+', table[i][j])) > 1:
                listOfLists[ord(re.split('\d+', table[i][j])[1]) - 97].append(table[i][j])
    for i in range(row):
        if len(listOfLists[i]) != col:
            listOfLists[i].append("#")
    for m in range(row):
        sorted_names = sorted(listOfLists[m], key=key)
        sorted_names = sorted_names[::-1]
        sortedLists.append(sorted_names)
    allGoals = permutations(sortedLists)
    return list(allGoals)


def isGoal(table, row):
    flag = 0
    i = 1
    for x in range(row):
        common = []
        for m in range(len(table[x])):
            if len(re.split('\d+', table[x][m])) > 1:
                common.append(re.split('\d+', table[x][m])[1])
            else:
                common.append(re.split('\d+', table[x][m])[0])

        sett = set(common)
        sett.discard("#")
        if not (len(sett) <= 1):
            flag = 1
        if flag == 0:
            if "#" in table[x]:
                j = table[x].index("#")
                if j != 0:
                    flag = 1
        if flag == 0:

            while i < len(table[x]):
                if (table[x][i] != "#") and (table[x][i - 1] != "#"):
                    if (int(re.findall('\d+', table[x][i])[0]) > int(
                            re.findall('\d+', table[x][i - 1])[0])):
                        flag = 1
                i += 1
            i = 1

    if (not flag):
        return True
    else:
        return False


def aStar(puzzle, row, col, get_moves):
    def swap(roww, coll, targetRow, targetCol, table):
        import copy
        s = copy.deepcopy(table)
        s[targetRow][targetCol], s[roww][coll] = s[roww][coll], s[targetRow][targetCol]
        return s

    eNodes = 0
    pNodes = 0
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([puzzle])
    pNodes += 1
    while queue:
        dict = {}
        for path in queue:
            node = path[-1]
            dict[repr(path)] = manhattanDistance(puzzle, node, row, col) + len(path) - 1

        removedpath = eval(min(dict, key=dict.get))

        queue.remove(removedpath)
        node = removedpath[-1]

        eNodes += 1
        # path found
        if isGoal(node, row):
            dirs = []

            print("depth:")
            print(len(removedpath) - 1)

            for routeDepth in range(len(removedpath) - 1):
                for x in range(row):
                    if "#" in (removedpath[routeDepth])[x]:
                        targetRow = x
                        targetCol = (removedpath[routeDepth])[x].index("#")

                if targetRow > 0:
                    if (swap(targetRow - 1, targetCol, targetRow, targetCol, (removedpath[routeDepth])) == removedpath[
                        routeDepth + 1]):
                        dirs.append("Up")
                        continue

                if targetCol < col - 1:
                    if (swap(targetRow, targetCol + 1, targetRow, targetCol, (removedpath[routeDepth])) == removedpath[
                        routeDepth + 1]):
                        dirs.append("Right")
                        continue
                if targetRow < row - 1:
                    if (swap(targetRow + 1, targetCol, targetRow, targetCol, (removedpath[routeDepth])) == removedpath[
                        routeDepth + 1]):
                        dirs.append("Down")
                        continue

                if targetCol > 0:
                    if (swap(targetRow, targetCol - 1, targetRow, targetCol, (removedpath[routeDepth])) == removedpath[
                        routeDepth + 1]):
                        dirs.append("Left")
                        continue

            for dir in range(len(dirs)):
                print(dirs[dir])

            print("Num of expanded nodes:")
            print(eNodes)
            print("Num of produced nodes:")
            print(pNodes)
            return removedpath
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in (get_moves(node, row, col)):
            pNodes += 1
            if adjacent not in removedpath:
                new_path = list(removedpath)
                new_path.append(adjacent)
                queue.append(new_path)


import re
import random

size = input()
row = int(re.split(' ', size)[0])
col = int(re.split(' ', size)[1])

table = []
for x in range(row):
    table.append([y for y in input().split()])

# table = [["17c", "11c", "8c", "4c"], ["5b", "4b", "3b", "3b"], ["#", "8d", "6d", "5d"], ["12a", "10a", "6a", "1a"]]
# get_moves = findMoves(row, col)
# for steps in range(16):
#     table = random.choice(get_moves(table, row, col))

solution = aStar(table, row, col, findMoves(row, col))

for i in range(len(solution)):
    print(solution[i])
