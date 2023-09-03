from copy import deepcopy

import boardModel
import aStarAlg
import boardModel

# aStarAlg
aStarAlg.init(4)


def puzzle():
    sumStateNum = 0
    sumNumMoves = 0

    NUMBER_OF_TRIES = 20

    for i in range(NUMBER_OF_TRIES):
        puzzle = boardModel.Puzzle(boardSize=4)
        while not puzzle.isSolvable():
        #     for i in range(4):
        #         for j in range(4):
        #             print(str(puzzle.board[i][j]), end=" ")
        #         print()
            print("Permutation isn't solvable! Shuffling...")
            puzzle.permutate()
        aStarAlgMovedElements, stateNumber = aStarAlg.idaStar(puzzle, 1)
        print("TestCase: " + str(i))
        print("Number of states: " + str(stateNumber))
        print("Number of states: " + str(len(aStarAlgMovedElements)))

        sumNumMoves += len(aStarAlgMovedElements)
        sumStateNum += stateNumber
    print("avg number of states: " + str(sumStateNum / NUMBER_OF_TRIES))
    print("avg number of moves: " + str(sumNumMoves / NUMBER_OF_TRIES))
    # puzzle = boardModel.Puzzle(boardSize=4)
    # while not puzzle.isSolvable():
    #     for i in range(4):
    #         for j in range(4):
    #             print(str(puzzle.board[i][j]), end=" ")
    #         print()
    #     print("Permutation isn't solvable! Shuffling...")
    #     puzzle.permutate()
    # print("Found solvable permutation!")
    # for i in range (4):
    #     for j in range (4):
    #         print(str(puzzle.board[i][j]), end=" ")
    #     print()
    #
    # puzzle1 = deepcopy(puzzle)
    #
    # aStarAlgMovedElements, stateNumber = aStarAlg.idaStar(puzzle, 1)
    #
    # for element in aStarAlgMovedElements:
    #     print(str(element), end=" ")
    # print()
    # print("Number of states:" + str(stateNumber))
    # print("Number of moves:" + str(len(aStarAlgMovedElements)))
    #
    # aStarAlgMovedElements, stateNumber = aStarAlg.idaStar(puzzle, 2)
    #
    # for element in aStarAlgMovedElements:
    #     print(str(element), end=" ")
    # print()
    # print("Number of states:" + str(stateNumber))
    # print("Number of moves:" + str(len(aStarAlgMovedElements)))


if __name__ == "__main__":
    puzzle()
