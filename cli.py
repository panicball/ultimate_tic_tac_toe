import argparse
from modals import UltimateBoard, CellStatus


def main():
    parser = argparse.ArgumentParser(description="Play Ultimate Tic-Tac-Toe via command line.")
    parser.add_argument("symbol", choices=["X", "O"], help="Player symbol (X or O)")
    args = parser.parse_args()

    board = UltimateBoard()
    current_player = args.symbol
    board_idx = int(input("Choose starting board (0–8): "))

    print("\nWelcome to Ultimate Tic-Tac-Toe!")
    print(board.render_super())

    while True:
        try:
            print(f"\nCurrent Player: {current_player}")
            print(f"Active Board: {board_idx if board_idx is not None else 'Any'}")

            board.activeBoard = board_idx

            legal = board.legal_moves()
            print(f"Legal moves: {legal}")

            if board_idx is None:
                board_idx = int(input("Choose a board to play in (0–8): "))
                if not (0 <= board_idx <= 8):
                    print(" xxx Board index must be between 0 and 8. xxx")
                    continue

            coords = input("Enter row and column (e.g., 0 2): ").strip().split()
            if len(coords) != 2:
                print(" xxx Please enter two numbers separated by a space. xxx")
                continue

            row, col = map(int, coords)

            if not (0 <= row <= 2 and 0 <= col <= 2):
                print(" xxx Coordinates must be between 0 and 2. xxx")
                continue

            move = (board_idx, (row, col))
            if move not in legal:
                print(" xxx Invalid move. Try again. xxx ")
                continue

            if board.apply(board_idx, (row, col), current_player):
                print("\nMove applied!")
                print(board.render_super())

                winner = board.check_global_winner(current_player)
                if winner in [CellStatus.x, CellStatus.o]:
                    print(f"\n{current_player} wins the game!")
                    break
                elif board.superBoard.is_full():
                    print("\nIts is a draw.")
                    break
                else:
                    current_player = CellStatus.o if current_player == CellStatus.x else CellStatus.x
                    board_idx = board.activeBoard
            else:
                print(" xxx Invalid move. Try again. xxx ")

        except ValueError:
            print(" xxx Invalid input. Please enter valid numbers. xxx")
        except KeyboardInterrupt:
            print("\nGame interrupted. byebye!")
            break


if __name__ == "__main__":
    main()
