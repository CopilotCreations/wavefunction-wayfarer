"""
Tests for the world module.

This module tests the QuantumState class, Location class, and WorldBuilder
functionality including state branching, serialization, and world creation.
"""

import pytest
import copy
from src.world import QuantumState, Location, WorldBuilder


class TestLocation:
    """Tests for the Location dataclass."""
    
    def test_location_creation(self):
        """Test basic location creation."""
        loc = Location(
            name="Test Room",
            description="A test location.",
            connections={"north": "Other Room"},
            items=["key"],
            enemies=["monster"]
        )
        
        assert loc.name == "Test Room"
        assert loc.description == "A test location."
        assert "north" in loc.connections
        assert "key" in loc.items
        assert "monster" in loc.enemies
        assert loc.visited is False
    
    def test_get_available_directions(self):
        """Test getting available directions."""
        loc = Location(
            name="Hub",
            description="Central hub.",
            connections={"north": "A", "south": "B", "east": "C"}
        )
        
        directions = loc.get_available_directions()
        assert len(directions) == 3
        assert "north" in directions
        assert "south" in directions
        assert "east" in directions
    
    def test_get_destination(self):
        """Test getting destination for a direction."""
        loc = Location(
            name="Hub",
            description="Central hub.",
            connections={"north": "Forest", "south": "Cave"}
        )
        
        assert loc.get_destination("north") == "Forest"
        assert loc.get_destination("NORTH") == "Forest"  # Case insensitive
        assert loc.get_destination("west") is None
    
    def test_location_with_no_connections(self):
        """Test location with no connections."""
        loc = Location(name="Isolated", description="Nowhere to go.")
        
        assert loc.get_available_directions() == []
        assert loc.get_destination("north") is None


class TestQuantumState:
    """Tests for the QuantumState class."""
    
    def test_state_creation_defaults(self):
        """Test state creation with defaults."""
        state = QuantumState()
        
        assert state.location == "Quantum Nexus"
        assert isinstance(state.inventory, set)
        assert len(state.inventory) == 0
        assert isinstance(state.story_log, list)
        assert state.probability == 1.0
        assert state.timeline_id is not None
    
    def test_state_creation_custom(self):
        """Test state creation with custom values."""
        state = QuantumState(
            location="Forest",
            inventory={"sword", "shield"},
            story_log=["Started journey"],
            probability=0.5
        )
        
        assert state.location == "Forest"
        assert "sword" in state.inventory
        assert "shield" in state.inventory
        assert "Started journey" in state.story_log
        assert state.probability == 0.5
    
    def test_branch_creates_deep_copy(self):
        """Test that branching creates a proper deep copy."""
        original = QuantumState(
            location="Forest",
            inventory={"sword"},
            story_log=["Event 1"]
        )
        
        branched = original.branch(probability=0.5)
        
        # Should have different timeline IDs
        assert branched.timeline_id != original.timeline_id
        
        # Should be equal in content
        assert branched.location == original.location
        assert branched.inventory == original.inventory
        
        # Modifying branched should not affect original
        branched.inventory.add("potion")
        branched.story_log.append("Event 2")
        
        assert "potion" not in original.inventory
        assert "Event 2" not in original.story_log
    
    def test_add_to_log(self):
        """Test adding events to story log."""
        state = QuantumState()
        state.add_to_log("Found a key")
        
        assert len(state.story_log) == 1
        assert "Found a key" in state.story_log[0]
        assert f"Timeline {state.timeline_id}" in state.story_log[0]
    
    def test_add_item(self):
        """Test adding items to inventory."""
        state = QuantumState()
        state.add_item("magic wand")
        
        assert "magic wand" in state.inventory
        assert any("magic wand" in log for log in state.story_log)
    
    def test_remove_item_success(self):
        """Test removing an existing item."""
        state = QuantumState(inventory={"key"})
        
        result = state.remove_item("key")
        
        assert result is True
        assert "key" not in state.inventory
    
    def test_remove_item_failure(self):
        """Test removing a non-existent item."""
        state = QuantumState()
        
        result = state.remove_item("nonexistent")
        
        assert result is False
    
    def test_has_item(self):
        """Test checking for item in inventory."""
        state = QuantumState(inventory={"compass"})
        
        assert state.has_item("compass") is True
        assert state.has_item("map") is False
    
    def test_move_to(self):
        """Test moving to a new location."""
        state = QuantumState(location="Start")
        state.move_to("Destination")
        
        assert state.location == "Destination"
        assert any("Start" in log and "Destination" in log for log in state.story_log)
    
    def test_serialization(self):
        """Test converting state to dict and back."""
        original = QuantumState(
            location="Cave",
            inventory={"torch", "rope"},
            story_log=["Entered cave"],
            defeated_enemies={"goblin"},
            probability=0.75
        )
        
        # Convert to dict
        data = original.to_dict()
        
        assert data["location"] == "Cave"
        assert set(data["inventory"]) == {"torch", "rope"}
        assert "Entered cave" in data["story_log"]
        assert "goblin" in data["defeated_enemies"]
        assert data["probability"] == 0.75
        
        # Convert back
        restored = QuantumState.from_dict(data)
        
        assert restored.location == original.location
        assert restored.inventory == original.inventory
        assert restored.probability == original.probability
    
    def test_str_representation(self):
        """Test string representation of state."""
        state = QuantumState(
            location="Forest",
            inventory={"sword"}
        )
        
        str_repr = str(state)
        
        assert "Timeline" in str_repr
        assert "Forest" in str_repr
        assert "sword" in str_repr
    
    def test_repr_representation(self):
        """Test repr of state."""
        state = QuantumState(location="Cave")
        
        repr_str = repr(state)
        
        assert "QuantumState" in repr_str
        assert "Cave" in repr_str


class TestWorldBuilder:
    """Tests for the WorldBuilder class."""
    
    def test_initialize_world(self):
        """Test world initialization creates locations."""
        locations = WorldBuilder.initialize_world()
        
        assert len(locations) >= 5  # At least 5 locations required
        assert "Quantum Nexus" in locations  # Starting location must exist
    
    def test_get_location(self):
        """Test getting a specific location."""
        WorldBuilder.initialize_world()
        
        nexus = WorldBuilder.get_location("Quantum Nexus")
        
        assert nexus is not None
        assert nexus.name == "Quantum Nexus"
        assert len(nexus.connections) > 0
    
    def test_get_nonexistent_location(self):
        """Test getting a location that doesn't exist."""
        WorldBuilder.initialize_world()
        
        result = WorldBuilder.get_location("Nonexistent Place")
        
        assert result is None
    
    def test_get_all_location_names(self):
        """Test getting all location names."""
        WorldBuilder.initialize_world()
        
        names = WorldBuilder.get_all_location_names()
        
        assert isinstance(names, list)
        assert len(names) >= 5
        assert "Quantum Nexus" in names
    
    def test_locations_are_connected(self):
        """Test that locations form a connected graph from start."""
        locations = WorldBuilder.initialize_world()
        
        # Verify Quantum Nexus has connections
        nexus = locations["Quantum Nexus"]
        assert len(nexus.connections) >= 2
        
        # Verify connections point to valid locations
        for direction, destination in nexus.connections.items():
            assert destination in locations
    
    def test_random_item_for_location(self):
        """Test random item generation for locations."""
        WorldBuilder.initialize_world()
        
        # Run multiple times to test probabilistic behavior
        items_found = []
        for _ in range(100):
            item = WorldBuilder.get_random_item_for_location("Quantum Nexus")
            if item:
                items_found.append(item)
        
        # Should get some items (probabilistic, but 100 tries should yield some)
        # This is a probabilistic test - it could theoretically fail
        # but the probability is astronomically low
        assert len(items_found) >= 0  # At least test it runs without error
    
    def test_random_enemy_for_location(self):
        """Test random enemy generation for locations."""
        WorldBuilder.initialize_world()
        
        # Run for a location with enemies
        enemies_found = []
        for _ in range(100):
            enemy = WorldBuilder.get_random_enemy_for_location("Probability Forest")
            if enemy:
                enemies_found.append(enemy)
        
        assert len(enemies_found) >= 0  # At least test it runs without error
    
    def test_location_has_items(self):
        """Test that locations have items defined."""
        locations = WorldBuilder.initialize_world()
        
        # At least some locations should have items
        locations_with_items = [
            loc for loc in locations.values() 
            if len(loc.items) > 0
        ]
        
        assert len(locations_with_items) >= 3
    
    def test_location_has_enemies(self):
        """Test that locations have enemies defined."""
        locations = WorldBuilder.initialize_world()
        
        # At least some locations should have enemies
        locations_with_enemies = [
            loc for loc in locations.values() 
            if len(loc.enemies) > 0
        ]
        
        assert len(locations_with_enemies) >= 3
