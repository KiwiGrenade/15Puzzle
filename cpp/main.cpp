#include <iostream>
#include <utility>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <deque>
#include "Puzzle.h"


bool visitNode(Puzzle &puzzle,
               std::unordered_set<std::string> &visited,
               std::unordered_map<std::string, std::size_t> &closedList, // database
               std::vector<unsigned short> &groupWithBlank,
               std::vector<unsigned short> &group) {
    std::string puzzleHashWithBlank = puzzle.hash(groupWithBlank);

    //if visited contains puzzleHashWithBlank
    if (visited.contains(puzzleHashWithBlank)) {
        return false;
    }

    visited.insert(puzzleHashWithBlank);

    std::string groupHash = puzzle.hash(group);
    // If the permutation (it's hash) hasn't been reached before
    // assign the number of moves it took to reach it as key in the database
    if (!closedList.contains(groupHash))    {
        closedList[groupHash] = puzzle.getCount();
    }
    // If the number of moves it took to reach the current permutation
    // is less than it's key in DB - update it!
    else if (closedList[groupHash] > puzzle.getCount()){
        closedList[groupHash] = puzzle.getCount();
    }

    return true;
}

std::unordered_map<std::string, std::size_t> buildPatternDB(std::vector<unsigned short> group)
{
    Puzzle puzzle = new Puzzle(false);
    std::vector<unsigned short> groupWithBlank = std::move(group);
    groupWithBlank.push_back(0);

    // Permutations of groupWithBlank already visited
    std::unordered_set<std::string> visited;
    // Permutation of group tile locations with min move count so far
    std::unordered_map<std::string, std::size_t> closedList;
    // Next permutations to visit
    std::deque<std::pair<Puzzle, direction>> openList;
    // puzzle, prior direction
    openList.emplace_back(puzzle, direction(none));

    while(!openList.empty()) {
        Puzzle current = openList[0].first;
        direction prevMove = openList[0].second;

        openList.pop_front();

        if(!visitNode(current,
                      visited,
                      closedList,
                      groupWithBlank,
                      group)) {
            continue;
        }
        for (unsigned short i = 0; i < 4; i++){
            if(direction(i) == prevMove) {
                continue;
            }

            Puzzle simPuzzle = current;
            bool validMove = simPuzzle.move(direction(i));

            if(!validMove) {
                continue;
            }

            unsigned short dispValue = simPuzzle.getFromBoard(current.getX(), current.getY());
            if (std::find(group.begin(), group.end(), dispValue) != group.end()) {
                simPuzzle.iterCount();
            }
            openList.emplace_back(simPuzzle, direction(i));
        }
    }
    return closedList;
}


int main()
{
    std::vector<std::vector<unsigned short>> groups {{1,5,6,9,10,13},{7,8,11,12,14,15},{2,3,4}};
    std::unordered_map<std::string, std::size_t> closedList;
    for (const std::vector<unsigned short>& group: groups) {
        auto list = buildPatternDB(group);
        closedList.insert(list.begin(),list.end());
    }

    return 0;
}
