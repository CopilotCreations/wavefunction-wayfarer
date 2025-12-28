"""
Tests for the player module.

This module tests the CommandParser, ParsedCommand, and Player classes
including command parsing, player stats, and serialization.
"""

import pytest
from src.player import (
    CommandParser, 
    ParsedCommand, 
    CommandType, 
    Player
)


class TestParsedCommand:
    """Tests for the ParsedCommand dataclass."""
    
    def test_parsed_command_creation(self):
        """Test basic parsed command creation."""
        cmd = ParsedCommand(
            command_type=CommandType.MOVE,
            arguments=["north"],
            raw_input="go north"
        )
        
        assert cmd.command_type == CommandType.MOVE
        assert cmd.arguments == ["north"]
        assert cmd.raw_input == "go north"
    
    def test_has_arguments_true(self):
        """Test has_arguments when arguments present."""
        cmd = ParsedCommand(CommandType.TAKE, ["sword"], "take sword")
        
        assert cmd.has_arguments() is True
    
    def test_has_arguments_false(self):
        """Test has_arguments when no arguments."""
        cmd = ParsedCommand(CommandType.LOOK, [], "look")
        
        assert cmd.has_arguments() is False
    
    def test_get_first_arg(self):
        """Test getting first argument."""
        cmd = ParsedCommand(CommandType.MOVE, ["north", "fast"], "go north fast")
        
        assert cmd.get_first_arg() == "north"
    
    def test_get_first_arg_none(self):
        """Test getting first arg when none exist."""
        cmd = ParsedCommand(CommandType.HELP, [], "help")
        
        assert cmd.get_first_arg() is None
    
    def test_get_all_args_as_string(self):
        """Test joining arguments into string."""
        cmd = ParsedCommand(CommandType.TAKE, ["magic", "sword"], "take magic sword")
        
        assert cmd.get_all_args_as_string() == "magic sword"


class TestCommandParser:
    """Tests for the CommandParser class."""
    
    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = CommandParser.parse("")
        
        assert result.command_type == CommandType.UNKNOWN
    
    def test_parse_whitespace_input(self):
        """Test parsing whitespace-only input."""
        result = CommandParser.parse("   ")
        
        assert result.command_type == CommandType.UNKNOWN
    
    # Movement commands
    def test_parse_go_north(self):
        """Test parsing 'go north' command."""
        result = CommandParser.parse("go north")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_direction_shortcut(self):
        """Test parsing direction shortcuts."""
        result = CommandParser.parse("n")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_bare_direction(self):
        """Test parsing bare direction like 'north'."""
        result = CommandParser.parse("north")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_all_directions(self):
        """Test all direction shortcuts."""
        directions = {
            "n": "north", "s": "south", "e": "east",
            "w": "west", "u": "up", "d": "down"
        }
        
        for shortcut, full in directions.items():
            result = CommandParser.parse(shortcut)
            assert result.command_type == CommandType.MOVE
            assert result.get_first_arg() == full
    
    def test_parse_move_aliases(self):
        """Test various move command aliases."""
        for alias in ["go", "move", "walk", "run", "travel"]:
            result = CommandParser.parse(f"{alias} north")
            assert result.command_type == CommandType.MOVE
    
    # Look commands
    def test_parse_look(self):
        """Test parsing look command."""
        result = CommandParser.parse("look")
        
        assert result.command_type == CommandType.LOOK
    
    def test_parse_look_at_object(self):
        """Test parsing look at specific object."""
        result = CommandParser.parse("look sword")
        
        assert result.command_type == CommandType.LOOK
        assert result.get_first_arg() == "sword"
    
    def test_parse_examine(self):
        """Test examine alias for look."""
        result = CommandParser.parse("examine key")
        
        assert result.command_type == CommandType.LOOK
        assert result.get_first_arg() == "key"
    
    # Inventory commands
    def test_parse_inventory(self):
        """Test parsing inventory command."""
        result = CommandParser.parse("inventory")
        
        assert result.command_type == CommandType.INVENTORY
    
    def test_parse_inventory_shortcuts(self):
        """Test inventory command shortcuts."""
        for alias in ["inv", "i", "items", "bag"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.INVENTORY
    
    # Take commands
    def test_parse_take(self):
        """Test parsing take command."""
        result = CommandParser.parse("take sword")
        
        assert result.command_type == CommandType.TAKE
        assert result.get_first_arg() == "sword"
    
    def test_parse_take_aliases(self):
        """Test take command aliases."""
        for alias in ["take", "get", "grab", "pick", "collect"]:
            result = CommandParser.parse(f"{alias} item")
            assert result.command_type == CommandType.TAKE
    
    # Drop commands
    def test_parse_drop(self):
        """Test parsing drop command."""
        result = CommandParser.parse("drop key")
        
        assert result.command_type == CommandType.DROP
        assert result.get_first_arg() == "key"
    
    # Use commands
    def test_parse_use(self):
        """Test parsing use command."""
        result = CommandParser.parse("use potion")
        
        assert result.command_type == CommandType.USE
        assert result.get_first_arg() == "potion"
    
    # Quantum commands
    def test_parse_observe(self):
        """Test parsing observe command."""
        result = CommandParser.parse("observe")
        
        assert result.command_type == CommandType.OBSERVE
    
    def test_parse_observe_aliases(self):
        """Test observe command aliases."""
        for alias in ["observe", "collapse", "measure"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.OBSERVE
    
    def test_parse_status(self):
        """Test parsing status command."""
        result = CommandParser.parse("status")
        
        assert result.command_type == CommandType.STATUS
    
    def test_parse_status_aliases(self):
        """Test status command aliases."""
        for alias in ["status", "superposition", "timelines", "worlds"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.STATUS
    
    # Save/Load commands
    def test_parse_save(self):
        """Test parsing save command."""
        result = CommandParser.parse("save mysave")
        
        assert result.command_type == CommandType.SAVE
        assert result.get_first_arg() == "mysave"
    
    def test_parse_load(self):
        """Test parsing load command."""
        result = CommandParser.parse("load mysave")
        
        assert result.command_type == CommandType.LOAD
        assert result.get_first_arg() == "mysave"
    
    # Attack commands
    def test_parse_attack(self):
        """Test parsing attack command."""
        result = CommandParser.parse("attack goblin")
        
        assert result.command_type == CommandType.ATTACK
        assert result.get_first_arg() == "goblin"
    
    def test_parse_attack_aliases(self):
        """Test attack command aliases."""
        for alias in ["attack", "fight", "hit", "strike"]:
            result = CommandParser.parse(f"{alias} enemy")
            assert result.command_type == CommandType.ATTACK
    
    # Help commands
    def test_parse_help(self):
        """Test parsing help command."""
        result = CommandParser.parse("help")
        
        assert result.command_type == CommandType.HELP
    
    def test_parse_help_question_mark(self):
        """Test parsing ? as help."""
        result = CommandParser.parse("?")
        
        assert result.command_type == CommandType.HELP
    
    # Quit commands
    def test_parse_quit(self):
        """Test parsing quit command."""
        result = CommandParser.parse("quit")
        
        assert result.command_type == CommandType.QUIT
    
    def test_parse_quit_aliases(self):
        """Test quit command aliases."""
        for alias in ["quit", "exit", "q", "bye"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.QUIT
    
    # History commands
    def test_parse_history(self):
        """Test parsing history command."""
        result = CommandParser.parse("history")
        
        assert result.command_type == CommandType.HISTORY
    
    # Case insensitivity
    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive."""
        result = CommandParser.parse("GO NORTH")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    # Unknown commands
    def test_parse_unknown_command(self):
        """Test parsing unknown command."""
        result = CommandParser.parse("xyzzy")
        
        assert result.command_type == CommandType.UNKNOWN
    
    # Help text
    def test_get_help_text(self):
        """Test help text generation."""
        help_text = CommandParser.get_help_text()
        
        assert "MOVEMENT" in help_text
        assert "QUANTUM" in help_text
        assert "observe" in help_text
        assert "status" in help_text


class TestPlayer:
    """Tests for the Player class."""
    
    def test_player_creation_default(self):
        """Test player creation with default name."""
        player = Player()
        
        assert player.name == "Traveler"
        assert isinstance(player.stats, dict)
    
    def test_player_creation_custom_name(self):
        """Test player creation with custom name."""
        player = Player(name="Alice")
        
        assert player.name == "Alice"
    
    def test_initial_stats(self):
        """Test that initial stats are zero."""
        player = Player()
        
        assert player.stats["observations"] == 0
        assert player.stats["timelines_created"] == 0
        assert player.stats["items_collected"] == 0
        assert player.stats["enemies_defeated"] == 0
        assert player.stats["moves"] == 0
    
    def test_record_observation(self):
        """Test recording an observation."""
        player = Player()
        player.record_observation()
        
        assert player.stats["observations"] == 1
        
        player.record_observation()
        assert player.stats["observations"] == 2
    
    def test_record_branch(self):
        """Test recording a timeline branch."""
        player = Player()
        player.record_branch()
        
        assert player.stats["timelines_created"] == 1
    
    def test_record_item_collected(self):
        """Test recording item collection."""
        player = Player()
        player.record_item_collected()
        
        assert player.stats["items_collected"] == 1
    
    def test_record_enemy_defeated(self):
        """Test recording enemy defeat."""
        player = Player()
        player.record_enemy_defeated()
        
        assert player.stats["enemies_defeated"] == 1
    
    def test_record_move(self):
        """Test recording a move."""
        player = Player()
        player.record_move()
        
        assert player.stats["moves"] == 1
    
    def test_get_stats_display(self):
        """Test stats display formatting."""
        player = Player(name="TestPlayer")
        player.record_observation()
        player.record_move()
        
        display = player.get_stats_display()
        
        assert "TestPlayer" in display
        assert "Observations" in display
        assert "Moves" in display
    
    def test_player_serialization(self):
        """Test converting player to dict and back."""
        original = Player(name="Bob")
        original.record_observation()
        original.record_move()
        original.record_item_collected()
        
        data = original.to_dict()
        
        assert data["name"] == "Bob"
        assert data["stats"]["observations"] == 1
        assert data["stats"]["moves"] == 1
        
        restored = Player.from_dict(data)
        
        assert restored.name == original.name
        assert restored.stats == original.stats
