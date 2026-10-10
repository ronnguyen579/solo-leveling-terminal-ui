import json
import tkinter as tk
import tkinter.messagebox as messagebox
from pathlib import Path

import customtkinter as ctk

try:
    import winsound  # Windows built-in audio; no extra package required.
except ImportError:
    winsound = None


# ============================================================
# CONFIG
# ============================================================

APP_NAME = "SHADOW MONARCH // HUNTER SYSTEM"
DATA_FILE = Path("hunter_data.json")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

C = {
    "bg": "#090B14",
    "header": "#111525",
    "panel": "#12182B",
    "panel_alt": "#19213A",
    "panel_hover": "#202B49",
    "purple": "#8B5CF6",
    "purple_bright": "#B69CFF",
    "purple_hover": "#7042D8",
    "blue": "#38BDF8",
    "text": "#F1F5F9",
    "muted": "#94A3B8",
    "green": "#4ADE80",
    "border": "#303852",
    "gold": "#FBBF24",
}

STAT_NAMES = {
    "STR": "Strength",
    "AGI": "Agility",
    "INT": "Intelligence",
    "VIT": "Vitality",
}


# ============================================================
# SAVE / GAME LOGIC
# ============================================================

def default_data():
    return {
        "player_name": "New Hunter",
        "level": 1,
        "exp": 0,
        "stat_points": 0,
        "stats": {"STR": 5, "AGI": 5, "INT": 5, "VIT": 5},
    }


def load_data():
    data = default_data()
    if not DATA_FILE.exists():
        return data

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            old = json.load(f)
        if not isinstance(old, dict):
            raise ValueError("Save data must be a JSON object.")

        # Keep old fields (quests, HP, MP, etc.) instead of deleting them.
        data.update(old)
        if "player_name" not in old and "name" in old:
            data["player_name"] = old["name"]

        old_stats = old.get("stats", {})
        if not isinstance(old_stats, dict):
            old_stats = {}
        stats = default_data()["stats"]
        stats.update(old_stats)
        for key in stats:
            if key in old:
                stats[key] = old[key]
        data["stats"] = {
            key: max(0, int(value)) for key, value in stats.items()
        }
        data["level"] = max(1, int(data.get("level", 1)))
        data["exp"] = max(0, int(data.get("exp", 0)))
        data["stat_points"] = max(0, int(data.get("stat_points", 0)))
        if not isinstance(data.get("player_name"), str):
            data["player_name"] = "New Hunter"
        return data
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        raise RuntimeError(
            f"Không đọc được {DATA_FILE}.\n"
            "File save gốc chưa bị ghi đè.\n\n"
            f"Chi tiết: {exc}"
        ) from exc


def save_data(data):
    temp = DATA_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
    temp.replace(DATA_FILE)


def get_rank(level):
    if level >= 100:
        return "NATIONAL"
    if level >= 70:
        return "S"
    if level >= 50:
        return "A"
    if level >= 35:
        return "B"
    if level >= 20:
        return "C"
    if level >= 10:
        return "D"
    return "E"


def exp_required(level):
    return max(1, level * 100)


# ============================================================
# APP
# ============================================================

class HunterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1020x760")
        self.minsize(720, 560)
        self.configure(fg_color=C["bg"])

        try:
            self.data = load_data()
        except RuntimeError as exc:
            messagebox.showerror("Save Error", str(exc))
            self.destroy()
            return

        self.stat_labels = {}
        self.stat_buttons = {}
        self.status_values = {}
        self._scroll_target = 0.0
        self._scroll_animating = False
        self._wheel_bind_id = None
        self._toast_job = None
        self._toast_animation_jobs = []
        self._build_ui()
        self.refresh_ui()
        self._bind_smooth_scroll()
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.bind("<Configure>", self._on_resize)

    # --------------------------------------------------------
    # UI BUILD
    # --------------------------------------------------------

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Compact fixed header
        header = ctk.CTkFrame(self, fg_color=C["header"], corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="SHADOW MONARCH",
            font=("Consolas", 19, "bold"), text_color=C["purple_bright"]
        ).grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        ctk.CTkLabel(
            header, text="HUNTER SYSTEM  /  PROTOCOL v1.1",
            font=("Consolas", 9), text_color=C["muted"]
        ).grid(row=1, column=0, padx=21, pady=(0, 10), sticky="w")

        # Canvas scroll region. CustomTkinter canvas + scrollbar allows
        # animated scrolling instead of jumping several rows per wheel tick.
        scroll_host = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        scroll_host.grid(row=1, column=0, sticky="nsew")
        scroll_host.grid_rowconfigure(0, weight=1)
        scroll_host.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            scroll_host,
            bg=C["bg"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ctk.CTkScrollbar(
            scroll_host, orientation="vertical", command=self._scrollbar_command,
            width=12, button_color=C["purple"], button_hover_color=C["purple_hover"]
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 3), pady=4)

        self.content = ctk.CTkFrame(self.canvas, fg_color=C["bg"], corner_radius=0)
        self.content_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )
        self.content.grid_columnconfigure(0, weight=1, uniform="panels")
        self.content.grid_columnconfigure(1, weight=1, uniform="panels")

        self.content.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_content_window)

        # Profile spans both columns.
        self._build_profile()
        self._build_attributes()
        self._build_status()
        self._build_actions()

        footer = ctk.CTkFrame(self, fg_color=C["header"], corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        ctk.CTkLabel(
            footer,
            text="LOCAL SAVE ENABLED  •  SHADOW MONARCH SYSTEM",
            font=("Consolas", 9), text_color=C["muted"]
        ).pack(pady=6)

        # Toast sits over the UI; hidden until an event happens.
        self.toast = ctk.CTkFrame(
            self, fg_color="#241A45", border_width=1,
            border_color=C["purple"], corner_radius=12
        )
        self.toast_title = ctk.CTkLabel(
            self.toast, text="SYSTEM NOTIFICATION",
            font=("Consolas", 10, "bold"), text_color=C["purple_bright"]
        )
        self.toast_title.pack(anchor="w", padx=14, pady=(10, 0))
        self.toast_message = ctk.CTkLabel(
            self.toast, text="", font=("Segoe UI", 13, "bold"),
            text_color=C["text"], wraplength=320, justify="left"
        )
        self.toast_message.pack(anchor="w", padx=14, pady=(3, 10))

    def _panel(self, parent, **kwargs):
        return ctk.CTkFrame(
            parent, fg_color=C["panel"], border_width=1,
            border_color=C["border"], corner_radius=14, **kwargs
        )

    def _build_profile(self):
        panel = self._panel(self.content)
        panel.grid(row=0, column=0, columnspan=2, sticky="ew",
                   padx=14, pady=(14, 8))
        panel.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(13, 0))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top, text="HUNTER PROFILE", font=("Consolas", 10, "bold"),
            text_color=C["muted"]
        ).grid(row=0, column=0, sticky="w")

        self.rank_badge = ctk.CTkLabel(
            top, text="RANK E", font=("Consolas", 11, "bold"),
            text_color=C["purple_bright"], fg_color="#241A45",
            corner_radius=7
        )
        self.rank_badge.grid(row=0, column=1, sticky="e", padx=(8, 0), ipady=4, ipadx=8)

        self.name_label = ctk.CTkLabel(
            panel, text="", font=("Segoe UI", 23, "bold"),
            text_color=C["text"], anchor="w"
        )
        self.name_label.grid(row=1, column=0, padx=16, pady=(7, 0), sticky="ew")

        line = ctk.CTkFrame(panel, fg_color="transparent")
        line.grid(row=2, column=0, padx=16, pady=(5, 0), sticky="ew")
        line.grid_columnconfigure(1, weight=1)
        self.level_label = ctk.CTkLabel(
            line, text="", font=("Consolas", 12, "bold"), text_color=C["blue"]
        )
        self.level_label.grid(row=0, column=0, sticky="w")
        self.exp_label = ctk.CTkLabel(
            line, text="", font=("Consolas", 10), text_color=C["muted"]
        )
        self.exp_label.grid(row=0, column=1, sticky="e")

        self.exp_bar = ctk.CTkProgressBar(
            panel, height=8, progress_color=C["purple"],
            fg_color=C["panel_hover"], corner_radius=6
        )
        self.exp_bar.grid(row=3, column=0, padx=16, pady=(9, 14), sticky="ew")

    def _build_attributes(self):
        panel = self._panel(self.content)
        self.attributes_panel = panel
        panel.grid(row=1, column=0, sticky="nsew", padx=(14, 6), pady=8)
        panel.grid_columnconfigure(0, weight=1)

        title_row = ctk.CTkFrame(panel, fg_color="transparent")
        title_row.grid(row=0, column=0, padx=13, pady=(13, 8), sticky="ew")
        title_row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            title_row, text="ATTRIBUTES", font=("Consolas", 12, "bold"),
            text_color=C["text"]
        ).grid(row=0, column=0, sticky="w")
        self.points_label = ctk.CTkLabel(
            title_row, text="POINTS 0", font=("Consolas", 9, "bold"),
            text_color=C["blue"]
        )
        self.points_label.grid(row=0, column=1, sticky="e")

        for row, (key, description) in enumerate(STAT_NAMES.items(), start=1):
            item = ctk.CTkFrame(panel, fg_color=C["panel_alt"], corner_radius=9)
            item.grid(row=row, column=0, padx=10, pady=4, sticky="ew")
            item.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                item, text=key, width=40, font=("Consolas", 13, "bold"),
                text_color=C["purple_bright"]
            ).grid(row=0, column=0, padx=(8, 2), pady=9)
            ctk.CTkLabel(
                item, text=description, font=("Segoe UI", 10),
                text_color=C["muted"]
            ).grid(row=0, column=1, padx=3, pady=9, sticky="w")

            self.stat_labels[key] = ctk.CTkLabel(
                item, text="5", width=26, font=("Consolas", 13, "bold"),
                text_color=C["text"]
            )
            self.stat_labels[key].grid(row=0, column=2, padx=3, pady=9)

            btn = ctk.CTkButton(
                item, text="+", width=28, height=27, corner_radius=7,
                font=("Consolas", 13, "bold"),
                fg_color=C["purple"], hover_color=C["purple_hover"],
                command=lambda stat=key: self.allocate_point(stat)
            )
            btn.grid(row=0, column=3, padx=(3, 8), pady=6)
            self.stat_buttons[key] = btn

    def _build_status(self):
        panel = self._panel(self.content)
        self.status_panel = panel
        panel.grid(row=1, column=1, sticky="nsew", padx=(6, 14), pady=8)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel, text="SYSTEM STATUS", font=("Consolas", 12, "bold"),
            text_color=C["text"]
        ).grid(row=0, column=0, padx=13, pady=(13, 8), sticky="w")

        for row, title in enumerate(
            ["HUNTER RANK", "CHARACTER LEVEL", "UNSPENT POINTS"], start=1
        ):
            card = ctk.CTkFrame(panel, fg_color=C["panel_alt"], corner_radius=9)
            card.grid(row=row, column=0, padx=10, pady=4, sticky="ew")
            card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                card, text=title, font=("Consolas", 8),
                text_color=C["muted"]
            ).grid(row=0, column=0, padx=10, pady=(8, 0), sticky="w")
            value = ctk.CTkLabel(
                card, text="--", font=("Segoe UI", 17, "bold"),
                text_color=C["blue"]
            )
            value.grid(row=1, column=0, padx=10, pady=(0, 7), sticky="w")
            self.status_values[title] = value

        self.system_message = ctk.CTkLabel(
            panel, text="SYSTEM READY", font=("Consolas", 9),
            text_color=C["purple_bright"], anchor="w"
        )
        self.system_message.grid(
            row=4, column=0, padx=13, pady=(9, 12), sticky="ew"
        )

    def _build_actions(self):
        actions = ctk.CTkFrame(self.content, fg_color="transparent")
        self.actions_panel = actions
        actions.grid(row=2, column=0, columnspan=2, sticky="ew",
                     padx=14, pady=(4, 14))
        actions.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            actions, text="+100 EXP  (TEST)", height=34, corner_radius=9,
            fg_color=C["purple"], hover_color=C["purple_hover"],
            command=lambda: self.add_exp(100, source="TEST")
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")

        ctk.CTkButton(
            actions, text="SAVE PROGRESS", height=34, corner_radius=9,
            fg_color=C["panel_alt"], hover_color=C["panel_hover"],
            command=self.save_progress
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")

    # --------------------------------------------------------
    # SMOOTH SCROLL
    # --------------------------------------------------------

    def _bind_smooth_scroll(self):
        # Bind wheel events to canvas and all child widgets. On Windows,
        # delta is normally a multiple of 120; normalize it for a small target.
        self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.canvas.bind("<Button-4>", lambda _e: self._queue_scroll(-50))
        self.canvas.bind("<Button-5>", lambda _e: self._queue_scroll(50))

    def _on_mousewheel(self, event):
        # Do not hijack scrolling if the pointer is outside this app.
        try:
            x, y = self.winfo_pointerxy()
            widget = self.winfo_containing(x, y)
            if widget is None or not str(widget).startswith(str(self)):
                return
        except tk.TclError:
            return

        if event.delta:
            self._queue_scroll(-event.delta / 120 * 52)

    def _queue_scroll(self, pixels):
        view = self.canvas.yview()
        if view == (0.0, 1.0):
            return
        height = max(1, self.canvas.winfo_height())
        current = view[0] * max(1, self.canvas.bbox("all")[3])
        self._scroll_target = max(0.0, min(
            current + pixels,
            max(0, self.canvas.bbox("all")[3] - height)
        ))
        if not self._scroll_animating:
            self._scroll_animating = True
            self._animate_scroll()

    def _animate_scroll(self):
        try:
            bbox = self.canvas.bbox("all")
            if not bbox:
                self._scroll_animating = False
                return
            total = max(1, bbox[3] - bbox[1])
            height = max(1, self.canvas.winfo_height())
            current = self.canvas.yview()[0] * total
            distance = self._scroll_target - current
            if abs(distance) < 1.5:
                self.canvas.yview_moveto(self._scroll_target / total)
                self._scroll_animating = False
                return
            # Ease toward the target. Repeated wheel events update the target.
            next_y = current + distance * 0.32
            self.canvas.yview_moveto(max(0.0, min(1.0, next_y / total)))
            self._sync_scrollbar()
            self.after(12, self._animate_scroll)
        except tk.TclError:
            self._scroll_animating = False

    def _scrollbar_command(self, *args):
        # Direct scrollbar drag remains precise; wheel scrolling is eased.
        self.canvas.yview(*args)
        view = self.canvas.yview()
        bbox = self.canvas.bbox("all")
        if bbox:
            self._scroll_target = view[0] * max(1, bbox[3])

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._sync_scrollbar()

    def _resize_content_window(self, event):
        self.canvas.itemconfigure(self.content_window, width=event.width)
        self._sync_scrollbar()

    def _sync_scrollbar(self):
        try:
            self.scrollbar.set(*self.canvas.yview())
        except tk.TclError:
            pass

    def _on_resize(self, _event=None):
        # Reflow to one column on narrower windows.
        if not hasattr(self, "attributes_panel"):
            return
        if self.winfo_width() < 790:
            self.attributes_panel.grid_configure(
                row=1, column=0, columnspan=2, padx=14, pady=6, sticky="ew"
            )
            self.status_panel.grid_configure(
                row=2, column=0, columnspan=2, padx=14, pady=6, sticky="ew"
            )
            self.actions_panel.grid_configure(row=3, column=0, columnspan=2)
        else:
            self.attributes_panel.grid_configure(
                row=1, column=0, columnspan=1, padx=(14, 6), pady=8,
                sticky="nsew"
            )
            self.status_panel.grid_configure(
                row=1, column=1, columnspan=1, padx=(6, 14), pady=8,
                sticky="nsew"
            )
            self.actions_panel.grid_configure(row=2, column=0, columnspan=2)

    # --------------------------------------------------------
    # NOTIFICATIONS, SOUND, EFFECTS
    # --------------------------------------------------------

    def play_levelup_sound(self):
        """Use built-in Windows system sounds; fallback to Tk bell."""
        try:
            if winsound:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
                # A second short tone makes the notification more noticeable.
                self.after(130, lambda: winsound.MessageBeep(winsound.MB_OK))
            else:
                self.bell()
        except (RuntimeError, tk.TclError):
            try:
                self.bell()
            except tk.TclError:
                pass

    def show_toast(self, title, message, level_up=False):
        if self._toast_job:
            try:
                self.after_cancel(self._toast_job)
            except tk.TclError:
                pass
        for job in self._toast_animation_jobs:
            try:
                self.after_cancel(job)
            except tk.TclError:
                pass
        self._toast_animation_jobs.clear()

        bg = "#2B1B51" if level_up else "#17233B"
        border = C["purple_bright"] if level_up else C["blue"]
        self.toast.configure(fg_color=bg, border_color=border)
        self.toast_title.configure(
            text=title,
            text_color=C["gold"] if level_up else C["blue"]
        )
        self.toast_message.configure(text=message)
        self.toast.place(relx=0.5, y=12, anchor="n")
        self.toast.lift()

        if level_up:
            self.play_levelup_sound()
            self._pulse_toast(0)
        self._toast_job = self.after(3600, self._hide_toast)

    def _pulse_toast(self, step):
        colors = ["#2B1B51", "#42266E", "#2B1B51", "#36205D", "#2B1B51"]
        if step >= len(colors):
            return
        try:
            self.toast.configure(fg_color=colors[step])
            job = self.after(110, lambda: self._pulse_toast(step + 1))
            self._toast_animation_jobs.append(job)
        except tk.TclError:
            return

    def _hide_toast(self):
        try:
            self.toast.place_forget()
        except tk.TclError:
            pass

    # --------------------------------------------------------
    # GAME ACTIONS
    # --------------------------------------------------------

    def add_exp(self, amount, source="QUEST"):
        # Snapshot so a failed save can revert the in-memory changes.
        before = json.loads(json.dumps(self.data))
        old_level = self.data["level"]
        self.data["exp"] += amount
        levels_gained = 0

        while self.data["exp"] >= exp_required(self.data["level"]):
            self.data["exp"] -= exp_required(self.data["level"])
            self.data["level"] += 1
            self.data["stat_points"] += 5
            levels_gained += 1

        try:
            save_data(self.data)
        except OSError as exc:
            self.data = before
            messagebox.showerror("Save Error", f"Không thể lưu tiến trình:\n{exc}")
            self.refresh_ui()
            return

        self.refresh_ui()
        if levels_gained:
            self.system_message.configure(
                text=f"LEVEL UP  •  {old_level} → {self.data['level']}",
                text_color=C["gold"]
            )
            self.show_toast(
                "✦ LEVEL UP ✦",
                f"Level {old_level} → {self.data['level']}  |  "
                f"+{levels_gained * 5} attribute points",
                level_up=True
            )
        else:
            self.system_message.configure(
                text=f"+{amount} EXP received from {source}.",
                text_color=C["blue"]
            )
            self.show_toast("SYSTEM MESSAGE", f"+{amount} EXP received.")

    def allocate_point(self, stat):
        if self.data["stat_points"] <= 0:
            self.show_toast("ATTRIBUTE POINTS", "No unspent points available.")
            return

        self.data["stats"][stat] += 1
        self.data["stat_points"] -= 1
        try:
            save_data(self.data)
        except OSError as exc:
            self.data["stats"][stat] -= 1
            self.data["stat_points"] += 1
            messagebox.showerror("Save Error", str(exc))
            return

        self.refresh_ui()
        self.system_message.configure(
            text=f"{stat} increased by 1.", text_color=C["green"]
        )

    def refresh_ui(self):
        level = self.data["level"]
        exp = self.data["exp"]
        needed = exp_required(level)
        rank = get_rank(level)
        points = self.data["stat_points"]

        self.name_label.configure(
            text=self.data.get("player_name", "New Hunter")
        )
        self.level_label.configure(text=f"LEVEL {level}")
        self.rank_badge.configure(text=f"RANK {rank}")
        self.exp_label.configure(text=f"{exp:,} / {needed:,} EXP")
        self.exp_bar.set(max(0.0, min(1.0, exp / needed)))
        self.points_label.configure(text=f"POINTS {points}")

        for key in STAT_NAMES:
            self.stat_labels[key].configure(text=str(self.data["stats"][key]))
            self.stat_buttons[key].configure(
                state="normal" if points > 0 else "disabled"
            )

        self.status_values["HUNTER RANK"].configure(text=rank)
        self.status_values["CHARACTER LEVEL"].configure(text=str(level))
        self.status_values["UNSPENT POINTS"].configure(text=str(points))

    def save_progress(self):
        try:
            save_data(self.data)
            self.system_message.configure(
                text="PROGRESS SAVED", text_color=C["green"]
            )
            self.show_toast("SAVE COMPLETE", "Hunter progress saved locally.")
        except OSError as exc:
            messagebox.showerror("Save Error", str(exc))

    def close_app(self):
        try:
            save_data(self.data)
        except OSError as exc:
            if not messagebox.askyesno(
                "Save Error",
                f"Could not save progress:\n{exc}\n\nClose anyway?"
            ):
                return
        self.destroy()


if __name__ == "__main__":
    app = HunterApp()
    if app.winfo_exists():
        # Store references for responsive layout reflow.
        # These are set after UI construction via widget labels.
        app.mainloop()
