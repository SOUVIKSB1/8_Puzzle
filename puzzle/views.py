from django.shortcuts import render
from django.http import JsonResponse
import random
import heapq

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def count_inversions(board):
    tiles = [x for x in board if x != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions

def is_solvable(board):
    return count_inversions(board) % 2 == 0

def get_random_solvable_board():
    board = GOAL_STATE[:]
    while True:
        random.shuffle(board)
        if is_solvable(board) and board != GOAL_STATE:
            return board

def manhattan_distance(board):
    distance = 0
    for i, val in enumerate(board):
        if val != 0:
            goal_row, goal_col = divmod(val - 1, 3)
            curr_row, curr_col = divmod(i, 3)
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def get_neighbors(board):
    empty = board.index(0)
    row, col = divmod(empty, 3)
    neighbors = []
    
    adjacents = []
    if row > 0: adjacents.append(empty - 3)
    if row < 2: adjacents.append(empty + 3)
    if col > 0: adjacents.append(empty - 1)
    if col < 2: adjacents.append(empty + 1)
    
    for adj in adjacents:
        new_board = list(board)
        new_board[empty], new_board[adj] = new_board[adj], new_board[empty]
        neighbors.append((tuple(new_board), new_board[empty]))
    return neighbors

def solve_a_star(start_board):
    start = tuple(start_board)
    goal = tuple(GOAL_STATE)
    
    if start == goal:
        return [], 0
        
    queue = []
    heapq.heappush(queue, (manhattan_distance(start), 0, start, ()))
    
    visited = {start: 0}
    nodes_explored = 0
    max_iterations = 25000
    
    while queue and nodes_explored < max_iterations:
        f, g, curr, path = heapq.heappop(queue)
        nodes_explored += 1
        
        if curr == goal:
            return list(path), nodes_explored
            
        if g > visited.get(curr, float('inf')):
            continue
            
        for neighbor, moved_tile in get_neighbors(curr):
            new_g = g + 1
            if new_g < visited.get(neighbor, float('inf')):
                visited[neighbor] = new_g
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(queue, (new_f, new_g, neighbor, path + (moved_tile,)))
                
    return None, nodes_explored

def index(request):
    board = request.session.get('board', None)
    if not board or not is_solvable(board):
        board = get_random_solvable_board()
        request.session['board'] = board
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'board': board,
            'game_won': board == GOAL_STATE
        })
        
    return render(request, 'puzzle/index.html', {'board': board})

def move_tile(request, tile):
    board = request.session.get('board')
    if not board:
        board = get_random_solvable_board()
        request.session['board'] = board
        
    try:
        tile_val = int(tile)
    except ValueError:
        return JsonResponse({'error': 'Invalid tile'}, status=400)
        
    if tile_val not in board or tile_val == 0:
        return JsonResponse({'error': 'Tile not on board'}, status=400)
        
    empty = board.index(0)
    tile_pos = board.index(tile_val)
    
    row_empty, col_empty = divmod(empty, 3)
    row_tile, col_tile = divmod(tile_pos, 3)
    
    is_adjacent = abs(row_empty - row_tile) + abs(col_empty - col_tile) == 1
    
    if is_adjacent:
        board[empty], board[tile_pos] = board[tile_pos], board[empty]
        request.session['board'] = board
        
    game_won = (board == GOAL_STATE)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'board': board,
            'game_won': game_won,
            'moved': is_adjacent
        })
        
    return render(request, 'puzzle/index.html', {'board': board, 'game_won': game_won})

def reset(request):
    board = get_random_solvable_board()
    request.session['board'] = board
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'board': board,
            'game_won': False
        })
        
    return render(request, 'puzzle/index.html', {'board': board})

def solve_puzzle(request):
    board = request.session.get('board')
    if not board:
        return JsonResponse({'error': 'No board active'}, status=400)
        
    path, nodes = solve_a_star(board)
    if path is None:
        return JsonResponse({'error': 'Puzzle is unsolvable', 'nodes_explored': nodes}, status=400)
        
    return JsonResponse({
        'solution': path,
        'steps': len(path),
        'nodes_explored': nodes
    })

def get_hint(request):
    board = request.session.get('board')
    if not board:
        return JsonResponse({'error': 'No board active'}, status=400)
        
    path, nodes = solve_a_star(board)
    if path is None:
        return JsonResponse({'error': 'Puzzle is unsolvable'}, status=400)
        
    if not path:
        return JsonResponse({'hint': None, 'message': 'Already solved!'})
        
    return JsonResponse({
        'hint': path[0],
        'nodes_explored': nodes
    })
