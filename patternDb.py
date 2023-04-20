import model
import pickle
from collections import deque
from multiprocessing import Pool

NANO_TO_SEC = 1000000000


def buildPatternDb(boardSize, group):
    # starting position
    puzzle = model.Puzzle(boardSize, shuffle=False)
    # number of moves = 0
    puzzle.count = 0

    blankGroup = group.copy()
    blankGroup.add(0)

    # visited permutations of groupWithBlank
    visited = set()
    # list of permutations with minimal move count so far
    evaluatedList = {}
    # permutations to visit
    notVisited = deque()

    # (puzzle, prior direction)
    notVisited.append((puzzle, (0, 0)))

    # do until you visit everything
    while notVisited:
        currentPuzzlePermutation, prevMove = notVisited.popleft()

        if not visitNode(currentPuzzlePermutation,
                         visited,
                         evaluatedList,
                         blankGroup,
                         group):
            continue
        for direction in puzzle.DIRECTIONS:
            if direction == prevMove:
                continue

            isValidMove, simulation = currentPuzzlePermutation.simulateMove(direction)

            if not isValidMove:
                continue

            # tile moved is belongs to the current group
            if simulation[currentPuzzlePermutation.blankPos[0]][currentPuzzlePermutation.blankPos[1]] in group:
                simulation.count += 1

            notVisited.append((simulation, (-direction[0], -direction[1])))

    return evaluatedList


def visitNode(puzzle, visited, closedList, groupWithBlank, group):
    puzzleHashWithBlank = puzzle.hash(groupWithBlank)

    # node has been visited
    if puzzleHashWithBlank in visited:
        return False

    # else mark as visited
    visited.add(puzzleHashWithBlank)

    # groupHash has no evaluation
    groupHash = puzzle.hash(group)
    if groupHash not in closedList:
        closedList[groupHash] = puzzle.count
    elif closedList[groupHash] > puzzle.count:
        closedList[groupHash] = puzzle.count

    return True


def main():
    boardSize = 4

    # 663
    groups = [{1, 5, 6, 9, 10, 13}, {7, 8, 11, 12, 14, 15}, {2, 3, 4}]
    closedList = []

    with Pool(processes=3) as pool:
        results = [pool.apply_async(buildPatternDb, (boardSize, groups[i], i)) for i in range(len(groups))]
        results = [res.get() for res in results]

        for res in results:
            closedList.append(res)

    with open('database_' + str(boardSize) + '.dat', 'wb') as patternDbFile:
        pickle.dump(groups, patternDbFile)
        pickle.dump(closedList, patternDbFile)


if __name__ == '__main__':
    main()
