import os
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
from parse_demo import parse_demo
import pandas as pd
from awpy import Demo

# Default demo directory
DEMO_DIRECTORY = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\"

# GUI class
class DemoSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CS2 POV Player")
        self.root.geometry("500x400")

        # Label for selecting demo
        self.label = tk.Label(root, text="Select a demo file:", font=("Arial", 12))
        self.label.pack(pady=10)

        # Listbox for available demos
        self.demo_listbox = tk.Listbox(root, height=10, width=50)
        self.demo_listbox.pack(pady=5)

        # Populate the demo list
        self.load_demos()

        # Button to parse selected demo
        self.parse_button = tk.Button(root, text="Parse Demo", command=self.parse_demo)
        self.parse_button.pack(pady=10)

        # Label for selecting player
        self.player_label = tk.Label(root, text="Select a player:", font=("Arial", 12))
        self.player_label.pack(pady=5)
        self.player_label.pack_forget()

        # Listbox for players
        self.player_listbox = tk.Listbox(root, height=10, width=50)
        self.player_listbox.pack(pady=5)
        self.player_listbox.pack_forget()

        # Button to play POV
        self.play_button = tk.Button(root, text="Play POV", command=self.play_pov)
        self.play_button.pack(pady=10)
        self.play_button.pack_forget()

    def load_demos(self):
        """Load available .dem files into the listbox."""
        demo_files = [f for f in os.listdir(DEMO_DIRECTORY) if f.endswith(".dem")]
        if not demo_files:
            messagebox.showerror("Error", "No demo files found in the directory!")
            return

        for demo in demo_files:
            self.demo_listbox.insert(tk.END, demo)

    def parse_demo(self):
        """Parse the selected demo and list players."""
        try:
            selected_demo = self.demo_listbox.get(tk.ACTIVE)
            if not selected_demo:
                messagebox.showerror("Error", "Please select a demo file!")
                return
            
            demo_path = os.path.join(DEMO_DIRECTORY, selected_demo)
            dem = Demo(demo_path)

            # Extract unique player names
            player_names = dem.ticks['name'].unique().tolist()

            if player_names is None:
                messagebox.showerror("Error", "Failed to parse demo!")
                return

            # Display players in the listbox
            self.player_listbox.delete(0, tk.END)
            for idx, player in enumerate(player_names, start=1):
                self.player_listbox.insert(tk.END, f"{idx}. {player}")

            self.player_label.pack()  # Show player selection label
            self.player_listbox.pack()  # Show player list
            self.play_button.pack()  # Show play button

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def play_pov(self):
        """Launch the pov_player script with the selected player."""
        try:
            selected_demo = self.demo_listbox.get(tk.ACTIVE)
            selected_player = self.player_listbox.get(tk.ACTIVE)

            if not selected_demo or not selected_player:
                messagebox.showerror("Error", "Please select a demo and a player!")
                return
            
            # Extract player name from listbox entry (e.g., "1. dev1ce" → "dev1ce")
            player_name = selected_player.split(". ", 1)[1]

            # Run pov_player.py with selected demo and player
            subprocess.Popen(["python", "pov_player.py", selected_demo, player_name])

            messagebox.showinfo("Success", f"Now watching {player_name} in {selected_demo}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch POV: {e}")

# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DemoSelectorApp(root)
    root.mainloop()
