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
import time

class cell:
    def __init__(self,i,j,value):
        self.i = i
        self.j = j
        self.value = value
        self.pos = (self.i, self.j)
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
        if self.value == 0:
            self.possible_vals = set([i for i in range(1,10)])
            self.not_possible_vals = set()
        else:
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

# Summarises the most properties for checkpoints
class checkpoint:
    def __init__(self, board, route, cell_position):
        self.values = []
        for i in range(9):
            for j in range(9):
                cell = board[i][j]
                self.values.append(cell.value)

        self.route = route
        self.cell_position = cell_position

class board:
    def __init__(self,problem):
        self.board = np.empty((9,9),dtype=cell)
        for i in range(9):
            for j in range(9):
                self.board[i][j] = cell(i,j,value = problem[i][j])

        # This is a checkpoint of the differnt states the problem can have
        self.checkpoints = []

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

    def display_vals(self,board):
        # Just displays the state of the board in a pretty way

        values = []
        for i in range(9):
            for j in range(9):
                values.append(board[i][j].value)
        mask = """\
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
        return mask

    def unsolved_cells(self):
        # Find the cells which need solving
        investigate_cells = []
        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                if cell.value == 0:
                    investigate_cells.append(cell)

        return investigate_cells

    def restore(self):
        # This method restores the values of the board using the checkpoints
        # Always take the latest copy of the checkpoint
        point = self.checkpoints[-1]
        for i in range(9):
            for j in range(9):
                self.board[i][j].value = point.values[9*i+j]
                self.board[i][j].reset()

        # There should be no changes in the values, just reset the possible
        # values
        self.reduce_state()

    def choose_route(self, unsolved_cells):
        # Choose the cell with the fewest possible values by sorting them by the
        # length of their possible values
        unsolved_cells.sort(key = lambda cell: len(cell.possible_vals))

        # Then need to know if the state is valid i.e. all unsolved cells have
        # possible values.
        # If a wrong assumption is chosen we will have a cell with no possible
        # values.
        if len(unsolved_cells[0].possible_vals) == 0:
            # when fail restore the list and choose an alternative route
            self.restore()
            # now we want to use the alternative route and remove the final
            # checkpoint
            # Delete the first route that failed
            self.checkpoints[-1].route.pop(0)

            # Then move to the previous level with a valid alternative route
            while len(self.checkpoints[-1].route) == 0:
                # Ultimate fail case, return to the previous level with a non
                # zero path
                self.checkpoints.pop()
                self.checkpoints[-1].route.pop(0)
                self.restore()

        else:
            # choose the next level and make the next assumption
            # only need the smallest route
            self.checkpoints.append(checkpoint(self.board,
             list(unsolved_cells[0].possible_vals), unsolved_cells[0].pos))

        # Make the assumption and set the value
        assumed_cell_pos = self.checkpoints[-1].cell_position
        assumed_cell = self.board[assumed_cell_pos[0], assumed_cell_pos[1]]
        assumed_cell.value = self.checkpoints[-1].route[0]

    def reduce_state(self):
        # This will solve a single state of the system
        # It will return the unsolved cells, if the solution is found there will
        # be no unsolved cells.

        # Generate the list of cells to investigate
        investigate_cells = self.unsolved_cells()

        # Array keeps track of the length of the unsolved cells to tell if it's
        # been stuck on a state for too long
        prev_lengths = np.array([0,0])

        while True:
            for num, cell in enumerate(investigate_cells):
                # Check does all the imporant stuff
                if self.check(cell):
                    investigate_cells.remove(cell)
                    break

            # First check if it solved the game
            if len(investigate_cells) == 0:
                break

            # In the first case does a unique check of remaining values
            elif len(investigate_cells) == prev_lengths[0] and len(investigate_cells) != prev_lengths[1]:
                for num, cell in enumerate(investigate_cells):
                    # Does the unique check for each cell
                    self.unique_check(cell)
                    # True if the it has a value
                    if cell.check_last():
                        # input(self.display_vals(self.board))
                        investigate_cells.remove(cell)
                        break

            # Finally breaks if there is a problem
            elif np.all(prev_lengths == len(investigate_cells)):
                # Erroneus board
                # print("Error, the board has no solution")
                break

            prev_lengths[1] = prev_lengths[0]
            prev_lengths[0] = len(investigate_cells)


        return investigate_cells

    def solve(self):
        # Loop through until solved
        t0 = time.time()
        while True:
            unsolved_cells = self.reduce_state()
            unsolved_cells.sort(key = lambda cell: len(cell.possible_vals))

            if len(unsolved_cells) != 0:
                self.choose_route(unsolved_cells)

            else:
                break

        t1 = time.time()
        delta_t = t1-t0
        print("Computational time: %.3f s"%delta_t)
        print("Assumptions made %i"%len(self.checkpoints))
        return self.display_vals(self.board)

problem = [[0, 0, 0, 6, 0, 0, 0, 0, 5],
           [0, 0, 0, 0, 0, 4, 0, 3, 0],
           [3, 0, 7, 0, 8, 0, 9, 0, 4],
           [0, 0, 0, 9, 0, 0, 0, 2, 0],
           [0, 8, 2, 0, 0, 0, 3, 5, 0],
           [0, 5, 0, 0, 0, 1, 0, 0, 0],
           [7, 0, 5, 0, 4, 0, 6, 0, 2],
           [0, 9, 0, 7, 0, 0, 0, 0, 0],
           [4, 0, 0, 0, 0, 9, 0, 0, 0]]
'''
problem = [[1, 0, 0, 0, 0, 0, 3, 0, 0],
           [9, 3, 5, 0, 1, 0, 0, 0, 0],
           [0, 0, 8, 7, 2, 0, 9, 0, 0],
           [0, 6, 0, 2, 7, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 8, 6, 0, 5, 0],
           [0, 0, 6, 0, 3, 2, 1, 0, 0],
           [0, 0, 0, 0, 5, 0, 2, 4, 9],
           [0, 0, 2, 0, 0, 0, 0, 0, 3],]
'''

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

problem = produce_problem()
board = board(problem)
print(board.display_vals(board.board))
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
