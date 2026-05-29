from django.shortcuts import render
import random

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def index(request):
    board = request.session.get('board', None)
    if not board:
        board = GOAL_STATE[:]
        random.shuffle(board)
        request.session['board'] = board

    return render(request, 'puzzle/index.html', {'board': board})

def move_tile(request, tile):
    board = request.session['board']
    empty = board.index(0)
    tile_pos = board.index(int(tile))

    # Allowed moves
    moves = []
    row, col = divmod(empty, 3)
    if row > 0: moves.append(empty - 3)
    if row < 2: moves.append(empty + 3)
    if col > 0: moves.append(empty - 1)
    if col < 2: moves.append(empty + 1)

    if tile_pos in moves:
        board[empty], board[tile_pos] = board[tile_pos], board[empty]
        request.session['board'] = board

    game_won = (board == GOAL_STATE)
    return render(request, 'puzzle/index.html', {'board': board, 'game_won': game_won})
def reset(request):
    import random
    GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    board = GOAL_STATE[:]
    random.shuffle(board)
    request.session['board'] = board
    return render(request, 'puzzle/index.html', {'board': board})