import pickle

INF = 100000
groups = []
dbDictionary = []
stateNumber = 0


def init(boardSize):
    global groups
    global dbDictionary
    global stateNumber
    # read groups and patternDictionary from file
    with open("database_" + str(boardSize) + ".dat", "rb") as dbFile:
        groups = pickle.load(dbFile)
        dbDictionary = pickle.load(dbFile)


def idaStar(puzzle, heuristic):
    # check if the
    if puzzle.checkWin():
        return []
    # initialize the database if it's empty
    if not dbDictionary:
        init(puzzle.boardSize)

    # upper bound of heuristic
    bound = patternDatabaseH(puzzle)
    # list of puzzle board that leads to solution
    path = [puzzle]
    # list of moves leading to solution
    dirs = []
    # list of elements that have to be moved
    movedElements = []
    while True:
        rem = search(path, 0, bound, dirs, movedElements, heuristic)
        if rem == True:
            return movedElements, stateNumber
        elif rem == INF:
            return None
        bound = rem


def search(path, g, bound, dirs, movedElements, heuristic):
    global stateNumber
    stateNumber += 1
    # currentPuzzlePermutation = last entry in path
    currentPuzzlePermutation = path[-1]
    # g - number of moves from start to currentPuzzlePermutation

    if(heuristic == 1):
        f = g + patternDatabaseH(currentPuzzlePermutation)
    else:
        f = g + manhattanH(currentPuzzlePermutation)

    # if f > bound --> f = bound
    if f > bound:
        return f

    if currentPuzzlePermutation.checkWin():
        return True
    minimalPath = INF

    # check all possible moves from currentPuzzlePermutation
    for direction in currentPuzzlePermutation.DIRECTIONS:
        # direction is the opposite of the last picked direction
        if dirs and (-direction[0], -direction[1]) == dirs[-1]:
            continue
        # create a copy of currentPuzzlePermutation, make a move on it and return:
        # simulated puzzle (simulation)
        # isValidMove (indicator if the move mad was valid)
        isValidMove, simulation = currentPuzzlePermutation.simulateMove(direction)

        # the move isn't valid or the simulated move is already inside the path
        if not isValidMove or simulation in path:
            continue

        # moved element was at the simulation position of previous puzzle permutation
        movedElements.append(currentPuzzlePermutation[simulation.blankPos[0]][simulation.blankPos[1]])
        path.append(simulation)
        dirs.append(direction)

        # reccure from here
        t = search(path, g + 1, bound, dirs, movedElements, heuristic)
        if t == True:
            return True
        if t < minimalPath:
            minimalPath = t

        # variables just added don't belong to minimalPath
        movedElements.pop()
        path.pop()
        dirs.pop()

    return minimalPath


def patternDatabaseH(puzzle):
    h = 0
    for g in range(len(groups)):
        group = groups[g]
        hashString = puzzle.hash(group)
        if hashString in dbDictionary[g]:
            h += dbDictionary[g][hashString]
        else:
            print("No pattern found in DB, using manhattan dist")
            for i in range(puzzle.boardSize):
                for j in range(puzzle.boardSize):
                    if puzzle[i][j] != 0 and puzzle[i][j] in group:
                        destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                   (puzzle[i][j] - 1) % puzzle.boardSize)
                        h += abs(destPos[0] - i)
                        h += abs(destPos[1] - j)
    return h


def manhattanH(puzzle):
    h = 0
    for g in range(len(groups)):
        group = groups[g]
        for i in range(puzzle.boardSize):
            for j in range(puzzle.boardSize):
                if puzzle[i][j] != 0 and puzzle[i][j] in group:
                    destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                               (puzzle[i][j] - 1) % puzzle.boardSize)
                    h += abs(destPos[0] - i)
                    h += abs(destPos[1] - j)
    return h
