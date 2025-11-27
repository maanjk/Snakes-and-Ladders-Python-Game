import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk


class SnakesAndLadders:
    def __init__(self):
        self.size = 10
        self.cell = 60
        self.margin = 40
        self.board_px = self.size * self.cell

        self.jumps = {
            # Ladders (base -> top)
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100,
            # Snakes (head -> tail)
            92: 73,
            17: 7,
            95: 75,
            98: 79,
            62: 19,
            87: 36,
            54: 34,
            
            64: 60,
            
        }

        self.root = tk.Tk()
        self.root.title("Snakes and Ladders")

        self.canvas = tk.Canvas(
            self.root,
            width=self.board_px + 2 * self.margin,
            height=self.board_px + 2 * self.margin,
            bg="#ffffff",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nw")

        controls = tk.Frame(self.root, bd=0, padx=16, pady=16, bg="#f7f7fb")
        controls.grid(row=0, column=1, sticky="nsw", padx=(10, 10), pady=(10, 10))

        title = tk.Label(controls, text="Dice Roller", font=("Segoe UI Semibold", 16), fg="#0f172a", bg="#f7f7fb")
        title.pack(anchor="center", pady=(0, 12))

        self.status = tk.StringVar(value="Player 1's turn")
        self.status_label = tk.Label(
            controls,
            textvariable=self.status,
            font=("Segoe UI", 10, "bold"),
            fg="#1e293b",
            bg="#e8f0ff",
            padx=12,
            pady=6,
        )
        self.status_label.pack(anchor="center", pady=(4, 14))

        self.dice_canvas = tk.Canvas(controls, width=110, height=110, bg="#f7f7fb", highlightthickness=0)
        self.dice_canvas.pack(pady=(4, 8))
        # Initial dice icon (empty)
        self._update_dice_icon(0)

        self.dice_value = tk.StringVar(value="Dice: -")
        self.dice_label = tk.Label(controls, textvariable=self.dice_value, font=("Segoe UI", 14, "bold"), fg="#6c63ff", bg="#f7f7fb")
        self.dice_label.pack(anchor="center", pady=(0, 16))

        self.roll_btn = tk.Button(
            controls,
            text="🎲  Roll Dice",
            width=18,
            font=("Segoe UI Semibold", 12),
            bg="#6c63ff",
            fg="#ffffff",
            activebackground="#5a52e0",
            activeforeground="#ffffff",
            relief="flat",
            command=self.roll_dice,
        )
        self.roll_btn.pack(pady=(8, 0))

        # Layout behavior
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.current_player = 1
        self.positions = {1: 1, 2: 1}
        self.tokens = {}
        self.animating = False
        # Load token images and keep references
        assets_dir = os.path.dirname(__file__)
        self.token_imgs = {
            1: tk.PhotoImage(file=os.path.join(assets_dir, "redgoti.png")),
            2: tk.PhotoImage(file=os.path.join(assets_dir, "yellowgoti.png")),
        }
        self._draw_board()
        # Drawing of arrows disabled because background image already has snakes/ladders
        self._create_tokens()

    def run(self):
        self.root.mainloop()

    def pos_to_rc(self, pos):
        pos0 = pos - 1
        r = pos0 // 10
        c = pos0 % 10
        if r % 2 == 1:
            c = 9 - c
        return r, c

    def rc_to_xy_center(self, r, c):
        x0 = self.margin
        y0 = self.margin
        x = x0 + c * self.cell + self.cell / 2
        y = y0 + (9 - r) * self.cell + self.cell / 2
        return x, y

    def pos_to_xy_center(self, pos):
        r, c = self.pos_to_rc(pos)
        return self.rc_to_xy_center(r, c)

    def _draw_board(self):
        # Load and place the board background image
        assets_dir = os.path.dirname(__file__)
        img_path = os.path.join(assets_dir, "Snakes-and-Ladders-Bigger.jpg")
        img = Image.open(img_path)
        img = img.resize((self.board_px, self.board_px), Image.LANCZOS)
        self.board_img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.margin, self.margin, image=self.board_img_tk, anchor="nw")

    def _draw_arrow(self, x1, y1, x2, y2, color):
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5, smooth=True, arrow="last", arrowshape=(12, 16, 6))
        self.canvas.create_oval(x2 - 6, y2 - 6, x2 + 6, y2 + 6, outline=color, width=3)

    def _update_dice_icon(self, value):
        c = self.dice_canvas
        c.delete("all")
        x0, y0, s = 5, 5, 100
        r = 16
        # Base square
        c.create_rectangle(x0, y0, x0 + s, y0 + s, fill="#ffffff", outline="#1e293b", width=3)
        # Pips positions
        centers = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)],
        }
        if value in centers:
            for cx, cy in centers[value]:
                px = x0 + cx * s
                py = y0 + cy * s
                c.create_oval(px - 8, py - 8, px + 8, py + 8, fill="#1e293b", outline="")

    def _create_tokens(self):
        x1, y1 = self.pos_to_xy_center(1)
        # Place player 1 and 2 images; offset P2 slightly to reduce overlap
        self.tokens[1] = self.canvas.create_image(x1, y1, image=self.token_imgs[1])
        self.tokens[2] = self.canvas.create_image(x1 + 12, y1 - 12, image=self.token_imgs[2])

    def animate_move(self, player, current, end, remaining, after_ms=120):
        if remaining <= 0:
            self._post_move(player)
            return
        new_pos = current + 1
        x, y = self.pos_to_xy_center(new_pos)
        token = self.tokens[player]
        cx, cy = self._center_of_item(token)
        dx = x - cx
        dy = y - cy
        self.canvas.move(token, dx, dy)
        self.positions[player] = new_pos
        self.root.after(after_ms, lambda: self.animate_move(player, new_pos, end, remaining - 1, after_ms))

    def _center_of_item(self, item_id):
        coords = self.canvas.coords(item_id)
        if len(coords) == 2:
            return coords[0], coords[1]
        elif len(coords) == 4:
            x0, y0, x1, y1 = coords
            return (x0 + x1) / 2, (y0 + y1) / 2
        else:
            # Fallback to origin for unexpected cases
            return 0, 0

    def move_token_to(self, player, pos):
        x, y = self.pos_to_xy_center(pos)
        token = self.tokens[player]
        cx, cy = self._center_of_item(token)
        self.canvas.move(token, x - cx, y - cy)
        self.positions[player] = pos

    def roll_dice(self):
        if self._game_over() or self.animating:
            return
        dice = random.randint(1, 6)
        self.dice_value.set(f"Dice: {dice}")
        try:
            self._update_dice_icon(dice)
        except Exception:
            pass
        p = self.current_player
        start = self.positions[p]
        target = start + dice
        if target > 100:
            self.status.set(f"Need exact roll for 100 • Player {3 - p}")
            self._switch_player()
            # Ensure button enabled and no animation state
            self.animating = False
            self.roll_btn.config(state=tk.NORMAL)
            return
        steps = dice
        self.status.set(f"Player {p} moving {dice}…")
        self.animating = True
        self.roll_btn.config(state=tk.DISABLED)
        self.animate_move(p, start, target, steps)

    def _post_move(self, player):
        pos = self.positions[player]
        if pos in self.jumps:
            end = self.jumps[pos]
            if end > pos:
                self.status.set(f"Player {player} climbs ladder to {end}.")
            else:
                self.status.set(f"Player {player} bitten by snake to {end}.")
            self.root.after(350, lambda: self.move_token_to(player, end))
            self.root.after(400, lambda: self._finalize_turn(player))
        else:
            self._finalize_turn(player)

    def _finalize_turn(self, player):
        pos = self.positions[player]
        if pos == 100:
            self.status.set(f"Player {player} wins!")
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            self.roll_btn.config(state=tk.DISABLED)
            return
        self._switch_player()
        self.status.set(f"Player {self.current_player}'s turn")
        self.animating = False
        self.roll_btn.config(state=tk.NORMAL)

    def _switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def _game_over(self):
        return self.positions[1] == 100 or self.positions[2] == 100


if __name__ == "__main__":
    app = SnakesAndLadders()
    app.run()

