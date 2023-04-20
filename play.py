import model
import ai

# ai
ai.init(4)


def gameLoop():
    sumStateNum = 0
    sumNumMoves = 0

    NUMBER_OF_TRIES = 5

    # for i in range(NUMBER_OF_TRIES):
    #     puzzle = model.Puzzle(boardSize=4)
    #     aiMovedElements, stateNumber = ai.idaStar(puzzle, 1)
    #     print("TestCase: " + str(i))
    #     print("Number of states: " + str(stateNumber))
    #     print("Number of states: " + str(len(aiMovedElements)))
    #
    #     sumNumMoves += len(aiMovedElements)
    #     sumStateNum += stateNumber
    #
    # avg
    # number
    # of
    # states: 2483932.15
    # avg
    # number
    # of
    # moves: 51.9
    #
    # print("avg number of states: " + str(sumStateNum / NUMBER_OF_TRIES))
    # print("avg number of moves: " + str(sumNumMoves / NUMBER_OF_TRIES))
    puzzle = model.Puzzle(boardSize=4)
    while not puzzle.isSolvable():
        for i in range(4):
            for j in range(4):
                print(str(puzzle.board[i][j]), end=" ")
            print()
        print("Permutation isn't solvable! Shuffling...")
        puzzle.permutate()

    print("Found solvable permutation!")
    for i in range (4):
        for j in range (4):
            print(str(puzzle.board[i][j]), end=" ")
        print()

    aiMovedElements, stateNumber = ai.idaStar(puzzle, 1)

    for element in aiMovedElements:
        print(str(element), end=" ")
    print()
    print("Number of states:" + str(stateNumber))
    print("Number of moves:" + str(len(aiMovedElements)))


if __name__ == "__main__":
    gameLoop()
