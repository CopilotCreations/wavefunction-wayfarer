"""
Tests for the utils module.

This module tests save/load functionality, helper functions,
and utility operations.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import shutil

from src.utils import (
    ensure_save_directory,
    get_save_filepath,
    save_game,
    load_game,
    list_saves,
    delete_save,
    format_separator,
    format_box,
    weighted_random_choice,
    calculate_probability_distribution,
    format_probability_bar,
    SAVE_DIR
)
from src.world import QuantumState
from src.player import Player


class TestEnsureSaveDirectory:
    """Tests for ensure_save_directory function."""
    
    def test_creates_directory(self, tmp_path):
        """Test that save directory is created."""
        with patch('src.utils.SAVE_DIR', tmp_path / "test_saves"):
            from src import utils
            original_save_dir = utils.SAVE_DIR
            utils.SAVE_DIR = tmp_path / "test_saves"
            
            result = ensure_save_directory()
            
            assert (tmp_path / "test_saves").exists()
            utils.SAVE_DIR = original_save_dir


class TestGetSaveFilepath:
    """Tests for get_save_filepath function."""
    
    def test_returns_correct_path(self, tmp_path):
        """Test filepath generation."""
        with patch('src.utils.SAVE_DIR', tmp_path):
            from src import utils
            original = utils.SAVE_DIR
            utils.SAVE_DIR = tmp_path
            
            result = get_save_filepath("mysave")
            
            assert result == tmp_path / "mysave.json"
            utils.SAVE_DIR = original


class TestFormatSeparator:
    """Tests for format_separator function."""
    
    def test_default_separator(self):
        """Test default separator."""
        result = format_separator()
        
        assert len(result) == 70
        assert result == "═" * 70
    
    def test_custom_char(self):
        """Test separator with custom character."""
        result = format_separator("-", 20)
        
        assert len(result) == 20
        assert result == "-" * 20
    
    def test_custom_length(self):
        """Test separator with custom length."""
        result = format_separator("*", 10)
        
        assert len(result) == 10
        assert result == "*" * 10


class TestFormatBox:
    """Tests for format_box function."""
    
    def test_basic_box(self):
        """Test basic box formatting."""
        result = format_box("Title", ["Line 1", "Line 2"])
        
        assert "Title" in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "╔" in result
        assert "╚" in result
    
    def test_box_with_long_content(self):
        """Test box truncates long content."""
        long_line = "x" * 100
        result = format_box("Title", [long_line], width=40)
        
        assert "..." in result
    
    def test_empty_content(self):
        """Test box with empty content."""
        result = format_box("Empty", [])
        
        assert "Empty" in result
        assert "╔" in result


class TestWeightedRandomChoice:
    """Tests for weighted_random_choice function."""
    
    def test_single_choice(self):
        """Test with single choice."""
        result = weighted_random_choice(["only"], [1.0])
        
        assert result == "only"
    
    def test_weighted_selection(self):
        """Test that weights affect selection."""
        choices = ["A", "B"]
        weights = [0.9, 0.1]
        
        counts = {"A": 0, "B": 0}
        for _ in range(1000):
            result = weighted_random_choice(choices, weights)
            counts[result] += 1
        
        # A should be selected much more often
        assert counts["A"] > counts["B"]
    
    def test_mismatched_lengths(self):
        """Test error on mismatched lengths."""
        with pytest.raises(ValueError):
            weighted_random_choice(["A", "B"], [1.0])
    
    def test_equal_weights(self):
        """Test with equal weights."""
        choices = ["A", "B", "C"]
        weights = [1.0, 1.0, 1.0]
        
        counts = {"A": 0, "B": 0, "C": 0}
        for _ in range(900):
            result = weighted_random_choice(choices, weights)
            counts[result] += 1
        
        # Each should be selected roughly equal times
        for count in counts.values():
            assert count > 100  # Each should have reasonable count


class TestCalculateProbabilityDistribution:
    """Tests for calculate_probability_distribution function."""
    
    def test_single_state(self):
        """Test distribution with single state."""
        states = [QuantumState(location="A", probability=1.0)]
        
        dist = calculate_probability_distribution(states)
        
        assert len(dist) == 1
        assert list(dist.values())[0] == 1.0
    
    def test_equal_probabilities(self):
        """Test distribution with equal probabilities."""
        states = [
            QuantumState(location="A", probability=0.5),
            QuantumState(location="B", probability=0.5)
        ]
        
        dist = calculate_probability_distribution(states)
        
        assert len(dist) == 2
        for prob in dist.values():
            assert abs(prob - 0.5) < 0.01
    
    def test_unequal_probabilities(self):
        """Test distribution with unequal probabilities."""
        states = [
            QuantumState(location="A", probability=0.75),
            QuantumState(location="B", probability=0.25)
        ]
        
        dist = calculate_probability_distribution(states)
        
        probs = list(dist.values())
        assert 0.75 in probs
        assert 0.25 in probs


class TestFormatProbabilityBar:
    """Tests for format_probability_bar function."""
    
    def test_zero_probability(self):
        """Test bar at 0%."""
        result = format_probability_bar(0.0)
        
        assert "0.0%" in result
        assert "░" * 20 in result
    
    def test_full_probability(self):
        """Test bar at 100%."""
        result = format_probability_bar(1.0)
        
        assert "100.0%" in result
        assert "█" * 20 in result
    
    def test_half_probability(self):
        """Test bar at 50%."""
        result = format_probability_bar(0.5)
        
        assert "50.0%" in result
        assert "█" * 10 in result
    
    def test_custom_width(self):
        """Test bar with custom width."""
        result = format_probability_bar(0.5, width=10)
        
        assert "█" * 5 in result
        assert "░" * 5 in result


class TestSaveGame:
    """Tests for save_game function."""
    
    def test_save_creates_file(self, tmp_path):
        """Test that save creates a file."""
        from src.quantum_adventure import QuantumAdventure
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        game = QuantumAdventure()
        result = save_game(game, "test_save")
        
        assert result is True
        assert (tmp_path / "test_save.json").exists()
        
        utils.SAVE_DIR = original
    
    def test_save_content_valid_json(self, tmp_path):
        """Test that save content is valid JSON."""
        from src.quantum_adventure import QuantumAdventure
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        game = QuantumAdventure()
        save_game(game, "json_test")
        
        with open(tmp_path / "json_test.json", "r") as f:
            data = json.load(f)
        
        assert "version" in data
        assert "timestamp" in data
        assert "game" in data
        
        utils.SAVE_DIR = original


class TestLoadGame:
    """Tests for load_game function."""
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test loading non-existent file returns None."""
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        result = load_game("nonexistent")
        
        assert result is None
        
        utils.SAVE_DIR = original
    
    def test_load_existing_save(self, tmp_path):
        """Test loading existing save."""
        from src.quantum_adventure import QuantumAdventure
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        # Save a game first
        game = QuantumAdventure(player_name="LoadTest")
        save_game(game, "load_test")
        
        # Load it back
        result = load_game("load_test")
        
        assert result is not None
        assert "states" in result
        assert "player" in result
        assert result["player"].name == "LoadTest"
        
        utils.SAVE_DIR = original


class TestListSaves:
    """Tests for list_saves function."""
    
    def test_list_empty_directory(self, tmp_path):
        """Test listing saves in empty directory."""
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        result = list_saves()
        
        assert result == []
        
        utils.SAVE_DIR = original
    
    def test_list_saves_with_files(self, tmp_path):
        """Test listing saves with save files."""
        from src.quantum_adventure import QuantumAdventure
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        # Create some saves
        game = QuantumAdventure()
        save_game(game, "save1")
        save_game(game, "save2")
        
        result = list_saves()
        
        assert len(result) == 2
        names = [s["name"] for s in result]
        assert "save1" in names
        assert "save2" in names
        
        utils.SAVE_DIR = original


class TestDeleteSave:
    """Tests for delete_save function."""
    
    def test_delete_nonexistent(self, tmp_path):
        """Test deleting non-existent save returns False."""
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        result = delete_save("nonexistent")
        
        assert result is False
        
        utils.SAVE_DIR = original
    
    def test_delete_existing(self, tmp_path):
        """Test deleting existing save."""
        from src.quantum_adventure import QuantumAdventure
        from src import utils
        
        original = utils.SAVE_DIR
        utils.SAVE_DIR = tmp_path
        
        # Create a save
        game = QuantumAdventure()
        save_game(game, "to_delete")
        assert (tmp_path / "to_delete.json").exists()
        
        # Delete it
        result = delete_save("to_delete")
        
        assert result is True
        assert not (tmp_path / "to_delete.json").exists()
        
        utils.SAVE_DIR = original
