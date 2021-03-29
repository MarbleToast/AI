from typing import List
import itertools


class Board:
    def __init__(self, tiles: List[List[int]], depth, f=None):
        self.tiles = tiles
        self.g = depth
        self.f = f

    def generate_successors(self):
        x, y = self.find_blank()
        children = []

        for i in [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]:
            if (
                i[0] >= 0
                and i[0] < len(self.tiles)
                and i[1] >= 0
                and i[1] < len(self.tiles)
            ):
                copied_tiles = [row[:] for row in self.tiles]
                temp = copied_tiles[i[0]][i[1]]
                copied_tiles[i[0]][i[1]] = copied_tiles[x][y]
                copied_tiles[x][y] = temp

                children.append(Board(copied_tiles, self.g + 1))

        return children

    def find_blank(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[i][j] == "_":
                    return i, j

    def hamming_distance(self, goal):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] != goal[i][j] and self.tiles[i][j] != "_":
                    distance += 1
        return distance

    def manhattan_distance(self, goal):
        flat_list = list(itertools.chain.from_iterable(self.tiles))
        flat_goal = list(itertools.chain.from_iterable(goal))
        return sum(
            abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
            for b, g in (
                (flat_list.index(str(i)), flat_goal.index(str(i))) for i in range(1, 9)
            )
        )

    def is_solvable(self, goal):
        flat_list = list(itertools.chain.from_iterable(self.tiles))
        flat_list.remove("_")
        list_inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    list_inversions += 1

        flat_goal = list(itertools.chain.from_iterable(goal))
        flat_goal.remove("_")
        goal_inversions = 0
        for i in range(len(flat_goal)):
            for j in range(i + 1, len(flat_goal)):
                if flat_goal[i] > flat_goal[j]:
                    goal_inversions += 1

        return (list_inversions % 2) == (goal_inversions % 2)

    def pretty_print(self):
        print()
        for i in range(3):
            for j in range(3):
                if j == 0:
                    print(end=" ")
                print(self.tiles[i][j], end="")
                if j < 2:
                    print(" | ", end="")
            if i < 2:
                print("\n---|---|---")
        print("\nf:", self.f, "h:", self.f - self.g, "g:", self.g)
        print("\n")


class Solver:
    def __init__(self, mode):
        self.board = Board(self.show_prompt(), 0)
        self.goal = self.show_prompt()
        self.mode = mode

        if self.mode == "h":
            self.board.f = self.board.hamming_distance(self.goal)
        else:
            self.board.f = self.board.manhattan_distance(self.goal)

        self.board.pretty_print()
        Board(self.goal, 0, 0).pretty_print()

    def show_prompt(self):
        grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        not_taken = ["1", "2", "3", "4", "5", "6", "7", "8", "_"]
        for i in range(3):
            for j in range(3):
                print("Available elements:", *not_taken)
                while grid[i][j] not in not_taken:
                    grid[i][j] = input(
                        "Input row {0}, column {1}: ".format(i + 1, j + 1)
                    )
                not_taken.remove(grid[i][j])
        return grid

    def solve(self):
        if not self.board.is_solvable(self.goal):
            print("Unsolvable")
        else:
            open_list = [self.board]
            closed_list = []

            iterations = 0
            while open_list:
                print("Iteration", iterations)
                current_board = open_list[0]
                current_board.pretty_print()

                if current_board.tiles == self.goal:
                    break

                for b in current_board.generate_successors():
                    if b.tiles in [c.tiles for c in closed_list] + [
                        o.tiles for o in open_list
                    ]:
                        continue
                    if self.mode == "h":
                        # Without adding depth, finds a path of 54 in 957 iterations
                        # Adding depth, finds a path of 26 in 68657 iterations
                        b.f = b.hamming_distance(self.goal) + b.g
                    else:
                        # Without adding depth, finds a path of 42 in 365 iterations
                        # Adding depth, finds a path of 26 in 3647 iterations
                        b.f = b.manhattan_distance(self.goal) + b.g

                    open_list.append(b)

                closed_list.append(current_board)
                open_list.remove(current_board)
                open_list.sort(key=lambda x: x.f)
                iterations += 1


if __name__ == "__main__":
    mode = input("[M]anhattan distance or [H]amming distance?")
    if mode.lower() == "h":
        Solver("h").solve()
    elif mode.lower() == "m":
        Solver("m").solve()
    else:
        print("...defaulting to Manhattan")
        Solver("m").solve()
