"""
World module for Quantum Text Adventure.

This module defines the QuantumState class that represents a single possible
state of the game world, including location, inventory, and story log.
The state can be deep-copied to create branching timelines.
"""

import copy
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any


@dataclass
class Location:
    """
    Represents a location in the game world.
    
    Attributes:
        name: The name of this location.
        description: A detailed description of the location.
        connections: Dictionary mapping directions to connected location names.
        items: List of items that can be found at this location.
        enemies: List of potential enemies at this location.
        visited: Whether the player has visited this location.
    """
    name: str
    description: str
    connections: Dict[str, str] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)
    enemies: List[str] = field(default_factory=list)
    visited: bool = False
    
    def get_available_directions(self) -> List[str]:
        """Return list of available movement directions."""
        return list(self.connections.keys())
    
    def get_destination(self, direction: str) -> Optional[str]:
        """Get the destination location for a given direction."""
        return self.connections.get(direction.lower())


class QuantumState:
    """
    Represents a single possible state of the game world.
    
    A QuantumState encapsulates all information about one possible reality:
    - Current location
    - Player inventory
    - Story log of events
    - World state (items, enemies encountered, etc.)
    
    This class can be deep-copied to create branching timelines when
    probabilistic events occur.
    
    Attributes:
        location: Current location name.
        inventory: Set of items the player is carrying.
        story_log: List of events that have occurred in this timeline.
        world_items: Dict tracking items at each location.
        defeated_enemies: Set of enemies that have been defeated.
        probability: The probability weight of this state (for weighted collapse).
        timeline_id: Unique identifier for this timeline branch.
    """
    
    _timeline_counter: int = 0
    
    def __init__(
        self,
        location: str = "Quantum Nexus",
        inventory: Optional[Set[str]] = None,
        story_log: Optional[List[str]] = None,
        world_items: Optional[Dict[str, List[str]]] = None,
        defeated_enemies: Optional[Set[str]] = None,
        probability: float = 1.0,
        timeline_id: Optional[int] = None
    ):
        """
        Initialize a new QuantumState.
        
        Args:
            location: Starting location name.
            inventory: Initial inventory items.
            story_log: Initial story log entries.
            world_items: Initial state of items in the world.
            defeated_enemies: Initially defeated enemies.
            probability: Probability weight of this state.
            timeline_id: Unique identifier (auto-generated if None).
        """
        self.location = location
        self.inventory = inventory if inventory is not None else set()
        self.story_log = story_log if story_log is not None else []
        self.world_items = world_items if world_items is not None else {}
        self.defeated_enemies = defeated_enemies if defeated_enemies is not None else set()
        self.probability = probability
        
        # Assign unique timeline ID
        if timeline_id is None:
            QuantumState._timeline_counter += 1
            self.timeline_id = QuantumState._timeline_counter
        else:
            self.timeline_id = timeline_id
    
    def branch(self, probability: float = 1.0) -> "QuantumState":
        """
        Create a deep copy of this state for timeline branching.
        
        This is the core mechanism for quantum superposition - when a
        probabilistic event occurs, the current state branches into
        multiple possible realities.
        
        Args:
            probability: The probability weight for the new branch.
            
        Returns:
            A new QuantumState that is a deep copy of this one.
        """
        new_state = QuantumState(
            location=self.location,
            inventory=copy.deepcopy(self.inventory),
            story_log=copy.deepcopy(self.story_log),
            world_items=copy.deepcopy(self.world_items),
            defeated_enemies=copy.deepcopy(self.defeated_enemies),
            probability=probability,
            timeline_id=None  # Will generate new ID
        )
        return new_state
    
    def add_to_log(self, event: str) -> None:
        """Add an event to the story log."""
        self.story_log.append(f"[Timeline {self.timeline_id}] {event}")
    
    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory."""
        self.inventory.add(item)
        self.add_to_log(f"Acquired: {item}")
    
    def remove_item(self, item: str) -> bool:
        """
        Remove an item from inventory.
        
        Returns:
            True if item was removed, False if not in inventory.
        """
        if item in self.inventory:
            self.inventory.remove(item)
            self.add_to_log(f"Used/Lost: {item}")
            return True
        return False
    
    def has_item(self, item: str) -> bool:
        """Check if player has an item in inventory."""
        return item in self.inventory
    
    def move_to(self, new_location: str) -> None:
        """Move to a new location."""
        self.add_to_log(f"Traveled from {self.location} to {new_location}")
        self.location = new_location
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "location": self.location,
            "inventory": list(self.inventory),
            "story_log": self.story_log,
            "world_items": self.world_items,
            "defeated_enemies": list(self.defeated_enemies),
            "probability": self.probability,
            "timeline_id": self.timeline_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuantumState":
        """Create a QuantumState from a dictionary."""
        return cls(
            location=data["location"],
            inventory=set(data["inventory"]),
            story_log=data["story_log"],
            world_items=data["world_items"],
            defeated_enemies=set(data["defeated_enemies"]),
            probability=data["probability"],
            timeline_id=data["timeline_id"]
        )
    
    def __str__(self) -> str:
        """Return a string representation of this state."""
        return (
            f"Timeline #{self.timeline_id} (p={self.probability:.2f})\n"
            f"  Location: {self.location}\n"
            f"  Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}\n"
            f"  Events: {len(self.story_log)}"
        )
    
    def __repr__(self) -> str:
        return f"QuantumState(timeline={self.timeline_id}, location={self.location})"


class WorldBuilder:
    """
    Factory class for building the game world.
    
    This class defines all locations, their connections, items, and enemies.
    It provides methods to create the initial world state and look up
    location information.
    """
    
    # Define the game world with 5+ locations and branching choices
    LOCATIONS: Dict[str, Location] = {}
    
    @classmethod
    def initialize_world(cls) -> Dict[str, Location]:
        """
        Create and return all game locations.
        
        The world consists of interconnected locations with probabilistic
        elements like random items and enemy encounters.
        
        Returns:
            Dictionary mapping location names to Location objects.
        """
        cls.LOCATIONS = {
            "Quantum Nexus": Location(
                name="Quantum Nexus",
                description=(
                    "You stand at the Quantum Nexus, a swirling vortex of infinite "
                    "possibilities. Reality itself seems unstable here, flickering "
                    "between states. Paths lead in multiple directions, each one "
                    "potentially leading to a different fate."
                ),
                connections={
                    "north": "Probability Forest",
                    "south": "Collapsed Caverns",
                    "east": "Schrödinger's Laboratory",
                    "west": "Entanglement Garden"
                },
                items=["quantum compass"],
                enemies=[]
            ),
            "Probability Forest": Location(
                name="Probability Forest",
                description=(
                    "Massive trees tower overhead, their branches existing in multiple "
                    "positions simultaneously. The path ahead splits into countless "
                    "trails that merge and diverge unpredictably. You can hear whispers "
                    "from parallel versions of yourself on nearby paths."
                ),
                connections={
                    "south": "Quantum Nexus",
                    "north": "Observer's Peak",
                    "east": "Uncertainty Glade"
                },
                items=["probability seed", "branch key"],
                enemies=["Wandering Paradox", "Shadow Self"]
            ),
            "Collapsed Caverns": Location(
                name="Collapsed Caverns",
                description=(
                    "These ancient caves were once in superposition, existing as both "
                    "open and collapsed. An observer long ago fixed them in this state. "
                    "Crystals embedded in the walls still shimmer with quantum energy, "
                    "hinting at their former glory."
                ),
                connections={
                    "north": "Quantum Nexus",
                    "down": "Eigenstate Depths"
                },
                items=["collapsed crystal", "ancient scroll"],
                enemies=["Cave Specter", "Quantum Mole"]
            ),
            "Schrödinger's Laboratory": Location(
                name="Schrödinger's Laboratory",
                description=(
                    "A vast laboratory filled with impossible experiments. In the center "
                    "sits the famous box - you dare not open it. Beakers bubble with "
                    "liquids that are both poison and medicine. Notes scrawled on "
                    "chalkboards describe the mathematics of uncertainty."
                ),
                connections={
                    "west": "Quantum Nexus",
                    "up": "Observation Deck"
                },
                items=["uncertainty potion", "measurement device", "cat treat"],
                enemies=["Lab Assistant Ghost", "Unstable Experiment"]
            ),
            "Entanglement Garden": Location(
                name="Entanglement Garden",
                description=(
                    "A serene garden where pairs of flowers bloom in perfect synchronization, "
                    "no matter how far apart. Touch one, and its partner responds instantly. "
                    "The air hums with the energy of connected particles spanning infinite "
                    "distances."
                ),
                connections={
                    "east": "Quantum Nexus",
                    "north": "Superposition Springs"
                },
                items=["entangled flower", "quantum fertilizer"],
                enemies=["Jealous Gardener", "Thorn Elemental"]
            ),
            "Observer's Peak": Location(
                name="Observer's Peak",
                description=(
                    "Atop this mountain, you can see all possible realities at once. "
                    "The view is dizzying - countless versions of the world stretch "
                    "below, some similar, others wildly different. Here, observation "
                    "has supreme power."
                ),
                connections={
                    "south": "Probability Forest",
                    "east": "Observation Deck"
                },
                items=["all-seeing lens", "reality anchor"],
                enemies=["Peak Guardian", "Void Watcher"]
            ),
            "Uncertainty Glade": Location(
                name="Uncertainty Glade",
                description=(
                    "A peaceful clearing where nothing is certain. The grass may be "
                    "green or blue. The sun might be rising or setting. Even your "
                    "own existence feels questionable here. It's strangely peaceful."
                ),
                connections={
                    "west": "Probability Forest"
                },
                items=["uncertain gem", "probability cloak"],
                enemies=["Maybe Monster"]
            ),
            "Eigenstate Depths": Location(
                name="Eigenstate Depths",
                description=(
                    "Deep beneath the caverns, you find chambers where reality has "
                    "settled into fixed states. Each room is frozen in a single "
                    "configuration, immune to quantum effects. Ancient machinery "
                    "hums with stabilizing energy."
                ),
                connections={
                    "up": "Collapsed Caverns"
                },
                items=["eigenstate core", "stability matrix"],
                enemies=["Depth Dweller", "Fixed State Sentinel"]
            ),
            "Observation Deck": Location(
                name="Observation Deck",
                description=(
                    "A glass-enclosed platform where scientists once watched quantum "
                    "experiments unfold. Massive telescopes and measurement devices "
                    "line the walls. From here, you can collapse any superposition "
                    "in the world below."
                ),
                connections={
                    "down": "Schrödinger's Laboratory",
                    "west": "Observer's Peak"
                },
                items=["observer's badge", "collapse trigger"],
                enemies=["Measurement Error", "Observer's Paradox"]
            ),
            "Superposition Springs": Location(
                name="Superposition Springs",
                description=(
                    "Hot springs that are simultaneously frozen and boiling. The water "
                    "is both refreshing and scalding. Bathing here is said to split "
                    "your consciousness across realities, granting visions of other "
                    "timelines."
                ),
                connections={
                    "south": "Entanglement Garden"
                },
                items=["quantum water vial", "vision stone"],
                enemies=["Spring Spirit", "Temperature Phantom"]
            )
        }
        
        return cls.LOCATIONS
    
    @classmethod
    def get_location(cls, name: str) -> Optional[Location]:
        """Get a location by name."""
        if not cls.LOCATIONS:
            cls.initialize_world()
        return cls.LOCATIONS.get(name)
    
    @classmethod
    def get_all_location_names(cls) -> List[str]:
        """Get a list of all location names."""
        if not cls.LOCATIONS:
            cls.initialize_world()
        return list(cls.LOCATIONS.keys())
    
    @classmethod
    def get_random_item_for_location(cls, location_name: str) -> Optional[str]:
        """
        Get a random item that might appear at a location.
        
        Items have a 30% chance of appearing when first visiting a location.
        This creates probabilistic world states.
        """
        location = cls.get_location(location_name)
        if location and location.items and random.random() < 0.3:
            return random.choice(location.items)
        return None
    
    @classmethod
    def get_random_enemy_for_location(cls, location_name: str) -> Optional[str]:
        """
        Get a random enemy that might appear at a location.
        
        Enemies have a 25% chance of appearing, creating probabilistic
        encounters across different timeline branches.
        """
        location = cls.get_location(location_name)
        if location and location.enemies and random.random() < 0.25:
            return random.choice(location.enemies)
        return None
