"""
Player module for Quantum Text Adventure.

This module handles player input parsing, command processing, and inventory
management. It provides a clean interface between user input and game actions.
"""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any


class CommandType(Enum):
    """Enumeration of all valid command types."""
    MOVE = auto()        # Movement commands (go, move, walk)
    LOOK = auto()        # Look at current location or objects
    INVENTORY = auto()   # Check inventory
    TAKE = auto()        # Pick up an item
    DROP = auto()        # Drop an item
    USE = auto()         # Use an item
    OBSERVE = auto()     # Collapse the wavefunction
    STATUS = auto()      # Show all superposition states
    SAVE = auto()        # Save game/timelines
    LOAD = auto()        # Load game/timelines
    HELP = auto()        # Show help
    QUIT = auto()        # Exit game
    ATTACK = auto()      # Attack an enemy
    TALK = auto()        # Talk/interact
    HISTORY = auto()     # Show story log
    UNKNOWN = auto()     # Unrecognized command


@dataclass
class ParsedCommand:
    """
    Represents a parsed player command.
    
    Attributes:
        command_type: The type of command.
        arguments: List of arguments/parameters for the command.
        raw_input: The original input string.
    """
    command_type: CommandType
    arguments: List[str]
    raw_input: str
    
    def has_arguments(self) -> bool:
        """Check if command has any arguments.

        Returns:
            bool: True if the command has one or more arguments, False otherwise.
        """
        return len(self.arguments) > 0
    
    def get_first_arg(self) -> Optional[str]:
        """Get the first argument if present.

        Returns:
            Optional[str]: The first argument string, or None if no arguments exist.
        """
        return self.arguments[0] if self.arguments else None
    
    def get_all_args_as_string(self) -> str:
        """Join all arguments into a single string.

        Returns:
            str: All arguments joined by spaces, or empty string if no arguments.
        """
        return " ".join(self.arguments)


class CommandParser:
    """
    Parses player input into structured commands.
    
    The parser supports various command formats and aliases to make
    the game more accessible. It normalizes input and extracts
    command types and arguments.
    """
    
    # Command aliases - map various inputs to command types
    COMMAND_ALIASES: Dict[str, CommandType] = {
        # Movement
        "go": CommandType.MOVE,
        "move": CommandType.MOVE,
        "walk": CommandType.MOVE,
        "run": CommandType.MOVE,
        "travel": CommandType.MOVE,
        "north": CommandType.MOVE,
        "south": CommandType.MOVE,
        "east": CommandType.MOVE,
        "west": CommandType.MOVE,
        "up": CommandType.MOVE,
        "down": CommandType.MOVE,
        "n": CommandType.MOVE,
        "s": CommandType.MOVE,
        "e": CommandType.MOVE,
        "w": CommandType.MOVE,
        "u": CommandType.MOVE,
        "d": CommandType.MOVE,
        
        # Looking
        "look": CommandType.LOOK,
        "l": CommandType.LOOK,
        "examine": CommandType.LOOK,
        "inspect": CommandType.LOOK,
        "describe": CommandType.LOOK,
        
        # Inventory
        "inventory": CommandType.INVENTORY,
        "inv": CommandType.INVENTORY,
        "i": CommandType.INVENTORY,
        "items": CommandType.INVENTORY,
        "bag": CommandType.INVENTORY,
        
        # Taking items
        "take": CommandType.TAKE,
        "get": CommandType.TAKE,
        "grab": CommandType.TAKE,
        "pick": CommandType.TAKE,
        "pickup": CommandType.TAKE,
        "collect": CommandType.TAKE,
        
        # Dropping items
        "drop": CommandType.DROP,
        "discard": CommandType.DROP,
        "throw": CommandType.DROP,
        "leave": CommandType.DROP,
        
        # Using items
        "use": CommandType.USE,
        "activate": CommandType.USE,
        "apply": CommandType.USE,
        "consume": CommandType.USE,
        
        # Quantum commands
        "observe": CommandType.OBSERVE,
        "collapse": CommandType.OBSERVE,
        "measure": CommandType.OBSERVE,
        "status": CommandType.STATUS,
        "superposition": CommandType.STATUS,
        "timelines": CommandType.STATUS,
        "worlds": CommandType.STATUS,
        
        # Save/Load
        "save": CommandType.SAVE,
        "load": CommandType.LOAD,
        "restore": CommandType.LOAD,
        
        # Combat
        "attack": CommandType.ATTACK,
        "fight": CommandType.ATTACK,
        "hit": CommandType.ATTACK,
        "strike": CommandType.ATTACK,
        
        # Interaction
        "talk": CommandType.TALK,
        "speak": CommandType.TALK,
        "interact": CommandType.TALK,
        
        # History
        "history": CommandType.HISTORY,
        "log": CommandType.HISTORY,
        "events": CommandType.HISTORY,
        
        # Help
        "help": CommandType.HELP,
        "?": CommandType.HELP,
        "commands": CommandType.HELP,
        
        # Quit
        "quit": CommandType.QUIT,
        "exit": CommandType.QUIT,
        "q": CommandType.QUIT,
        "bye": CommandType.QUIT
    }
    
    # Direction expansions for shorthand
    DIRECTION_EXPANSIONS: Dict[str, str] = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west",
        "u": "up",
        "d": "down"
    }
    
    @classmethod
    def parse(cls, raw_input: str) -> ParsedCommand:
        """
        Parse raw player input into a structured command.
        
        Args:
            raw_input: The raw input string from the player.
            
        Returns:
            A ParsedCommand object containing the parsed command.
        """
        # Normalize input: lowercase and strip whitespace
        normalized = raw_input.lower().strip()
        
        if not normalized:
            return ParsedCommand(CommandType.UNKNOWN, [], raw_input)
        
        # Split into words
        words = normalized.split()
        first_word = words[0]
        arguments = words[1:] if len(words) > 1 else []
        
        # Check if first word is a command or alias
        command_type = cls.COMMAND_ALIASES.get(first_word, CommandType.UNKNOWN)
        
        # Handle directional shortcuts (n, s, e, w become move north, etc.)
        if first_word in cls.DIRECTION_EXPANSIONS:
            direction = cls.DIRECTION_EXPANSIONS[first_word]
            return ParsedCommand(CommandType.MOVE, [direction], raw_input)
        
        # Handle bare directions (north, south, etc.)
        if first_word in ["north", "south", "east", "west", "up", "down"]:
            return ParsedCommand(CommandType.MOVE, [first_word], raw_input)
        
        # Handle "go north" style commands
        if command_type == CommandType.MOVE and arguments:
            # Expand direction shorthand in arguments
            expanded_args = [
                cls.DIRECTION_EXPANSIONS.get(arg, arg) 
                for arg in arguments
            ]
            return ParsedCommand(CommandType.MOVE, expanded_args, raw_input)
        
        return ParsedCommand(command_type, arguments, raw_input)
    
    @classmethod
    def get_help_text(cls) -> str:
        """Return formatted help text showing all available commands.

        Returns:
            str: A formatted help string with all available commands and their usage.
        """
        help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                     QUANTUM TEXT ADVENTURE - HELP                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  MOVEMENT:                                                            ║
║    go/move/walk [direction]  - Move in a direction                    ║
║    north/south/east/west     - Move in that direction (or n/s/e/w)    ║
║    up/down                   - Move up or down (or u/d)               ║
║                                                                       ║
║  EXPLORATION:                                                         ║
║    look/examine [object]     - Look around or examine something       ║
║    inventory/inv/i           - Check your inventory                   ║
║    take/get [item]           - Pick up an item                        ║
║    drop [item]               - Drop an item                           ║
║    use [item]                - Use an item (may collapse timelines!)  ║
║                                                                       ║
║  QUANTUM COMMANDS:                                                    ║
║    observe/collapse          - Collapse the wavefunction to one state ║
║    status/timelines          - View all superposition states          ║
║    history/log               - View your story log                    ║
║                                                                       ║
║  COMBAT:                                                              ║
║    attack/fight [target]     - Attack an enemy                        ║
║                                                                       ║
║  SYSTEM:                                                              ║
║    save [name]               - Save current timelines                 ║
║    load [name]               - Load saved timelines                   ║
║    help/?                    - Show this help message                 ║
║    quit/exit                 - Exit the game                          ║
║                                                                       ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        return help_text


class Player:
    """
    Represents the player and manages player-related state.
    
    The Player class serves as a high-level interface for player actions
    and coordinates between the command parser and the game state.
    
    Attributes:
        name: The player's name.
        stats: Dictionary of player statistics.
    """
    
    def __init__(self, name: str = "Traveler"):
        """
        Initialize a new Player.
        
        Args:
            name: The player's name (default: "Traveler").
        """
        self.name = name
        self.stats: Dict[str, Any] = {
            "observations": 0,       # Number of times wavefunction was collapsed
            "timelines_created": 0,  # Number of branching events
            "items_collected": 0,    # Total items ever collected
            "enemies_defeated": 0,   # Total enemies defeated
            "moves": 0               # Total moves made
        }
    
    def record_observation(self) -> None:
        """Record that the player observed/collapsed the wavefunction.

        Increments the observations counter in player stats.
        """
        self.stats["observations"] += 1
    
    def record_branch(self) -> None:
        """Record that a new timeline branch was created.

        Increments the timelines_created counter in player stats.
        """
        self.stats["timelines_created"] += 1
    
    def record_item_collected(self) -> None:
        """Record that an item was collected.

        Increments the items_collected counter in player stats.
        """
        self.stats["items_collected"] += 1
    
    def record_enemy_defeated(self) -> None:
        """Record that an enemy was defeated.

        Increments the enemies_defeated counter in player stats.
        """
        self.stats["enemies_defeated"] += 1
    
    def record_move(self) -> None:
        """Record that a move was made.

        Increments the moves counter in player stats.
        """
        self.stats["moves"] += 1
    
    def get_stats_display(self) -> str:
        """Return a formatted string of player statistics.

        Returns:
            str: A formatted box-style display of all player stats.
        """
        return (
            f"╔═══════════════════════════════════╗\n"
            f"║ Player: {self.name:25} ║\n"
            f"╠═══════════════════════════════════╣\n"
            f"║ Observations: {self.stats['observations']:18} ║\n"
            f"║ Timelines Created: {self.stats['timelines_created']:13} ║\n"
            f"║ Items Collected: {self.stats['items_collected']:15} ║\n"
            f"║ Enemies Defeated: {self.stats['enemies_defeated']:14} ║\n"
            f"║ Total Moves: {self.stats['moves']:19} ║\n"
            f"╚═══════════════════════════════════╝"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary containing player name and stats.
        """
        return {
            "name": self.name,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        """Create a Player from a dictionary.

        Args:
            data: Dictionary containing player data with 'name' and 'stats' keys.

        Returns:
            Player: A new Player instance with the restored state.
        """
        player = cls(name=data["name"])
        player.stats = data["stats"]
        return player
