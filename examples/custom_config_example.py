#!/usr/bin/env python3
"""Example: Custom game configuration for Battalion simulator."""

import sys
sys.path.insert(0, '../simulator')

from battalion_simulator import simulate_game, GameConfig

# Create aggressive, fast-paced variant
fast_config = GameConfig(
    tower_base_hp=3,              # Easier to eliminate (default: 4)
    starting_influence=8,         # More resources (default: 6)
    troop_deck_size=60,           # Smaller deck = faster games (default: 115)
    attack_chains_allowed=3,      # Allow consecutive attacks (default: 1)
    leader_contract_cost=2,       # Cheaper leaders (default: 3)
)

print("🎮 Running fast-paced Battalion variant...")
print(f"   - Tower HP: {fast_config.tower_base_hp}")
print(f"   - Starting Influence: {fast_config.starting_influence}")
print(f"   - Troop Deck: {fast_config.troop_deck_size}")
print("")

result = simulate_game(num_players=4, config=fast_config, detailed_log=False)

print(f"✅ Game Complete!")
print(f"   Winner: Player {result['winner']}")
print(f"   Game Length: {result['turn_count']} turns")
print(f"   Elimination Victory: {result.get('elimination_victory', False)}")
