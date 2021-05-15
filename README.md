# tictactoe-minimax
tic tac toe board game, with the minimax algorithm implemented

The opponent is an Automated System using the minimax algorithm to play against you
in the most optimal way possible. 

It uses the minimax to calculate all the end positions and anylze them to make the most
optimal move from the current position by using recursive backtracking

```

# this recursive function claculates ALL THE POSSIBLE moves that can be played
# at each point in the game and plays the most optimal move for itself
# by analyzing each point in the game


def minimax(board, depth, maxim):
    # checks if there is a winner and returns the winner score
    state = board.state()
    if state != None:
        return state

    # the maximizing player turn
    if maxim:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                # if a position is available it
                # makes a move there and sees the end results
                # and makes a score for each move. then it
                # plays the best possible move for X, i.e., the
                # highest score
                if board.available((i, j)):
                    board.board[i][j] = 1
                    score = minimax(board, depth + 1, False)
                    board.board[i][j] = 0
                    # maximizing the score
                    best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                # if a position is available it
                # makes a move there and sees the end results
                # and makes a score for each move. then it
                # plays the best possible move for O, i.e., the
                # lowest score
                if board.available((i, j)):
                    board.board[i][j] = -1
                    score = minimax(board, depth + 1, True)
                    board.board[i][j] = 0
                    # minimizing the score
                    best_score = min(best_score, score)

        return best_score
```

this takes in a boolean(```maxim```) and uses it to make recursive decisions given that the oppnonent plays
optimally as well(it changes and calculates for both sides optimally depending on the boolean variable).

This algorithm can be optimaized by using alpha beta pruning to make educated predictions and decisions to 
save time by not calculating worst moves.
