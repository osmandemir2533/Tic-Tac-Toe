import math
import time
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Session için gerekli

MAX_TIME = 3  # AI'nin bir hamle yapması için verilen maksimum süre (saniye)
MAX_DEPTH = 6  # Büyük tahtalar için maksimum derinlik
MCTS_SIMULATIONS = 3000  # MCTS için simülasyon sayısı (daha güçlü)
MCTS_TIME_LIMIT = 5.0  # MCTS için süre limiti (saniye)

class TicTacToe:
    
    def __init__(self, size=3):
        self.n = size  # Boyutu alıyoruz
        self.board = [[' ' for _ in range(self.n)] for _ in range(self.n)]  # Tahtayı doğru boyutta oluşturuyoruz
        self.current_player = None
        self.first_player = None
        self.A1 = 'X'
        self.A2 = 'O'
        self.game_over = False  # Oyun bitmiş mi?

    def start_game(self, first_player):
        self.first_player = first_player
        self.current_player = self.first_player
        self.board = [[' ' for _ in range(self.n)] for _ in range(self.n)]  # Yeni boyutla tahta oluşturuyoruz
        self.game_over = False

    def user_move(self, row, col):
        if not self.game_over and self.board[row][col] == ' ' and self.current_player == self.A1:
            self.board[row][col] = self.A1
            self.current_player = self.A2
            return True
        return False

    def ai_move(self):
        if not self.game_over:
            # Öncelikle: Rakibin kazanacağı hamle var mı, engelle!
            for i in range(self.n):
                for j in range(self.n):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.A1
                        if self.check_winner(self.A1):
                            self.board[i][j] = self.A2
                            self.current_player = self.A1
                            return (i, j)
                        self.board[i][j] = ' '
            # AI'nın ilk hamlesi mi?
            if all(cell != self.A2 for row in self.board for cell in row):
                if self.n % 2 == 1:
                    center = self.n // 2
                    if self.board[center][center] == ' ':
                        self.board[center][center] = self.A2
                        self.current_player = self.A1
                        return (center, center)
                else:
                    # Çift sayı: merkez bölge (2x2)
                    centers = [
                        (self.n//2 - 1, self.n//2 - 1),
                        (self.n//2 - 1, self.n//2),
                        (self.n//2, self.n//2 - 1),
                        (self.n//2, self.n//2)
                    ]
                    for c in centers:
                        if self.board[c[0]][c[1]] == ' ':
                            self.board[c[0]][c[1]] = self.A2
                            self.current_player = self.A1
                            return c
            # AI'nın ikinci hamlesi mi? (ilk taşı merkezdeyse ve tahtada sadece bir O varsa)
            elif sum(cell == self.A2 for row in self.board for cell in row) == 1:
                center = self.n // 2
                if self.n % 2 == 1 and self.board[center][center] == self.A2:
                    # Boş köşe bul ve oraya oyna
                    corners = [(0,0), (0,self.n-1), (self.n-1,0), (self.n-1,self.n-1)]
                    for corner in corners:
                        if self.board[corner[0]][corner[1]] == ' ':
                            self.board[corner[0]][corner[1]] = self.A2
                            self.current_player = self.A1
                            return corner
            if self.n <= 4:
                move = self.best_move()
            else:
                move = self.mcts_move()
            if move:
                row, col = move
                self.board[row][col] = self.A2
                self.current_player = self.A1
                return (row, col)
        return None

    # Minimax (küçük tahtalar için)
    def best_move(self):
        best_score = -math.inf
        best_moves = []
        start_time = time.time()
        if self.n == 3:
            max_depth = 9  # 3x3 için tüm hamleleri dene
        else:
            max_depth = min(MAX_DEPTH, self.n * 2)  # 4x4 için daha derin arama
        
        # İlk hamle stratejisi
        if self.n == 3 and all(cell != self.A2 for row in self.board for cell in row):
            center = self.n // 2
            if self.board[center][center] == ' ':
                return (center, center)
            corners = [(0,0), (0,self.n-1), (self.n-1,0), (self.n-1,self.n-1)]
            for corner in corners:
                if self.board[corner[0]][corner[1]] == ' ':
                    return corner

        empty_cells = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']
        # Hamleleri merkeze ve köşelere yakınlığa göre sırala
        def move_priority(move):
            i, j = move
            center = self.n // 2
            # Merkez en yüksek öncelik, sonra köşeler, sonra kenarlar
            if (i, j) == (center, center):
                return 0
            elif (i, j) in [(0,0), (0,self.n-1), (self.n-1,0), (self.n-1,self.n-1)]:
                return 1
            else:
                return 2
        empty_cells.sort(key=move_priority)

        # Öncelikle kazanma ve bloklama hamlelerini bul
        for move in empty_cells:
            i, j = move
            # Kazanma hamlesi
            self.board[i][j] = self.A2
            if self.check_winner(self.A2):
                self.board[i][j] = ' '
                return (i, j)
            self.board[i][j] = ' '
            # Bloklama hamlesi
            self.board[i][j] = self.A1
            if self.check_winner(self.A1):
                self.board[i][j] = ' '
                return (i, j)
            self.board[i][j] = ' '

        # Çatallama hamlelerini bul
        fork_moves = []
        for move in empty_cells:
            i, j = move
            self.board[i][j] = self.A2
            forks = 0
            # Her boş hücreye oynayınca kaç tane kazanma hamlesi oluşuyor?
            for m in empty_cells:
                if m == move:
                    continue
                x, y = m
                if self.board[x][y] == ' ':
                    self.board[x][y] = self.A2
                    if self.check_winner(self.A2):
                        forks += 1
                    self.board[x][y] = ' '
            self.board[i][j] = ' '
            if forks >= 2:
                fork_moves.append(move)
        if fork_moves:
            return fork_moves[0]

        # Standart minimax ile en iyi hamleyi bul
        for i, j in empty_cells:
            self.board[i][j] = self.A2
            score = self.minimax(0, False, -math.inf, math.inf, start_time, max_depth)
            self.board[i][j] = ' '
            if score > best_score:
                best_score = score
                best_moves = [(i, j)]
            elif score == best_score:
                best_moves.append((i, j))
            if time.time() - start_time > MAX_TIME:
                break
        # En iyi hamleler arasında merkez/köşe öncelikli olanı seç
        if best_moves:
            best_moves.sort(key=move_priority)
            return best_moves[0]
        return None

    def minimax(self, depth, is_max, alpha, beta, start_time, max_depth):
        if time.time() - start_time > MAX_TIME or depth >= max_depth:
            return self.evaluate_board()
        
        # Kazanma durumlarını kontrol et
        if self.check_winner(self.A2):
            return 100000 - depth  # Daha hızlı kazanmayı tercih et
        if self.check_winner(self.A1):
            return -100000 + depth  # Daha geç kaybetmeyi tercih et
        if self.is_full():
            return 0

        # --- Hamleleri MCTS mantığıyla sırala ---
        def move_priority(i, j, player):
            # Kazanma
            self.board[i][j] = player
            if self.check_winner(player):
                self.board[i][j] = ' '
                return 0
            self.board[i][j] = ' '
            # Bloklama
            opponent = self.A1 if player == self.A2 else self.A2
            self.board[i][j] = opponent
            if self.check_winner(opponent):
                self.board[i][j] = ' '
                return 1
            self.board[i][j] = ' '
            # Çatallama
            self.board[i][j] = player
            forks = 0
            for x in range(self.n):
                for y in range(self.n):
                    if (x, y) != (i, j) and self.board[x][y] == ' ':
                        self.board[x][y] = player
                        if self.check_winner(player):
                            forks += 1
                        self.board[x][y] = ' '
            self.board[i][j] = ' '
            if forks >= 2:
                return 2
            # Merkez
            center = self.n // 2
            if (i, j) == (center, center):
                return 3
            # Köşe
            if (i, j) in [(0,0), (0,self.n-1), (self.n-1,0), (self.n-1,self.n-1)]:
                return 4
            # Çapraz (köşe değilse)
            if i == j or i + j == self.n - 1:
                return 5
            # Kenar
            return 6

        moves = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']
        if is_max:
            # AI'nın hamleleri için öncelik sırasına göre sırala
            moves.sort(key=lambda move: move_priority(move[0], move[1], self.A2))
            best_score = -math.inf
            for i, j in moves:
                self.board[i][j] = self.A2
                score = self.minimax(depth + 1, False, alpha, beta, start_time, max_depth)
                self.board[i][j] = ' '
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    return best_score  # Beta kesmesi: daha fazla arama gereksiz
            return best_score
        else:
            # Rakibin hamleleri için öncelik sırasına göre sırala
            moves.sort(key=lambda move: move_priority(move[0], move[1], self.A1))
            best_score = math.inf
            for i, j in moves:
                self.board[i][j] = self.A1
                score = self.minimax(depth + 1, True, alpha, beta, start_time, max_depth)
                self.board[i][j] = ' '
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score  # Alfa kesmesi: daha fazla arama gereksiz
            return best_score

    # MCTS (büyük tahtalar için)
    def mcts_move(self):
        root_board = [row[:] for row in self.board]
        moves = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == ' ']
        if not moves:
            return None
        wins = {move: 0 for move in moves}
        plays = {move: 0 for move in moves}
        start_time = time.time()
        simulations = 0
        while time.time() - start_time < MCTS_TIME_LIMIT and simulations < MCTS_SIMULATIONS:
            move = self.mcts_best_simulation_move(root_board, moves)
            result = self.simulate_mcts_game_strong(root_board, move)
            plays[move] += 1
            if result == self.A2:
                wins[move] += 1
            simulations += 1
        best_move = max(moves, key=lambda m: (wins[m], plays[m]))
        return best_move

    def mcts_best_simulation_move(self, board, moves):
        n = self.n
        # İlk hamle: merkez veya merkez bölge öncelikli
        if all(cell != self.A2 for row in board for cell in row):
            if n % 2 == 1:
                center = n // 2
                if board[center][center] == ' ':
                    return (center, center)
            else:
                centers = [
                    (n//2 - 1, n//2 - 1),
                    (n//2 - 1, n//2),
                    (n//2, n//2 - 1),
                    (n//2, n//2)
                ]
                for c in centers:
                    if board[c[0]][c[1]] == ' ':
                        return c
        # --- Bloklama önceliği: Rakibin n-1 ve n-2 tehditlerini daha erken blokla ---
        # n-1 bloklama
        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[0]][move[1]] = self.A1
            # Satır
            row = [temp_board[move[0]][j] for j in range(n)]
            if row.count(self.A1) == n-1 and row.count(' ') == 1:
                return move
            # Sütun
            col = [temp_board[i][move[1]] for i in range(n)]
            if col.count(self.A1) == n-1 and col.count(' ') == 1:
                return move
            # Çaprazlar
            if move[0] == move[1]:
                diag1 = [temp_board[k][k] for k in range(n)]
                if diag1.count(self.A1) == n-1 and diag1.count(' ') == 1:
                    return move
            if move[0] + move[1] == n-1:
                diag2 = [temp_board[k][n-1-k] for k in range(n)]
                if diag2.count(self.A1) == n-1 and diag2.count(' ') == 1:
                    return move
        # n-2 bloklama
        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[0]][move[1]] = self.A1
            # Satır
            row = [temp_board[move[0]][j] for j in range(n)]
            if row.count(self.A1) == n-2 and row.count(' ') == 2:
                return move
            # Sütun
            col = [temp_board[i][move[1]] for i in range(n)]
            if col.count(self.A1) == n-2 and col.count(' ') == 2:
                return move
            # Çaprazlar
            if move[0] == move[1]:
                diag1 = [temp_board[k][k] for k in range(n)]
                if diag1.count(self.A1) == n-2 and diag1.count(' ') == 2:
                    return move
            if move[0] + move[1] == n-1:
                diag2 = [temp_board[k][n-1-k] for k in range(n)]
                if diag2.count(self.A1) == n-2 and diag2.count(' ') == 2:
                    return move
        # Kazanma hamlesi
        for move in moves:
            temp_board = [row[:] for row in board]
            temp_board[move[0]][move[1]] = self.A2
            if self.sim_check_winner(temp_board, self.A2):
                return move

        # Çatallama: AI'nın birden fazla kazanma hattı oluşturabileceği hamleleri bul
        fork_moves = []
        for move in moves:
            win_threats = 0
            row = [board[move[0]][j] for j in range(n)]
            col = [board[i][move[1]] for i in range(n)]
            diag1 = [board[i][i] for i in range(n)] if move[0] == move[1] else None
            diag2 = [board[i][n-1-i] for i in range(n)] if move[0] + move[1] == n-1 else None
            lines = [row, col]
            if diag1: lines.append(diag1)
            if diag2: lines.append(diag2)
            for line in lines:
                if line.count(self.A2) == n-2 and line.count(' ') == 2 and self.A1 not in line:
                    win_threats += 1
            if win_threats >= 2:
                fork_moves.append(move)
        if fork_moves:
            return fork_moves[0]

        # Rakip çatallama yapacaksa engelle
        block_fork_moves = []
        for move in moves:
            opp_threats = 0
            row = [board[move[0]][j] for j in range(n)]
            col = [board[i][move[1]] for i in range(n)]
            diag1 = [board[i][i] for i in range(n)] if move[0] == move[1] else None
            diag2 = [board[i][n-1-i] for i in range(n)] if move[0] + move[1] == n-1 else None
            lines = [row, col]
            if diag1: lines.append(diag1)
            if diag2: lines.append(diag2)
            for line in lines:
                if line.count(self.A1) == n-2 and line.count(' ') == 2 and self.A2 not in line:
                    opp_threats += 1
            if opp_threats >= 2:
                block_fork_moves.append(move)
        if block_fork_moves:
            return block_fork_moves[0]

        # Kendi kazanma ihtimali olan hatlara öncelik ver (her türlü hat)
        candidate_moves = []
        max_ai_count = -1
        for move in moves:
            row = [board[move[0]][j] for j in range(n)]
            col = [board[i][move[1]] for i in range(n)]
            diag1 = [board[i][i] for i in range(n)] if move[0] == move[1] else None
            diag2 = [board[i][n-1-i] for i in range(n)] if move[0] + move[1] == n-1 else None
            lines = [row, col]
            if diag1: lines.append(diag1)
            if diag2: lines.append(diag2)
            for line in lines:
                if set(line) <= {self.A2, ' '}:
                    ai_count = line.count(self.A2)
                    if ai_count > max_ai_count:
                        candidate_moves = [move]
                        max_ai_count = ai_count
                    elif ai_count == max_ai_count:
                        candidate_moves.append(move)
        if candidate_moves:
            return candidate_moves[0]

        # Merkez kontrolü
        center = n // 2
        if n % 2 == 1:
            center_move = (center, center)
            if center_move in moves:
                return center_move

        # Köşeler
        corners = [(0,0), (0,n-1), (n-1,0), (n-1,n-1)]
        available_corners = [corner for corner in corners if corner in moves]
        if available_corners:
            return available_corners[0]

        # Kenarlar
        edges = []
        for i in range(n):
            if i != center:
                edges.extend([(i,0), (i,n-1), (0,i), (n-1,i)])
        available_edges = [edge for edge in edges if edge in moves]
        if available_edges:
            return available_edges[0]

        # En çok komşusu olan hamle (her yöne bakar, random yok)
        best_move = None
        max_neighbors = -1
        for move in moves:
            neighbors = 0
            for i in range(max(0, move[0]-1), min(n, move[0]+2)):
                for j in range(max(0, move[1]-1), min(n, move[1]+2)):
                    if board[i][j] != ' ':
                        neighbors += 1
            if neighbors > max_neighbors:
                max_neighbors = neighbors
                best_move = move
        return best_move

    def simulate_mcts_game_strong(self, board, first_move):
        n = self.n
        sim_board = [row[:] for row in board]
        sim_board[first_move[0]][first_move[1]] = self.A2
        player = self.A1
        while True:
            moves = [(i, j) for i in range(n) for j in range(n) if sim_board[i][j] == ' ']
            if not moves:
                return None  # Beraberlik
            move = self.find_winning_or_blocking_move(sim_board, player)
            if not move:
                # Merkez, köşe, rastgele
                move = self.mcts_best_simulation_move(sim_board, moves)
            sim_board[move[0]][move[1]] = player
            if self.sim_check_winner(sim_board, player):
                return player
            player = self.A2 if player == self.A1 else self.A1

    def find_winning_or_blocking_move(self, board, player):
        n = self.n
        for i in range(n):
            for j in range(n):
                if board[i][j] == ' ':
                    # Kazanma
                    board[i][j] = player
                    if self.sim_check_winner(board, player):
                        board[i][j] = ' '
                        return (i, j)
                    board[i][j] = ' '
        # Bloklama
        opponent = self.A1 if player == self.A2 else self.A2
        for i in range(n):
            for j in range(n):
                if board[i][j] == ' ':
                    board[i][j] = opponent
                    if self.sim_check_winner(board, opponent):
                        board[i][j] = ' '
                        return (i, j)
                    board[i][j] = ' '
        return None

    def sim_check_winner(self, board, player):
        n = self.n
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(n):
            if all(board[row][col] == player for row in range(n)):
                return True
        if all(board[i][i] == player for i in range(n)):
            return True
        if all(board[i][n - 1 - i] == player for i in range(n)):
            return True
        return False

    def evaluate_board(self):
        ai_score = 0
        user_score = 0
        
        # Satır ve sütunları değerlendir
        for i in range(self.n):
            # Satırlar
            row = [self.board[i][j] for j in range(self.n)]
            ai_score += self.evaluate_line(row, self.A2)
            user_score += self.evaluate_line(row, self.A1)
            
            # Sütunlar
            col = [self.board[j][i] for j in range(self.n)]
            ai_score += self.evaluate_line(col, self.A2)
            user_score += self.evaluate_line(col, self.A1)
        
        # Çaprazları değerlendir
        diag1 = [self.board[i][i] for i in range(self.n)]
        diag2 = [self.board[i][self.n-1-i] for i in range(self.n)]
        ai_score += self.evaluate_line(diag1, self.A2)
        ai_score += self.evaluate_line(diag2, self.A2)
        user_score += self.evaluate_line(diag1, self.A1)
        user_score += self.evaluate_line(diag2, self.A1)
        
        # Özel durumları değerlendir
        ai_score += self.evaluate_special_patterns(self.A2)
        user_score += self.evaluate_special_patterns(self.A1)
        
        return ai_score - user_score

    def evaluate_line(self, line, player):
        opponent = self.A1 if player == self.A2 else self.A2
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(' ')
        
        if player_count > 0 and opponent_count > 0:
            return 0  # Bloklanmış satır
        
        if player_count == 0 and opponent_count == 0:
            return 0
        
        # Kazanma durumu
        if player_count == self.n:
            return 100000
        # Rakip kazanacaksa büyük negatif puan
        if opponent_count == self.n:
            return -100000
        
        # Tek hamlede kazanma durumu
        if player_count == self.n - 1 and empty_count == 1:
            return 10000
        # Rakip tek hamlede kazanacaksa büyük negatif puan
        if opponent_count == self.n - 1 and empty_count == 1:
            return -10000
        
        # İki hamlede kazanma durumu
        if player_count == self.n - 2 and empty_count == 2:
            return 1000
        if opponent_count == self.n - 2 and empty_count == 2:
            return -1000
        
        # Üç hamlede kazanma durumu
        if player_count == self.n - 3 and empty_count == 3:
            return 100
        if opponent_count == self.n - 3 and empty_count == 3:
            return -100
        
        return player_count * 10 - opponent_count * 10

    def evaluate_special_patterns(self, player):
        score = 0
        n = self.n
        
        # Çatallama durumları
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == ' ':
                    # Yatay ve dikey çatallama
                    row_threats = 0
                    col_threats = 0
                    
                    # Satır kontrolü
                    row = [self.board[i][k] for k in range(n)]
                    if row.count(player) == n-2 and row.count(' ') == 2:
                        row_threats += 1
                    
                    # Sütun kontrolü
                    col = [self.board[k][j] for k in range(n)]
                    if col.count(player) == n-2 and col.count(' ') == 2:
                        col_threats += 1
                    
                    # Çapraz kontrolü
                    diag1_threat = False
                    diag2_threat = False
                    if i == j:
                        diag1 = [self.board[k][k] for k in range(n)]
                        if diag1.count(player) == n-2 and diag1.count(' ') == 2:
                            diag1_threat = True
                    if i + j == n-1:
                        diag2 = [self.board[k][n-1-k] for k in range(n)]
                        if diag2.count(player) == n-2 and diag2.count(' ') == 2:
                            diag2_threat = True
                    
                    # Çatallama puanı
                    total_threats = row_threats + col_threats + (1 if diag1_threat else 0) + (1 if diag2_threat else 0)
                    if total_threats >= 2:
                        score += 5000  # Çatallama durumu
        
        return score

    def check_winner(self, player):
        # Satırlar
        for row in self.board:
            if all(cell == player for cell in row) and all(cell != ' ' for cell in row):
                return True
        # Sütunlar
        for col in range(self.n):
            col_cells = [self.board[row][col] for row in range(self.n)]
            if all(cell == player for cell in col_cells) and all(cell != ' ' for cell in col_cells):
                return True
        # Ana çapraz
        diag1 = [self.board[i][i] for i in range(self.n)]
        if all(cell == player for cell in diag1) and all(cell != ' ' for cell in diag1):
            return True
        # Yan çapraz
        diag2 = [self.board[i][self.n - 1 - i] for i in range(self.n)]
        if all(cell == player for cell in diag2) and all(cell != ' ' for cell in diag2):
            return True
        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def set_game_over(self, winner=None):
        self.game_over = True
        self.winner = winner

    def is_early_draw(self):
        n = self.n
        lines = []
        for i in range(n):
            lines.append([self.board[i][j] for j in range(n)])  # Satır
            lines.append([self.board[j][i] for j in range(n)])  # Sütun
        lines.append([self.board[i][i] for i in range(n)])      # Ana çapraz
        lines.append([self.board[i][n-1-i] for i in range(n)])  # Yan çapraz

        # Her satır/sütun/çaprazda sadece tek oyuncunun kazanma ihtimali varsa oyun devam eder
        for line in lines:
            if (set(line) <= {'X', ' '} or set(line) <= {'O', ' '}):
                return False
        # Eğer tüm hatlarda iki oyuncu da varsa, kimse kazanamaz, erken beraberlik
        return True

@app.route('/')
def index():
    session.clear()  # Yeni oyun başlatırken session'ı temizle
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    try:
        size = int(request.form['size'])
        if size < 3 or size > 15:
            flash('Tahta boyutu 3 ile 15 arasında olmalıdır.', 'error')
            return redirect(url_for('index'))
        first_player = 'X' if request.form['start'] == '1' else 'O'
        game = TicTacToe(size)
        game.start_game(first_player)
        last_move = None
        winner = None
        # Eğer AI ilk oynayacaksa hemen hamle yapma, sadece sayfayı aç
        # AI hamlesi game.html açıldıktan sonra başlatılacak
        session['game_state'] = {
            'board': game.board,
            'current_player': game.current_player,
            'first_player': game.first_player,
            'size': size,
            'game_over': game.game_over
        }
        session['last_move'] = last_move
        return render_template('game.html', board=game.board, first_player=first_player, size=size, last_move=session.get('last_move'), winner=winner)
    except ValueError:
        flash('Geçerli bir sayı giriniz.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Bir hata oluştu: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def move():
    try:
        if 'game_state' not in session:
            flash('Oyun durumu bulunamadı. Lütfen yeni bir oyun başlatın.', 'error')
            return redirect(url_for('index'))
        game_state = session['game_state']
        game = TicTacToe(game_state['size'])
        game.board = game_state['board']
        game.current_player = game_state['current_player']
        game.first_player = game_state['first_player']
        game.game_over = game_state['game_over']
        row = int(request.form['row'])
        col = int(request.form['col'])
        last_move = None
        if row < 0 or row >= game.n or col < 0 or col >= game.n:
            flash('Geçersiz hamle!', 'error')
            return render_template('game.html', board=game.board, size=game.n, last_move=session.get('last_move'))
        if game.user_move(row, col):
            last_move = (row, col)
            total_moves = sum(cell != ' ' for row_ in game.board for cell in row_)
            if game.check_winner(game.A1):
                game.set_game_over("Kazandınız!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="Kazandınız!", size=game.n, last_move=session.get('last_move'))
            elif game.is_early_draw():
                game.set_game_over("Erken Beraberlik!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="Erken Beraberlik!", size=game.n, last_move=session.get('last_move'))
            elif game.is_full():
                game.set_game_over("Beraberlik!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="Beraberlik!", size=game.n, last_move=session.get('last_move'))
            ai_move = game.ai_move()
            if ai_move:
                last_move = ai_move
            total_moves = sum(cell != ' ' for row_ in game.board for cell in row_)
            if game.check_winner(game.A2):
                game.set_game_over("AI Kazandı!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="AI Kazandı!", size=game.n, last_move=session.get('last_move'))
            elif game.is_early_draw():
                game.set_game_over("Erken Beraberlik!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="Erken Beraberlik!", size=game.n, last_move=session.get('last_move'))
            elif game.is_full():
                game.set_game_over("Beraberlik!")
                session['game_state']['game_over'] = True
                session['last_move'] = last_move
                return render_template('game.html', board=game.board, winner="Beraberlik!", size=game.n, last_move=session.get('last_move'))
        session['game_state'] = {
            'board': game.board,
            'current_player': game.current_player,
            'first_player': game.first_player,
            'size': game.n,
            'game_over': game.game_over
        }
        session['last_move'] = last_move
        return render_template('game.html', board=game.board, size=game.n, last_move=session.get('last_move'))
    except Exception as e:
        flash(f'Bir hata oluştu: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/restart', methods=['POST'])
def restart():
    if 'game_state' in session:
        game_state = session['game_state']
        game = TicTacToe(game_state['size'])
        game.start_game(game_state['first_player'])
        last_move = None
        winner = None
        # Eğer AI ilk oynayacaksa hemen hamle yapsın
        if game.first_player == 'O':
            last_move = game.ai_move()
            total_moves = sum(cell != ' ' for row in game.board for cell in row)
            if total_moves >= game.n:
                if game.check_winner(game.A2):
                    game.set_game_over("AI Kazandı!")
                    winner = "AI Kazandı!"
                elif game.is_full():
                    game.set_game_over("Beraberlik!")
                    winner = "Beraberlik!"
        session['game_state'] = {
            'board': game.board,
            'current_player': game.current_player,
            'first_player': game.first_player,
            'size': game.n,
            'game_over': False
        }
        session['last_move'] = last_move
        return render_template('game.html', board=game.board, winner=winner, size=game.n, last_move=last_move)
    return render_template('game.html', board=game.board, winner=None, size=game.n, last_move=None)

@app.route('/end', methods=['POST'])
def end():
    session.clear()
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ai_first_move', methods=['POST'])
def ai_first_move():
    if 'game_state' not in session:
        return jsonify({'error': 'Oyun durumu bulunamadı.'}), 400
    game_state = session['game_state']
    game = TicTacToe(game_state['size'])
    game.board = game_state['board']
    game.current_player = game_state['current_player']
    game.first_player = game_state['first_player']
    game.game_over = game_state['game_over']
    last_move = game.ai_move()
    winner = None
    # Kazanan veya beraberlik kontrolü
    total_moves = sum(cell != ' ' for row in game.board for cell in row)
    if total_moves >= game.n:
        if game.check_winner(game.A2):
            game.set_game_over("AI Kazandı!")
            winner = "AI Kazandı!"
        elif game.is_full():
            game.set_game_over("Beraberlik!")
            winner = "Beraberlik!"
    session['game_state'] = {
        'board': game.board,
        'current_player': game.current_player,
        'first_player': game.first_player,
        'size': game.n,
        'game_over': game.game_over
    }
    session['last_move'] = last_move
    return jsonify({
        'board': game.board,
        'last_move': last_move,
        'winner': winner
    })

@app.route('/game')
def game_page():
    if 'game_state' not in session:
        return redirect(url_for('index'))
    game_state = session['game_state']
    return render_template(
        'game.html',
        board=game_state['board'],
        first_player=game_state['first_player'],
        size=game_state['size'],
        last_move=session.get('last_move'),
        winner=None  # Eğer winner session'da tutuluyorsa onu da ekleyebilirsin
    )

def check_winner(board):
    n = len(board)
    # Satırları kontrol et
    for row in board:
        if all(cell == row[0] for cell in row) and row[0] != ' ':
            return f"{row[0]} Kazandı!"
    
    # Sütunları kontrol et
    for col in range(n):
        if all(board[row][col] == board[0][col] for row in range(n)) and board[0][col] != ' ':
            return f"{board[0][col]} Kazandı!"
    
    # Ana çaprazı kontrol et
    if all(board[i][i] == board[0][0] for i in range(n)) and board[0][0] != ' ':
        return f"{board[0][0]} Kazandı!"
    
    # Yan çaprazı kontrol et
    if all(board[i][n-1-i] == board[0][n-1] for i in range(n)) and board[0][n-1] != ' ':
        return f"{board[0][n-1]} Kazandı!"
    
    return None

def is_early_draw(board):
    n = len(board)
    lines = []
    for i in range(n):
        lines.append([board[i][j] for j in range(n)])  # Satır
        lines.append([board[j][i] for j in range(n)])  # Sütun
    lines.append([board[i][i] for i in range(n)])      # Ana çapraz
    lines.append([board[i][n-1-i] for i in range(n)])  # Yan çapraz

    # Her satır/sütun/çaprazda sadece tek oyuncunun kazanma ihtimali varsa oyun devam eder
    for line in lines:
        if (set(line) <= {'X', ' '} or set(line) <= {'O', ' '}):
            return False
    # Eğer tüm hatlarda iki oyuncu da varsa, kimse kazanamaz, erken beraberlik
    return True

@app.route('/twoplayer', methods=['GET', 'POST'])
def twoplayer():
    if request.method == 'GET':
        # Yeni oyun başlat veya yeniden başlat
        size = int(request.args.get('size', 3))
        session['board'] = [[' ' for _ in range(size)] for _ in range(size)]
        session['current_player'] = 'X'
        session['winner'] = None
        session['last_move'] = None
        session['size'] = size
    else:
        # POST isteği - hamle yap
        if 'board' not in session:
            size = int(request.args.get('size', 3))
            session['board'] = [[' ' for _ in range(size)] for _ in range(size)]
            session['current_player'] = 'X'
            session['winner'] = None
            session['last_move'] = None
            session['size'] = size
        else:
            size = session.get('size', 3)
        
        row = int(request.form.get('row'))
        col = int(request.form.get('col'))
        board = session['board']
        
        if board[row][col] == ' ' and not session.get('winner'):
            board[row][col] = session['current_player']
            session['last_move'] = (row, col)
            
            # Kazanan kontrolü
            winner = check_winner(board)
            if winner:
                session['winner'] = winner
            else:
                # Erken beraberlik kontrolü
                if is_early_draw(board):
                    session['winner'] = 'Erken Beraberlik!'
                # Normal beraberlik kontrolü
                elif all(cell != ' ' for row in board for cell in row):
                    session['winner'] = 'Beraberlik!'
                else:
                    session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
            
            session['board'] = board
    
    return render_template('twoplayer.html', 
                         board=session['board'],
                         current_player=session['current_player'],
                         winner=session.get('winner'),
                         last_move=session.get('last_move'),
                         size=size)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
