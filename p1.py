# Ghazal Sadeghian- 9533054
# AI- First Project
# Q1- IDS algorithm

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


def ids(table, row, col, getMoves, start):
    import itertools
    global eNodes
    eNodes = 0
    global pNodes
    pNodes = 0

    def swap(roww, coll, targetRow, targetCol, table):
        import copy
        s = copy.deepcopy(table)
        s[targetRow][targetCol], s[roww][coll] = s[roww][coll], s[targetRow][targetCol]
        return s

    def dfs(route, depth):
        global pNodes
        global eNodes
        pNodes += 1
        if depth == 0:
            return

        if (isGoal((route[-1]), row)):
            dirs = []

            print("depth:")
            print(len(route) - 1)

            for routeDepth in range(len(route) - 1):
                for x in range(row):
                    if "#" in (route[routeDepth])[x]:
                        targetRow = x
                        targetCol = (route[routeDepth])[x].index("#")

                if targetRow > 0:
                    if (swap(targetRow - 1, targetCol, targetRow, targetCol, (route[routeDepth])) == route[
                        routeDepth + 1]):
                        dirs.append("Up")
                        continue

                if targetCol < col - 1:
                    if (swap(targetRow, targetCol + 1, targetRow, targetCol, (route[routeDepth])) == route[
                        routeDepth + 1]):
                        dirs.append("Right")
                        continue
                if targetRow < row - 1:
                    if (swap(targetRow + 1, targetCol, targetRow, targetCol, (route[routeDepth])) == route[
                        routeDepth + 1]):
                        dirs.append("Down")
                        continue

                if targetCol > 0:
                    if (swap(targetRow, targetCol - 1, targetRow, targetCol, (route[routeDepth])) == route[
                        routeDepth + 1]):
                        dirs.append("Left")
                        continue

            for dir in range(len(dirs)):
                print(dirs[dir])

            print("Num of expanded nodes:")
            print(eNodes)
            print("Num of produced nodes:")
            print(pNodes)
            return route

        for move in getMoves(route[-1], row, col):
            if move not in route:
                eNodes += 1
                next_route = dfs(route + [move], depth - 1)
                if next_route:
                    return next_route

    for depth in itertools.count(start=start):
        route = dfs([table], depth)
        if route:
            return route


import re
import random

size = input()
row = int(re.split(' ', size)[0])
col = int(re.split(' ', size)[1])
initialDepth = int(input("Enter initial depth:"))

table = []
for x in range(row):
    table.append([y for y in input().split()])

# table = [["17c", "11c", "8c", "4c"], ["5b", "4b", "3b", "3b"], ["#", "8d", "6d", "5d"], ["12a", "10a", "6a", "1a"]]
# get_moves = findMoves(row, col)
# for steps in range(17):
#     table = random.choice(get_moves(table, row, col))

solution = ids(table, row, col, findMoves(row, col), initialDepth)
for i in range(len(solution)):
    print(solution[i])
