"""
Quantum Adventure module - Main game logic.

This module contains the QuantumAdventure class which manages multiple
QuantumState instances in superposition. It handles the core mechanics
of probabilistic branching, wavefunction collapse, and game progression.
"""

import random
from typing import List, Optional, Tuple, Dict, Any

from .world import QuantumState, WorldBuilder, Location
from .player import Player, CommandParser, ParsedCommand, CommandType


class QuantumAdventure:
    """
    Main game class managing quantum superposition of game states.
    
    The QuantumAdventure maintains multiple QuantumState instances representing
    parallel realities. Player actions can affect all states, create new
    branches, or collapse the wavefunction to a single state.
    
    Key concepts:
    - Superposition: Multiple states exist simultaneously
    - Branching: Actions create new timeline branches with different outcomes
    - Collapse: Observing the world selects one state based on probability
    - Entanglement: Some actions affect all states uniformly
    
    Attributes:
        states: List of QuantumState instances in superposition.
        player: The Player instance.
        locations: Dictionary of all game locations.
        running: Whether the game loop should continue.
        current_enemies: Dict mapping location to current enemy encounter.
    """
    
    # Probability thresholds for various events
    BRANCH_PROBABILITY = 0.5      # Chance of branching on movement
    ITEM_APPEAR_PROBABILITY = 0.3 # Chance of item appearing
    ENEMY_APPEAR_PROBABILITY = 0.25 # Chance of enemy appearing
    
    def __init__(self, player_name: str = "Traveler"):
        """
        Initialize a new Quantum Adventure game.
        
        Args:
            player_name: Name for the player character.
        """
        self.player = Player(name=player_name)
        self.locations = WorldBuilder.initialize_world()
        
        # Start with a single state - the quantum superposition begins here
        initial_state = QuantumState(location="Quantum Nexus")
        initial_state.add_to_log("The adventure begins at the Quantum Nexus...")
        self.states: List[QuantumState] = [initial_state]
        
        self.running = True
        self.current_enemies: Dict[int, str] = {}  # timeline_id -> enemy name
    
    def get_current_location_info(self) -> str:
        """
        Get information about current location(s) across all states.
        
        When in superposition, shows that multiple realities exist.
        
        Returns:
            Formatted string describing current location(s).
        """
        if len(self.states) == 1:
            state = self.states[0]
            location = self.locations.get(state.location)
            if location:
                return self._format_location(location, state)
            return f"You are at: {state.location}"
        else:
            # Multiple states in superposition
            locations_summary = {}
            for state in self.states:
                loc = state.location
                if loc in locations_summary:
                    locations_summary[loc] += 1
                else:
                    locations_summary[loc] = 1
            
            result = "╔══════════════════════════════════════════════════════════════════════╗\n"
            result += "║        ⚛ QUANTUM SUPERPOSITION DETECTED ⚛                           ║\n"
            result += "╠══════════════════════════════════════════════════════════════════════╣\n"
            result += f"║ You exist in {len(self.states)} parallel realities simultaneously:              ║\n"
            for loc, count in locations_summary.items():
                prob = count / len(self.states) * 100
                result += f"║   • {loc}: {prob:.1f}% probability                              ║\n"
            result += "║                                                                       ║\n"
            result += "║ Use 'observe' to collapse into a single reality.                     ║\n"
            result += "║ Use 'status' to see details of all timelines.                        ║\n"
            result += "╚══════════════════════════════════════════════════════════════════════╝"
            return result
    
    def _format_location(self, location: Location, state: QuantumState) -> str:
        """Format a location description for display.

        Args:
            location: The Location object to format.
            state: The current QuantumState for context (e.g., enemy encounters).

        Returns:
            A formatted string with the location's details in a bordered box.
        """
        separator = "═" * 70
        result = f"╔{separator}╗\n"
        result += f"║ 📍 {location.name:65} ║\n"
        result += f"╠{separator}╣\n"
        
        # Word wrap the description
        desc_lines = self._wrap_text(location.description, 68)
        for line in desc_lines:
            result += f"║ {line:68} ║\n"
        
        result += f"╠{separator}╣\n"
        
        # Available directions
        directions = location.get_available_directions()
        if directions:
            dir_str = ", ".join(directions)
            result += f"║ Exits: {dir_str:61} ║\n"
        
        # Show if there are items here (probabilistic hint)
        if location.items:
            result += f"║ ✨ You sense potential items in this area...                         ║\n"
        
        # Show current enemy if any
        timeline_id = state.timeline_id
        if timeline_id in self.current_enemies:
            enemy = self.current_enemies[timeline_id]
            result += f"║ ⚔️ A {enemy} blocks your path!                                       ║\n"
        
        result += f"╚{separator}╝"
        return result
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width.

        Args:
            text: The text string to wrap.
            width: Maximum character width per line.

        Returns:
            A list of strings, each representing a wrapped line.
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def process_command(self, command: ParsedCommand) -> str:
        """
        Process a parsed command and return the result.
        
        This is the main command dispatcher that routes commands to
        their appropriate handlers.
        
        Args:
            command: The parsed command to process.
            
        Returns:
            String result of the command execution.
        """
        handlers = {
            CommandType.MOVE: self._handle_move,
            CommandType.LOOK: self._handle_look,
            CommandType.INVENTORY: self._handle_inventory,
            CommandType.TAKE: self._handle_take,
            CommandType.DROP: self._handle_drop,
            CommandType.USE: self._handle_use,
            CommandType.OBSERVE: self._handle_observe,
            CommandType.STATUS: self._handle_status,
            CommandType.HISTORY: self._handle_history,
            CommandType.ATTACK: self._handle_attack,
            CommandType.HELP: self._handle_help,
            CommandType.QUIT: self._handle_quit,
            CommandType.SAVE: self._handle_save,
            CommandType.LOAD: self._handle_load,
        }
        
        handler = handlers.get(command.command_type)
        if handler:
            return handler(command)
        else:
            return "Unknown command. Type 'help' for a list of commands."
    
    def _handle_move(self, command: ParsedCommand) -> str:
        """
        Handle movement commands.
        
        Movement in the quantum world is probabilistic. When moving to a
        location with multiple possible outcomes, the game branches into
        multiple timelines.
        """
        direction = command.get_first_arg()
        if not direction:
            return "Move where? Specify a direction (north, south, east, west, up, down)."
        
        # Movement affects all states, potentially creating branches
        new_states = []
        movement_results = []
        
        for state in self.states:
            location = self.locations.get(state.location)
            if not location:
                new_states.append(state)
                continue
            
            destination = location.get_destination(direction)
            if destination:
                # Check if this is a probabilistic movement (random branching)
                # Some movements might lead to different outcomes
                if random.random() < self.BRANCH_PROBABILITY and len(self.states) < 4:
                    # Create a branch - one timeline moves, one stays
                    # This simulates quantum uncertainty in choice
                    branch1 = state.branch(probability=0.5)
                    branch2 = state.branch(probability=0.5)
                    
                    branch1.move_to(destination)
                    branch1.add_to_log(f"Chose to go {direction}")
                    
                    branch2.add_to_log(f"Hesitated going {direction}")
                    
                    new_states.extend([branch1, branch2])
                    movement_results.append(
                        f"⚛ QUANTUM BRANCHING: Your decision to go {direction} "
                        f"creates parallel timelines!"
                    )
                    self.player.record_branch()
                else:
                    # Normal movement
                    state.move_to(destination)
                    new_states.append(state)
                    
                # Check for random encounters in new location
                self._check_random_events(state)
            else:
                new_states.append(state)
                movement_results.append(f"Cannot go {direction} from {state.location}.")
        
        self.states = new_states
        self.player.record_move()
        
        result = "\n".join(movement_results) if movement_results else ""
        result += "\n" + self.get_current_location_info()
        return result
    
    def _check_random_events(self, state: QuantumState) -> None:
        """Check for random item or enemy appearances.

        Probabilistically spawns items or enemies in the player's current
        location based on configured probability thresholds.

        Args:
            state: The QuantumState to check and potentially modify.
        """
        location = self.locations.get(state.location)
        if not location:
            return
        
        # Random item appearance
        if random.random() < self.ITEM_APPEAR_PROBABILITY:
            item = WorldBuilder.get_random_item_for_location(state.location)
            if item and item not in state.world_items.get(state.location, []):
                if state.location not in state.world_items:
                    state.world_items[state.location] = []
                state.world_items[state.location].append(item)
                state.add_to_log(f"A {item} materializes nearby!")
        
        # Random enemy appearance
        if random.random() < self.ENEMY_APPEAR_PROBABILITY:
            enemy = WorldBuilder.get_random_enemy_for_location(state.location)
            if enemy and enemy not in state.defeated_enemies:
                self.current_enemies[state.timeline_id] = enemy
                state.add_to_log(f"A {enemy} appears!")
    
    def _handle_look(self, command: ParsedCommand) -> str:
        """Handle look/examine commands.

        If no target is specified, displays the current location. Otherwise,
        examines a specific object in the inventory or world.

        Args:
            command: The parsed command containing optional target argument.

        Returns:
            A description of the location or examined object.
        """
        target = command.get_first_arg()
        
        if not target:
            # Look at current location
            return self.get_current_location_info()
        
        # Look at specific object
        results = []
        for state in self.states:
            if target in state.inventory:
                results.append(f"[Timeline {state.timeline_id}] You examine the {target}. "
                              f"It pulses with quantum energy.")
            elif target in state.world_items.get(state.location, []):
                results.append(f"[Timeline {state.timeline_id}] The {target} lies on the ground, "
                              f"waiting to be picked up.")
        
        if results:
            return "\n".join(results)
        return f"You don't see any '{target}' here."
    
    def _handle_inventory(self, command: ParsedCommand) -> str:
        """Handle inventory display.

        Shows the inventory contents for all active timelines in superposition.

        Args:
            command: The parsed command (no arguments used).

        Returns:
            A formatted inventory status display for all timelines.
        """
        results = []
        for state in self.states:
            inv_list = ", ".join(state.inventory) if state.inventory else "Empty"
            results.append(f"Timeline #{state.timeline_id} Inventory: {inv_list}")
        
        header = "╔══════════════════════════════════════════════════════════════════════╗\n"
        header += "║                        INVENTORY STATUS                              ║\n"
        header += "╠══════════════════════════════════════════════════════════════════════╣\n"
        
        body = ""
        for r in results:
            body += f"║ {r:68} ║\n"
        
        footer = "╚══════════════════════════════════════════════════════════════════════╝"
        
        return header + body + footer
    
    def _handle_take(self, command: ParsedCommand) -> str:
        """Handle taking items.

        Picks up an item from the current location across all timelines
        where the item exists.

        Args:
            command: The parsed command containing the item name to take.

        Returns:
            Result messages indicating success or failure per timeline.
        """
        item = command.get_all_args_as_string()
        if not item:
            return "Take what? Specify an item."
        
        results = []
        for state in self.states:
            available_items = state.world_items.get(state.location, [])
            if item in available_items:
                available_items.remove(item)
                state.add_item(item)
                results.append(f"[Timeline {state.timeline_id}] You pick up the {item}.")
                self.player.record_item_collected()
            elif item in [i.lower() for i in available_items]:
                # Case-insensitive match
                for actual_item in available_items:
                    if actual_item.lower() == item:
                        available_items.remove(actual_item)
                        state.add_item(actual_item)
                        results.append(f"[Timeline {state.timeline_id}] You pick up the {actual_item}.")
                        self.player.record_item_collected()
                        break
        
        if results:
            return "\n".join(results)
        return f"There is no '{item}' here to take."
    
    def _handle_drop(self, command: ParsedCommand) -> str:
        """Handle dropping items.

        Drops an item from inventory to the current location across all
        timelines where the player has the item.

        Args:
            command: The parsed command containing the item name to drop.

        Returns:
            Result messages indicating success or failure per timeline.
        """
        item = command.get_all_args_as_string()
        if not item:
            return "Drop what? Specify an item."
        
        results = []
        for state in self.states:
            if state.remove_item(item):
                if state.location not in state.world_items:
                    state.world_items[state.location] = []
                state.world_items[state.location].append(item)
                results.append(f"[Timeline {state.timeline_id}] You drop the {item}.")
        
        if results:
            return "\n".join(results)
        return f"You don't have '{item}' in your inventory."
    
    def _handle_use(self, command: ParsedCommand) -> str:
        """
        Handle using items.
        
        Using items triggers wavefunction collapse! The item's effect
        is determined probabilistically, and the superposition collapses
        to a single state.
        """
        item = command.get_all_args_as_string()
        if not item:
            return "Use what? Specify an item."
        
        # Check if any state has the item
        states_with_item = [s for s in self.states if s.has_item(item)]
        if not states_with_item:
            return f"You don't have '{item}' in any timeline."
        
        # Using items causes wavefunction collapse!
        result = "╔══════════════════════════════════════════════════════════════════════╗\n"
        result += "║           ⚛ WAVEFUNCTION COLLAPSE TRIGGERED! ⚛                       ║\n"
        result += "╠══════════════════════════════════════════════════════════════════════╣\n"
        result += f"║ Using the {item} causes reality to resolve...                        ║\n"
        result += "╚══════════════════════════════════════════════════════════════════════╝\n\n"
        
        # Collapse to a single state
        collapsed_state = self._collapse_wavefunction()
        
        # Apply item effect (probabilistic outcome)
        effect_roll = random.random()
        if effect_roll < 0.4:
            outcome = f"The {item} glows brightly and vanishes, leaving you feeling empowered!"
            collapsed_state.remove_item(item)
        elif effect_roll < 0.7:
            outcome = f"The {item} reacts unexpectedly but remains intact."
        else:
            outcome = f"The {item} transforms into something else!"
            collapsed_state.remove_item(item)
            new_item = random.choice(["quantum shard", "mystery orb", "temporal key", "void essence"])
            collapsed_state.add_item(new_item)
            outcome += f"\nYou now have a {new_item}!"
        
        collapsed_state.add_to_log(f"Used {item}: {outcome}")
        result += outcome
        result += "\n\n" + self.get_current_location_info()
        
        return result
    
    def _handle_observe(self, command: ParsedCommand) -> str:
        """
        Handle the observe command - collapse the wavefunction.
        
        This is the core quantum mechanic. When the player observes,
        all superposition states collapse to a single state, selected
        based on probability weights.
        """
        if len(self.states) == 1:
            return "Reality is already collapsed to a single timeline. No superposition to observe."
        
        result = "╔══════════════════════════════════════════════════════════════════════╗\n"
        result += "║                    ⚛ OBSERVATION EVENT ⚛                             ║\n"
        result += "╠══════════════════════════════════════════════════════════════════════╣\n"
        result += f"║ You focus your consciousness, collapsing {len(self.states)} parallel realities...   ║\n"
        result += "║                                                                       ║\n"
        
        # Show what was in superposition
        for state in self.states:
            prob_pct = state.probability / sum(s.probability for s in self.states) * 100
            result += f"║   Timeline #{state.timeline_id}: {state.location} ({prob_pct:.1f}% chance)         ║\n"
        
        result += "║                                                                       ║\n"
        result += "║ The quantum fog clears...                                             ║\n"
        result += "╚══════════════════════════════════════════════════════════════════════╝\n\n"
        
        # Perform the collapse
        collapsed_state = self._collapse_wavefunction()
        collapsed_state.add_to_log("Reality collapsed through observation!")
        
        result += f"✓ Collapsed to Timeline #{collapsed_state.timeline_id}: {collapsed_state.location}\n\n"
        result += self.get_current_location_info()
        
        return result
    
    def _collapse_wavefunction(self) -> QuantumState:
        """
        Collapse the wavefunction to a single state.
        
        Selection is weighted by the probability of each state.
        This simulates the probabilistic nature of quantum measurement.
        
        Returns:
            The selected QuantumState after collapse.
        """
        if len(self.states) == 1:
            return self.states[0]
        
        # Weighted random selection based on probability
        total_prob = sum(s.probability for s in self.states)
        r = random.random() * total_prob
        
        cumulative = 0
        selected = self.states[0]
        for state in self.states:
            cumulative += state.probability
            if r <= cumulative:
                selected = state
                break
        
        # Collapse to single state
        self.states = [selected]
        self.player.record_observation()
        
        # Clean up enemy tracking for other timelines
        valid_ids = {s.timeline_id for s in self.states}
        self.current_enemies = {
            k: v for k, v in self.current_enemies.items() 
            if k in valid_ids
        }
        
        return selected
    
    def _handle_status(self, command: ParsedCommand) -> str:
        """Display status of all states in superposition.

        Shows detailed information about each timeline including location,
        probability, and inventory.

        Args:
            command: The parsed command (no arguments used).

        Returns:
            A formatted status display showing all parallel realities.
        """
        result = "╔══════════════════════════════════════════════════════════════════════╗\n"
        result += "║                 QUANTUM SUPERPOSITION STATUS                         ║\n"
        result += "╠══════════════════════════════════════════════════════════════════════╣\n"
        result += f"║ Total parallel realities: {len(self.states):41} ║\n"
        result += "╠══════════════════════════════════════════════════════════════════════╣\n"
        
        total_prob = sum(s.probability for s in self.states)
        for state in self.states:
            prob_pct = state.probability / total_prob * 100
            result += f"║ Timeline #{state.timeline_id}:                                                    ║\n"
            result += f"║   Location: {state.location:55} ║\n"
            result += f"║   Probability: {prob_pct:.1f}%                                               ║\n"
            inv = ", ".join(state.inventory) if state.inventory else "Empty"
            if len(inv) > 50:
                inv = inv[:47] + "..."
            result += f"║   Inventory: {inv:54} ║\n"
            result += "╟──────────────────────────────────────────────────────────────────────╢\n"
        
        result += "╚══════════════════════════════════════════════════════════════════════╝"
        
        return result
    
    def _handle_history(self, command: ParsedCommand) -> str:
        """Display story log for all timelines.

        Shows the last 5 events from the story log for each active timeline.

        Args:
            command: The parsed command (no arguments used).

        Returns:
            A formatted history display showing recent events per timeline.
        """
        result = "╔══════════════════════════════════════════════════════════════════════╗\n"
        result += "║                        STORY LOG / HISTORY                           ║\n"
        result += "╠══════════════════════════════════════════════════════════════════════╣\n"
        
        for state in self.states:
            result += f"║ Timeline #{state.timeline_id}:                                                    ║\n"
            for event in state.story_log[-5:]:  # Show last 5 events
                if len(event) > 66:
                    event = event[:63] + "..."
                result += f"║   {event:66} ║\n"
            result += "╟──────────────────────────────────────────────────────────────────────╢\n"
        
        result += "╚══════════════════════════════════════════════════════════════════════╝"
        
        return result
    
    def _handle_attack(self, command: ParsedCommand) -> str:
        """Handle attacking enemies.

        Combat is probabilistic with a 60% success rate. Attacks the current
        enemy in each timeline, or a specific target if specified.

        Args:
            command: The parsed command containing optional target name.

        Returns:
            Result messages indicating combat outcomes per timeline.
        """
        target = command.get_all_args_as_string()
        
        results = []
        for state in self.states:
            enemy = self.current_enemies.get(state.timeline_id)
            if enemy:
                if not target or target.lower() in enemy.lower():
                    # Combat is probabilistic!
                    if random.random() < 0.6:  # 60% success rate
                        state.defeated_enemies.add(enemy)
                        del self.current_enemies[state.timeline_id]
                        state.add_to_log(f"Defeated the {enemy}!")
                        results.append(f"[Timeline {state.timeline_id}] You defeat the {enemy}!")
                        self.player.record_enemy_defeated()
                    else:
                        state.add_to_log(f"Failed attack on {enemy}")
                        results.append(f"[Timeline {state.timeline_id}] Your attack misses the {enemy}!")
                else:
                    results.append(f"[Timeline {state.timeline_id}] There's no {target} here, but a {enemy} threatens you!")
            else:
                results.append(f"[Timeline {state.timeline_id}] There's nothing to attack here.")
        
        if results:
            return "\n".join(results)
        return "There's nothing to attack."
    
    def _handle_help(self, command: ParsedCommand) -> str:
        """Display help text.

        Args:
            command: The parsed command (no arguments used).

        Returns:
            The help text listing all available commands.
        """
        return CommandParser.get_help_text()
    
    def _handle_quit(self, command: ParsedCommand) -> str:
        """Handle quit command.

        Sets the game running flag to False and returns a farewell message.

        Args:
            command: The parsed command (no arguments used).

        Returns:
            A farewell message to the player.
        """
        self.running = False
        return "Thank you for playing Quantum Text Adventure! All realities collapse..."
    
    def _handle_save(self, command: ParsedCommand) -> str:
        """Handle save command - delegates to utils.

        Saves the current game state to a file with the specified name.

        Args:
            command: The parsed command containing optional save name
                (defaults to "quicksave").

        Returns:
            A message indicating save success or failure.
        """
        from .utils import save_game
        
        save_name = command.get_first_arg() or "quicksave"
        success = save_game(self, save_name)
        
        if success:
            return f"Game saved as '{save_name}' with {len(self.states)} timeline(s)."
        return "Failed to save game."
    
    def _handle_load(self, command: ParsedCommand) -> str:
        """Handle load command - delegates to utils.

        Loads a previously saved game state from a file.

        Args:
            command: The parsed command containing optional save name
                (defaults to "quicksave").

        Returns:
            A message indicating load success or failure.
        """
        from .utils import load_game
        
        save_name = command.get_first_arg() or "quicksave"
        loaded = load_game(save_name)
        
        if loaded:
            self.states = loaded["states"]
            self.player = loaded["player"]
            return f"Game loaded from '{save_name}' with {len(self.states)} timeline(s)."
        return f"Failed to load game '{save_name}'. File may not exist."
    
    def is_running(self) -> bool:
        """Check if the game should continue running.

        Returns:
            True if the game loop should continue, False otherwise.
        """
        return self.running
    
    def get_welcome_message(self) -> str:
        """Return the game welcome/intro message.

        Returns:
            A formatted ASCII art welcome banner with game instructions.
        """
        return """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║             ⚛  QUANTUM TEXT ADVENTURE  ⚛                              ║
║                                                                       ║
║         Where Every Choice Creates Parallel Realities                 ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  Welcome, Traveler, to a world governed by quantum mechanics.         ║
║                                                                       ║
║  In this realm, your actions exist in superposition - multiple        ║
║  outcomes occur simultaneously across parallel timelines until        ║
║  you OBSERVE reality and collapse the wavefunction.                   ║
║                                                                       ║
║  QUANTUM RULES:                                                       ║
║  • Your choices may create branching timelines                        ║
║  • Multiple realities exist until you observe them                    ║
║  • Using items triggers wavefunction collapse                         ║
║  • Type 'help' to see all commands                                    ║
║                                                                       ║
║  The adventure begins now...                                          ║
║                                                                       ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary for serialization.

        Returns:
            A dictionary containing all game state data suitable for
            JSON serialization.
        """
        return {
            "states": [s.to_dict() for s in self.states],
            "player": self.player.to_dict(),
            "current_enemies": self.current_enemies
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuantumAdventure":
        """Create a QuantumAdventure from a dictionary.

        Args:
            data: A dictionary containing serialized game state data.

        Returns:
            A new QuantumAdventure instance restored from the saved data.
        """
        game = cls()
        game.states = [QuantumState.from_dict(s) for s in data["states"]]
        game.player = Player.from_dict(data["player"])
        game.current_enemies = data.get("current_enemies", {})
        return game
