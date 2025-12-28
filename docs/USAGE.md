# Quantum Text Adventure - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Game Concepts](#game-concepts)
5. [Commands Reference](#commands-reference)
6. [Gameplay Tips](#gameplay-tips)
7. [Save and Load](#save-and-load)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

**Quantum Text Adventure** is a mind-bending console-based text adventure game where your actions exist in multiple parallel realities simultaneously. The game implements quantum mechanics concepts as core gameplay mechanics:

- **Superposition**: Your character exists in multiple states at once
- **Observation**: Looking at reality collapses it to a single state
- **Branching**: Your choices create new timeline branches
- **Probability**: Each timeline has a probability of becoming "real"

Experience the bizarre world of quantum mechanics as you explore the Quantum Nexus and its surrounding realms!

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the repository**

```bash
git clone <repository-url>
cd wavefunction-wayfarer
```

2. **Install dependencies** (optional, for development/testing)

```bash
pip install -r requirements.txt
```

3. **Run the game**

```bash
python run.py
```

---

## Quick Start

1. Start the game:
   ```bash
   python run.py
   ```

2. Enter your name when prompted (or press Enter for "Traveler")

3. You start at the **Quantum Nexus**. Type `look` to see your surroundings.

4. Move around with directions: `north`, `south`, `east`, `west` (or `n`, `s`, `e`, `w`)

5. Your actions may create parallel timelines! Use `status` to see all realities.

6. Type `observe` to collapse the wavefunction and fix reality to one state.

7. Type `help` at any time to see all available commands.

---

## Game Concepts

### Quantum Superposition

In the quantum world, you can exist in multiple states simultaneously. When you take actions (especially movement), there's a chance your reality will "branch" into multiple parallel timelines.

```
╔══════════════════════════════════════════════════════════════════════╗
║        ⚛ QUANTUM SUPERPOSITION DETECTED ⚛                           ║
╠══════════════════════════════════════════════════════════════════════╣
║ You exist in 2 parallel realities simultaneously:                    ║
║   • Probability Forest: 50.0% probability                           ║
║   • Quantum Nexus: 50.0% probability                                 ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Wavefunction Collapse

When you **observe** (use the `observe` command) or **use an item**, reality collapses to a single state. The timeline that survives is chosen based on probability weights.

### Timeline Branching

Certain actions cause your reality to split:
- **Movement**: There's a chance you'll both move AND stay
- **Combat**: Outcomes may differ across timelines
- **Item discovery**: Items appear probabilistically

### Probability Weights

Each timeline has a probability weight. When collapse occurs:
- Higher probability timelines are more likely to survive
- The chosen timeline becomes your new reality
- All other timelines are lost forever

---

## Commands Reference

### Movement

| Command | Description |
|---------|-------------|
| `north` or `n` | Move north |
| `south` or `s` | Move south |
| `east` or `e` | Move east |
| `west` or `w` | Move west |
| `up` or `u` | Move up |
| `down` or `d` | Move down |
| `go [direction]` | Move in a direction |

### Exploration

| Command | Description |
|---------|-------------|
| `look` or `l` | Look at your current location |
| `look [object]` | Examine a specific object |
| `examine [object]` | Same as look |

### Inventory

| Command | Description |
|---------|-------------|
| `inventory` or `i` | View your inventory |
| `take [item]` | Pick up an item |
| `get [item]` | Same as take |
| `drop [item]` | Drop an item |
| `use [item]` | Use an item (triggers collapse!) |

### Quantum Commands

| Command | Description |
|---------|-------------|
| `observe` | Collapse the wavefunction to one reality |
| `status` | View all parallel realities |
| `history` | View your story log |

### Combat

| Command | Description |
|---------|-------------|
| `attack [enemy]` | Attack an enemy |
| `fight [enemy]` | Same as attack |

### System

| Command | Description |
|---------|-------------|
| `save [name]` | Save the game (default: quicksave) |
| `load [name]` | Load a saved game |
| `help` or `?` | Show command help |
| `quit` or `exit` | Exit the game |

---

## Gameplay Tips

### 1. Use Status Frequently

The `status` command shows all your parallel realities. This helps you understand:
- Where you exist in each timeline
- Your inventory in each timeline
- The probability of each timeline

### 2. Strategic Observation

Don't observe too early! Having multiple timelines can be beneficial:
- Different items in different timelines
- Different paths explored
- More options for outcomes

But also don't wait too long - too many timelines can be confusing!

### 3. Items Trigger Collapse

Using items causes immediate wavefunction collapse. Consider:
- Which timeline has the best position?
- What items do you want to keep?
- Is now the right time to collapse?

### 4. Combat is Probabilistic

When you attack enemies:
- You have a 60% chance of success
- Different timelines may have different outcomes
- Defeated enemies stay defeated in their timeline

### 5. Explore Before Collapsing

Movement might branch your reality. Use this to your advantage:
- Explore multiple directions simultaneously
- Find the best path before committing
- Observe when you've found something good

### 6. Save Often

Use the `save` command to preserve your progress:
- Saves include all parallel timelines
- You can have multiple save files
- Load with `load [name]`

---

## Save and Load

### Saving Your Game

```
> save myadventure
Game saved as 'myadventure' with 2 timeline(s).
```

If you don't specify a name, it saves as "quicksave":
```
> save
Game saved as 'quicksave' with 1 timeline(s).
```

### Loading Your Game

```
> load myadventure
Game loaded from 'myadventure' with 2 timeline(s).
```

### Save File Location

Saves are stored in the `saves/` directory as JSON files.

---

## Troubleshooting

### Game Won't Start

1. Ensure Python 3.8+ is installed:
   ```bash
   python --version
   ```

2. Run from the correct directory:
   ```bash
   cd wavefunction-wayfarer
   python run.py
   ```

### Commands Not Recognized

- Commands are case-insensitive
- Make sure you're spelling commands correctly
- Type `help` to see all valid commands

### Save/Load Errors

- Check that the `saves/` directory exists
- Ensure you have write permissions
- Verify the save name is correct

### Display Issues

The game uses Unicode box-drawing characters. If they display incorrectly:
- Use a terminal with Unicode support
- Try a different font (e.g., Consolas, Courier New)
- On Windows, use Windows Terminal or PowerShell

### Too Many Timelines

The game limits parallel timelines to 4 to prevent confusion. If you're stuck:
- Use `observe` to collapse to one reality
- Use `status` to see where you are
- Consider which timeline is best before observing

---

## The World

### Locations

The game features 10 unique locations:

1. **Quantum Nexus** - The starting point, a swirling vortex of possibilities
2. **Probability Forest** - Trees existing in multiple positions
3. **Collapsed Caverns** - Ancient caves fixed in a single state
4. **Schrödinger's Laboratory** - Site of impossible experiments
5. **Entanglement Garden** - Flowers blooming in perfect synchronization
6. **Observer's Peak** - See all possible realities at once
7. **Uncertainty Glade** - Where nothing is certain
8. **Eigenstate Depths** - Chambers frozen in fixed states
9. **Observation Deck** - Collapse any superposition from here
10. **Superposition Springs** - Waters both frozen and boiling

### Items

Items appear probabilistically at locations. Some notable items:
- **Quantum Compass** - Navigate the quantum realm
- **Probability Seed** - Plant possibilities
- **Collapsed Crystal** - Stabilized quantum energy
- **Uncertainty Potion** - Unknown effects...
- **Observer's Badge** - Authority to collapse reality

### Enemies

Enemies may appear at locations with a 25% chance:
- **Wandering Paradox** - A logical contradiction made manifest
- **Shadow Self** - Your alternate timeline counterpart
- **Cave Specter** - Ghost of collapsed possibilities
- **Lab Assistant Ghost** - Former researcher, now ethereal
- **Peak Guardian** - Protector of the observation point

---

## Credits

**Quantum Text Adventure** - A game exploring quantum mechanics through interactive fiction.

May your wavefunction remain forever uncollapsed... ⚛
