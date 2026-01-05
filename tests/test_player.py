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
        """Test basic parsed command creation.

        Verifies that a ParsedCommand can be instantiated with command_type,
        arguments, and raw_input, and that all attributes are correctly stored.
        """
        cmd = ParsedCommand(
            command_type=CommandType.MOVE,
            arguments=["north"],
            raw_input="go north"
        )
        
        assert cmd.command_type == CommandType.MOVE
        assert cmd.arguments == ["north"]
        assert cmd.raw_input == "go north"
    
    def test_has_arguments_true(self):
        """Test has_arguments when arguments present.

        Verifies that has_arguments() returns True when the command
        contains one or more arguments.
        """
        cmd = ParsedCommand(CommandType.TAKE, ["sword"], "take sword")
        
        assert cmd.has_arguments() is True
    
    def test_has_arguments_false(self):
        """Test has_arguments when no arguments.

        Verifies that has_arguments() returns False when the command
        has an empty arguments list.
        """
        cmd = ParsedCommand(CommandType.LOOK, [], "look")
        
        assert cmd.has_arguments() is False
    
    def test_get_first_arg(self):
        """Test getting first argument.

        Verifies that get_first_arg() returns the first argument
        when multiple arguments are present.
        """
        cmd = ParsedCommand(CommandType.MOVE, ["north", "fast"], "go north fast")
        
        assert cmd.get_first_arg() == "north"
    
    def test_get_first_arg_none(self):
        """Test getting first arg when none exist.

        Verifies that get_first_arg() returns None when the command
        has no arguments.
        """
        cmd = ParsedCommand(CommandType.HELP, [], "help")
        
        assert cmd.get_first_arg() is None
    
    def test_get_all_args_as_string(self):
        """Test joining arguments into string.

        Verifies that get_all_args_as_string() joins all arguments
        with spaces into a single string.
        """
        cmd = ParsedCommand(CommandType.TAKE, ["magic", "sword"], "take magic sword")
        
        assert cmd.get_all_args_as_string() == "magic sword"


class TestCommandParser:
    """Tests for the CommandParser class."""
    
    def test_parse_empty_input(self):
        """Test parsing empty input.

        Verifies that an empty string input results in an UNKNOWN command type.
        """
        result = CommandParser.parse("")
        
        assert result.command_type == CommandType.UNKNOWN
    
    def test_parse_whitespace_input(self):
        """Test parsing whitespace-only input.

        Verifies that whitespace-only input results in an UNKNOWN command type.
        """
        result = CommandParser.parse("   ")
        
        assert result.command_type == CommandType.UNKNOWN
    
    # Movement commands
    def test_parse_go_north(self):
        """Test parsing 'go north' command.

        Verifies that 'go north' is parsed as a MOVE command
        with 'north' as the direction argument.
        """
        result = CommandParser.parse("go north")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_direction_shortcut(self):
        """Test parsing direction shortcuts.

        Verifies that single-letter direction shortcuts (e.g., 'n')
        are correctly expanded to full direction names (e.g., 'north').
        """
        result = CommandParser.parse("n")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_bare_direction(self):
        """Test parsing bare direction like 'north'.

        Verifies that typing just a direction name without a verb
        is parsed as a MOVE command.
        """
        result = CommandParser.parse("north")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    def test_parse_all_directions(self):
        """Test all direction shortcuts.

        Verifies that all single-letter direction shortcuts (n, s, e, w, u, d)
        are correctly mapped to their full direction names.
        """
        directions = {
            "n": "north", "s": "south", "e": "east",
            "w": "west", "u": "up", "d": "down"
        }
        
        for shortcut, full in directions.items():
            result = CommandParser.parse(shortcut)
            assert result.command_type == CommandType.MOVE
            assert result.get_first_arg() == full
    
    def test_parse_move_aliases(self):
        """Test various move command aliases.

        Verifies that all movement verb aliases (go, move, walk, run, travel)
        are recognized as MOVE commands.
        """
        for alias in ["go", "move", "walk", "run", "travel"]:
            result = CommandParser.parse(f"{alias} north")
            assert result.command_type == CommandType.MOVE
    
    # Look commands
    def test_parse_look(self):
        """Test parsing look command.

        Verifies that 'look' without arguments is parsed as a LOOK command.
        """
        result = CommandParser.parse("look")
        
        assert result.command_type == CommandType.LOOK
    
    def test_parse_look_at_object(self):
        """Test parsing look at specific object.

        Verifies that 'look <object>' is parsed as a LOOK command
        with the object name as an argument.
        """
        result = CommandParser.parse("look sword")
        
        assert result.command_type == CommandType.LOOK
        assert result.get_first_arg() == "sword"
    
    def test_parse_examine(self):
        """Test examine alias for look.

        Verifies that 'examine' is recognized as an alias for the LOOK command.
        """
        result = CommandParser.parse("examine key")
        
        assert result.command_type == CommandType.LOOK
        assert result.get_first_arg() == "key"
    
    # Inventory commands
    def test_parse_inventory(self):
        """Test parsing inventory command.

        Verifies that 'inventory' is parsed as an INVENTORY command.
        """
        result = CommandParser.parse("inventory")
        
        assert result.command_type == CommandType.INVENTORY
    
    def test_parse_inventory_shortcuts(self):
        """Test inventory command shortcuts.

        Verifies that all inventory aliases (inv, i, items, bag)
        are recognized as INVENTORY commands.
        """
        for alias in ["inv", "i", "items", "bag"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.INVENTORY
    
    # Take commands
    def test_parse_take(self):
        """Test parsing take command.

        Verifies that 'take <item>' is parsed as a TAKE command
        with the item name as an argument.
        """
        result = CommandParser.parse("take sword")
        
        assert result.command_type == CommandType.TAKE
        assert result.get_first_arg() == "sword"
    
    def test_parse_take_aliases(self):
        """Test take command aliases.

        Verifies that all take verb aliases (take, get, grab, pick, collect)
        are recognized as TAKE commands.
        """
        for alias in ["take", "get", "grab", "pick", "collect"]:
            result = CommandParser.parse(f"{alias} item")
            assert result.command_type == CommandType.TAKE
    
    # Drop commands
    def test_parse_drop(self):
        """Test parsing drop command.

        Verifies that 'drop <item>' is parsed as a DROP command
        with the item name as an argument.
        """
        result = CommandParser.parse("drop key")
        
        assert result.command_type == CommandType.DROP
        assert result.get_first_arg() == "key"
    
    # Use commands
    def test_parse_use(self):
        """Test parsing use command.

        Verifies that 'use <item>' is parsed as a USE command
        with the item name as an argument.
        """
        result = CommandParser.parse("use potion")
        
        assert result.command_type == CommandType.USE
        assert result.get_first_arg() == "potion"
    
    # Quantum commands
    def test_parse_observe(self):
        """Test parsing observe command.

        Verifies that 'observe' is parsed as an OBSERVE command
        for quantum state collapse.
        """
        result = CommandParser.parse("observe")
        
        assert result.command_type == CommandType.OBSERVE
    
    def test_parse_observe_aliases(self):
        """Test observe command aliases.

        Verifies that all quantum observation aliases (observe, collapse, measure)
        are recognized as OBSERVE commands.
        """
        for alias in ["observe", "collapse", "measure"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.OBSERVE
    
    def test_parse_status(self):
        """Test parsing status command.

        Verifies that 'status' is parsed as a STATUS command
        for viewing quantum superposition state.
        """
        result = CommandParser.parse("status")
        
        assert result.command_type == CommandType.STATUS
    
    def test_parse_status_aliases(self):
        """Test status command aliases.

        Verifies that all status aliases (status, superposition, timelines, worlds)
        are recognized as STATUS commands.
        """
        for alias in ["status", "superposition", "timelines", "worlds"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.STATUS
    
    # Save/Load commands
    def test_parse_save(self):
        """Test parsing save command.

        Verifies that 'save <name>' is parsed as a SAVE command
        with the save name as an argument.
        """
        result = CommandParser.parse("save mysave")
        
        assert result.command_type == CommandType.SAVE
        assert result.get_first_arg() == "mysave"
    
    def test_parse_load(self):
        """Test parsing load command.

        Verifies that 'load <name>' is parsed as a LOAD command
        with the save name as an argument.
        """
        result = CommandParser.parse("load mysave")
        
        assert result.command_type == CommandType.LOAD
        assert result.get_first_arg() == "mysave"
    
    # Attack commands
    def test_parse_attack(self):
        """Test parsing attack command.

        Verifies that 'attack <target>' is parsed as an ATTACK command
        with the target name as an argument.
        """
        result = CommandParser.parse("attack goblin")
        
        assert result.command_type == CommandType.ATTACK
        assert result.get_first_arg() == "goblin"
    
    def test_parse_attack_aliases(self):
        """Test attack command aliases.

        Verifies that all attack verb aliases (attack, fight, hit, strike)
        are recognized as ATTACK commands.
        """
        for alias in ["attack", "fight", "hit", "strike"]:
            result = CommandParser.parse(f"{alias} enemy")
            assert result.command_type == CommandType.ATTACK
    
    # Help commands
    def test_parse_help(self):
        """Test parsing help command.

        Verifies that 'help' is parsed as a HELP command.
        """
        result = CommandParser.parse("help")
        
        assert result.command_type == CommandType.HELP
    
    def test_parse_help_question_mark(self):
        """Test parsing ? as help.

        Verifies that '?' is recognized as an alias for the HELP command.
        """
        result = CommandParser.parse("?")
        
        assert result.command_type == CommandType.HELP
    
    # Quit commands
    def test_parse_quit(self):
        """Test parsing quit command.

        Verifies that 'quit' is parsed as a QUIT command.
        """
        result = CommandParser.parse("quit")
        
        assert result.command_type == CommandType.QUIT
    
    def test_parse_quit_aliases(self):
        """Test quit command aliases.

        Verifies that all quit aliases (quit, exit, q, bye)
        are recognized as QUIT commands.
        """
        for alias in ["quit", "exit", "q", "bye"]:
            result = CommandParser.parse(alias)
            assert result.command_type == CommandType.QUIT
    
    # History commands
    def test_parse_history(self):
        """Test parsing history command.

        Verifies that 'history' is parsed as a HISTORY command.
        """
        result = CommandParser.parse("history")
        
        assert result.command_type == CommandType.HISTORY
    
    # Case insensitivity
    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive.

        Verifies that commands are parsed correctly regardless of
        uppercase, lowercase, or mixed case input.
        """
        result = CommandParser.parse("GO NORTH")
        
        assert result.command_type == CommandType.MOVE
        assert result.get_first_arg() == "north"
    
    # Unknown commands
    def test_parse_unknown_command(self):
        """Test parsing unknown command.

        Verifies that unrecognized input results in an UNKNOWN command type.
        """
        result = CommandParser.parse("xyzzy")
        
        assert result.command_type == CommandType.UNKNOWN
    
    # Help text
    def test_get_help_text(self):
        """Test help text generation.

        Verifies that get_help_text() returns a string containing
        expected sections like MOVEMENT and QUANTUM commands.
        """
        help_text = CommandParser.get_help_text()
        
        assert "MOVEMENT" in help_text
        assert "QUANTUM" in help_text
        assert "observe" in help_text
        assert "status" in help_text


class TestPlayer:
    """Tests for the Player class."""
    
    def test_player_creation_default(self):
        """Test player creation with default name.

        Verifies that a Player created without arguments has the
        default name 'Traveler' and a stats dictionary.
        """
        player = Player()
        
        assert player.name == "Traveler"
        assert isinstance(player.stats, dict)
    
    def test_player_creation_custom_name(self):
        """Test player creation with custom name.

        Verifies that a Player can be created with a custom name.
        """
        player = Player(name="Alice")
        
        assert player.name == "Alice"
    
    def test_initial_stats(self):
        """Test that initial stats are zero.

        Verifies that all player statistics (observations, timelines_created,
        items_collected, enemies_defeated, moves) start at zero.
        """
        player = Player()
        
        assert player.stats["observations"] == 0
        assert player.stats["timelines_created"] == 0
        assert player.stats["items_collected"] == 0
        assert player.stats["enemies_defeated"] == 0
        assert player.stats["moves"] == 0
    
    def test_record_observation(self):
        """Test recording an observation.

        Verifies that record_observation() increments the observations
        stat counter correctly, including multiple increments.
        """
        player = Player()
        player.record_observation()
        
        assert player.stats["observations"] == 1
        
        player.record_observation()
        assert player.stats["observations"] == 2
    
    def test_record_branch(self):
        """Test recording a timeline branch.

        Verifies that record_branch() increments the timelines_created stat.
        """
        player = Player()
        player.record_branch()
        
        assert player.stats["timelines_created"] == 1
    
    def test_record_item_collected(self):
        """Test recording item collection.

        Verifies that record_item_collected() increments the items_collected stat.
        """
        player = Player()
        player.record_item_collected()
        
        assert player.stats["items_collected"] == 1
    
    def test_record_enemy_defeated(self):
        """Test recording enemy defeat.

        Verifies that record_enemy_defeated() increments the enemies_defeated stat.
        """
        player = Player()
        player.record_enemy_defeated()
        
        assert player.stats["enemies_defeated"] == 1
    
    def test_record_move(self):
        """Test recording a move.

        Verifies that record_move() increments the moves stat.
        """
        player = Player()
        player.record_move()
        
        assert player.stats["moves"] == 1
    
    def test_get_stats_display(self):
        """Test stats display formatting.

        Verifies that get_stats_display() returns a formatted string
        containing the player name and stat labels.
        """
        player = Player(name="TestPlayer")
        player.record_observation()
        player.record_move()
        
        display = player.get_stats_display()
        
        assert "TestPlayer" in display
        assert "Observations" in display
        assert "Moves" in display
    
    def test_player_serialization(self):
        """Test converting player to dict and back.

        Verifies that a Player can be serialized to a dictionary with to_dict()
        and restored with from_dict(), preserving name and stats.
        """
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
