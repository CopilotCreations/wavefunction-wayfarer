"""
Utilities module for Quantum Text Adventure.

This module provides helper functions for saving/loading game states,
file I/O operations, and other utility functions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .quantum_adventure import QuantumAdventure

from .world import QuantumState
from .player import Player

# Default save directory
SAVE_DIR = Path("saves")


def ensure_save_directory() -> Path:
    """Ensure the save directory exists.

    Returns:
        Path: Path to the save directory.
    """
    SAVE_DIR.mkdir(exist_ok=True)
    return SAVE_DIR


def get_save_filepath(save_name: str) -> Path:
    """Get the full filepath for a save file.

    Args:
        save_name: Name of the save file (without extension).

    Returns:
        Path: Path to the save file.
    """
    ensure_save_directory()
    return SAVE_DIR / f"{save_name}.json"


def save_game(game: "QuantumAdventure", save_name: str = "quicksave") -> bool:
    """Save the current game state to a file.

    This saves all parallel timelines, player state, and game metadata
    to a JSON file that can be loaded later.

    Args:
        game: The QuantumAdventure instance to save.
        save_name: Name for the save file.

    Returns:
        bool: True if save was successful, False otherwise.
    """
    try:
        filepath = get_save_filepath(save_name)
        
        save_data = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "game": game.to_dict()
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)
        
        return True
    except (IOError, OSError, TypeError) as e:
        print(f"Error saving game: {e}")
        return False


def load_game(save_name: str = "quicksave") -> Optional[Dict[str, Any]]:
    """Load a game state from a file.

    Args:
        save_name: Name of the save file to load.

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing loaded game data,
            or None if load failed.
    """
    try:
        filepath = get_save_filepath(save_name)
        
        if not filepath.exists():
            return None
        
        with open(filepath, "r", encoding="utf-8") as f:
            save_data = json.load(f)
        
        # Reconstruct game objects
        game_data = save_data["game"]
        states = [QuantumState.from_dict(s) for s in game_data["states"]]
        player = Player.from_dict(game_data["player"])
        
        return {
            "states": states,
            "player": player,
            "metadata": {
                "version": save_data.get("version", "unknown"),
                "timestamp": save_data.get("timestamp", "unknown")
            }
        }
    except (IOError, OSError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading game: {e}")
        return None


def list_saves() -> List[Dict[str, str]]:
    """List all available save files.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing save file
            information.
    """
    ensure_save_directory()
    saves = []
    
    for filepath in SAVE_DIR.glob("*.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            saves.append({
                "name": filepath.stem,
                "timestamp": data.get("timestamp", "unknown"),
                "version": data.get("version", "unknown"),
                "timelines": len(data.get("game", {}).get("states", []))
            })
        except (json.JSONDecodeError, IOError):
            # Skip invalid save files
            pass
    
    return sorted(saves, key=lambda x: x["timestamp"], reverse=True)


def delete_save(save_name: str) -> bool:
    """Delete a save file.

    Args:
        save_name: Name of the save file to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        filepath = get_save_filepath(save_name)
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    except (IOError, OSError) as e:
        print(f"Error deleting save: {e}")
        return False


def format_separator(char: str = "═", length: int = 70) -> str:
    """Create a formatted separator line.

    Args:
        char: Character to use for the separator.
        length: Length of the separator.

    Returns:
        str: Formatted separator string.
    """
    return char * length


def format_box(title: str, content: List[str], width: int = 70) -> str:
    """Format content in a box with a title.

    Args:
        title: Title for the box.
        content: List of content lines.
        width: Width of the box.

    Returns:
        str: Formatted box string.
    """
    inner_width = width - 4
    
    result = f"╔{'═' * (width - 2)}╗\n"
    result += f"║ {title:^{inner_width}} ║\n"
    result += f"╠{'═' * (width - 2)}╣\n"
    
    for line in content:
        if len(line) > inner_width:
            line = line[:inner_width - 3] + "..."
        result += f"║ {line:<{inner_width}} ║\n"
    
    result += f"╚{'═' * (width - 2)}╝"
    
    return result


def clear_screen() -> None:
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def weighted_random_choice(choices: List[Any], weights: List[float]) -> Any:
    """Make a weighted random selection from a list.

    Args:
        choices: List of items to choose from.
        weights: Corresponding weights for each choice.

    Returns:
        Any: The selected item.

    Raises:
        ValueError: If choices and weights have different lengths.
    """
    import random
    
    if len(choices) != len(weights):
        raise ValueError("Choices and weights must have the same length")
    
    total = sum(weights)
    r = random.random() * total
    
    cumulative = 0
    for choice, weight in zip(choices, weights):
        cumulative += weight
        if r <= cumulative:
            return choice
    
    return choices[-1]  # Fallback to last choice


def calculate_probability_distribution(
    states: List[QuantumState]
) -> Dict[str, float]:
    """Calculate the probability distribution across states.

    Args:
        states: List of QuantumState instances.

    Returns:
        Dict[str, float]: Dictionary mapping state descriptions to probabilities.
    """
    total_prob = sum(s.probability for s in states)
    
    distribution = {}
    for state in states:
        key = f"Timeline {state.timeline_id}: {state.location}"
        distribution[key] = state.probability / total_prob
    
    return distribution


def format_probability_bar(probability: float, width: int = 20) -> str:
    """Create a visual probability bar.

    Args:
        probability: Probability value between 0 and 1.
        width: Width of the bar in characters.

    Returns:
        str: Formatted probability bar string.
    """
    filled = int(probability * width)
    empty = width - filled
    
    bar = "█" * filled + "░" * empty
    percentage = probability * 100
    
    return f"[{bar}] {percentage:.1f}%"
