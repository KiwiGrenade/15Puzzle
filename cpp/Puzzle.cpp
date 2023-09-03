//
// Created by Grim Reaper on 16.04.2023.
//
#include <iostream>
#include <unordered_set>
#include <random>
#include "Puzzle.h"
#include <algorithm>
void Puzzle::printBoard() const noexcept {
    for (auto & i : board) {
        for (auto j: i) {
            std::cout << j << " ";
        }
        std::cout << std::endl;
    }
}

Puzzle::Puzzle(bool shuffle) {
    x = 3;
    y = 3;

    unsigned short counter = 1;
    for (auto & i : board) {
        for (auto& j: i) {
            if(counter == 16)
            {
                counter = 0;
            }
            j = counter;
            counter++;
        }
    }
    if(shuffle)
    {
        this->shuffle();
    }
}

void Puzzle::shuffle() noexcept {
    std::random_device randomDevice;
    std::mt19937 generator(randomDevice());
    std::uniform_int_distribution<unsigned short> distribution(0, 3);
    for (int i = 0; i < 1000; ++i) {
        unsigned short x1 = distribution(generator);
        unsigned short x2 = distribution(generator);
        unsigned short y1 = distribution(generator);
        unsigned short y2 = distribution(generator);
        std::swap(board[y1][x1], board[y2][x2]);
    }
}

bool Puzzle::move(direction dir) noexcept{
    switch (dir) {
        case up:
            //can't move up if you're in the last row
            if(y != 3){
                std::swap(board[y][x], board[y + 1][x]);
                y++;
                return true;
            }
            break;
        case down:
            //can't move down if you're in the first row
            if(y != 0){
                std::swap(board[y][x], board[y - 1][x]);
                y--;
                return true;
            }
            break;
        case left:
            //can't move left if you're in the first column
            if(x != 3){
                std::swap(board[y][x], board[y][x + 1]);
                x++;
                return true;
            }
            break;
        case right:
            //can't move right if you're in the last column
            if(x != 0){
                std::swap(board[y][x], board[y][x - 1]);
                x--;
                return true;
            }
            break;
    }
    return false;
}

bool Puzzle::checkWin() noexcept {
    size_t counter = 1;
    for (auto & i : board) {
        for (auto& j: i) {
            if(counter == 16)
            {
                counter = 0;
            }
            if(j != counter)
            {
                return false;
            }
            counter++;
        }
    }
    return true;
}

bool Puzzle::isSolvable() noexcept {
    unsigned short num[16]{0};
    for(size_t i = 2; i < 16; i++) {
        bool isPassed = false;
        for (auto & j : board) {
            for (unsigned short k : j) {
                if(k == i) {
                    isPassed = true;
                }
                if(isPassed && k != 0 && k < i) {
                    num[i]++;
                }
            }
        }
    }

    int sum = 0;
    sum = std::accumulate(num, num + 16, sum);

    return (sum + y + 1) % 2 == 0;
}

 std::string Puzzle::hash(std::vector<unsigned short> group) noexcept {
    if(group.empty()) {
        for (unsigned short i = 0; i < 16; ++i) {
            group.push_back(i);
        }
    }

    std::string hashString(16*2, '0');

    for(unsigned short i = 0; i < 4; i++) {
        for(unsigned short j = 0; j < 4; j++) {
            if(std::find(group.begin(), group.end(), board[i][j]) != group.end()) {
                hashString[2 * board[i][j]] = char(i);
                hashString[2 * board[i][j] + 1] = char(j);
            }
            else {
                hashString[2 * board[i][j]] = 'x';
                hashString[2 * board[i][j] + 1] = 'x';
            }
        }
    }

    hashString.erase(std::remove(hashString.begin(), hashString.end(), 'x'), hashString.end());
    return hashString;
}

size_t Puzzle::getCount() const noexcept {
    return count;
}

void Puzzle::iterCount() noexcept {
    count++;
}

unsigned short Puzzle::getFromBoard(unsigned short x, unsigned short y) noexcept {
    return board[y][x];
}

unsigned short Puzzle::getX() const {
    return x;
}

unsigned short Puzzle::getY() const {
    return y;
}

