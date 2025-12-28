# Quantum Text Adventure ⚛️

A mind-bending console-based text adventure game where player actions exist in multiple parallel realities until observation collapses the wavefunction.

[![CI](https://github.com/yourusername/wavefunction-wayfarer/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/wavefunction-wayfarer/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)](https://github.com/yourusername/wavefunction-wayfarer)

## Overview

In **Quantum Text Adventure**, you explore a strange world governed by quantum mechanics principles:

- 🌀 **Superposition**: Exist in multiple realities simultaneously
- 🌿 **Branching**: Your choices create new timeline branches
- 👁️ **Observation**: Collapse reality to a single state
- 🎲 **Probability**: Weighted outcomes determine your fate

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd wavefunction-wayfarer

# Run the game
python run.py

# Or with a specific player name
python run.py --name "Quantum Explorer"
```

## Gameplay

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║             ⚛  QUANTUM TEXT ADVENTURE  ⚛                              ║
║                                                                       ║
║         Where Every Choice Creates Parallel Realities                 ║
║                                                                       ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Basic Commands

| Command | Description |
|---------|-------------|
| `look` | Look around |
| `north`, `south`, `east`, `west` | Move in a direction |
| `take [item]` | Pick up an item |
| `inventory` | Check your items |
| `observe` | Collapse the wavefunction |
| `status` | View all parallel realities |
| `help` | See all commands |

### Quantum Mechanics

- **Movement may branch timelines** - Going north might create two realities: one where you moved, one where you hesitated
- **Items trigger collapse** - Using items forces reality to resolve
- **Observation selects fate** - The `observe` command collapses all timelines to one, weighted by probability

## Project Structure

```
wavefunction-wayfarer/
├── run.py                    # Application entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment configuration
├── .gitignore                # Git ignore patterns
│
├── src/                      # Source code
│   ├── main.py               # Game loop
│   ├── quantum_adventure.py  # Core game engine
│   ├── world.py              # World and quantum states
│   ├── player.py             # Player and command parsing
│   └── utils.py              # Utilities (save/load)
│
├── tests/                    # Test suite (91% coverage)
│   ├── test_quantum_adventure.py
│   ├── test_world.py
│   ├── test_player.py
│   ├── test_utils.py
│   └── test_main.py
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # System architecture
│   ├── USAGE.md              # User guide
│   └── SUGGESTIONS.md        # Future improvements
│
└── .github/workflows/        # CI/CD
    └── ci.yml                # GitHub Actions workflow
```

## Installation

### Requirements

- Python 3.8 or higher

### Development Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=src
```

## Game World

Explore 10 unique quantum-themed locations:

- **Quantum Nexus** - The starting point, a vortex of possibilities
- **Probability Forest** - Trees existing in multiple positions
- **Schrödinger's Laboratory** - Site of impossible experiments
- **Entanglement Garden** - Synchronized flower pairs
- **Observer's Peak** - See all realities at once
- And 5 more mysterious locations...

## Save & Load

```
> save myquest       # Save with custom name
> load myquest       # Load saved game
> save               # Quick save (default name)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_quantum_adventure.py -v
```

## Documentation

- [User Guide](docs/USAGE.md) - Complete gameplay instructions
- [Architecture](docs/ARCHITECTURE.md) - Technical design documentation
- [Suggestions](docs/SUGGESTIONS.md) - Future improvement ideas

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

---

*"Reality is merely an illusion, albeit a very persistent one."* - Albert Einstein

May your wavefunction remain forever uncollapsed... ⚛️
