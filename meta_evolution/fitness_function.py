#!/usr/bin/env python3
"""
Battalion Meta-Evolution Fitness Function
==========================================

Comprehensive fitness scoring based on Universal Game Design Principles.

Scoring System:
- Core Fitness: 400 pts (playability, depth, pacing, engagement)
- Universal Principles: 500 pts (20 principles × 0-100, averaged × 5.0)
- Exploration Bonus: +200 pts (novelty, extreme viability)
- Variance Penalties: -300 pts max (pathology detection)
- Elimination Multiplier: 0.5× to 2.0× (CRITICAL constraint)

Total Range: -100 to 1,100 points (theoretical max: 1,100 × 2.0 = 2,200)
Typical Range: 200-1,200 points
Excellence Threshold: 800+ points
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
import statistics


@dataclass
class FitnessBreakdown:
    """Detailed breakdown of fitness scoring for transparency."""

    # Core components (400 pts)
    playability_score: float = 0.0
    strategic_depth_score: float = 0.0
    pacing_score: float = 0.0
    engagement_score: float = 0.0
    core_fitness: float = 0.0

    # Universal Principles (500 pts)
    principle_scores: Dict[str, float] = None
    principles_average: float = 0.0
    principles_bonus: float = 0.0

    # Exploration bonus (200 pts)
    novelty_score: float = 0.0
    extreme_viability_score: float = 0.0
    exploration_bonus: float = 0.0

    # Variance penalties (-300 pts)
    high_variance_penalty: float = 0.0
    low_differentiation_penalty: float = 0.0
    runaway_leader_penalty: float = 0.0
    variance_penalties: float = 0.0

    # Elimination multiplier (0.5× to 2.0×)
    elimination_rate: float = 0.0
    elimination_multiplier: float = 1.0

    # Final score
    pre_multiplier_score: float = 0.0
    final_score: float = 0.0

    def __post_init__(self):
        if self.principle_scores is None:
            self.principle_scores = {}


def calculate_core_fitness(game_stats: Dict) -> Tuple[float, Dict[str, float]]:
    """
    Calculate Core Fitness (400 pts total)

    Components:
    - Playability (100 pts): Can players actually play?
    - Strategic Depth (100 pts): Do choices matter?
    - Pacing (100 pts): Is the game experience well-timed?
    - Engagement (100 pts): Are players doing interesting things?
    """
    breakdown = {}

    # 1. PLAYABILITY (100 pts) - Critical: game must be playable
    dead_hand_rate = game_stats.get('dead_hand_rate', 0.15)  # % of turns gridlocked
    infinite_loops = game_stats.get('infinite_loops', 0)
    avg_turns = game_stats.get('avg_turns', 25)

    playability = 100.0

    # Dead hand penalty (primary playability issue)
    if dead_hand_rate < 0.05:
        playability = 100.0
    elif dead_hand_rate < 0.10:
        playability = 90.0 - (dead_hand_rate - 0.05) * 200  # Gradient 90→80
    elif dead_hand_rate < 0.15:
        playability = 70.0 - (dead_hand_rate - 0.10) * 400  # Gradient 70→50
    else:
        playability = max(0, 50.0 - (dead_hand_rate - 0.15) * 500)  # Steep drop

    # Infinite loop killer
    if infinite_loops > 0:
        playability *= 0.5

    # Game completion check (must finish in reasonable time)
    if avg_turns > 60:
        playability *= 0.7  # Too long = playability issue

    breakdown['playability'] = playability

    # 2. STRATEGIC DEPTH (100 pts) - Do choices matter?
    strategy_balance = game_stats.get('strategy_balance', {})
    win_rates = list(strategy_balance.values()) if strategy_balance else [25.0]

    strategic_depth = 100.0

    if len(win_rates) >= 3:
        # All strategies should win 15-35% (in 4P)
        min_rate = min(win_rates)
        max_rate = max(win_rates)
        spread = max_rate - min_rate

        # Perfect: all within 15-35%, spread < 15%
        if min_rate >= 15 and max_rate <= 35 and spread < 15:
            strategic_depth = 100.0
        elif min_rate >= 10 and max_rate <= 40 and spread < 20:
            strategic_depth = 85.0
        elif min_rate >= 5 and max_rate <= 45 and spread < 30:
            strategic_depth = 65.0
        else:
            # Penalty for extreme imbalance
            imbalance = max(abs(min_rate - 20), abs(max_rate - 30))
            strategic_depth = max(0, 100 - imbalance * 2)

    # Comeback potential
    comeback_rate = game_stats.get('comeback_rate', 0.15)
    if comeback_rate > 0.20:
        strategic_depth = min(100, strategic_depth + 10)  # Bonus for depth
    elif comeback_rate < 0.05:
        strategic_depth *= 0.8  # Penalty for deterministic outcomes

    breakdown['strategic_depth'] = strategic_depth

    # 3. PACING (100 pts) - Is the experience well-timed?
    avg_turns = game_stats.get('avg_turns', 25)
    early_elim_rate = game_stats.get('early_elimination_rate', 0.0)
    endgame_pressure = game_stats.get('endgame_pressure', 0.5)

    pacing = 100.0

    # Game length scoring (target: 20-30 turns)
    if 20 <= avg_turns <= 30:
        pacing = 100.0
    elif 15 <= avg_turns < 20 or 30 < avg_turns <= 35:
        pacing = 85.0
    elif 12 <= avg_turns < 15 or 35 < avg_turns <= 40:
        pacing = 65.0
    elif 10 <= avg_turns < 12 or 40 < avg_turns <= 50:
        pacing = 40.0
    else:
        pacing = max(0, 20 - abs(avg_turns - 25) * 2)

    # Early elimination penalty (rounds 1-2 eliminations = bad pacing)
    if early_elim_rate > 0.05:
        pacing *= (1.0 - early_elim_rate)  # Severe penalty

    # Endgame pressure bonus (games should build tension)
    if endgame_pressure > 0.6:
        pacing = min(100, pacing + 10)
    elif endgame_pressure < 0.3:
        pacing *= 0.85  # Games peter out = bad pacing

    breakdown['pacing'] = pacing

    # 4. ENGAGEMENT (100 pts) - Are players doing things?
    dead_turn_rate = game_stats.get('dead_turn_rate', 0.2)  # % turns with no meaningful action
    decisions_per_turn = game_stats.get('decisions_per_turn', 2.0)
    action_variety = game_stats.get('action_variety', 0.6)  # Shannon entropy of actions

    engagement = 100.0

    # Dead turn penalty (boring = death)
    if dead_turn_rate < 0.10:
        engagement = 100.0
    elif dead_turn_rate < 0.20:
        engagement = 85.0 - (dead_turn_rate - 0.10) * 150  # Gradient
    elif dead_turn_rate < 0.30:
        engagement = 50.0 - (dead_turn_rate - 0.20) * 200
    else:
        engagement = max(0, 30 - (dead_turn_rate - 0.30) * 100)

    # Decisions per turn bonus
    if decisions_per_turn >= 3.0:
        engagement = min(100, engagement + 15)
    elif decisions_per_turn < 1.5:
        engagement *= 0.7

    # Action variety bonus (players doing different things = engaging)
    if action_variety > 0.7:
        engagement = min(100, engagement + 10)
    elif action_variety < 0.4:
        engagement *= 0.85

    breakdown['engagement'] = engagement

    # TOTAL CORE FITNESS
    core_total = playability + strategic_depth + pacing + engagement

    return core_total, breakdown


def calculate_universal_principles(game_stats: Dict, simulation_data: Dict) -> Tuple[float, Dict[str, float]]:
    """
    Calculate Universal Principles Bonus (500 pts total)

    20 principles × 0-100 each, averaged and multiplied by 5.0
    This makes principles the LARGEST fitness component.
    """
    principles = {}

    # Extract metrics from simulation data
    frustration_rate = game_stats.get('dead_hand_rate', 0.15)
    endgame_symmetry = game_stats.get('endgame_beauty', 0.5)
    strategy_coherence = game_stats.get('strategy_coherence', 0.6)
    leader_clarity = game_stats.get('leader_tower_gap', 1.5)
    excitement_score = game_stats.get('excitement_rate', 0.25)
    aggression_reward = game_stats.get('aggression_correlation', 0.0)
    strategy_divergence = game_stats.get('strategy_game_length_variance', 5.0)
    memorable_moments = game_stats.get('nail_biter_rate', 0.3)
    game_uniqueness = game_stats.get('game_pattern_variance', 8.0)
    upset_victories = game_stats.get('underdog_win_rate', 0.15)
    strategy_polarization = game_stats.get('strategy_polarization', 0.1)
    mechanical_simplicity = game_stats.get('unique_mechanics_count', 10)
    combat_effectiveness = game_stats.get('combat_win_correlation', 0.2)
    impact_magnitude = game_stats.get('avg_tower_damage_per_combat', 0.5)
    archetype_extremity = game_stats.get('rush_fortress_gap', 10.0)
    dead_turn_rate = game_stats.get('dead_turn_rate', 0.2)
    constraint_pressure = game_stats.get('constraint_hit_rate', 0.25)
    metric_harmony = game_stats.get('metric_harmony', 0.6)

    # 1. Fighting Against Human Nature (frustration_rate)
    if frustration_rate < 0.05:
        principles['human_nature'] = 100.0
    elif frustration_rate < 0.15:
        principles['human_nature'] = 100 - (frustration_rate - 0.05) * 300
    else:
        principles['human_nature'] = max(0, 70 - (frustration_rate - 0.15) * 200)

    # 2. Aesthetics Matter (endgame_beauty)
    if endgame_symmetry >= 0.85:
        principles['aesthetics'] = 100.0
    elif endgame_symmetry >= 0.70:
        principles['aesthetics'] = 70 + (endgame_symmetry - 0.70) * 200
    else:
        principles['aesthetics'] = endgame_symmetry * 100

    # 3. Resonance (strategy_coherence)
    if strategy_coherence >= 0.8:
        principles['resonance'] = 100.0
    elif strategy_coherence >= 0.6:
        principles['resonance'] = 60 + (strategy_coherence - 0.6) * 200
    else:
        principles['resonance'] = strategy_coherence * 100

    # 4. Piggybacking (leader_clarity)
    if 1.5 <= leader_clarity <= 2.5:
        principles['piggybacking'] = 100.0
    elif 1.0 <= leader_clarity < 1.5 or 2.5 < leader_clarity <= 3.0:
        principles['piggybacking'] = 75.0
    else:
        principles['piggybacking'] = max(0, 100 - abs(leader_clarity - 2.0) * 30)

    # 5. Interesting vs Fun (excitement_score)
    if 0.2 <= excitement_score <= 0.4:
        principles['emotional_over_intellectual'] = 100.0
    elif 0.15 <= excitement_score < 0.2 or 0.4 < excitement_score <= 0.5:
        principles['emotional_over_intellectual'] = 75.0
    else:
        principles['emotional_over_intellectual'] = max(0, 100 - abs(excitement_score - 0.3) * 150)

    # 6. Target Emotion: Aggression Rewarded (aggression_reward)
    if aggression_reward > 0.3:
        principles['target_emotion'] = 100.0
    elif aggression_reward > 0.15:
        principles['target_emotion'] = 50 + aggression_reward * 150
    elif aggression_reward > 0:
        principles['target_emotion'] = aggression_reward * 200
    else:
        # PENALTY for negative correlation (aggression punished = BAD)
        principles['target_emotion'] = max(0, 50 + aggression_reward * 100)

    # 7. Make it Personal (strategy_divergence)
    if strategy_divergence > 10:
        principles['personal'] = 100.0
    elif strategy_divergence > 5:
        principles['personal'] = 50 + strategy_divergence * 5
    else:
        principles['personal'] = strategy_divergence * 10

    # 8. Details Matter (memorable_moments)
    if 0.3 <= memorable_moments <= 0.5:
        principles['details'] = 100.0
    elif 0.2 <= memorable_moments < 0.3 or 0.5 < memorable_moments <= 0.6:
        principles['details'] = 70.0
    else:
        principles['details'] = max(0, 100 - abs(memorable_moments - 0.4) * 150)

    # 9. Sense of Ownership (game_uniqueness)
    if game_uniqueness > 10.0:
        principles['ownership'] = 100.0
    elif game_uniqueness > 6.0:
        principles['ownership'] = 60 + (game_uniqueness - 6.0) * 10
    else:
        principles['ownership'] = game_uniqueness * 10

    # 10. Room to Explore (upset_victories)
    if 0.10 <= upset_victories <= 0.25:
        principles['exploration'] = 100.0
    elif 0.05 <= upset_victories < 0.10 or 0.25 < upset_victories <= 0.35:
        principles['exploration'] = 70.0
    else:
        principles['exploration'] = max(0, 100 - abs(upset_victories - 0.175) * 200)

    # 11. Strong Responses > Universal Approval (strategy_polarization)
    if strategy_polarization > 0.15:
        principles['strong_responses'] = 100.0
    elif strategy_polarization > 0.08:
        principles['strong_responses'] = 50 + strategy_polarization * 300
    else:
        principles['strong_responses'] = strategy_polarization * 500

    # 12. Not About Ego (mechanical_simplicity)
    if mechanical_simplicity < 8:
        principles['serve_game'] = 100.0
    elif mechanical_simplicity < 15:
        principles['serve_game'] = 100 - (mechanical_simplicity - 8) * 10
    else:
        principles['serve_game'] = max(0, 70 - (mechanical_simplicity - 15) * 5)

    # 13. Make Fun = Winning (combat_effectiveness)
    if combat_effectiveness > 0.3:
        principles['fun_equals_winning'] = 100.0
    elif combat_effectiveness > 0.15:
        principles['fun_equals_winning'] = 50 + combat_effectiveness * 150
    elif combat_effectiveness > 0:
        principles['fun_equals_winning'] = combat_effectiveness * 200
    else:
        # PENALTY for negative correlation
        principles['fun_equals_winning'] = max(0, 50 + combat_effectiveness * 100)

    # 14. Be Blunt (impact_magnitude)
    if 0.33 <= impact_magnitude <= 1.0:
        principles['be_blunt'] = 100.0
    elif 0.2 <= impact_magnitude < 0.33 or 1.0 < impact_magnitude <= 1.5:
        principles['be_blunt'] = 70.0
    else:
        principles['be_blunt'] = max(0, 100 - abs(impact_magnitude - 0.6) * 80)

    # 15. Design for Audience (archetype_extremity)
    if archetype_extremity > 15:
        principles['target_audience'] = 100.0
    elif archetype_extremity > 8:
        principles['target_audience'] = 50 + archetype_extremity * 3.33
    else:
        principles['target_audience'] = archetype_extremity * 6.25

    # 16. Be More Afraid of Boring (dead_turn_rate)
    if dead_turn_rate < 0.10:
        principles['avoid_boring'] = 100.0
    elif dead_turn_rate < 0.25:
        principles['avoid_boring'] = 100 - (dead_turn_rate - 0.10) * 300
    else:
        principles['avoid_boring'] = max(0, 55 - (dead_turn_rate - 0.25) * 100)

    # 17. Change Little to Change Everything (parameter_sensitivity)
    # This requires historical data - use placeholder for now
    param_leverage = game_stats.get('parameter_leverage', 0.6)
    if param_leverage > 0.7:
        principles['leverage'] = 100.0
    else:
        principles['leverage'] = param_leverage * 140

    # 18. Restrictions Breed Creativity (constraint_pressure)
    if 0.20 <= constraint_pressure <= 0.40:
        principles['constraints'] = 100.0
    elif 0.10 <= constraint_pressure < 0.20 or 0.40 < constraint_pressure <= 0.50:
        principles['constraints'] = 70.0
    else:
        principles['constraints'] = max(0, 100 - abs(constraint_pressure - 0.30) * 150)

    # 19. Audience Recognizes Problems (metric_correlation)
    # This measures if problems are obvious in data
    if metric_harmony > 0.6:
        principles['problem_clarity'] = 100.0
    else:
        principles['problem_clarity'] = metric_harmony * 160

    # 20. All Lessons Connect (metric_harmony)
    if metric_harmony > 0.75:
        principles['holistic'] = 100.0
    elif metric_harmony > 0.60:
        principles['holistic'] = 60 + (metric_harmony - 0.6) * 267
    else:
        principles['holistic'] = metric_harmony * 100

    # Calculate average and bonus
    avg_principle = sum(principles.values()) / len(principles)
    bonus = avg_principle * 5.0  # Max 500 points

    return bonus, principles


def calculate_exploration_bonus(genome: Dict, population_genomes: List[Dict]) -> Tuple[float, Dict[str, float]]:
    """
    Calculate Exploration Bonus (+200 pts max)

    Rewards genomes that discover unexpected solutions:
    - Novelty: How different from other genomes in this cycle
    - Extreme viability: Do extreme parameter values work?
    """
    breakdown = {}

    # 1. NOVELTY SCORE (100 pts) - Parameter distance from population
    if len(population_genomes) > 1:
        distances = []
        for other_genome in population_genomes:
            if other_genome == genome:
                continue

            # Calculate normalized parameter distance
            dist = 0.0
            param_count = 0

            for key, value in genome.items():
                if key not in other_genome:
                    continue

                other_value = other_genome[key]

                # Normalize by parameter range (rough estimates)
                if isinstance(value, bool):
                    dist += 1.0 if value != other_value else 0.0
                elif isinstance(value, int):
                    # Assume int ranges are ~10-20 wide
                    range_size = 20
                    dist += abs(value - other_value) / range_size
                elif isinstance(value, float):
                    # Assume float ranges are ~5 wide
                    range_size = 5.0
                    dist += abs(value - other_value) / range_size

                param_count += 1

            if param_count > 0:
                distances.append(dist / param_count)

        if distances:
            avg_distance = sum(distances) / len(distances)
            # Normalize to 0-1 scale (0.3 = very different)
            novelty_score = min(100.0, (avg_distance / 0.3) * 100)
        else:
            novelty_score = 0.0
    else:
        novelty_score = 0.0

    breakdown['novelty'] = novelty_score

    # 2. EXTREME VIABILITY (100 pts) - Do extreme values work?
    extreme_count = 0
    param_count = 0

    for key, value in genome.items():
        param_count += 1

        # Check if parameter is at extremes of its range
        if isinstance(value, bool):
            # Bools are always "extreme" in a sense
            continue
        elif isinstance(value, int):
            # Consider top/bottom 20% of range as "extreme"
            # This is approximate - would need actual ranges
            if key.endswith('_count'):
                # Card counts typically 0-10
                if value <= 1 or value >= 8:
                    extreme_count += 1
            else:
                # Other ints typically have smaller ranges
                continue
        elif isinstance(value, float):
            # Similar logic for floats
            continue

    if param_count > 0:
        extreme_ratio = extreme_count / param_count
        extreme_score = min(100.0, extreme_ratio * 400)  # 25% extreme params = 100 pts
    else:
        extreme_score = 0.0

    breakdown['extreme_viability'] = extreme_score

    total_bonus = novelty_score + extreme_score

    return total_bonus, breakdown


def calculate_variance_penalties(simulation_data: Dict) -> Tuple[float, Dict[str, float]]:
    """
    Calculate Variance Penalties (-300 pts max)

    Detect pathological cases:
    - High inter-game variance: Every game wildly different
    - Low strategy differentiation: All strategies identical
    - Runaway leaders: Games decided too early
    """
    breakdown = {}

    # 1. HIGH INTER-GAME VARIANCE PENALTY (-100 pts)
    game_length_stddev = simulation_data.get('game_length_stddev', 8.0)

    # Healthy variance: ~5-10 turns stddev
    # Pathological: >15 turns stddev
    if game_length_stddev < 10:
        penalty = 0.0
    elif game_length_stddev < 15:
        penalty = (game_length_stddev - 10) * 10  # Gradient 0→50
    else:
        penalty = 50 + (game_length_stddev - 15) * 5  # Up to 100

    breakdown['high_variance'] = -min(100.0, penalty)

    # 2. LOW STRATEGY DIFFERENTIATION PENALTY (-100 pts)
    strategy_play_similarity = simulation_data.get('strategy_similarity', 0.5)

    # 0 = completely different, 1 = identical play patterns
    # Target: <0.3 (strategies feel distinct)
    # Pathological: >0.7 (all play the same)
    if strategy_play_similarity < 0.3:
        penalty = 0.0
    elif strategy_play_similarity < 0.5:
        penalty = (strategy_play_similarity - 0.3) * 150  # Gradient 0→30
    else:
        penalty = 30 + (strategy_play_similarity - 0.5) * 140  # Up to 100

    breakdown['low_differentiation'] = -min(100.0, penalty)

    # 3. RUNAWAY LEADER PENALTY (-100 pts)
    early_leader_win_rate = simulation_data.get('turn5_leader_win_rate', 0.4)

    # Healthy: ~40-50% (early lead helps but not decisive)
    # Pathological: >75% (game decided turn 5)
    if early_leader_win_rate < 0.60:
        penalty = 0.0
    elif early_leader_win_rate < 0.75:
        penalty = (early_leader_win_rate - 0.60) * 200  # Gradient 0→30
    else:
        penalty = 30 + (early_leader_win_rate - 0.75) * 280  # Up to 100

    breakdown['runaway_leader'] = -min(100.0, penalty)

    total_penalty = sum(breakdown.values())

    return total_penalty, breakdown


def calculate_elimination_multiplier(elimination_rate: float) -> float:
    """
    Calculate Elimination Multiplier (0.5× to 2.5×)

    UPDATED FOR CYCLE 2: More aggressive scaling to prevent regression.

    This is the CRITICAL constraint for current development.
    Elimination rate is THE primary metric to solve.

    Cycle 2 Multiplier ranges (MORE AGGRESSIVE):
    - 90%+: 2.5× (exceptional) - was 2.0×
    - 80-90%: 2.2× (excellent) - was 1.7-2.0×
    - 70-80%: 2.0× (good - target range) - was 1.4-1.7×
    - 60-70%: 1.7× (acceptable) - was 1.2-1.4×
    - 50-60%: 1.4× (problematic) - was 1.0-1.2×
    - 40-50%: 1.0× (broken) - was 0.88-1.0×
    - <40%: 0.5+rate (severe punishment)

    Impact: At 58% elim (Gen 100 peak), genome now gets 1.7× vs Cycle 1's 1.26×.
    This should prevent regression like Gen 100→150 in Cycle 1.
    """
    if elimination_rate >= 0.90:
        return 2.5  # INCREASED from 2.0
    elif elimination_rate >= 0.80:
        return 2.2  # INCREASED from 1.7-2.0 range
    elif elimination_rate >= 0.70:
        return 2.0  # INCREASED from 1.4-1.7 range
    elif elimination_rate >= 0.60:
        return 1.7  # NEW threshold
    elif elimination_rate >= 0.50:
        return 1.4  # INCREASED from 1.0-1.2 range
    elif elimination_rate >= 0.40:
        return 1.0  # DECREASED from 0.88-1.0 range
    else:
        # Punish low elimination harder
        return 0.5 + elimination_rate


def calculate_fitness(
    genome: Dict,
    game_stats: Dict,
    simulation_data: Dict,
    population_genomes: List[Dict]
) -> FitnessBreakdown:
    """
    Master fitness calculation function.

    Args:
        genome: Genome parameters
        game_stats: Aggregated game statistics
        simulation_data: Raw simulation data
        population_genomes: All genomes in current generation (for novelty)

    Returns:
        FitnessBreakdown with complete scoring details
    """
    breakdown = FitnessBreakdown()

    # 1. CORE FITNESS (400 pts)
    core_total, core_breakdown = calculate_core_fitness(game_stats)
    breakdown.playability_score = core_breakdown['playability']
    breakdown.strategic_depth_score = core_breakdown['strategic_depth']
    breakdown.pacing_score = core_breakdown['pacing']
    breakdown.engagement_score = core_breakdown['engagement']
    breakdown.core_fitness = core_total

    # 2. UNIVERSAL PRINCIPLES (500 pts)
    principles_bonus, principle_scores = calculate_universal_principles(game_stats, simulation_data)
    breakdown.principle_scores = principle_scores
    breakdown.principles_average = sum(principle_scores.values()) / len(principle_scores)
    breakdown.principles_bonus = principles_bonus

    # 3. EXPLORATION BONUS (200 pts)
    exploration_total, exploration_breakdown = calculate_exploration_bonus(genome, population_genomes)
    breakdown.novelty_score = exploration_breakdown['novelty']
    breakdown.extreme_viability_score = exploration_breakdown['extreme_viability']
    breakdown.exploration_bonus = exploration_total

    # 4. VARIANCE PENALTIES (-300 pts)
    variance_penalty, variance_breakdown = calculate_variance_penalties(simulation_data)
    breakdown.high_variance_penalty = variance_breakdown['high_variance']
    breakdown.low_differentiation_penalty = variance_breakdown['low_differentiation']
    breakdown.runaway_leader_penalty = variance_breakdown['runaway_leader']
    breakdown.variance_penalties = variance_penalty

    # 5. ELIMINATION MULTIPLIER (0.5× to 2.0×)
    elimination_rate = game_stats.get('elimination_rate', 0.0)
    elimination_mult = calculate_elimination_multiplier(elimination_rate)
    breakdown.elimination_rate = elimination_rate
    breakdown.elimination_multiplier = elimination_mult

    # FINAL CALCULATION
    pre_mult = (
        breakdown.core_fitness +
        breakdown.principles_bonus +
        breakdown.exploration_bonus +
        breakdown.variance_penalties
    )

    breakdown.pre_multiplier_score = pre_mult
    breakdown.final_score = pre_mult * elimination_mult

    return breakdown


def format_fitness_breakdown(breakdown: FitnessBreakdown) -> str:
    """Generate human-readable fitness breakdown."""

    lines = []
    lines.append("=" * 80)
    lines.append("FITNESS BREAKDOWN")
    lines.append("=" * 80)
    lines.append("")

    # Core Fitness
    lines.append(f"CORE FITNESS: {breakdown.core_fitness:.1f}/400 pts")
    lines.append(f"  - Playability:      {breakdown.playability_score:5.1f}/100")
    lines.append(f"  - Strategic Depth:  {breakdown.strategic_depth_score:5.1f}/100")
    lines.append(f"  - Pacing:           {breakdown.pacing_score:5.1f}/100")
    lines.append(f"  - Engagement:       {breakdown.engagement_score:5.1f}/100")
    lines.append("")

    # Universal Principles
    lines.append(f"UNIVERSAL PRINCIPLES: {breakdown.principles_bonus:.1f}/500 pts")
    lines.append(f"  Average Score: {breakdown.principles_average:.1f}/100")
    lines.append("")
    lines.append("  Top 5 Principles:")
    sorted_principles = sorted(breakdown.principle_scores.items(), key=lambda x: -x[1])
    for name, score in sorted_principles[:5]:
        lines.append(f"    {name:30s}: {score:5.1f}/100")
    lines.append("")
    lines.append("  Bottom 5 Principles:")
    for name, score in sorted_principles[-5:]:
        lines.append(f"    {name:30s}: {score:5.1f}/100")
    lines.append("")

    # Exploration Bonus
    lines.append(f"EXPLORATION BONUS: {breakdown.exploration_bonus:.1f}/200 pts")
    lines.append(f"  - Novelty:            {breakdown.novelty_score:5.1f}/100")
    lines.append(f"  - Extreme Viability:  {breakdown.extreme_viability_score:5.1f}/100")
    lines.append("")

    # Variance Penalties
    lines.append(f"VARIANCE PENALTIES: {breakdown.variance_penalties:.1f}/0 pts (max -300)")
    lines.append(f"  - High variance:          {breakdown.high_variance_penalty:6.1f}")
    lines.append(f"  - Low differentiation:    {breakdown.low_differentiation_penalty:6.1f}")
    lines.append(f"  - Runaway leaders:        {breakdown.runaway_leader_penalty:6.1f}")
    lines.append("")

    # Elimination Multiplier
    lines.append(f"ELIMINATION RATE: {breakdown.elimination_rate*100:.1f}%")
    lines.append(f"ELIMINATION MULTIPLIER: {breakdown.elimination_multiplier:.2f}×")
    lines.append("")

    # Final Score
    lines.append("=" * 80)
    lines.append(f"PRE-MULTIPLIER SCORE:  {breakdown.pre_multiplier_score:7.1f} pts")
    lines.append(f"FINAL SCORE:           {breakdown.final_score:7.1f} pts")
    lines.append("=" * 80)

    # Rating
    if breakdown.final_score >= 1000:
        rating = "EXCEPTIONAL"
    elif breakdown.final_score >= 800:
        rating = "EXCELLENT"
    elif breakdown.final_score >= 600:
        rating = "GOOD"
    elif breakdown.final_score >= 400:
        rating = "ACCEPTABLE"
    else:
        rating = "POOR"

    lines.append(f"RATING: {rating}")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    print("Battalion Fitness Function - Test Mode")
    print()

    test_genome = {
        'enable_optional_blocking': True,
        'enable_bypass_attacks': False,
        'bypass_damage_amount': 2,
        'battle_frenzy_count': 3,
        'troop_deck_size': 120,
    }

    test_stats = {
        'dead_hand_rate': 0.08,
        'avg_turns': 25.3,
        'elimination_rate': 0.72,
        'strategy_balance': {'RUSH': 24.0, 'FORTRESS': 26.0, 'TEMPO': 25.0, 'ADAPTIVE': 25.0},
        'dead_turn_rate': 0.12,
        'decisions_per_turn': 2.8,
        'action_variety': 0.68,
        'comeback_rate': 0.18,
        'endgame_pressure': 0.65,
        'early_elimination_rate': 0.02,
    }

    test_simulation = {
        'game_length_stddev': 8.5,
        'strategy_similarity': 0.25,
        'turn5_leader_win_rate': 0.48,
    }

    breakdown = calculate_fitness(test_genome, test_stats, test_simulation, [test_genome])

    print(format_fitness_breakdown(breakdown))
