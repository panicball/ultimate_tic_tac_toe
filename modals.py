from enum import StrEnum

GRID_SIZE_X = 3
GRID_SIZE_Y = 3


class CellStatus(StrEnum):
    empty = ' '
    x = 'X'
    o = 'O'


class GameStatus(StrEnum):
    empty = "empty"
    x = "X"
    o = "O"
    draw = "draw"


class SuperBoardStatus(StrEnum):
    anywhere = 'anywhere'


class MiniBoard:
    def __init__(self):
        self.grid: list[list[str]] = [[CellStatus.empty for _ in range(GRID_SIZE_X)] for _ in range(GRID_SIZE_Y)]
        self.status: str = GameStatus.empty

    def mark_cell(self, cell_idx: tuple[int, int], player_value: str) -> bool:
        if len(cell_idx) == 2:
            row, column = cell_idx
        else:
            raise ValueError('Not Enough cell coordinates given.')

        if not (0 <= row <= 2 and 0 <= column <= 2):
            raise ValueError("Given cell indexes are out of the grid.")

        if player_value not in [CellStatus.x, CellStatus.o]:
            raise ValueError("Given player value is unknown. Value should be x or o.")

        if self.grid[row][column] == CellStatus.empty:
            self.grid[row][column] = player_value
            self.update_status(player_value)
            self.is_full()
            return True
        return False

    def update_status(self, player_value: str) -> str|None:
        movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if player_value not in [CellStatus.x, CellStatus.o]:
            raise ValueError("Given player value is unknown. Value should be x or o.")

        keyword = "XXX" if player_value == "X" else "OOO"
        answer: str | None = None

        for row_index, row in enumerate(self.grid):
            for column_index, column in enumerate(row):
                if self.grid[row_index][column_index] == keyword[0]:
                    for i, j in movements:
                        whole_word = []
                        word_coordinates = []

                        for k in range(len(keyword)):
                            new_row = row_index + k * i
                            new_col = column_index + k * j

                            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]) and self.grid[new_row][new_col] == keyword[k]:
                                whole_word.append(self.grid[new_row][new_col])
                                word_coordinates.append((new_row, new_col))

                        if whole_word == list(keyword):
                            answer = keyword[0]
                            self.status = GameStatus.x if keyword[0] == "X" else GameStatus.o
                            break
                        else:
                            answer = None
        return answer

    def is_full(self) -> bool:
        for row in self.grid:
            for cell in row:
                if cell == " ":
                    return False
        self.status = GameStatus.draw
        return True

    def render(self) -> str:
        rendered_rows = []
        for row in self.grid:
            rendered_rows.append("|".join(row))
        return "\n-----\n".join(rendered_rows)


class UltimateBoard:
    def __init__(self):
        self.boards: list[MiniBoard] = [MiniBoard() for _ in range(9)]
        self.superBoard: MiniBoard = MiniBoard()
        self.activeBoard: int | None = None
        self.superBoardStatus: str = GameStatus.empty
        self.activeBoardStatus: tuple[int, int] | None
        self.boardIndexes: list[list[int]] = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def legal_moves(self) -> list[tuple[int, tuple[int, int]]]:
        def available_cells(board_idx: int, mini_board: MiniBoard) -> list[tuple[int, tuple[int, int]]]:
            empty_cells = []
            for r in range(GRID_SIZE_X):
                for c in range(GRID_SIZE_Y):
                    if mini_board.grid[r][c] == CellStatus.empty:
                        empty_cells.append((board_idx, (r, c)))
            return empty_cells

        if self.activeBoard is not None:
            board = self.boards[self.activeBoard]
            if board.status == GameStatus.empty:
                return available_cells(self.activeBoard, board)
            self.activeBoard = None

        moves = []
        for idx, board in enumerate(self.boards):
            if board.status == GameStatus.empty:
                moves.extend(available_cells(idx, board))
        return moves

    def apply(self, board_idx: int, cell_idx: tuple[int, int], player_value: str) -> bool:
        if not (0 <= board_idx <= 8):
            raise ValueError("Incorrect board index provided.")

        if not isinstance(cell_idx, tuple) or len(cell_idx) != 2:
            raise ValueError("Cell index must be a tuple of two integers.")

        row, column = cell_idx

        if not all(isinstance(i, int) and 0 <= i < 3 for i in (row, column)):
            raise ValueError("Row and column must be integers between 0 and 2.")

        if player_value not in [CellStatus.x, CellStatus.o]:
            raise ValueError("Given player value is unknown. Value should be x or o.")

        small_board = self.boards[board_idx]
        if small_board.status != GameStatus.empty:
            return False

        success = small_board.mark_cell(cell_idx, player_value)
        if not success:
            return False

        if small_board.status in [GameStatus.x, GameStatus.o, GameStatus.draw]:
            for row_index, row_list in enumerate(self.boardIndexes):
                if board_idx in row_list:
                    col_index = row_list.index(board_idx)
                    self.superBoard.grid[row_index][col_index] = (
                        small_board.status if small_board.status != GameStatus.draw else CellStatus.empty
                    )
            self.superBoard.update_status(player_value)

        next_board = self.boardIndexes[row][column]
        if self.boards[next_board].status == GameStatus.empty:
            self.activeBoard = next_board
        else:
            self.activeBoard = None

        return True

    def check_global_winner(self, player_value: str) -> str | None:
        if player_value not in [CellStatus.x, CellStatus.o]:
            raise ValueError("Given player value is unknown. Value should be x or o.")
        return self.superBoard.update_status(player_value)

    def render_super(self) -> str:
        lines = []
        for big_row in range(GRID_SIZE_X):
            rendered_small = []
            for big_col in range(GRID_SIZE_Y):
                index = big_row * 3 + big_col
                mini = self.boards[index]

                rendered_small.append(mini.render().split("\n"))
            for row_idx in range(len(rendered_small[0])):
                lines.append(" # ".join(small[row_idx] for small in rendered_small))

            if big_row < 2:
                lines.append("# " * 11)

        return "\n".join(lines)
