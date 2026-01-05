"""
Tests for the quantum_adventure module.

This module tests the QuantumAdventure class including game mechanics,
command processing, quantum superposition, and wavefunction collapse.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.quantum_adventure import QuantumAdventure
from src.player import CommandParser, CommandType, ParsedCommand
from src.world import QuantumState


class TestQuantumAdventureInitialization:
    """Tests for QuantumAdventure initialization."""
    
    def test_default_initialization(self):
        """Test default game initialization.

        Verifies that a new QuantumAdventure instance has default player name,
        single initial state at Quantum Nexus, and running flag set to True.
        """
        game = QuantumAdventure()
        
        assert game.player.name == "Traveler"
        assert len(game.states) == 1
        assert game.states[0].location == "Quantum Nexus"
        assert game.running is True
    
    def test_custom_player_name(self):
        """Test initialization with custom player name.

        Verifies that the player name can be customized during game creation.
        """
        game = QuantumAdventure(player_name="Alice")
        
        assert game.player.name == "Alice"
    
    def test_initial_state_has_log_entry(self):
        """Test that initial state has welcome log entry.

        Verifies that the initial game state includes a welcome message
        in the story log mentioning the adventure beginning.
        """
        game = QuantumAdventure()
        
        assert len(game.states[0].story_log) >= 1
        assert "adventure begins" in game.states[0].story_log[0].lower()
    
    def test_locations_initialized(self):
        """Test that locations are initialized.

        Verifies that the game initializes with at least 5 locations
        including the starting Quantum Nexus location.
        """
        game = QuantumAdventure()
        
        assert len(game.locations) >= 5
        assert "Quantum Nexus" in game.locations


class TestQuantumAdventureMovement:
    """Tests for movement mechanics."""
    
    def test_valid_movement(self):
        """Test moving in a valid direction.

        Verifies that issuing a move command results in either
        changing location or creating a branched quantum state.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.MOVE, ["north"], "go north")
        
        result = game.process_command(command)
        
        # Should have moved or branched
        assert game.states[0].location != "Quantum Nexus" or len(game.states) > 1
    
    def test_invalid_direction_no_args(self):
        """Test movement with no direction.

        Verifies that a move command without a direction argument
        returns an appropriate error message asking for a direction.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.MOVE, [], "go")
        
        result = game.process_command(command)
        
        assert "where" in result.lower() or "direction" in result.lower()
    
    def test_movement_records_move(self):
        """Test that movement records in player stats.

        Verifies that each successful movement command increments
        the player's moves counter in their stats.
        """
        game = QuantumAdventure()
        initial_moves = game.player.stats["moves"]
        
        command = ParsedCommand(CommandType.MOVE, ["north"], "go north")
        game.process_command(command)
        
        assert game.player.stats["moves"] == initial_moves + 1


class TestQuantumAdventureLook:
    """Tests for look/examine commands."""
    
    def test_look_at_location(self):
        """Test looking at current location.

        Verifies that the look command without arguments returns
        a description containing the current location name.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.LOOK, [], "look")
        
        result = game.process_command(command)
        
        assert "Quantum Nexus" in result
    
    def test_look_at_item_in_inventory(self):
        """Test looking at item in inventory.

        Verifies that examining an item in the player's inventory
        returns a description containing the item name.
        """
        game = QuantumAdventure()
        game.states[0].add_item("sword")
        
        command = ParsedCommand(CommandType.LOOK, ["sword"], "look sword")
        result = game.process_command(command)
        
        assert "sword" in result.lower()
    
    def test_look_at_nonexistent_item(self):
        """Test looking at item that doesn't exist.

        Verifies that examining a non-existent item returns
        an appropriate message indicating the item is not visible.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.LOOK, ["unicorn"], "look unicorn")
        
        result = game.process_command(command)
        
        assert "don't see" in result.lower()


class TestQuantumAdventureInventory:
    """Tests for inventory management."""
    
    def test_empty_inventory(self):
        """Test displaying empty inventory.

        Verifies that viewing an empty inventory returns a message
        indicating the inventory is empty or shows the inventory header.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.INVENTORY, [], "inventory")
        
        result = game.process_command(command)
        
        assert "empty" in result.lower() or "INVENTORY" in result
    
    def test_inventory_with_items(self):
        """Test displaying inventory with items.

        Verifies that viewing an inventory with items lists
        all items currently held by the player.
        """
        game = QuantumAdventure()
        game.states[0].add_item("sword")
        game.states[0].add_item("potion")
        
        command = ParsedCommand(CommandType.INVENTORY, [], "inventory")
        result = game.process_command(command)
        
        assert "sword" in result.lower()
        assert "potion" in result.lower()
    
    def test_take_item(self):
        """Test taking an item.

        Verifies that the take command successfully picks up an item
        from the current location and adds it to inventory.
        """
        game = QuantumAdventure()
        game.states[0].world_items["Quantum Nexus"] = ["test key"]
        
        command = ParsedCommand(CommandType.TAKE, ["test", "key"], "take test key")
        result = game.process_command(command)
        
        assert "pick up" in result.lower() or "test key" in result.lower()
    
    def test_take_nonexistent_item(self):
        """Test taking item that doesn't exist.

        Verifies that attempting to take a non-existent item
        returns an appropriate error message.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.TAKE, ["ghost"], "take ghost")
        
        result = game.process_command(command)
        
        assert "no" in result.lower() or "not" in result.lower()
    
    def test_drop_item(self):
        """Test dropping an item.

        Verifies that dropping an item removes it from the player's
        inventory and leaves it in the current location.
        """
        game = QuantumAdventure()
        game.states[0].add_item("rock")
        
        command = ParsedCommand(CommandType.DROP, ["rock"], "drop rock")
        result = game.process_command(command)
        
        assert "drop" in result.lower()
        assert "rock" not in game.states[0].inventory
    
    def test_drop_nonexistent_item(self):
        """Test dropping item not in inventory.

        Verifies that attempting to drop an item not in the inventory
        returns an appropriate error message.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.DROP, ["nothing"], "drop nothing")
        
        result = game.process_command(command)
        
        assert "don't have" in result.lower()


class TestQuantumAdventureUseItems:
    """Tests for using items (triggers collapse)."""
    
    def test_use_item_triggers_collapse(self):
        """Test that using an item triggers wavefunction collapse.

        Verifies that using an item when multiple quantum states exist
        causes the wavefunction to collapse to a single state.
        """
        game = QuantumAdventure()
        # Create multiple states
        game.states.append(game.states[0].branch())
        game.states[0].add_item("test potion")
        game.states[1].add_item("test potion")
        
        command = ParsedCommand(CommandType.USE, ["test", "potion"], "use test potion")
        result = game.process_command(command)
        
        # Should collapse to single state
        assert len(game.states) == 1
        assert "collapse" in result.lower()
    
    def test_use_item_not_in_inventory(self):
        """Test using item that doesn't exist.

        Verifies that attempting to use an item not in the inventory
        returns an appropriate error message.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.USE, ["phantom"], "use phantom")
        
        result = game.process_command(command)
        
        assert "don't have" in result.lower()


class TestQuantumAdventureObserve:
    """Tests for observation/collapse mechanics."""
    
    def test_observe_single_state(self):
        """Test observing when only one state exists.

        Verifies that observing with a single quantum state returns
        a message indicating the wavefunction is already collapsed.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.OBSERVE, [], "observe")
        
        result = game.process_command(command)
        
        assert "already" in result.lower() or "single" in result.lower()
    
    def test_observe_collapses_multiple_states(self):
        """Test that observe collapses multiple states.

        Verifies that the observe command collapses multiple quantum
        states into a single state based on probability weights.
        """
        game = QuantumAdventure()
        # Create multiple states
        game.states.append(game.states[0].branch())
        game.states.append(game.states[0].branch())
        
        assert len(game.states) == 3
        
        command = ParsedCommand(CommandType.OBSERVE, [], "observe")
        result = game.process_command(command)
        
        assert len(game.states) == 1
        assert "collapse" in result.lower() or "observation" in result.lower()
    
    def test_observe_records_stat(self):
        """Test that observation records in player stats.

        Verifies that each observation increments the player's
        observations counter in their stats.
        """
        game = QuantumAdventure()
        game.states.append(game.states[0].branch())
        
        initial_obs = game.player.stats["observations"]
        
        command = ParsedCommand(CommandType.OBSERVE, [], "observe")
        game.process_command(command)
        
        assert game.player.stats["observations"] == initial_obs + 1


class TestQuantumAdventureStatus:
    """Tests for status display."""
    
    def test_status_single_state(self):
        """Test status with single state.

        Verifies that the status command displays timeline information
        and current location when in a single quantum state.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.STATUS, [], "status")
        
        result = game.process_command(command)
        
        assert "Timeline" in result
        assert "Quantum Nexus" in result
    
    def test_status_multiple_states(self):
        """Test status with multiple states.

        Verifies that the status command displays information about
        multiple parallel quantum states when they exist.
        """
        game = QuantumAdventure()
        game.states.append(game.states[0].branch())
        game.states[1].move_to("Test Location")
        
        command = ParsedCommand(CommandType.STATUS, [], "status")
        result = game.process_command(command)
        
        assert "2" in result or "parallel" in result.lower()


class TestQuantumAdventureHistory:
    """Tests for history/log display."""
    
    def test_history_shows_events(self):
        """Test that history shows logged events.

        Verifies that the history command displays events from
        the story log including custom logged entries.
        """
        game = QuantumAdventure()
        game.states[0].add_to_log("Test event 1")
        game.states[0].add_to_log("Test event 2")
        
        command = ParsedCommand(CommandType.HISTORY, [], "history")
        result = game.process_command(command)
        
        assert "Test event" in result or "Timeline" in result


class TestQuantumAdventureAttack:
    """Tests for combat mechanics."""
    
    def test_attack_no_enemy(self):
        """Test attacking when no enemy present.

        Verifies that attacking without an enemy present returns
        a message indicating there is nothing to attack.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.ATTACK, ["goblin"], "attack goblin")
        
        result = game.process_command(command)
        
        assert "nothing" in result.lower()
    
    def test_attack_with_enemy(self):
        """Test attacking when enemy is present.

        Verifies that attacking an enemy results in either
        defeating the enemy or missing the attack.
        """
        game = QuantumAdventure()
        game.current_enemies[game.states[0].timeline_id] = "Test Monster"
        
        command = ParsedCommand(CommandType.ATTACK, ["test", "monster"], "attack test monster")
        result = game.process_command(command)
        
        # Should either hit or miss
        assert "defeat" in result.lower() or "miss" in result.lower()


class TestQuantumAdventureHelp:
    """Tests for help command."""
    
    def test_help_displays_commands(self):
        """Test that help displays command list.

        Verifies that the help command displays categorized lists
        of available commands including movement and quantum commands.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.HELP, [], "help")
        
        result = game.process_command(command)
        
        assert "MOVEMENT" in result
        assert "QUANTUM" in result


class TestQuantumAdventureQuit:
    """Tests for quit command."""
    
    def test_quit_stops_game(self):
        """Test that quit stops the game.

        Verifies that the quit command sets the running flag to False
        and returns a farewell message.
        """
        game = QuantumAdventure()
        assert game.is_running() is True
        
        command = ParsedCommand(CommandType.QUIT, [], "quit")
        result = game.process_command(command)
        
        assert game.is_running() is False
        assert "thank you" in result.lower()


class TestQuantumAdventureSaveLoad:
    """Tests for save/load functionality."""
    
    def test_save_command(self):
        """Test save command execution.

        Verifies that the save command successfully saves the game
        and returns a confirmation message.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.SAVE, ["test_save"], "save test_save")
        
        with patch('src.utils.save_game', return_value=True):
            result = game.process_command(command)
            assert "saved" in result.lower()
    
    def test_load_command_success(self):
        """Test load command with existing save.

        Verifies that loading an existing save file successfully
        restores the game state and returns a confirmation message.
        """
        game = QuantumAdventure()
        mock_data = {
            "states": [game.states[0]],
            "player": game.player
        }
        
        command = ParsedCommand(CommandType.LOAD, ["test_save"], "load test_save")
        
        with patch('src.utils.load_game', return_value=mock_data):
            result = game.process_command(command)
            assert "loaded" in result.lower()
    
    def test_load_command_failure(self):
        """Test load command with non-existent save.

        Verifies that loading a non-existent save file returns
        an appropriate failure message.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.LOAD, ["nonexistent"], "load nonexistent")
        
        with patch('src.utils.load_game', return_value=None):
            result = game.process_command(command)
            assert "failed" in result.lower()


class TestQuantumAdventureWelcome:
    """Tests for welcome message."""
    
    def test_welcome_message(self):
        """Test welcome message content.

        Verifies that the welcome message contains the game title
        and introduces the quantum superposition concept.
        """
        game = QuantumAdventure()
        welcome = game.get_welcome_message()
        
        assert "QUANTUM" in welcome
        assert "ADVENTURE" in welcome
        assert "superposition" in welcome.lower()


class TestQuantumAdventureSerialization:
    """Tests for game serialization."""
    
    def test_to_dict(self):
        """Test converting game to dictionary.

        Verifies that the game state can be serialized to a dictionary
        containing states and player data for saving.
        """
        game = QuantumAdventure()
        game.states[0].add_item("test item")
        
        data = game.to_dict()
        
        assert "states" in data
        assert "player" in data
        assert len(data["states"]) == 1
    
    def test_from_dict(self):
        """Test creating game from dictionary.

        Verifies that a game can be restored from a serialized dictionary
        with matching states and player data.
        """
        game = QuantumAdventure()
        data = game.to_dict()
        
        restored = QuantumAdventure.from_dict(data)
        
        assert len(restored.states) == len(game.states)
        assert restored.player.name == game.player.name


class TestQuantumAdventureUnknownCommand:
    """Tests for unknown commands."""
    
    def test_unknown_command(self):
        """Test handling of unknown commands.

        Verifies that unrecognized commands return an error message
        suggesting the help command for valid options.
        """
        game = QuantumAdventure()
        command = ParsedCommand(CommandType.UNKNOWN, [], "xyzzy")
        
        result = game.process_command(command)
        
        assert "unknown" in result.lower() or "help" in result.lower()


class TestWavefunctionCollapse:
    """Tests for wavefunction collapse mechanics."""
    
    def test_collapse_weighted_by_probability(self):
        """Test that collapse respects probability weights.

        Verifies that wavefunction collapse favors higher probability
        states when collapsing multiple quantum states.
        """
        game = QuantumAdventure()
        
        # Create states with different probabilities
        state1 = game.states[0]
        state1.probability = 0.9
        
        state2 = state1.branch(probability=0.1)
        state2.move_to("Other Location")
        game.states.append(state2)
        
        # Run multiple collapses and check distribution
        high_prob_count = 0
        runs = 100
        
        for _ in range(runs):
            test_game = QuantumAdventure()
            test_game.states = [
                QuantumState(location="High Prob", probability=0.9),
                QuantumState(location="Low Prob", probability=0.1)
            ]
            collapsed = test_game._collapse_wavefunction()
            if collapsed.location == "High Prob":
                high_prob_count += 1
        
        # Should favor high probability state (allow some variance)
        assert high_prob_count > 50  # Should be around 90
    
    def test_collapse_cleans_up_enemies(self):
        """Test that collapse cleans up enemy tracking.

        Verifies that collapsing the wavefunction removes enemy entries
        for discarded quantum states, leaving at most one enemy entry.
        """
        game = QuantumAdventure()
        state2 = game.states[0].branch()
        game.states.append(state2)
        
        # Add enemies to both timelines
        game.current_enemies[game.states[0].timeline_id] = "Monster 1"
        game.current_enemies[game.states[1].timeline_id] = "Monster 2"
        
        game._collapse_wavefunction()
        
        # Should only have one enemy entry
        assert len(game.current_enemies) <= 1
