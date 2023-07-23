import random

board = [[" " for _ in range(3)] for _ in range(3)]

def draw_board():
  print("  0 1 2")
  for i, row in enumerate(board):
    print(i, " ".join(row))

def get_human_move():
  while True:
    col = input("Enter column: ")
    row = input("Enter row: ")
    if col.isdigit() and row.isdigit():
      col, row = int(col), int(row)
      if 0 <= col < 3 and 0 <= row < 3:
        if board[row][col] == " ":
          board[row][col] = "X"
          return
        else:
          print("That space is already occupied. Try again.")
      else:
        print("Invalid move. Try again.")
    else:
      print("Invalid input. Try again.")

def get_computer_move():
  while True:
    col = random.randint(0, 2)
    row = random.randint(0, 2)
    if board[row][col] == " ":
      board[row][col] = "O"
      return

def has_winner():
  for row in board:
    if row[0] == row[1] == row[2] and row[0] != " ":
      return True
  for col in range(3):
    if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
      return True
  if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
    return True
  if board[2][0] == board[1][1] == board[0][2] and board[2][0] != " ":
    return True
  return False

def main():
  while True:
    draw_board()
    get_human_move()
    if has_winner():
      print("X wins!")
      break
    draw_board()
    get_computer_move()
    if has_winner():
      print("O wins!")
      break

main()