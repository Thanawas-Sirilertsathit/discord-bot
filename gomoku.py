class Gomoku:
    def __init__(self, player1, player2):
        self.board = [['🟤' for _ in range(15)] for _ in range(15)]
        self.players = {player1: '⚪', player2: '⚫'}
        self.current_player = player1
        self.winner = None
        self.moves = 0

    def place_piece(self, x, y):
        if self.board[x][y] == '🟤':
            self.board[x][y] = self.players[self.current_player]
            self.moves += 1
            if self.check_winner(x, y):
                self.winner = self.current_player
            else:
                self.current_player = list(self.players.keys())[1 - list(self.players.keys()).index(self.current_player)]
            return True
        return False

    def check_winner(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        symbol = self.players[self.current_player]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == symbol:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == symbol:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def display_board(self):
        board_str = "\n".join([f"{' '.join(row)}" for row in self.board])
        return f"```{board_str}```"