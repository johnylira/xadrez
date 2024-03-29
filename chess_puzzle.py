import copy
import random

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    col, row = loc[0], loc[1:]
    col_index = ord(col.lower()) - ord('a') + 1
    return (col_index, int(row))
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    col = chr(ord('a') + x - 1)
    return f"{col}{y}"
class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_  # True for White, False for Black

Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece
    raise ValueError("No piece was found at specified coordinates")

class Knight(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this knight can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        # O cavalo move em "L": duas casas em uma direção e uma casa na direção perpendicular
        dx = abs(self.pos_x - pos_X)
        dy = abs(self.pos_y - pos_Y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this knight can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            if captured_piece.side == self.side:
                return False  # Não pode capturar peças do mesmo lado

        return True
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this knight to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        # new_board = copy.deepcopy(B)
        # for piece in new_board[1]:
        #     if piece == self:
        #         piece.pos_x = pos_X
        #         piece.pos_y = pos_Y
        #         break
        # return new_board
        
        new_pieces = [piece for piece in B[1] if not (piece.pos_x == pos_X and piece.pos_y == pos_Y)]  # Remove a peça na posição de destino, se houver
        new_board = (B[0], new_pieces)

        for piece in new_board[1]:
            if piece == self:
                piece.pos_x = pos_X
                piece.pos_y = pos_Y
                break

        return new_board


class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    # Encontrar a posição do rei do lado especificado
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king_pos = (piece.pos_x, piece.pos_y)

    # Verificar se alguma peça do lado oposto pode se mover para a posição do rei
    for piece in B[1]:
        if piece.side != side and piece.can_move_to(king_pos[0], king_pos[1], B):
            return True

    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
    if not is_check(side, B):
        return False

    # Verificar se há algum movimento que o lado em cheque pode fazer para escapar do cheque
    for piece in B[1]:
        if piece.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if piece.can_move_to(x, y, B):
                        # Criar um novo tabuleiro com esse movimento e verificar se ainda está em cheque
                        new_board = piece.move_to(x, y, B)
                        if not is_check(side, new_board):
                            return False

    return True

def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B):
        return False

    # Verificar se há algum movimento legal que o lado pode fazer
    for piece in B[1]:
        if piece.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if piece.can_move_to(x, y, B):
                        return False

    return True

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {filename} não foi encontrado no diretório especificado.")

    size = int(lines[0].strip())
    pieces = []

    # Adicionando peças brancas
    white_pieces = lines[1].split()
    for wp in white_pieces:
        piece_type, loc = wp[0], wp[1:]
        x, y = location2index(loc)
        piece = Knight(x, y, True) if piece_type == 'N' else King(x, y, True)
        pieces.append(piece)

    # Adicionando peças pretas
    black_pieces = lines[2].split()
    for bp in black_pieces:
        piece_type, loc = bp[0], bp[1:]
        x, y = location2index(loc)
        piece = Knight(x, y, False) if piece_type == 'N' else King(x, y, False)
        pieces.append(piece)

    return size, pieces

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    with open(filename, 'w') as file:
        file.write(str(B[0]) + '\n')
        white_pieces = ' '.join([index2location(piece.pos_x, piece.pos_y) for piece in B[1] if piece.side])
        black_pieces = ' '.join([index2location(piece.pos_x, piece.pos_y) for piece in B[1] if not piece.side])
        file.write(white_pieces + '\n')
        file.write(black_pieces + '\n')

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    black_pieces = [piece for piece in B[1] if not piece.side]
    random.shuffle(black_pieces)
    for piece in black_pieces:
        possible_moves = [(x, y) for x in range(1, B[0]+1) for y in range(1, B[0]+1) if piece.can_move_to(x, y, B)]
        if possible_moves:
            return piece, *random.choice(possible_moves)
    return None, 0, 0  # Caso não encontre nenhum movimento válido

def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    board_str = ""
    for y in range(B[0], 0, -1):
        for x in range(1, B[0]+1):
            piece = piece_at(x, y, B) if is_piece_at(x, y, B) else None
            if piece:
                if isinstance(piece, King):
                    board_str += "\u2654" if piece.side else "\u265A"
                else:
                    board_str += "\u2658" if piece.side else "\u265E"
            else:
                board_str += "\u2001"
        board_str += "\n"
    return board_str

def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    while True:
        filename = input("Nome do arquivo para a configuração inicial: ")
        if filename.upper() == "QUIT":
            return
        try:
            B = read_board(filename)
            break
        except IOError:
            print("Este não é um arquivo válido. Por favor, insira um novo nome de arquivo.")

    print("A configuração inicial é:\n" + conf2unicode(B))

    while True:
        # Movimento do jogador branco
        user_move = input("Próximo movimento do Branco: ")
        if user_move.upper() == "QUIT":
            save_filename = input("Nome do arquivo para salvar a configuração: ")
            save_board(save_filename, B)
            print("Configuração do jogo salva.")
            break

        # Processar movimento do jogador branco aqui

        # Checar por condições de fim de jogo para o Branco
        if is_checkmate(False, B):
            print("Jogo terminado. Branco vence.")
            break
        elif is_stalemate(False, B):
            print("Jogo terminado. Afogamento.")
            break

        # Movimento do computador (preto)
        black_piece, x, y = find_black_move(B)
        if black_piece:
            print(f"Próximo movimento do Preto: {index2location(black_piece.pos_x, black_piece.pos_y)}{index2location(x, y)}")
            B = black_piece.move_to(x, y, B)
            print("A configuração após o movimento do Preto é:\n" + conf2unicode(B))

        # Checar por condições de fim de jogo para o Preto
        if is_checkmate(True, B):
            print("Jogo terminado. Preto vence.")
            break
        elif is_stalemate(True, B):
            print("Jogo terminado. Afogamento.")
            break

if __name__ == '__main__': #keep this in
   main()
