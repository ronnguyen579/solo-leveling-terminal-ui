
<div align="center">

# 🌑 SOLO LEVELING: TERMINAL UI

### `ARISE, HUNTER.`

A beginner-friendly Python GUI inspired by the System from Solo Leveling.

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:080B18,50:312e81,100:9B6DFF&height=180&section=header&text=HUNTER%20SYSTEM&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=40" width="100%" />

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-9B6DFF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-MVP-72E6B1?style=for-the-badge)

*"There is no limit to how much stronger you can become."*

— Sung Jin-Woo

</div>

---

## ⚔️ About the Project

**Solo Leveling Terminal UI** is a beginner-friendly desktop application built with Python and Tkinter.

Inspired by the Hunter System from *Solo Leveling*, this project transforms basic programming concepts into a simple RPG-style interface where players can complete quests, earn EXP, level up, and improve their attributes.

This is my first personal Python GUI project as a second-year Information Technology student at **HCMUS**.

## ✨ Features

- 🧙 **Hunter Profile** — View your name, Hunter Rank, and Level.
- 📊 **Character Stats** — Track HP, MP, STR, AGI, and INT.
- ⚔️ **Daily Quests** — Complete quests to earn EXP.
- 🔮 **Level-Up System** — Gain levels and improve attributes.
- 💾 **Save System** — Save and load progress using JSON.
- 🌑 **Dark UI** — A dark interface with purple and blue accents inspired by Solo Leveling.

## 🛠️ Built With

- **Python 3** — Core programming language.
- **Tkinter** — Desktop GUI framework.
- **JSON** — Local data persistence.
- **Git & GitHub** — Version control and project hosting.

## 🚀 Getting Started

### Prerequisites

- Python 3 installed on your computer.
- Git (optional, for cloning the repository).

No third-party Python packages are required for the MVP.

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/solo-leveling-terminal-ui.git
```

### 2. Navigate to the Project Folder

```bash
cd solo-leveling-terminal-ui
```

### 3. Run the Application

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

## 📁 Project Structure

```text
solo-leveling-terminal-ui/
├── main.py
├── hunter_data.json
├── README.md
└── .gitignore
```

- `main.py` — Main application, GUI, quest logic, and leveling system.
- `hunter_data.json` — Automatically generated file containing saved Hunter progress.
- `README.md` — Project documentation.
- `.gitignore` — Excludes local data and unnecessary files from Git.

> **Note:** `hunter_data.json` is generated automatically when the application saves its progress for the first time.

## 🎮 How to Use

1. Launch the application.
2. View your Hunter profile and current attributes.
3. Select a Daily Quest.
4. Click **COMPLETE QUEST** to earn EXP.
5. Earn enough EXP to level up and increase your attributes.
6. Click **SAVE PROGRESS** to save your data.
7. Use **RESET DAILY QUESTS** to make the quests available again.

Your level, EXP, attributes, and completed quest status are saved locally.

## 📈 Leveling System

The required EXP increases with each level.

| Hunter Level | Required EXP |
|:---:|---:|
| Level 1 | 100 EXP |
| Level 2 | 200 EXP |
| Level 3 | 300 EXP |
| Level 4 | 400 EXP |

Each level gained increases the following attributes:

- STR +1
- AGI +1
- INT +1

Hunter Rank is determined by level:

| Rank | Required Level |
|:---:|---:|
| E-Rank | Level 1–4 |
| D-Rank | Level 5–9 |
| C-Rank | Level 10–19 |
| B-Rank | Level 20–29 |
| A-Rank | Level 30–49 |
| S-Rank | Level 50+ |

## 🎯 Learning Goals

Through this project, I am learning and practicing:

- Python variables, functions, loops, and conditional statements.
- Object-oriented programming with classes and objects.
- GUI development with Tkinter.
- File handling and JSON serialization.
- Basic game mechanics and state management.
- Git and GitHub workflows.

## 🗺️ Roadmap

- [x] Create the initial GUI.
- [x] Display Hunter attributes and status.
- [x] Implement Daily Quests and EXP rewards.
- [x] Add the level-up system.
- [x] Save and load progress using JSON.
- [ ] Automatically reset Daily Quests each day.
- [ ] Add skill points and equipment.
- [ ] Implement Dungeon exploration and monster battles.
- [ ] Improve animations and visual effects.
- [ ] Package the application as a Windows executable.

## 🔮 Future Improvements

Planned features for future versions:

- Shadow Army management inspired by Sung Jin-Woo.
- Inventory and equipment systems.
- Skill trees and ability upgrades.
- Dungeon battles and boss encounters.
- Sound effects and enhanced UI animations.
- A more immersive Solo Leveling-inspired interface.

## 👤 About Me

Hi! I'm **Ron Nguyễn**, a second-year Information Technology student at **HCMUS**.

I'm currently a beginner in programming, learning C++ and Python one step at a time.

Outside of coding, I enjoy gaming, listening to music, watching anime, and reading manga.

I'm building this project to improve my programming skills while combining my interests in software development and Solo Leveling.

## 🌐 Connect With Me

- GitHub: [@ronnguyen579](https://github.com/ronnguyen579)

---

<div align="center">

### 🌑 `KEEP GRINDING. KEEP LEVELING UP.`

*Made with Python and a little Shadow Monarch energy.*

**ARISE, HUNTER.**

</div>
