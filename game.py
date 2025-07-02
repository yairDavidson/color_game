import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class WerewolfGame:
    def __init__(self, root):
        self.root = root
        self.players = []
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Ultimate Werewolf")
        tk.Label(self.root, text="Enter player names (comma-separated):").pack()
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack()
        tk.Button(self.root, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        names = [n.strip() for n in self.name_entry.get().split(',')]
        if len(names) < 3:
            messagebox.showwarning("Oops", "At least 3 players are needed.")
            return

        roles = ['Werewolf', 'Seer'] + ['Villager'] * (len(names) - 2)
        random.shuffle(roles)
        self.players = [{'name': name, 'role': role, 'alive': True} for name, role in zip(names, roles)]

        for player in self.players:
            messagebox.showinfo("Role Assignment", f"{player['name']}, your role is: {player['role']}")

        self.next_phase()

    def next_phase(self):
        if self.game_over():
            self.show_result()
            return
        self.night_phase()
        if self.game_over():
            self.show_result()
            return
        self.day_phase()
        self.next_phase()

    def night_phase(self):
        seer = next((p for p in self.players if p['role'] == 'Seer' and p['alive']), None)
        werewolf = next((p for p in self.players if p['role'] == 'Werewolf' and p['alive']), None)

        if seer:
            options = [p['name'] for p in self.players if p['alive'] and p != seer]
            guess = simpledialog.askstring("Seer", f"{seer['name']}, who do you want to inspect? {options}")
            inspected = next(p for p in self.players if p['name'] == guess)
            messagebox.showinfo("Vision", f"{guess} is a {inspected['role']}")

        if werewolf:
            targets = [p['name'] for p in self.players if p['alive'] and p != werewolf]
            victim_name = simpledialog.askstring("Werewolf", f"{werewolf['name']}, choose victim: {targets}")
            victim = next(p for p in self.players if p['name'] == victim_name)
            victim['alive'] = False
            messagebox.showinfo("Night", f"{victim_name} was eliminated!")

    def day_phase(self):
        alive = [p['name'] for p in self.players if p['alive']]
        vote = simpledialog.askstring("Vote", f"Who do you vote to eliminate? {alive}")
        accused = next((p for p in self.players if p['name'] == vote and p['alive']), None)
        if accused:
            accused['alive'] = False
            messagebox.showinfo("Day", f"{accused['name']} was voted out. They were a {accused['role']}.")

    def game_over(self):
        werewolves = [p for p in self.players if p['role'] == 'Werewolf' and p['alive']]
        villagers = [p for p in self.players if p['role'] != 'Werewolf' and p['alive']]
        return len(werewolves) == 0 or len(werewolves) >= len(villagers)

    def show_result(self):
        if any(p['role'] == 'Werewolf' and p['alive'] for p in self.players):
            messagebox.showinfo("Game Over", "🐺 Werewolves win!")
        else:
            messagebox.showinfo("Game Over", "👨‍🌾 Villagers win!")

if __name__ == "__main__":
    root = tk.Tk()
    game = WerewolfGame(root)
    root.mainloop()
