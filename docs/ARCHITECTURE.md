# Quantum Text Adventure - Architecture

## Overview

Quantum Text Adventure is a console-based text adventure game built in Python that implements quantum mechanics concepts as core gameplay mechanics. The game allows players to exist in multiple parallel realities simultaneously, with their actions affecting all timelines until an observation event collapses the wavefunction to a single state.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Application Layer                              │
├─────────────────────────────────────────────────────────────────────────┤
│  run.py              Entry point, CLI argument parsing                   │
│  src/main.py         Game loop, user I/O management                      │
├─────────────────────────────────────────────────────────────────────────┤
│                            Game Logic Layer                              │
├─────────────────────────────────────────────────────────────────────────┤
│  src/quantum_adventure.py   Core game engine, command processing         │
│                             Manages quantum superposition and collapse    │
├─────────────────────────────────────────────────────────────────────────┤
│                             Domain Layer                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  src/world.py        QuantumState, Location, WorldBuilder                │
│  src/player.py       Player, CommandParser, ParsedCommand                │
├─────────────────────────────────────────────────────────────────────────┤
│                           Infrastructure Layer                           │
├─────────────────────────────────────────────────────────────────────────┤
│  src/utils.py        Save/Load, file I/O, formatting utilities           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### run.py
The application entry point that handles command-line arguments and bootstraps the game.

**Responsibilities:**
- Parse command-line arguments (player name, etc.)
- Initialize and start the game
- Handle top-level exceptions

### src/main.py
Manages the main game loop and user interaction.

**Responsibilities:**
- Prompt user for input
- Coordinate between user I/O and game engine
- Display game output
- Handle graceful shutdown

### src/quantum_adventure.py
The core game engine implementing quantum mechanics gameplay.

**Key Class: `QuantumAdventure`**

**Responsibilities:**
- Maintain multiple `QuantumState` instances in superposition
- Process player commands and route to appropriate handlers
- Implement probabilistic branching on actions
- Perform wavefunction collapse when observed
- Coordinate combat, inventory, and movement

**Quantum Mechanics Implementation:**
- **Superposition**: Multiple game states exist simultaneously
- **Branching**: Movement and actions probabilistically create new timeline branches
- **Collapse**: Observation or item use collapses all states to one
- **Probability Weighting**: States have probability weights affecting collapse outcome

### src/world.py
Defines the game world, locations, and quantum state representation.

**Key Classes:**

#### `QuantumState`
Represents a single possible reality state.

**Attributes:**
- `location`: Current location name
- `inventory`: Set of items the player carries
- `story_log`: List of events in this timeline
- `world_items`: Items present at each location
- `defeated_enemies`: Set of defeated enemies
- `probability`: Weight for wavefunction collapse
- `timeline_id`: Unique identifier for this branch

**Methods:**
- `branch()`: Deep copy state for timeline branching
- `add_item()`, `remove_item()`: Inventory management
- `move_to()`: Location changes
- `to_dict()`, `from_dict()`: Serialization

#### `Location`
Represents a game location.

**Attributes:**
- `name`: Location name
- `description`: Narrative description
- `connections`: Dict mapping directions to destinations
- `items`: Possible items at this location
- `enemies`: Possible enemies at this location

#### `WorldBuilder`
Factory class for creating the game world.

**Responsibilities:**
- Define all game locations and their connections
- Provide random item/enemy generation for probabilistic encounters

### src/player.py
Handles player representation and command parsing.

**Key Classes:**

#### `CommandParser`
Parses raw text input into structured commands.

**Features:**
- Supports multiple command aliases
- Direction shortcuts (n, s, e, w, u, d)
- Case-insensitive parsing
- Returns `ParsedCommand` objects

#### `ParsedCommand`
Structured representation of a parsed command.

**Attributes:**
- `command_type`: Enum value (MOVE, LOOK, TAKE, etc.)
- `arguments`: List of command arguments
- `raw_input`: Original input string

#### `Player`
Represents the player and tracks statistics.

**Attributes:**
- `name`: Player's name
- `stats`: Dictionary of gameplay statistics

### src/utils.py
Provides utility functions for file I/O and formatting.

**Key Functions:**
- `save_game()`: Serialize and save game state to JSON
- `load_game()`: Load and deserialize game state from JSON
- `list_saves()`: List available save files
- `delete_save()`: Remove a save file
- `format_box()`, `format_separator()`: Text formatting helpers
- `weighted_random_choice()`: Probability-weighted selection
- `calculate_probability_distribution()`: Compute state probabilities

## Data Flow

### Command Processing Flow

```
User Input
    │
    ▼
CommandParser.parse()
    │
    ▼
ParsedCommand
    │
    ▼
QuantumAdventure.process_command()
    │
    ├──► Movement Handler ──► May branch timelines
    ├──► Look Handler ──► Display information
    ├──► Take/Drop Handler ──► Modify inventory
    ├──► Use Handler ──► Triggers collapse
    ├──► Observe Handler ──► Triggers collapse
    ├──► Status Handler ──► Display all states
    └──► Other Handlers
    │
    ▼
Result String
    │
    ▼
Display to User
```

### Wavefunction Collapse Flow

```
Multiple QuantumStates in superposition
    │
    ▼
Collapse triggered (observe/use item)
    │
    ▼
Calculate probability weights
    │
    ▼
Weighted random selection
    │
    ▼
Single QuantumState remains
    │
    ▼
Clean up orphaned state references
```

### Save/Load Flow

```
Save:
QuantumAdventure
    │
    ▼
game.to_dict()
    │
    ▼
Add metadata (version, timestamp)
    │
    ▼
JSON serialize
    │
    ▼
Write to saves/{name}.json

Load:
Read from saves/{name}.json
    │
    ▼
JSON deserialize
    │
    ▼
QuantumState.from_dict() for each state
    │
    ▼
Player.from_dict()
    │
    ▼
Reconstruct QuantumAdventure
```

## Key Design Decisions

### 1. State Immutability for Branching
The `QuantumState.branch()` method creates deep copies to ensure timeline independence. Modifying one branch never affects another.

### 2. Probability-Weighted Collapse
States carry probability weights that affect the likelihood of being selected during collapse. This enables weighted outcomes based on player actions.

### 3. Separation of Concerns
- **World** module: Pure data structures for game state
- **Player** module: Input parsing and player representation
- **QuantumAdventure**: Game logic and coordination
- **Utils**: Cross-cutting concerns like persistence

### 4. Extensible Command System
Commands are parsed into structured objects and dispatched via a handler dictionary. Adding new commands requires:
1. Add to `CommandType` enum
2. Add aliases to `COMMAND_ALIASES`
3. Implement handler method
4. Register in handler dictionary

### 5. Text-Based UI with Box Drawing
ASCII box-drawing characters create a clean, readable console interface without external dependencies.

## File Structure

```
wavefunction-wayfarer/
├── run.py                    # CLI entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment config template
├── .gitignore                # Git ignore patterns
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── main.py               # Game loop
│   ├── quantum_adventure.py  # Core game engine
│   ├── world.py              # World and state
│   ├── player.py             # Player and commands
│   └── utils.py              # Utilities
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_world.py
│   ├── test_player.py
│   ├── test_quantum_adventure.py
│   ├── test_utils.py
│   └── test_main.py
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # This file
│   ├── USAGE.md              # User guide
│   └── SUGGESTIONS.md        # Future improvements
│
├── saves/                    # Game saves (created at runtime)
│
└── .github/workflows/        # CI/CD
    └── ci.yml
```

## Dependencies

The project uses only Python standard library modules:
- `copy`: Deep copying for state branching
- `random`: Probabilistic mechanics
- `json`: Save/load serialization
- `dataclasses`: Location and command structures
- `enum`: Command type enumeration
- `pathlib`: File path handling
- `typing`: Type hints

Development dependencies (optional):
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking utilities
- `mypy`: Static type checking
- `black`, `isort`: Code formatting
- `flake8`: Linting

## Testing Strategy

Tests are organized by module:
- `test_world.py`: QuantumState, Location, WorldBuilder
- `test_player.py`: CommandParser, Player
- `test_quantum_adventure.py`: Game mechanics
- `test_utils.py`: Save/load, utilities
- `test_main.py`: Entry point and game loop

Coverage target: 75%+

## Performance Considerations

1. **State Copying**: Deep copying is O(n) where n is state size. Limited to 4 parallel states to prevent exponential growth.

2. **Command Parsing**: O(1) dictionary lookup for command type identification.

3. **Collapse Selection**: O(n) where n is number of states in superposition.

4. **Save/Load**: File I/O is the bottleneck; state serialization is lightweight.
