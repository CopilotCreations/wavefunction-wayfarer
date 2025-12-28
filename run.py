#!/usr/bin/env python3
"""
Quantum Text Adventure - Application Entry Point

A mind-bending text adventure game where player actions exist in multiple
parallel realities until observation collapses the wavefunction.

Usage:
    python run.py [--name <player_name>]
    
Options:
    --name, -n    Set the player name (default: prompts user)
    --help, -h    Show this help message
"""

import argparse
import sys

from src.main import main


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Quantum Text Adventure - A quantum mechanics text adventure game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py                    # Start game with name prompt
    python run.py --name Alice       # Start game as Alice
    python run.py -n "Time Lord"     # Start game with a custom name
        """
    )
    
    parser.add_argument(
        "--name", "-n",
        type=str,
        default=None,
        help="Player name (prompts if not provided)"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    sys.exit(main(player_name=args.name))
