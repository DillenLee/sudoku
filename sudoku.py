#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 22:24:35 2022

@author:
   ___  _ ____             __
  / _ \(_) / /__ ___      / /  ___ ___
 / // / / / / -_) _ \    / /__/ -_) -_)
/____/_/_/_/\__/_//_/   /____/\__/\__/

"""

import numpy as np
import scipy.optimize

class cell:
    def __init__(self,i,j,value):
        self.i = i
        self.j = j
        self.value = value
        if value == 0:
            self.possible_vals = set([i for i in range(1,10)])
            self.not_possible_vals = set()
        else:
            self.possible_vals = set([value])
            self.not_possible_vals = set([i for i in range(1,10)])-self.possible_vals

        # Give the boxes a number from top to bottom, left to right, 0 to 8
        i_box_val = i//3
        j_box_val = j//3
        self.box_number = int(3*i_box_val+j_box_val)

    def reset(self):
        self.possible_vals = set([self.value])
        self.not_possible_vals = set([i for i in range(1,10)])-self.possible_vals


    def is_not(self,value):
        self.not_possible_vals.add(value)
        self.possible_vals = self.possible_vals.difference(self.not_possible_vals)

    def check_last(self):
        # Returns True if the cell has a value and False if it doesn't
        if len(self.possible_vals) == 1:
            self.value = list(self.possible_vals)[0]
            self.reset()
            return True
        else:
            return False

    def compare(self,other_set):
        # Compare the possible numbers with another set
        diff_vals = self.possible_vals-other_set
        return diff_vals

class board:
    def __init__(self,problem):
        self.board = np.empty((9,9),dtype=cell)
        for i in range(9):
            for j in range(9):
                self.board[i][j] = cell(i,j,value = problem[i][j])


    def horizontal_check(self,cell):
        # Checks the column

        # cell is the cell we want to check
        column = cell.j

        for i in range(9):
            other_val = self.board[i][column].value
            if other_val != 0:
                cell.is_not(other_val)

    def vertical_check(self,cell):
        # Checks the cells in the column

        # cell is the cell we want to check
        row = cell.i

        for j in range(9):
            other_val = self.board[row][j].value
            if other_val != 0:
                cell.is_not(other_val)

    def box_check(self,cell):
        # Checks the cells in the box
        box_number = cell.box_number

        # Now we need to sort through the values with the same box
        start_i = (box_number//3)*3
        start_j = (box_number%3)*3
        for i in range(3):
            for j in range(3):
                other_val = self.board[i+start_i][j+start_j].value
                if other_val != 0:
                    cell.is_not(other_val)

    def unique_check(self,cell):
        # Checks if it contains any unique values in a box
        box_number = cell.box_number
        all_other_vals = set()


        # Now we need to sort through the values with the same box
        start_i = int(box_number//3)*3
        start_j = (box_number%3)*3
        for i in range(3):
            for j in range(3):
                other_cell = self.board[i+start_i][j+start_j]
                if other_cell.value == 0 and other_cell != cell:
                    all_other_vals = all_other_vals.union(other_cell.possible_vals)

        diff_vals = cell.compare(all_other_vals)
        # if cell.i == 4 and cell.j == 6:
        #     print(all_other_vals)
        #     print(cell.possible_vals)
        #     print(diff_vals)
        #     print(cell.i)
        #     input(cell.j)

        if len(diff_vals) == 1:
            cell.value = list(diff_vals)[0]
            cell.possible_vals = diff_vals


    def check(self,cell):
        # Simply string all the checks together
        self.horizontal_check(cell)
        self.vertical_check(cell)
        self.box_check(cell)

        # Returns True if last possible number and False if it isn't
        return cell.check_last()


    def display_vals(self):

        values = []
        for i in range(9):
            for j in range(9):
                values.append(self.board[i][j].value)
        board = """\
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┠───────────╂───────────╂───────────┨
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┠───────────╂───────────╂───────────┨
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃ %i ┊ %i ┊ %i ┃
┗━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━┛
"""%tuple(values)
        return board

    def unsolved_cells(self):
        # Find the cells which need solving
        investigate_cells = []
        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                if cell.value == 0:
                    investigate_cells.append(cell)

        return investigate_cells

    def solve(self):

        investigate_cells = self.unsolved_cells()

        prev_lengths = np.array([0,0])

        while True:
            for num, cell in enumerate(investigate_cells):
                # print(num)
                if self.check(cell):
                    input(self.display_vals())
                    investigate_cells = self.unsolved_cells()
                    break

            if len(investigate_cells) == 0:
                break

            elif len(investigate_cells) == prev_lengths[0] and len(investigate_cells) != prev_lengths[1]:
                for num, cell in enumerate(investigate_cells):
                    self.unique_check(cell)
                    if cell.check_last():
                        input(self.display_vals())
                        investigate_cells.remove(cell)
                        break

            elif np.all(prev_lengths == len(investigate_cells)):
                print([cell.possible_vals for cell in investigate_cells])
                print(self.display_vals())
                input("We have reached a problem")

            prev_lengths[1] = prev_lengths[0]
            prev_lengths[0] = len(investigate_cells)

        val_board = self.display_vals()
        return val_board

problem = [[2, 8, 0, 4, 0, 9, 0, 0, 6],
           [9, 0, 0, 3, 5, 0, 0, 0, 0],
           [0, 0, 0, 0, 6, 0, 0, 4, 0],
           [0, 0, 0, 0, 0, 0, 6, 0, 0],
           [0, 3, 0, 7, 0, 2, 0, 5, 0],
           [0, 0, 4, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 7, 0, 0, 0, 0],
           [0, 0, 0, 0, 3, 6, 0, 0, 8],
           [7, 0, 0, 8, 0, 1, 0, 3, 4]]


def produce_problem():
    row_nums = [i for i in range(1,10)]
    problem = []
    for row_num in row_nums:
        while True:
            row = input("Enter the values of the %s row: \n"%row_num)
            if len(row) != 9:
                print("Too many digits! Entered %s number(s) when it should be 9"%len(row))
            else:
                row = [int(i) for i in row]
                problem.append(row)
                break

    return problem

# problem = produce_problem()
board = board(problem)
solution = board.solve()
print(solution)
# ┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┠───────────╂───────────╂───────────┨
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┠───────────╂───────────╂───────────┨
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃ 0 ┊ 0 ┊ 0 ┃
# ┗━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━┛
