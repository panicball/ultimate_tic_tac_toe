def make_move(board: list[list[str]], row: int, column: int, player_value: str) -> bool:
    if board[row][column] == " ":
        board[row][column] = player_value
        return True
    return False


def check_winner(board: list[list[str]], current_player: str) -> str | None:
    movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    keyword = "XXX" if current_player == "X" else "OOO"
    answer: str | None = None

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            # for keyword in keywords:
            if board[row_index][column_index] == keyword[0]:
                for i, j in movements:
                    whole_word = []
                    word_coordinates = []

                    for k in range(len(keyword)):
                        new_row = row_index + k * i
                        new_col = column_index + k * j

                        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == keyword[k]:
                            whole_word.append(board[new_row][new_col])
                            word_coordinates.append((new_row, new_col))

                    if whole_word == list(keyword):
                        answer = keyword[0]
                        break
                    else:
                        answer = None
    return answer


def is_full(board: list[list[str]]) -> bool:
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def render(board: list[list[str]]) -> str:
    rendered_rows = []
    for row in board:
        rendered_rows.append("|".join(row))
    return "\n-----\n".join(rendered_rows)



