#FirstTime
#himalsubedi@Mac Himal Subedi PY Projects % python3 -m venv studysession

#EveryTime
#himalsubedi@Mac Himal Subedi PY Projects % source studysession/bin/activate
#OR
#himalsubedi@Mac Himal Subedi PY Projects % . studysession/bin/activate

import tkinter as tk

class ThreeMensMorris:
    def __init__(self, root):
        self.root = root #Holds the tkinter window (Tk()object) passed into the class
        self.root.title("3 Men's Morris")

        # Game state
        self.current_player = "X"
        self.board = [""] * 9
        self.pieces_placed = {"X": 0, "O": 0}
        self.max_pieces = 3
        self.selected_piece = None #For moving phase

        # Helps to track if we are in placement or moving phase
        self.phase = "placement"

        # Rule or Lineup for adjacent positions
        self.adjacent_positions = {
            0: [1, 3, 4],
            1: [0, 2, 4],
            2: [1, 4, 5],
            3: [0, 4, 6],
            4: [0, 1, 2, 3, 5, 6, 7, 8],
            5: [2, 4, 8],
            6: [3, 4, 7],
            7: [4, 6, 8],
            8: [4, 5, 7]
        }

        # User Interface
        self.buttons = []
        for i in range(9):
            btn = tk.Button(root, text="", width=6, height=3,
                            font=("Arial", 20),
                            command=lambda i = i: self.on_click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        self.status_label = tk.Label(root, text="Player X's turn (placement)", font=("Arial", 14))
        self.status_label.grid(row=3, column=0, columnspan=3)

        reset_btn = tk.Button(root, text="Reset", font=("Arial", 14), command=self.reset_game)
        reset_btn.grid(row=4, column=0, columnspan=3, pady=5)
        #Note: Root tells tkinter to attach button to the main window

    def on_click(self, i):
        #Handling the function of button depending on Phase
        if self.phase == "placement":
            self.place_piece(i)
        else:
            self.move_piece(i)

    def place_piece(self, i):
        if self.board[i] == "":
            self.board[i] = self.current_player
            self.buttons[i].config(text=self.current_player)
            self.pieces_placed[self.current_player] += 1

            if self.check_winner():
                self.end_game(f"Player {self.current_player} wins!")
                return

            # If both players have placed 3 pieces, move to moving phase
            if self.pieces_placed["X"] == self.max_pieces and self.pieces_placed["O"] == self.max_pieces:
                self.phase = "moving"
                self.switch_player()  #  switching players
                self.status_label.config(text=f"Player {self.current_player}'s turn (moving)")
            else:
                self.switch_player()


    def move_piece(self, i):
        # Step 1: Select player's piece
        if self.selected_piece is None:
            if self.board[i] == self.current_player:
                self.selected_piece = i
                self.buttons[i].config(bg="yellow")
            return

        # Step 2: Moving the piece to adjacent empty cell
        if self.board[i] == "" and i in self.adjacent_positions[self.selected_piece]:
            self.board[i] = self.current_player
            self.board[self.selected_piece] = "" #clearing old cell

            self.buttons[i].config(text=self.current_player)
            self.buttons[self.selected_piece].config(text="", bg="SystemButtonFace") #clearing old button in gui

            self.selected_piece = None

            if self.check_winner():
                self.end_game(f"Player {self.current_player} wins!")
                return

            self.switch_player()
        else:
            # Resetting if the player goes for invalid move
            self.buttons[self.selected_piece].config(bg="SystemButtonFace")
            self.selected_piece = None

    def check_winner(self):
        winning_combos = [(0,1,2), (3,4,5), (6,7,8),
                          (0,3,6), (1,4,7), (2,5,8),
                          (0,4,8), (2,4,6)]
        for a, b, c in winning_combos:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

        if self.phase == "placement":
            phase_text = "placement" 
        else:
            phase_text = "moving"

        self.status_label.config(text=f"Player {self.current_player}'s turn ({phase_text})")

    def end_game(self, message):
        self.status_label.config(text=message)
        for btn in self.buttons:
            btn.config(state="disabled") #disabling all the buttons

    def reset_game(self):
        self.board = [""] * 9
        self.pieces_placed = {"X": 0, "O": 0}
        self.current_player = "X"
        self.selected_piece = None
        self.phase = "placement"
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="SystemButtonFace")
        self.status_label.config(text="Player X's turn (placement)")

if __name__ == "__main__":
    root = tk.Tk()
    game = ThreeMensMorris(root)
    root.mainloop()
