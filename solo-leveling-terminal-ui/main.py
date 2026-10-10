
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk


# =========================
# 1. CONFIGURATION
# =========================

BG = "#080B18"
PANEL = "#11172B"
PURPLE = "#9B6DFF"
BLUE = "#69B7FF"
WHITE = "#F1F3FF"
MUTED = "#9AA6C5"
GREEN = "#72E6B1"

DATA_FILE = Path(__file__).with_name("hunter_data.json")

QUESTS = [
    {"name": "Complete 1 coding lesson", "exp": 20},
    {"name": "Solve 1 programming problem", "exp": 35},
    {"name": "Study for 30 minutes", "exp": 50},
]


# =========================
# 2. MAIN APPLICATION
# =========================

class HunterSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SOLO LEVELING | HUNTER SYSTEM")
        self.root.geometry("900x680")
        self.root.minsize(760, 580)
        self.root.configure(bg=BG)

        self.data = self.load_data()

        self.setup_style()
        self.build_ui()
        self.refresh_ui()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # =====================
    # 3. SAVE AND LOAD
    # =====================

    def default_data(self):
        return {
            "name": "Ron Nguyen",
            "rank": "E",
            "level": 1,
            "exp": 0,
            "hp": 100,
            "mp": 50,
            "str": 10,
            "agi": 10,
            "int": 10,
            "completed_quests": [],
        }

    def load_data(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)

                default = self.default_data()
                default.update(data)

                if not isinstance(default["completed_quests"], list):
                    default["completed_quests"] = []

                return default

            except (json.JSONDecodeError, OSError):
                messagebox.showwarning(
                    "Save Data",
                    "Save file could not be read. New data will be used."
                )

        return self.default_data()

    def save_data(self):
        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )
        except OSError as error:
            messagebox.showerror("Save Error", str(error))

    # =====================
    # 4. GUI STYLE
    # =====================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "XP.Horizontal.TProgressbar",
            troughcolor=PANEL,
            background=PURPLE,
            bordercolor=PANEL,
            lightcolor=PURPLE,
            darkcolor=PURPLE,
            thickness=16,
        )

    def make_label(
        self, parent, text, size=12,
        color=WHITE, bold=False
    ):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
        )

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#292044",
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=9,
        )

    # =====================
    # 5. BUILD THE WINDOW
    # =====================

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 12))

        self.make_label(
            header, "SHADOW MONARCH // SYSTEM",
            20, PURPLE, True
        ).pack(anchor="w")

        self.make_label(
            header, "ARISE, HUNTER. YOUR JOURNEY STARTS HERE.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 0))

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=24, pady=8)

        left = tk.Frame(main, bg=PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = tk.Frame(main, bg=PANEL)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # Hunter profile
        self.make_label(
            left, "PLAYER STATUS", 14, BLUE, True
        ).pack(anchor="w", padx=18, pady=(18, 12))

        self.name_label = self.make_label(
            left, "", 17, WHITE, True
        )
        self.name_label.pack(anchor="w", padx=18)

        self.rank_label = self.make_label(
            left, "", 11, PURPLE, True
        )
        self.rank_label.pack(anchor="w", padx=18, pady=(4, 0))

        self.level_label = self.make_label(
            left, "", 13, WHITE, True
        )
        self.level_label.pack(anchor="w", padx=18, pady=(18, 6))

        self.xp_bar = ttk.Progressbar(
            left,
            style="XP.Horizontal.TProgressbar",
            maximum=100,
            mode="determinate",
        )
        self.xp_bar.pack(fill="x", padx=18)

        self.xp_label = self.make_label(
            left, "", 10, MUTED
        )
        self.xp_label.pack(anchor="w", padx=18, pady=(5, 18))

        self.make_label(
            left, "ATTRIBUTES", 12, BLUE, True
        ).pack(anchor="w", padx=18, pady=(0, 10))

        self.stats_label = self.make_label(
            left, "", 12, WHITE
        )
        self.stats_label.pack(anchor="w", padx=18)

        self.make_button(
            left, "SAVE PROGRESS", self.save_data
        ).pack(fill="x", padx=18, pady=(24, 8))

        # Daily quests
        self.make_label(
            right, "DAILY QUESTS", 14, PURPLE, True
        ).pack(anchor="w", padx=18, pady=(18, 5))

        self.make_label(
            right, "Complete quests to earn EXP.",
            10, MUTED
        ).pack(anchor="w", padx=18, pady=(0, 16))

        self.quest_buttons = []

        for index, quest in enumerate(QUESTS):
            card = tk.Frame(
                right, bg="#1A2038",
                highlightbackground="#39305F",
                highlightthickness=1,
            )
            card.pack(fill="x", padx=14, pady=6)

            self.make_label(
                card, quest["name"], 10, WHITE, True
            ).pack(anchor="w", padx=10, pady=(10, 3))

            self.make_label(
                card, f'+{quest["exp"]} EXP', 10, GREEN
            ).pack(anchor="w", padx=10, pady=(0, 6))

            button = self.make_button(
                card, "COMPLETE QUEST",
                lambda i=index: self.complete_quest(i)
            )
            button.pack(fill="x", padx=10, pady=(0, 10))

            self.quest_buttons.append(button)

        self.make_button(
            right, "RESET DAILY QUESTS",
            self.reset_quests
        ).pack(fill="x", padx=14, pady=(18, 8))

        footer = tk.Label(
            self.root,
            text="SYSTEM ONLINE  |  EVERY DAY IS A NEW LEVEL",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 9),
        )
        footer.pack(pady=(4, 16))

    # =====================
    # 6. GAME LOGIC
    # =====================

    def complete_quest(self, index):
        completed = self.data["completed_quests"]

        if index in completed:
            messagebox.showinfo(
                "Quest Complete",
                "You have already completed this quest!"
            )
            return

        completed.append(index)
        earned_exp = QUESTS[index]["exp"]
        self.data["exp"] += earned_exp

        levels_gained = 0

        while self.data["exp"] >= self.data["level"] * 100:
            required_exp = self.data["level"] * 100
            self.data["exp"] -= required_exp
            self.data["level"] += 1

            self.data["str"] += 1
            self.data["agi"] += 1
            self.data["int"] += 1
            levels_gained += 1

        self.save_data()
        self.refresh_ui()

        if levels_gained:
            messagebox.showinfo(
                "LEVEL UP!",
                f"You gained {levels_gained} level(s)!\n"
                "STR +1 | AGI +1 | INT +1"
            )
        else:
            messagebox.showinfo(
                "QUEST COMPLETE",
                f"+{earned_exp} EXP earned. Keep going, Hunter!"
            )

    def reset_quests(self):
        if not messagebox.askyesno(
            "Reset Quests",
            "Reset all daily quests? Your EXP and level will stay."
        ):
            return

        self.data["completed_quests"] = []
        self.save_data()
        self.refresh_ui()

    def get_rank(self):
        level = self.data["level"]

        if level >= 50:
            return "S"
        if level >= 30:
            return "A"
        if level >= 20:
            return "B"
        if level >= 10:
            return "C"
        if level >= 5:
            return "D"
        return "E"

    # =====================
    # 7. REFRESH THE GUI
    # =====================

    def refresh_ui(self):
        self.data["rank"] = self.get_rank()

        self.name_label.config(
            text=self.data["name"]
        )
        self.rank_label.config(
            text=f'HUNTER RANK: {self.data["rank"]}'
        )
        self.level_label.config(
            text=f'LEVEL {self.data["level"]}'
        )

        required_exp = self.data["level"] * 100
        current_exp = self.data["exp"]

        self.xp_bar["maximum"] = required_exp
        self.xp_bar["value"] = current_exp

        self.xp_label.config(
            text=f"{current_exp} / {required_exp} EXP"
        )

        self.stats_label.config(
            text=(
                f'HP     : {self.data["hp"]}\n\n'
                f'MP     : {self.data["mp"]}\n\n'
                f'STR    : {self.data["str"]}\n\n'
                f'AGI    : {self.data["agi"]}\n\n'
                f'INT    : {self.data["int"]}'
            )
        )

        completed = self.data["completed_quests"]

        for index, button in enumerate(self.quest_buttons):
            if index in completed:
                button.config(
                    text="COMPLETED ✓",
                    state="disabled",
                    disabledforeground=GREEN,
                )
            else:
                button.config(
                    text="COMPLETE QUEST",
                    state="normal",
                )

    def close_app(self):
        self.save_data()
        self.root.destroy()


# =========================
# 8. START THE APPLICATION
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    app = HunterSystem(root)
    root.mainloop()
