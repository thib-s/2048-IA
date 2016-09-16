#! /usr/bin/env python3

import logic

#FONCTIONS###############################################################

def start_test(name):
    print("*********** start test: " + name + " *******************")

def assert_compress(before, expected):
    actual = logic.compress(before)
    if actual != expected:
        print("Error, lists differ. Expected list:")
        print(expected)
        print("Actual list:")
        print(actual)
        raise AssertionError("Lists differ")
       
def assert_game_over(board, game_over):
    assert logic.game_over(board) == game_over


#TESTS###################################################################

start_test('Compress with one tile')

assert_compress([0, 1, 0, 0],
                [1, 0, 0, 0])

start_test('Compress with one tile at the top')

assert_compress([1, 0, 0, 0],
                [1, 0, 0, 0])

start_test('Compress with two different tiles')

assert_compress([0, 1, 0, 2],
                [1, 2, 0, 0])

start_test('Compress with two identical tiles')

assert_compress([0, 1, 0, 1],
                [2, 0, 0, 0])

start_test('Compress with two identical consecutive tiles')

assert_compress([0, 3, 3, 0],
                [4, 0, 0, 0])

start_test('Compress with two identical consecutive tiles at bottom')

assert_compress([2, 2, 0, 0],
                [3, 0, 0, 0])

start_test('Compress with 3 mixed tiles')

assert_compress([2, 1, 0, 2],
                [2, 1, 2, 0])

start_test('Compress with 3 identical tiles')

assert_compress([4, 4, 4, 0],
                [5, 4, 0, 0])

start_test('Compress with 2 identical tiles and 1 greater')

assert_compress([4, 4, 5, 0],
                [5, 5, 0, 0])

start_test('Compress with 4 identical tiles')

assert_compress([6, 6, 6, 6],
                [7, 7, 0, 0])

print()
print("    function logic.compress() seems to be correct")
print()

def assert_board(actual, expected):
    expected_board = logic.init(expected)
    if actual != expected_board:
        print("Error, boards differ. Expected board:")
        print(logic.board_to_string(expected_board))
        print("Actual board:")
        print(logic.board_to_string(actual))
        raise AssertionError("Boards differ")
        
simple_board = logic.init([
    [0, 0, 0, 0],
    [0, 2, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])

start_test('Slide left with one tile')

board = logic.copy_board(simple_board)
moved = logic.slide(logic.LEFT, board)
assert moved == True
assert_board(board, [
    [0, 0, 0, 0],
    [2, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])

start_test('Slide right with one tile')

board = logic.copy_board(simple_board)
moved = logic.slide(logic.RIGHT, board)
assert moved == True
assert_board(board, [
    [0, 0, 0, 0],
    [0, 0, 0, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])

start_test('Slide up with one tile')

board = logic.copy_board(simple_board)
moved = logic.slide(logic.UP, board)
assert moved == True
assert_board(board, [
    [0, 2, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])


start_test('Slide down with one tile')

board = logic.copy_board(simple_board)
moved = logic.slide(logic.DOWN, board)
assert moved == True
assert_board(board, [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 2, 0, 0],
])


complex_board = logic.init([
    [2, 2, 2, 4],
    [2, 2, 2, 0],
    [4, 2, 4, 4],
    [4, 0, 0, 0],
])

start_test('Slide down with several tiles')

board = logic.copy_board(complex_board)
moved = logic.slide(logic.DOWN, board)
assert moved == True
assert_board(board, [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [4, 2, 4, 0],
    [8, 4, 4, 8],
])

start_test('Slide up with several tiles')

board = logic.copy_board(complex_board)
moved = logic.slide(logic.UP, board)
assert moved == True
assert_board(board, [
    [4, 4, 4, 8],
    [8, 2, 4, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
])

start_test('Try to slide when no move is possible')

semifull_board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16, 32],
    [8, 16,  8,  4],
    [16, 8, 16, 16],
])

for direction in (logic.UP, logic.DOWN):
    board = logic.copy_board(semifull_board)
    moved = logic.slide(direction, board)
    assert moved == False
    assert board == semifull_board

for direction in (logic.LEFT, logic.RIGHT):
    board = logic.copy_board(semifull_board)
    moved = logic.slide(direction, board)
    assert moved == True
    assert board != semifull_board

print()
print("Function slide seems to be correct")
print()

start_test('check for a full board')
full_board = logic.init([
    [2,  4,  8, 16],
    [4,  8, 16, 32],
    [8, 16,  8,  4],
    [16, 8, 32, 16],
])
assert_game_over(full_board, True)

start_test('check for a full board whith one move possible')
assert_game_over(semifull_board, False)

start_test('check if the board changed after game over test')
after_test = logic.init([
    [2, 2, 2, 4],
    [2, 2, 2, 0],
    [4, 2, 4, 4],
    [4, 0, 0, 0],
])
before_test = logic.copy_board(after_test)
assert logic.game_over(after_test) == False
assert after_test == before_test
#un board vide renvoie True mais ce cas n'arrive jamais

print()
print("Function game_over seems to be correct")
print()

print()
print("   All tests passed successfully!")
print()