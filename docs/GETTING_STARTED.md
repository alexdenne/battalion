# Getting Started with Meta-Evolution

## Current Status: CORE MODULES COMPLETE ✅

The meta-evolution system has the following components ready:

### ✅ Complete Modules

1. **Fitness Function** (`fitness_function.py`)
   - Comprehensive 1,100+ point scoring system
   - Universal Principles integration (500 pts)
   - Elimination multiplier (0.5× to 2.0×)
   - Detailed transparency breakdowns
   - **TESTED AND WORKING**

2. **Narrative Generator** (`narrative_generator.py`)
   - Selects most exciting games
   - Generates turn-by-turn narratives
   - Highlights key moments and cards
   - Excitement scoring (0-10)
   - **TESTED AND WORKING**

3. **Analyzer** (`analyzer.py`)
   - Parameter convergence detection
   - Variance quality assessment
   - Bottleneck identification
   - Pattern recognition
   - Data-driven insights
   - **TESTED AND WORKING**

### 🚧 Next Steps (To Complete System)

4. **Proposal Generator** (needs creation)
   - Reads analyzer insights
   - Generates specific, testable proposals
   - Categorizes by priority (Must/Should/Optional)
   - Estimates expected impact

5. **Integration with v1.13** (needs configuration)
   - Adapt v1.13 simulator to new fitness function
   - Wire up narrative generation
   - Connect analyzer to GA output

6. **Cycle Runner** (needs creation)
   - Orchestrates complete cycle
   - Manages checkpoints
   - Saves outputs to cycle directories

## Quick Start - Run Cycle 1

### Step 1: Integrate Fitness Function with v1.13 GA

The current v1.13 has a simple 100-point fitness in `genetic_algorithm_v1_13.py`.
We need to replace it with our comprehensive fitness function.

**Option A: Manual Integration (Recommended for first cycle)**

Edit `/Users/alexdenne/Desktop/Batallion/Rules version 1.6 (2025)/testing/genetic_algorithm_v1_13.py`:

```python
# Add at top:
import sys
sys.path.append('/Users/alexdenne/Desktop/Batallion/meta_evolution')
from fitness_function import calculate_fitness, format_fitness_breakdown

# Replace calculate_fitness_score() function with:
def calculate_fitness_score_v1_13(genome, game_stats, simulation_data, population_genomes):
    """Wrapper to use new comprehensive fitness."""

    # Calculate using new system
    breakdown = calculate_fitness(genome, game_stats, simulation_data, population_genomes)

    # Log detailed breakdown for best genomes
    if breakdown.final_score > 800:  # Threshold for excellence
        print("\n" + format_fitness_breakdown(breakdown))

    # Return final score (normalized to 0-100 for compatibility, or use raw score)
    return breakdown.final_score / 11.0  # Scale to ~100 for comparison
    # OR: return breakdown.final_score  # Use raw 0-1100 scale
```

**Option B: Create New GA File (Cleaner)**

I can create `genetic_algorithm_cycle_01.py` that uses the new fitness natively.

### Step 2: Run Cycle 1 Genetic Algorithm

```bash
cd /Users/alexdenne/Desktop/Batallion/Rules\ version\ 1.6\ \(2025\)/testing

# Large population for high variance exploration
python3 genetic_algorithm_v1_13.py \
    --population 48 \
    --generations 150 \
    --games 100 \
    --output /Users/alexdenne/Desktop/Batallion/meta_evolution/cycles/cycle_01/ga_results_cycle_01.json \
    2>&1 | tee /Users/alexdenne/Desktop/Batallion/meta_evolution/cycles/cycle_01/ga_run.log
```

**Expected Duration**: 2-4 hours
**Expected Games**: 48 × 150 × 100 = 720,000 games

### Step 3: Analyze Results

```bash
cd /Users/alexdenne/Desktop/Batallion/meta_evolution

python3 -c "
import json
from analyzer import analyze_ga_results, format_analysis_report

with open('cycles/cycle_01/ga_results_cycle_01.json') as f:
    results = json.load(f)

report = analyze_ga_results(results)
analysis_text = format_analysis_report(report)

with open('cycles/cycle_01/analysis_cycle_01.md', 'w') as f:
    f.write(analysis_text)

print(analysis_text)
"
```

###  4: Generate Narrative

```bash
python3 -c "
import json
from narrative_generator import select_most_exciting_game, generate_game_narrative

with open('cycles/cycle_01/ga_results_cycle_01.json') as f:
    results = json.load(f)

# Get best genome's games
best_results = results['generation_history'][-1]['top_results']
games = best_results.get('games_data', [])

if games:
    best_game, excitement = select_most_exciting_game(games)
    narrative = generate_game_narrative(best_game, results['best_genome'])

    with open('cycles/cycle_01/narrative_cycle_01.md', 'w') as f:
        f.write(narrative)

    print(narrative)
else:
    print('No game data available - check simulator output')
"
```

### Step 5: Review & Approve (HUMAN CHECKPOINT)

1. Read `cycles/cycle_01/analysis_cycle_01.md`
2. Read `cycles/cycle_01/narrative_cycle_01.md`
3. Check:
   - Is elimination rate improving?
   - Does the game feel fun in the narrative?
   - Are there clear insights about what to change?

4. If approved:
```bash
touch cycles/cycle_01/APPROVED.flag
```

### Step 6: Generate Proposals (To Be Built)

This will be a Python script that:
- Reads the analysis report
- Identifies top 3-5 actionable changes
- Proposes specific parameter adjustments
- Estimates impact

**Example Manual Proposals Based on Analysis**:

If analysis shows:
- ❌ Elimination rate: 45% (target: 70%+)
- ❌ Low variance: 25 points early spread
- ✅ Cards/turn: 2.8 (target: 2.0-3.0)
- ✅ Attacks: 8.2/game (target: 7+)

**Proposals**:
1. **MUST**: Increase mutation rate 0.15 → 0.30 (low variance issue)
2. **MUST**: Widen parameter ranges by 50% (premature convergence)
3. **SHOULD**: If blocking=False dominates, consider removing mutual damage
4. **SHOULD**: If bypass_damage converged to 3-4, lock and add new mechanic
5. **OPTIONAL**: Add card that rewards eliminations directly

### Step 7: Implement Proposals (Manual for Cycle 1)

Create `battalion_simulator_cycle_02.py` with approved changes.

### Step 8: Run Cycle 2

Repeat from Step 2 with new simulator.

## Key Files Reference

### Modules You Can Use Now

```python
# Fitness scoring
from fitness_function import calculate_fitness, format_fitness_breakdown

# Narrative generation
from narrative_generator import (
    calculate_excitement_score,
    select_most_exciting_game,
    generate_game_narrative
)

# Analysis
from analyzer import analyze_ga_results, format_analysis_report
```

### Example Integration

```python
# In your GA evaluation loop
def evaluate_genome_comprehensive(genome, games_per_genome=100, population_genomes=[]):
    """Enhanced evaluation with full fitness."""

    config = genome.to_config()

    # Run games across all player counts (equal weighting per new principles)
    all_results = []
    for player_count in [2, 3, 4, 5, 6]:
        for _ in range(games_per_genome // 5):  # 20 games each
            result = simulate_game(player_count, config, verbose=False)
            all_results.append(result)

    # Aggregate statistics
    game_stats = aggregate_game_stats(all_results)
    simulation_data = extract_simulation_data(all_results)

    # Calculate comprehensive fitness
    breakdown = calculate_fitness(
        genome=asdict(genome),
        game_stats=game_stats,
        simulation_data=simulation_data,
        population_genomes=[asdict(g) for g in population_genomes]
    )

    return breakdown.final_score, breakdown, all_results
```

## Configuration Recommendations

### For Cycle 1 (Exploration Focus)

```python
GA_CONFIG = {
    'population_size': 48,          # High diversity
    'generations': 150,             # Enough for convergence
    'games_per_genome': 100,        # 20 per player count
    'mutation_rate': 0.25,          # High for exploration
    'crossover_rate': 0.50,
    'elite_count': 3,
    'tournament_size': 5,
}
```

### For Later Cycles (Refinement Focus)

```python
GA_CONFIG = {
    'population_size': 32,          # Smaller = faster
    'generations': 100,
    'games_per_genome': 100,
    'mutation_rate': 0.15,          # Lower for refinement
    'crossover_rate': 0.60,
    'elite_count': 4,
    'tournament_size': 3,
}
```

## Fitness Score Interpretation

### Rating Scale

- **1,000+**: Exceptional - production ready
- **800-1,000**: Excellent - minor tuning needed
- **600-800**: Good - significant improvement area
- **400-600**: Acceptable - major work needed
- **<400**: Poor - fundamental issues

### What Each Score Means

**Core Fitness (400 pts)**:
- 320+: Playable and balanced
- 240-320: Playable but imbalanced
- <240: Playability issues

**Universal Principles (500 pts)**:
- 400+: Fun and coherent
- 300-400: Functional but not optimized
- <300: Design philosophy violations

**Exploration Bonus (200 pts)**:
- 150+: Novel solutions discovered
- 80-150: Standard improvement
- <80: Incremental changes only

**Elimination Multiplier**:
- 1.7-2.0×: 80-90%+ elimination (excellent)
- 1.4-1.7×: 70-80% elimination (target met)
- 1.0-1.4×: 50-70% elimination (approaching target)
- <1.0×: <50% elimination (critical issue)

## Troubleshooting

### GA Takes Too Long

**Solution**: Reduce games per genome or player counts

```python
# Fast test run
games_per_genome = 20  # 4 per player count
# OR
player_counts = [3, 4]  # Skip 2P, 5P, 6P
```

### Fitness Scores Very Low (<300)

**Check**:
1. Is simulator producing valid games?
2. Run verbose game manually and inspect
3. Check for errors in game_stats aggregation
4. Verify fitness function getting correct data

### No Games Data for Narrative

**Solution**: Modify simulator to return complete game logs

```python
# In simulate_game()
return {
    'winner': winner,
    'turns': turn,
    'players': players,
    # ADD:
    'turn_log': turn_by_turn_log,  # List of turn events
    'cards_played_types': cards_played,
    'eliminations': elimination_count,
    # ... etc
}
```

### Analyzer Shows No Convergence

**Causes**:
- Mutation rate too high
- Parameter ranges too wide
- Not enough generations

**Solutions**:
- Reduce mutation rate to 0.15
- Narrow converged parameter ranges
- Run more generations (200+)

## Next Session Workflow

When you're ready to continue:

1. **I can create**:
   - `proposal_generator.py` - Automated proposal system
   - `genetic_algorithm_cycle_01.py` - Clean integration
   - `run_cycle.py` - One-command cycle execution
   - `dashboard.py` - Progress visualization

2. **You run**:
   - Cycle 1 GA (2-4 hours)
   - Review analysis & narrative
   - Approve proposals

3. **We iterate**:
   - Implement proposals together
   - Run Cycle 2
   - Track progress across cycles

## Questions?

The system is modular - you can use individual components (fitness, narrative, analyzer) right now with minimal integration.

Would you like me to:
1. Create the proposal generator next?
2. Build a complete integration script for v1.13?
3. Run a test cycle with smaller parameters to verify everything works?
4. Create the full orchestration engine?

Let me know what would be most helpful!
