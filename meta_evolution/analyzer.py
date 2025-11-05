#!/usr/bin/env python3
"""
Battalion GA Results Analyzer
==============================

Deep analysis of genetic algorithm results to identify:
- Parameter convergence patterns
- Fitness trajectory and variance quality
- Bottlenecks preventing improvement
- Success/failure patterns
- Data-driven insights for proposals
"""

import json
import statistics
import random
from typing import Dict, List, Tuple
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class AnalysisReport:
    """Comprehensive analysis of GA results."""

    # Summary statistics
    best_fitness: float
    avg_fitness: float
    fitness_improvement: float
    convergence_generation: int

    # Parameter analysis
    converged_parameters: List[Dict]  # {param, values, variance}
    divergent_parameters: List[Dict]  # {param, values, variance}

    # Variance quality
    early_variance: float  # Gen 1-20
    late_variance: float   # Gen 80-100
    exploration_quality: str  # 'excellent', 'good', 'poor'

    # Bottlenecks
    bottlenecks: List[Dict]  # {metric, current, target, severity}

    # Strengths
    strengths: List[str]

    # Problem areas
    problems: List[str]

    # Insights
    insights: List[Dict]  # {type, description, evidence, confidence}


def analyze_ga_results(ga_results: Dict) -> AnalysisReport:
    """
    Main analysis function.

    Args:
        ga_results: Complete GA results JSON

    Returns:
        AnalysisReport with comprehensive findings
    """

    # Extract data
    history = ga_results.get('generation_history', [])
    best_genome = ga_results.get('best_genome', {})
    best_fitness = ga_results.get('best_fitness', 0.0)

    # Initialize report
    report = AnalysisReport(
        best_fitness=best_fitness,
        avg_fitness=0.0,
        fitness_improvement=0.0,
        convergence_generation=0,
        converged_parameters=[],
        divergent_parameters=[],
        early_variance=0.0,
        late_variance=0.0,
        exploration_quality='unknown',
        bottlenecks=[],
        strengths=[],
        problems=[],
        insights=[]
    )

    if not history:
        return report

    # 1. FITNESS TRAJECTORY ANALYSIS
    analyze_fitness_trajectory(history, report)

    # 2. VARIANCE QUALITY ANALYSIS
    analyze_variance_quality(history, report)

    # 3. PARAMETER CONVERGENCE ANALYSIS
    analyze_parameter_convergence(history, best_genome, report)

    # 4. BOTTLENECK IDENTIFICATION
    identify_bottlenecks(history, report)

    # 5. PATTERN RECOGNITION
    recognize_patterns(history, report)

    # 6. GENERATE INSIGHTS
    generate_insights(report)

    return report


def analyze_fitness_trajectory(history: List[Dict], report: AnalysisReport):
    """Analyze how fitness evolved over generations."""

    best_scores = [gen['best_fitness'] for gen in history]
    avg_scores = [gen['avg_fitness'] for gen in history]

    # Overall improvement
    initial_best = best_scores[0] if best_scores else 0
    final_best = best_scores[-1] if best_scores else 0
    report.fitness_improvement = final_best - initial_best

    # Average fitness
    report.avg_fitness = statistics.mean(avg_scores) if avg_scores else 0

    # Convergence detection (when improvement plateaus)
    convergence_gen = len(history)  # Default: didn't converge
    improvement_threshold = 5.0  # 5 points

    for i in range(20, len(best_scores)):
        # Check if last 20 gens improved < threshold
        recent_improvement = best_scores[i] - best_scores[i-20]
        if recent_improvement < improvement_threshold:
            convergence_gen = i - 10  # Converged ~10 gens ago
            break

    report.convergence_generation = convergence_gen

    # Assess trajectory
    if report.fitness_improvement > 100:
        report.strengths.append(f"Strong fitness improvement (+{report.fitness_improvement:.1f} points)")
    elif report.fitness_improvement > 50:
        report.strengths.append(f"Moderate fitness improvement (+{report.fitness_improvement:.1f} points)")
    elif report.fitness_improvement < 20:
        report.problems.append(f"Weak fitness improvement (+{report.fitness_improvement:.1f} points)")
        report.insights.append({
            'type': 'stagnation',
            'description': 'Evolution stagnating - parameter space may be too narrow or local optimum reached',
            'evidence': f'Only {report.fitness_improvement:.1f} point improvement over {len(history)} generations',
            'confidence': 'high'
        })


def analyze_variance_quality(history: List[Dict], report: AnalysisReport):
    """
    Analyze variance quality - CRITICAL for exploration.

    Good evolution needs HIGH variance early (exploration)
    and convergence late (exploitation).
    """

    if len(history) < 40:
        report.exploration_quality = 'insufficient_data'
        return

    # Extract best scores by generation
    best_scores = [gen['best_fitness'] for gen in history]

    # Early variance (first 20 gens)
    early_scores = best_scores[:20]
    early_range = max(early_scores) - min(early_scores)
    report.early_variance = early_range

    # Late variance (last 20 gens)
    late_scores = best_scores[-20:]
    late_range = max(late_scores) - min(late_scores)
    report.late_variance = late_range

    # Quality assessment
    if early_range > 100 and late_range < 30:
        report.exploration_quality = 'excellent'
        report.strengths.append(f'Excellent exploration (early range: {early_range:.1f}, late range: {late_range:.1f})')
    elif early_range > 50 and late_range < 50:
        report.exploration_quality = 'good'
    elif early_range < 30:
        report.exploration_quality = 'poor'
        report.problems.append(f'⚠️ LOW VARIANCE: Early generations only span {early_range:.1f} points (need 50+ for effective exploration)')
        report.problems.append('🔥 MUTATION RATE TOO LOW: Population converging before exploring parameter space')
        report.insights.append({
            'type': 'low_variance',
            'description': 'Insufficient exploration - increase mutation rate and parameter ranges',
            'evidence': f'Early variance: {early_range:.1f} (target: 80+), Late variance: {late_range:.1f}',
            'confidence': 'very_high'
        })
    elif late_range > 50:
        report.exploration_quality = 'unstable'
        report.problems.append(f'High late variance ({late_range:.1f}) suggests unstable parameter space')


def analyze_parameter_convergence(history: List[Dict], best_genome: Dict, report: AnalysisReport):
    """
    Analyze which parameters converged vs remained diverse.

    Converged params = GA found optimal value
    Divergent params = Still exploring OR don't matter
    """

    # Collect parameter values from final generation
    final_gen = history[-1] if history else {}
    population = final_gen.get('population', [])

    if not population:
        return

    # Analyze each parameter
    param_stats = defaultdict(list)

    for genome_data in population:
        genome = genome_data.get('genome', {})
        for param, value in genome.items():
            param_stats[param].append(value)

    # Determine convergence
    for param, values in param_stats.items():
        if not values:
            continue

        # Handle bools separately
        if all(isinstance(v, bool) for v in values):
            true_count = sum(values)
            ratio = true_count / len(values)
            variance_ratio = min(ratio, 1 - ratio)  # 0 = converged, 0.5 = split

            if variance_ratio < 0.2:
                # Converged to True or False
                converged_value = ratio > 0.5
                report.converged_parameters.append({
                    'param': param,
                    'value': converged_value,
                    'variance': variance_ratio,
                    'type': 'bool'
                })
            else:
                report.divergent_parameters.append({
                    'param': param,
                    'values': values,
                    'variance': variance_ratio,
                    'type': 'bool'
                })
        else:
            # Numeric parameters
            mean_val = statistics.mean(values)
            stddev = statistics.stdev(values) if len(values) > 1 else 0
            value_range = max(values) - min(values)

            # Coefficient of variation (normalized variance)
            cv = (stddev / mean_val) if mean_val != 0 else 0

            if cv < 0.15 or value_range < 2:
                # Converged
                report.converged_parameters.append({
                    'param': param,
                    'value': round(mean_val, 2),
                    'variance': stddev,
                    'range': value_range,
                    'type': 'numeric'
                })
            else:
                # Still divergent
                report.divergent_parameters.append({
                    'param': param,
                    'mean': round(mean_val, 2),
                    'stddev': round(stddev, 2),
                    'min': min(values),
                    'max': max(values),
                    'type': 'numeric'
                })

    # Generate insights
    if len(report.converged_parameters) > len(best_genome) * 0.6:
        report.strengths.append(f'{len(report.converged_parameters)} parameters converged (strong signal)')
        report.insights.append({
            'type': 'convergence',
            'description': 'Many parameters converged - consider locking these and adding new parameters',
            'evidence': f'{len(report.converged_parameters)}/{len(best_genome)} parameters converged',
            'confidence': 'high'
        })
    elif len(report.converged_parameters) < 3:
        report.problems.append('Few parameters converged - may need more generations or narrower ranges')


def identify_bottlenecks(history: List[Dict], report: AnalysisReport):
    """
    Identify what's preventing higher fitness.

    Check final generation results for metrics below target.
    """

    if not history:
        return

    final_gen = history[-1]
    best_results = final_gen.get('top_results', {})

    # Define targets (from Universal Principles)
    targets = {
        'elimination_rate': (0.70, 0.90, 'critical'),  # (min, target, severity)
        'avg_cards_per_turn': (2.0, 3.0, 'high'),
        'avg_attacks': (7.0, 9.0, 'high'),
        'avg_turns': (20.0, 30.0, 'medium'),
        'dead_hand_rate': (0.0, 0.10, 'critical'),
        'dead_turn_rate': (0.0, 0.15, 'high'),
        'strategy_balance': (None, None, 'medium'),  # Special handling
    }

    for metric, (min_target, optimal_target, severity) in targets.items():
        current_value = best_results.get(metric, 0)

        if metric == 'elimination_rate':
            if current_value < 0.30:
                report.bottlenecks.append({
                    'metric': metric,
                    'current': current_value,
                    'target': optimal_target,
                    'severity': 'critical',
                    'gap': optimal_target - current_value
                })
                report.problems.append(f'🔥 CRITICAL: Elimination rate only {current_value*100:.1f}% (target: 70%+)')
            elif current_value < min_target:
                report.bottlenecks.append({
                    'metric': metric,
                    'current': current_value,
                    'target': optimal_target,
                    'severity': severity,
                    'gap': optimal_target - current_value
                })
                report.problems.append(f'Elimination rate {current_value*100:.1f}% below target ({min_target*100:.0f}%+)')

        elif metric == 'avg_cards_per_turn':
            if current_value < min_target:
                report.bottlenecks.append({
                    'metric': metric,
                    'current': current_value,
                    'target': optimal_target,
                    'severity': severity,
                    'gap': min_target - current_value
                })
                report.problems.append(f'Cards/turn {current_value:.2f} below target ({min_target:.1f}+)')

        elif metric == 'avg_attacks':
            if current_value < min_target:
                report.bottlenecks.append({
                    'metric': metric,
                    'current': current_value,
                    'target': optimal_target,
                    'severity': severity,
                    'gap': min_target - current_value
                })
                report.problems.append(f'Attacks/game {current_value:.1f} below target ({min_target:.1f}+)')

        elif metric in ['dead_hand_rate', 'dead_turn_rate']:
            if current_value > optimal_target:
                report.bottlenecks.append({
                    'metric': metric,
                    'current': current_value,
                    'target': optimal_target,
                    'severity': severity,
                    'gap': current_value - optimal_target
                })
                report.problems.append(f'{metric.replace("_", " ").title()} {current_value*100:.1f}% above target (<{optimal_target*100:.0f}%)')


def recognize_patterns(history: List[Dict], report: AnalysisReport):
    """
    Recognize common patterns in evolution.

    - Oscillation (fitness bouncing up/down)
    - Plateau (stuck at local optimum)
    - Linear improvement (healthy)
    - Exponential improvement (exceptional)
    - Degradation (getting worse)
    """

    if len(history) < 20:
        return

    best_scores = [gen['best_fitness'] for gen in history]

    # Calculate trend
    x = list(range(len(best_scores)))
    y = best_scores

    # Simple linear regression
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] ** 2 for i in range(n))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2) if (n * sum_x2 - sum_x ** 2) != 0 else 0

    # Oscillation detection
    direction_changes = 0
    for i in range(1, len(best_scores) - 1):
        if (best_scores[i] > best_scores[i-1] and best_scores[i] > best_scores[i+1]) or \
           (best_scores[i] < best_scores[i-1] and best_scores[i] < best_scores[i+1]):
            direction_changes += 1

    oscillation_rate = direction_changes / len(best_scores)

    if oscillation_rate > 0.3:
        report.problems.append(f'High oscillation ({oscillation_rate*100:.0f}% of generations) - parameter space unstable')
        report.insights.append({
            'type': 'oscillation',
            'description': 'Fitness oscillating - reduce mutation rate or stabilize parameters',
            'evidence': f'{direction_changes} direction changes in {len(best_scores)} generations',
            'confidence': 'medium'
        })

    # Trend assessment
    if slope > 1.0:
        report.strengths.append('Strong positive trend (consistent improvement)')
    elif slope < 0:
        report.problems.append('Negative trend (fitness degrading)')
        report.insights.append({
            'type': 'degradation',
            'description': 'Fitness degrading over time - check for bugs or invalid parameter combinations',
            'evidence': f'Negative slope: {slope:.2f}',
            'confidence': 'high'
        })


def generate_insights(report: AnalysisReport):
    """
    Generate high-level insights from all analyses.

    These drive proposal generation.
    """

    # Insight: What's the #1 blocker?
    if report.bottlenecks:
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_bottlenecks = sorted(report.bottlenecks, key=lambda b: (severity_order.get(b['severity'], 99), -abs(b['gap'])))

        top_bottleneck = sorted_bottlenecks[0]
        report.insights.append({
            'type': 'primary_bottleneck',
            'description': f'Primary blocker: {top_bottleneck["metric"]} at {top_bottleneck["current"]:.2f} (target: {top_bottleneck["target"]:.2f})',
            'evidence': f'Severity: {top_bottleneck["severity"]}, Gap: {top_bottleneck["gap"]:.2f}',
            'confidence': 'very_high'
        })

    # Insight: Is exploration sufficient?
    if report.exploration_quality in ['poor', 'unstable']:
        report.insights.append({
            'type': 'exploration_issue',
            'description': f'Exploration quality: {report.exploration_quality} - adjust GA parameters',
            'evidence': f'Early variance: {report.early_variance:.1f}, Late variance: {report.late_variance:.1f}',
            'confidence': 'high'
        })

    # Insight: Are we at diminishing returns?
    if report.convergence_generation < len(report.bottlenecks) * 20:
        # Converged quickly = either great or stuck
        if report.best_fitness > 800:
            report.insights.append({
                'type': 'early_success',
                'description': f'Converged to high fitness quickly (gen {report.convergence_generation}) - parameter space well-suited',
                'evidence': f'Best fitness: {report.best_fitness:.1f}',
                'confidence': 'medium'
            })
        else:
            report.insights.append({
                'type': 'premature_convergence',
                'description': f'Converged too early (gen {report.convergence_generation}) to suboptimal fitness - widen parameter space',
                'evidence': f'Best fitness only {report.best_fitness:.1f}',
                'confidence': 'high'
            })


def format_analysis_report(report: AnalysisReport) -> str:
    """Generate human-readable analysis report."""

    lines = []
    lines.append("=" * 80)
    lines.append("GA RESULTS ANALYSIS REPORT")
    lines.append("=" * 80)
    lines.append("")

    # SUMMARY
    lines.append("## SUMMARY")
    lines.append("")
    lines.append(f"Best Fitness:        {report.best_fitness:.1f} points")
    lines.append(f"Avg Fitness:         {report.avg_fitness:.1f} points")
    lines.append(f"Improvement:         +{report.fitness_improvement:.1f} points")
    lines.append(f"Convergence:         Generation {report.convergence_generation}")
    lines.append(f"Exploration Quality: {report.exploration_quality.upper()}")
    lines.append("")

    # STRENGTHS
    if report.strengths:
        lines.append("## STRENGTHS")
        lines.append("")
        for strength in report.strengths:
            lines.append(f"✓ {strength}")
        lines.append("")

    # PROBLEMS
    if report.problems:
        lines.append("## PROBLEMS")
        lines.append("")
        for problem in report.problems:
            lines.append(f"⚠ {problem}")
        lines.append("")

    # BOTTLENECKS
    if report.bottlenecks:
        lines.append("## BOTTLENECKS")
        lines.append("")
        lines.append("Metrics preventing higher fitness:")
        lines.append("")
        for bottleneck in sorted(report.bottlenecks, key=lambda b: -abs(b['gap']))[:5]:
            lines.append(f"  [{bottleneck['severity'].upper()}] {bottleneck['metric']}")
            lines.append(f"    Current: {bottleneck['current']:.2f}")
            lines.append(f"    Target:  {bottleneck['target']:.2f}")
            lines.append(f"    Gap:     {bottleneck['gap']:.2f}")
            lines.append("")

    # PARAMETER CONVERGENCE
    if report.converged_parameters:
        lines.append("## CONVERGED PARAMETERS")
        lines.append("")
        lines.append("These parameters found optimal values:")
        lines.append("")
        for param_data in report.converged_parameters[:10]:
            if param_data['type'] == 'bool':
                lines.append(f"  {param_data['param']}: {param_data['value']} (variance: {param_data['variance']:.3f})")
            else:
                lines.append(f"  {param_data['param']}: {param_data['value']} (σ={param_data['variance']:.2f}, range={param_data['range']})")
        lines.append("")

    if report.divergent_parameters:
        lines.append("## DIVERGENT PARAMETERS")
        lines.append("")
        lines.append("These parameters remain diverse (still exploring or irrelevant):")
        lines.append("")
        for param_data in report.divergent_parameters[:10]:
            if param_data['type'] == 'bool':
                lines.append(f"  {param_data['param']}: split {param_data['variance']*100:.1f}%")
            else:
                lines.append(f"  {param_data['param']}: {param_data['mean']} ± {param_data['stddev']} (range: {param_data['min']}-{param_data['max']})")
        lines.append("")

    # VARIANCE ANALYSIS
    lines.append("## VARIANCE ANALYSIS")
    lines.append("")
    lines.append(f"Early Variance (Gen 1-20):   {report.early_variance:.1f} points")
    lines.append(f"Late Variance (Gen 80-100):  {report.late_variance:.1f} points")
    lines.append("")
    if report.early_variance > 80:
        lines.append("✓ Excellent early exploration (broad search)")
    elif report.early_variance < 30:
        lines.append("⚠ Poor early exploration (increase mutation rate)")

    if report.late_variance < 30:
        lines.append("✓ Good convergence (focused exploitation)")
    elif report.late_variance > 60:
        lines.append("⚠ Poor convergence (unstable parameter space)")
    lines.append("")

    # KEY INSIGHTS
    if report.insights:
        lines.append("## KEY INSIGHTS")
        lines.append("")
        for insight in report.insights:
            confidence_icon = {
                'very_high': '🔥',
                'high': '⚡',
                'medium': '💡',
                'low': '🤔'
            }.get(insight['confidence'], '•')

            lines.append(f"{confidence_icon} [{insight['type'].upper()}] {insight['description']}")
            lines.append(f"   Evidence: {insight['evidence']}")
            lines.append(f"   Confidence: {insight['confidence']}")
            lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    print("Battalion GA Analyzer - Test Mode")
    print()

    # Simulate GA results
    test_history = []
    base_score = 400
    for i in range(100):
        gen_score = base_score + i * 3 + random.randint(-10, 20)
        test_history.append({
            'generation': i + 1,
            'best_fitness': gen_score,
            'avg_fitness': gen_score - 50,
            'top_results': {
                'elimination_rate': 0.45 + i * 0.002,
                'avg_cards_per_turn': 2.3,
                'avg_attacks': 4.5 + i * 0.02,
                'avg_turns': 25.0,
                'dead_hand_rate': 0.08,
                'dead_turn_rate': 0.12,
            },
            'population': [
                {
                    'genome': {
                        'enable_optional_blocking': bool(j % 2),
                        'enable_bypass_attacks': True,
                        'bypass_damage_amount': 2 + (j % 3),
                        'battle_frenzy_count': 3 + (j % 4),
                        'troop_deck_size': 120 + j * 2,
                    }
                }
                for j in range(32)
            ]
        })

    import random

    test_results = {
        'best_fitness': test_history[-1]['best_fitness'],
        'best_genome': test_history[-1]['population'][0]['genome'],
        'generation_history': test_history
    }

    report = analyze_ga_results(test_results)
    print(format_analysis_report(report))
