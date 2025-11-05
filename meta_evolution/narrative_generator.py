#!/usr/bin/env python3
"""
Battalion Verbose Game Narrative Generator
==========================================

Generates human-readable narratives from simulation data to show
if the game is actually fun, not just statistically sound.

Selects the most exciting game based on:
- Dramatic moments (eliminations, comebacks, close calls)
- Combat frequency and variety
- Strategic coherence
- Emotional peaks
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class GameMoment:
    """A significant moment in the game."""
    turn: int
    player: int
    moment_type: str  # 'attack', 'elimination', 'comeback', 'card_combo', etc.
    description: str
    excitement_value: float


def calculate_excitement_score(game_data: Dict) -> float:
    """
    Calculate excitement score for a single game.

    Higher score = more dramatic, memorable game
    """
    score = 0.0

    # Eliminations (major excitement)
    eliminations = game_data.get('eliminations', 0)
    score += eliminations * 2.0

    # Close combats (decided by ±2 troops)
    nail_biters = game_data.get('nail_biter_combats', 0)
    score += nail_biters * 0.5

    # Comebacks (player went from behind to ahead)
    comebacks = game_data.get('comeback_attempts', 0)
    score += comebacks * 1.5

    # Overkills (tower destroyed with excess damage)
    overkills = game_data.get('overkill_events', 0)
    score += overkills * 0.3

    # First blood (first attack/elimination)
    if game_data.get('first_blood_turn', 999) < 10:
        score += 1.0

    # Dramatic finish (1 tower vs 1 tower)
    if game_data.get('final_tower_gap', 3) <= 1:
        score += 1.5

    # Combat frequency (attacks per turn)
    attacks = game_data.get('total_attacks', 0)
    turns = game_data.get('turns', 20)
    attacks_per_turn = attacks / turns if turns > 0 else 0
    if attacks_per_turn > 0.5:
        score += attacks_per_turn

    # Card variety (different card types played)
    unique_cards = len(game_data.get('cards_played_types', []))
    score += unique_cards * 0.2

    # Normalize to 0-10 scale (typical max ~15-20)
    return min(10.0, score)


def select_most_exciting_game(games_data: List[Dict]) -> Tuple[Dict, float]:
    """
    Select the most exciting game from a list of game results.

    Returns:
        (game_data, excitement_score)
    """
    best_game = None
    best_score = 0.0

    for game in games_data:
        score = calculate_excitement_score(game)
        if score > best_score:
            best_score = score
            best_game = game

    return best_game, best_score


def generate_game_narrative(game_data: Dict, genome: Dict) -> str:
    """
    Generate human-readable narrative of a game.

    Args:
        game_data: Complete game simulation data
        genome: Genome parameters that generated this game

    Returns:
        Formatted narrative string
    """
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append("MOST EXCITING GAME NARRATIVE")
    lines.append("=" * 80)
    lines.append("")

    # Game setup
    player_count = game_data.get('player_count', 4)
    players = game_data.get('players', [])

    lines.append(f"Setup: {player_count}P game")
    for i, player in enumerate(players):
        strategy = player.get('strategy', 'UNKNOWN')
        lines.append(f"  P{i}: {strategy}")
    lines.append("")

    # Genome configuration (highlight key mechanics)
    lines.append("Key Mechanics:")
    if genome.get('enable_optional_blocking'):
        lines.append("  ✓ Optional Blocking ENABLED (MTG-style)")
    if genome.get('enable_bypass_attacks'):
        bypass_dmg = genome.get('bypass_damage_amount', 2)
        lines.append(f"  ✓ Bypass Attacks ENABLED ({bypass_dmg} tower damage)")

    # Notable card composition
    notable_cards = []
    for card_type in ['battle_frenzy', 'blitzkrieg', 'siege_attack', 'tactical_retreat']:
        count_key = f"{card_type}_count"
        if count_key in genome and genome[count_key] > 0:
            notable_cards.append(f"{card_type.replace('_', ' ').title()} x{genome[count_key]}")
    if notable_cards:
        lines.append(f"  Cards: {', '.join(notable_cards[:4])}")
    lines.append("")

    # Turn-by-turn narrative (key moments only)
    lines.append("Key Moments:")
    lines.append("")

    moments = extract_key_moments(game_data)
    for moment in moments:
        lines.append(format_moment(moment))

    # Game conclusion
    lines.append("")
    lines.append("=" * 80)
    winner_id = game_data.get('winner', 0)
    winner_strategy = players[winner_id].get('strategy', 'UNKNOWN') if winner_id < len(players) else 'UNKNOWN'
    turns = game_data.get('turns', 0)
    win_condition = "Elimination" if not game_data.get('troop_deck_depleted', False) else "Deck Depletion"

    lines.append(f"Winner: P{winner_id} ({winner_strategy}) - {win_condition} on turn {turns}")
    lines.append("")

    # Statistics
    lines.append("Game Statistics:")
    lines.append(f"  Total Attacks:      {game_data.get('total_attacks', 0)}")
    lines.append(f"  Eliminations:       {game_data.get('eliminations', 0)}")
    lines.append(f"  Close Combats:      {game_data.get('nail_biter_combats', 0)}")
    lines.append(f"  Cards Played:       {game_data.get('total_cards_played', 0)}")
    lines.append(f"  Avg Cards/Turn:     {game_data.get('avg_cards_per_turn', 0.0):.2f}")
    lines.append("")

    # Card highlights
    cards_played = game_data.get('cards_played_types', [])
    if cards_played:
        from collections import Counter
        card_counts = Counter(cards_played)
        lines.append("Most Played Cards:")
        for card, count in card_counts.most_common(5):
            lines.append(f"  {card}: {count}x")
        lines.append("")

    # Excitement rating
    excitement = calculate_excitement_score(game_data)
    lines.append(f"Excitement Score: {excitement:.1f}/10.0")

    # Breakdown
    lines.append("  Excitement Sources:")
    if game_data.get('eliminations', 0) > 0:
        lines.append(f"    ✓ {game_data['eliminations']} eliminations")
    if game_data.get('comeback_attempts', 0) > 0:
        lines.append(f"    ✓ {game_data['comeback_attempts']} comeback attempts")
    if game_data.get('nail_biter_combats', 0) > 0:
        lines.append(f"    ✓ {game_data['nail_biter_combats']} close combats")

    attacks = game_data.get('total_attacks', 0)
    turns_total = game_data.get('turns', 20)
    if attacks > 0 and turns_total > 0:
        lines.append(f"    ✓ {attacks/turns_total:.2f} attacks/turn (high engagement)")

    lines.append("")
    lines.append("=" * 80)

    return "\n".join(lines)


def extract_key_moments(game_data: Dict) -> List[GameMoment]:
    """
    Extract key moments from game data for narrative.

    Prioritizes:
    - First attack
    - Eliminations
    - Comebacks
    - Large combats
    - Final turns
    """
    moments = []

    # Parse turn-by-turn data if available
    turn_log = game_data.get('turn_log', [])

    if turn_log:
        for turn_data in turn_log:
            turn_num = turn_data.get('turn', 0)

            # Attacks
            for attack in turn_data.get('attacks', []):
                attacker = attack.get('attacker', 0)
                defender = attack.get('defender', 0)
                attacker_troops = attack.get('attacker_troops', 0)
                defender_troops = attack.get('defender_troops', 0)
                towers_destroyed = attack.get('towers_destroyed', 0)
                blocked = attack.get('blocked', True)

                excitement = 0.5
                if towers_destroyed > 0:
                    excitement += towers_destroyed * 0.5
                if abs(attacker_troops - defender_troops) <= 2:
                    excitement += 0.3  # Close call
                if not blocked:
                    excitement += 0.2  # Unblocked attack

                desc_parts = [f"P{attacker} attacks P{defender}"]
                desc_parts.append(f"({attacker_troops} vs {defender_troops} troops)")

                if not blocked:
                    desc_parts.append("- Defender chooses NOT to block!")
                if towers_destroyed > 0:
                    desc_parts.append(f"→ {towers_destroyed} tower(s) destroyed")

                moments.append(GameMoment(
                    turn=turn_num,
                    player=attacker,
                    moment_type='attack',
                    description=' '.join(desc_parts),
                    excitement_value=excitement
                ))

            # Eliminations
            for elimination in turn_data.get('eliminations', []):
                player_id = elimination.get('player', 0)
                eliminated_by = elimination.get('eliminated_by', 0)

                moments.append(GameMoment(
                    turn=turn_num,
                    player=eliminated_by,
                    moment_type='elimination',
                    description=f"P{player_id} ELIMINATED by P{eliminated_by}! (First blood)" if len([m for m in moments if m.moment_type == 'elimination']) == 0 else f"P{player_id} eliminated by P{eliminated_by}",
                    excitement_value=2.0
                ))

            # Major card plays
            for card_play in turn_data.get('cards', []):
                player_id = card_play.get('player', 0)
                card_type = card_play.get('type', 'UNKNOWN')
                effect = card_play.get('effect', '')

                # Only highlight dramatic cards
                if card_type in ['BLITZKRIEG', 'SIEGE_ATTACK', 'PYRRHIC_VICTORY', 'MOMENTUM']:
                    moments.append(GameMoment(
                        turn=turn_num,
                        player=player_id,
                        moment_type='card_play',
                        description=f"P{player_id} plays {card_type} → {effect}",
                        excitement_value=0.8
                    ))
    else:
        # Fallback: generate generic moments from aggregate data
        moments.append(GameMoment(
            turn=1,
            player=0,
            moment_type='game_start',
            description="Game begins - all players at 3 towers, building armies",
            excitement_value=0.1
        ))

        # Estimate first attack turn
        total_attacks = game_data.get('total_attacks', 0)
        if total_attacks > 0:
            moments.append(GameMoment(
                turn=5,
                player=0,
                moment_type='first_attack',
                description=f"First attack launched - combat begins! ({total_attacks} total attacks this game)",
                excitement_value=1.0
            ))

        # Eliminations
        eliminations = game_data.get('eliminations', 0)
        if eliminations > 0:
            moments.append(GameMoment(
                turn=10,
                player=0,
                moment_type='elimination',
                description=f"First elimination! ({eliminations} total eliminations)",
                excitement_value=2.0
            ))

    # Sort by turn, then by excitement
    moments.sort(key=lambda m: (m.turn, -m.excitement_value))

    # Keep only top 10-12 most exciting moments
    # Group by turn to avoid repetition
    selected_moments = []
    moments_per_turn = {}

    for moment in moments:
        if moment.turn not in moments_per_turn:
            moments_per_turn[moment.turn] = []
        moments_per_turn[moment.turn].append(moment)

    # Select best 1-2 moments per turn, up to 12 total
    for turn in sorted(moments_per_turn.keys()):
        turn_moments = sorted(moments_per_turn[turn], key=lambda m: -m.excitement_value)
        selected_moments.extend(turn_moments[:2])
        if len(selected_moments) >= 12:
            break

    return selected_moments[:12]


def format_moment(moment: GameMoment) -> str:
    """Format a single moment for narrative output."""
    icon = {
        'attack': '⚔️',
        'elimination': '💀',
        'card_play': '🃏',
        'comeback': '🔄',
        'first_attack': '⚡',
        'game_start': '🎮',
    }.get(moment.moment_type, '•')

    return f"Turn {moment.turn:2d}: {icon} {moment.description}"


def generate_generation_summary_narrative(generation_data: Dict, generation_num: int) -> str:
    """
    Generate a summary narrative for an entire generation.

    Shows the best genome's most exciting game.
    """
    lines = []

    lines.append("")
    lines.append("=" * 80)
    lines.append(f"GENERATION {generation_num} - BEST GENOME SHOWCASE")
    lines.append("=" * 80)
    lines.append("")

    # Best genome stats
    best_genome = generation_data.get('best_genome', {})
    best_fitness = generation_data.get('best_fitness', 0.0)
    best_results = generation_data.get('best_results', {})

    lines.append(f"Best Fitness: {best_fitness:.1f} points")
    lines.append(f"Elimination Rate: {best_results.get('elimination_rate', 0)*100:.1f}%")
    lines.append(f"Avg Game Length: {best_results.get('avg_turns', 0):.1f} turns")
    lines.append(f"Attacks/Game: {best_results.get('avg_attacks', 0):.1f}")
    lines.append("")

    # Select most exciting game from best genome's simulations
    games = best_results.get('games_data', [])
    if games:
        best_game, excitement = select_most_exciting_game(games)
        lines.append(f"Showcasing most exciting game (excitement: {excitement:.1f}/10.0):")
        lines.append("")
        lines.append(generate_game_narrative(best_game, best_genome))
    else:
        lines.append("(No game data available for narrative generation)")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    print("Battalion Narrative Generator - Test Mode")
    print()

    test_game = {
        'player_count': 4,
        'players': [
            {'strategy': 'RUSH'},
            {'strategy': 'FORTRESS'},
            {'strategy': 'TEMPO'},
            {'strategy': 'ADAPTIVE'},
        ],
        'winner': 0,
        'turns': 18,
        'troop_deck_depleted': False,
        'total_attacks': 12,
        'eliminations': 3,
        'nail_biter_combats': 4,
        'comeback_attempts': 1,
        'total_cards_played': 54,
        'avg_cards_per_turn': 3.0,
        'cards_played_types': ['BLITZKRIEG', 'ATTACK', 'ATTACK', 'TACTICAL_RETREAT', 'BLITZKRIEG', 'SIEGE_ATTACK'],
        'first_blood_turn': 6,
        'final_tower_gap': 1,
        'overkill_events': 2,
    }

    test_genome = {
        'enable_optional_blocking': True,
        'enable_bypass_attacks': True,
        'bypass_damage_amount': 3,
        'battle_frenzy_count': 2,
        'blitzkrieg_count': 4,
        'tactical_retreat_count': 6,
    }

    excitement = calculate_excitement_score(test_game)
    print(f"Excitement Score: {excitement:.1f}/10.0")
    print()

    narrative = generate_game_narrative(test_game, test_genome)
    print(narrative)
