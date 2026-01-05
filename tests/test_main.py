"""
Tests for the main module.

This module tests the entry point and game loop functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from src.main import get_player_name, print_prompt, game_loop, main


class TestGetPlayerName:
    """Tests for get_player_name function."""
    
    def test_default_name_on_empty_input(self):
        """Test that empty input returns default name.

        Verifies that when the user provides no input, the function
        returns the default name 'Traveler'.
        """
        with patch('builtins.input', return_value=""):
            result = get_player_name()
            assert result == "Traveler"
    
    def test_custom_name(self):
        """Test custom name input.

        Verifies that a user-provided name is returned correctly.
        """
        with patch('builtins.input', return_value="Alice"):
            result = get_player_name()
            assert result == "Alice"
    
    def test_whitespace_name_returns_default(self):
        """Test that whitespace-only input returns default.

        Verifies that when the user provides only whitespace, the function
        returns the default name 'Traveler'.
        """
        with patch('builtins.input', return_value="   "):
            result = get_player_name()
            assert result == "Traveler"


class TestPrintPrompt:
    """Tests for print_prompt function."""
    
    def test_prompt_prints(self, capsys):
        """Test that prompt prints something.

        Args:
            capsys: Pytest fixture for capturing stdout/stderr.

        Verifies that the prompt output contains the expected '>>' symbol.
        """
        print_prompt()
        captured = capsys.readouterr()
        assert ">>" in captured.out


class TestMain:
    """Tests for main entry point."""
    
    def test_main_with_name(self):
        """Test main with provided name.

        Verifies that when a player name is provided, main creates
        a game instance, calls game_loop, and returns 0.
        """
        with patch('src.main.game_loop') as mock_loop:
            result = main(player_name="TestPlayer")
            # Should create game and call game_loop
            mock_loop.assert_called_once()
            assert result == 0
    
    def test_main_prompts_for_name(self):
        """Test main prompts for name if not provided.

        Verifies that when no player name is provided, main calls
        get_player_name to prompt the user.
        """
        with patch('src.main.get_player_name', return_value="Prompted") as mock_name:
            with patch('src.main.game_loop'):
                result = main()
                mock_name.assert_called_once()
                assert result == 0


class TestGameLoop:
    """Tests for game_loop function."""
    
    def test_game_loop_handles_quit(self):
        """Test game loop exits on quit command.

        Verifies that when the user enters 'quit', the game loop
        exits and the game is no longer running.
        """
        from src.quantum_adventure import QuantumAdventure
        
        game = QuantumAdventure()
        
        with patch('builtins.input', return_value="quit"):
            game_loop(game)
            assert game.is_running() is False
    
    def test_game_loop_handles_keyboard_interrupt(self):
        """Test game loop handles Ctrl+C gracefully.

        Verifies that when a KeyboardInterrupt is raised (user presses
        Ctrl+C), the game loop exits without raising an exception.
        """
        from src.quantum_adventure import QuantumAdventure
        
        game = QuantumAdventure()
        
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            # Should not raise, should exit gracefully
            game_loop(game)
    
    def test_game_loop_handles_eof(self):
        """Test game loop handles EOF gracefully.

        Verifies that when an EOFError is raised (end of input stream),
        the game loop exits without raising an exception.
        """
        from src.quantum_adventure import QuantumAdventure
        
        game = QuantumAdventure()
        
        with patch('builtins.input', side_effect=EOFError):
            # Should not raise, should exit gracefully
            game_loop(game)
    
    def test_game_loop_ignores_empty_input(self):
        """Test game loop ignores empty input.

        Verifies that when the user provides empty input, the game loop
        continues and processes subsequent commands.
        """
        from src.quantum_adventure import QuantumAdventure
        
        game = QuantumAdventure()
        
        # First input is empty, second is quit
        inputs = iter(["", "quit"])
        
        with patch('builtins.input', side_effect=lambda: next(inputs)):
            game_loop(game)
            # Should have processed quit, ignoring empty
            assert game.is_running() is False
