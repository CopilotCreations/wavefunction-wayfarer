"""
Main entry point for Quantum Text Adventure.

This module contains the main game loop and initialization logic.
It handles user input/output and coordinates between the player
interface and the game engine.
"""

import sys
from typing import Optional

from .quantum_adventure import QuantumAdventure
from .player import CommandParser


def get_player_name() -> str:
    """
    Prompt the player for their name.
    
    Returns:
        The player's chosen name, or "Traveler" if none provided.
    """
    print("\n" + "=" * 70)
    print("  Welcome to the Quantum Realm!")
    print("=" * 70)
    
    name = input("\nWhat is your name, Traveler? [Enter for 'Traveler']: ").strip()
    return name if name else "Traveler"


def print_prompt() -> None:
    """Print the input prompt."""
    print("\n" + "-" * 40)
    print(">> ", end="", flush=True)


def game_loop(game: QuantumAdventure) -> None:
    """
    Main game loop.
    
    Continuously prompts for player input, processes commands,
    and displays results until the game ends.
    
    Args:
        game: The QuantumAdventure instance to run.
    """
    # Display welcome message and initial location
    print(game.get_welcome_message())
    print(game.get_current_location_info())
    
    while game.is_running():
        try:
            print_prompt()
            raw_input_str = input()
            
            if not raw_input_str.strip():
                continue
            
            # Parse and process the command
            command = CommandParser.parse(raw_input_str)
            result = game.process_command(command)
            
            print()
            print(result)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted! Exiting game...")
            break
        except EOFError:
            print("\n\nEnd of input. Exiting game...")
            break


def main(player_name: Optional[str] = None) -> int:
    """
    Main entry point for the game.
    
    Args:
        player_name: Optional player name (prompts if not provided).
        
    Returns:
        Exit code (0 for success).
    """
    try:
        # Get player name if not provided
        if player_name is None:
            player_name = get_player_name()
        
        # Initialize the game
        game = QuantumAdventure(player_name=player_name)
        
        # Run the game loop
        game_loop(game)
        
        # Show final stats
        print("\n" + "=" * 70)
        print("  FINAL STATISTICS")
        print("=" * 70)
        print(game.player.get_stats_display())
        print("\nThank you for playing Quantum Text Adventure!")
        print("May your wavefunction remain forever uncollapsed... ⚛")
        print("=" * 70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
