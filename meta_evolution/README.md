# Battalion Meta-Evolution System

Autonomous evolutionary cycle system for optimizing Battalion through genetic algorithms guided by Universal Game Design Principles.

## Overview

This system runs 15-cycle meta-evolution:
1. Run genetic algorithm (160K+ games per cycle)
2. Analyze results (identify strengths, weaknesses, opportunities)
3. Generate proposals (data-driven improvements)
4. **HUMAN CHECKPOINT**: Review and approve proposals
5. Implement proposals (create next version)
6. **HUMAN CHECKPOINT**: Review verbose game narrative
7. Repeat for next cycle

## Directory Structure

```
meta_evolution/
├── README.md                       # This file
├── fitness_function.py             # Comprehensive fitness scoring
├── narrative_generator.py          # Verbose game narratives
├── analyzer.py                     # GA results analysis
├── proposal_generator.py           # Data-driven proposals
├── meta_engine.py                  # Main orchestration engine
├── run_cycle.py                    # Single cycle runner
├── cycles/                         # Cycle outputs
│   ├── cycle_01/
│   │   ├── simulator_cycle_01.py
│   │   ├── ga_results_cycle_01.json
│   │   ├── analysis_cycle_01.md
│   │   ├── proposals_cycle_01.md
│   │   ├── narrative_cycle_01.md
│   │   └── APPROVED.flag          # Human creates this
│   ├── cycle_02/
│   └── ...
└── dashboard.py                    # Progress visualization
```

## Components

### 1. Fitness Function (`fitness_function.py`)

Comprehensive scoring based on Universal Principles:
- **Core Fitness**: 400 pts (playability, depth, pacing, engagement)
- **Universal Principles**: 500 pts (20 principles × 0-100, avg × 5.0)
- **Exploration Bonus**: +200 pts (novelty, extreme viability)
- **Variance Penalties**: -300 pts (pathology detection)
- **Elimination Multiplier**: 0.5× to 2.0× (CRITICAL constraint)

**Total Range**: -100 to 1,100 pts (theoretical max with multiplier: 2,200)

### 2. Narrative Generator (`narrative_generator.py`)

Generates human-readable game narratives:
- Selects most exciting game (eliminations, comebacks, close calls)
- Turn-by-turn key moments
- Card highlights and strategy coherence
- Excitement rating (0-10)

### 3. Analyzer (`analyzer.py`)

Deep analysis of GA results:
- Parameter convergence patterns
- Fitness trajectory analysis
- Variance quality assessment
- Bottleneck identification
- Success/failure pattern recognition

### 4. Proposal Generator (`proposal_generator.py`)

Data-driven improvement proposals:
- Parameter range adjustments (narrow converged, widen unexplored)
- New mechanic suggestions (based on bottlenecks)
- Card composition changes (based on usage patterns)
- Fitness function tweaks (based on pathologies)

### 5. Meta Engine (`meta_engine.py`)

Orchestrates complete cycles:
- Runs GA with current simulator
- Analyzes results
- Generates proposals
- **Pauses for human approval**
- Implements approved proposals
- Generates new simulator version
- **Pauses for verbose game review**
- Continues to next cycle

### 6. Dashboard (`dashboard.py`)

Progress visualization:
- Fitness progression across cycles
- Parameter evolution heatmaps
- Elimination rate tracking
- Universal Principles scores
- Comparative analysis

## Workflow

### Running a Single Cycle

```bash
cd /Users/alexdenne/Desktop/Batallion/meta_evolution
python3 run_cycle.py --cycle 1 --population 48 --generations 150 --games 100
```

**Parameters**:
- `--cycle`: Cycle number (1-15)
- `--population`: Population size (recommend: 32-64 for high variance)
- `--generations`: Generations (recommend: 100-200)
- `--games`: Games per genome (recommend: 50-100 per player count = 250-500 total)

**What Happens**:
1. Loads simulator from previous cycle (or baseline for cycle 1)
2. Runs GA (can take 1-3 hours for large runs)
3. Generates analysis markdown
4. Generates proposals markdown
5. Generates narrative of best game
6. **STOPS** and waits for your approval

### Reviewing Proposals

```bash
cat cycles/cycle_01/proposals_cycle_01.md
```

Proposals show:
- **Must Implement**: Critical changes backed by strong data
- **Should Implement**: Recommended changes with good evidence
- **Optional**: Exploratory changes worth testing
- **Reject**: Changes that would hurt progress

Edit the proposals file to mark which to implement, then:

```bash
touch cycles/cycle_01/APPROVED.flag
```

### Implementing Proposals

```bash
python3 run_cycle.py --cycle 1 --implement
```

This:
1. Reads approved proposals
2. Modifies simulator code
3. Creates new version: `simulator_cycle_02.py`
4. Runs 1 verbose test game
5. Generates narrative
6. **STOPS** for your review

### Reviewing Verbose Game

```bash
cat cycles/cycle_01/narrative_cycle_01.md
```

Check:
- Does the game feel fun?
- Are strategies behaving as expected?
- Are cards creating interesting moments?
- Is pacing appropriate?

If approved:

```bash
touch cycles/cycle_01/VERBOSE_APPROVED.flag
python3 run_cycle.py --cycle 2  # Start next cycle
```

### Running Full 15-Cycle Evolution

```bash
python3 meta_engine.py --cycles 15 --auto-checkpoint
```

This runs all 15 cycles but stops at each checkpoint for approval.

**Estimated Time**: 15-30 hours total (1-2 hours per cycle)

## Configuration

### Baseline (Cycle 1)

Cycle 1 starts from: `/Users/alexdenne/Desktop/Batallion/Rules version 1.6 (2025)/testing/battalion_simulator_v1_13.py`

This is v1.13 with:
- Optional blocking mechanic
- Bypass attack mechanic
- 23 GA parameters
- Full event card system

### GA Configuration

Default parameters (optimized for exploration):
```python
POPULATION_SIZE = 48        # Higher = more diversity
GENERATIONS = 150           # Enough for convergence
GAMES_PER_GENOME = 100      # 20 per player count (2-6P)
MUTATION_RATE = 0.20        # High for exploration
CROSSOVER_RATE = 0.50       # Standard
ELITE_COUNT = 3             # Preserve top performers
TOURNAMENT_SIZE = 5         # Moderate selection pressure
```

### Fitness Targets

**Excellence Threshold**: 800+ points
- Core Fitness: 320+/400 (80%)
- Universal Principles: 400+/500 (80% avg)
- Exploration Bonus: 80+/200 (40%)
- Variance Penalties: < -50
- Elimination Multiplier: 1.4×+ (70%+ elimination)

## Output Files

### Per Cycle

- `simulator_cycle_XX.py`: Simulator implementation
- `ga_results_cycle_XX.json`: Complete GA data
- `analysis_cycle_XX.md`: Human-readable analysis
- `proposals_cycle_XX.md`: Improvement proposals
- `narrative_cycle_XX.md`: Most exciting game
- `fitness_breakdown_cycle_XX.json`: Detailed scoring
- `APPROVED.flag`: Created by human to proceed
- `VERBOSE_APPROVED.flag`: Created by human after game review

### Cross-Cycle

- `evolution_history.json`: All cycles metadata
- `dashboard.html`: Interactive progress visualization
- `parameter_evolution.png`: Heatmap of parameter changes
- `fitness_trajectory.png`: Score progression
- `FINAL_REPORT.md`: Complete 15-cycle summary

## Best Practices

### DO:
- Review proposals carefully - data-driven doesn't mean always correct
- Read verbose game narratives - numbers don't show fun
- Check for unintended consequences in proposals
- Run larger populations for important cycles (48-64 genomes)
- Save intermediate results frequently

### DON'T:
- Skip verbose game review - it's the only way to catch "technically correct but unfun"
- Rush through cycles - 1-2 hours per cycle is normal
- Ignore low Universal Principles scores - they indicate design problems
- Over-constrain parameter ranges too early - let evolution explore
- Implement all proposals - some are mutually exclusive

## Troubleshooting

### GA Not Converging

**Symptoms**: Fitness not improving after 50+ generations
**Causes**: Local optimum, parameter ranges too narrow, insufficient population
**Solutions**:
- Increase mutation rate to 0.30
- Widen parameter ranges by 50%
- Increase population to 64

### All Genomes Score Poorly

**Symptoms**: Best fitness < 400 consistently
**Causes**: Fundamental game design issue, fitness function mismatch
**Solutions**:
- Review Universal Principles scores - which are consistently low?
- Check elimination multiplier - is it below 1.0?
- Generate verbose game - is the game playable?
- Consider reverting to previous cycle

### Proposals Make No Sense

**Symptoms**: Contradictory or nonsensical suggestions
**Causes**: Insufficient data, analyzer misinterpreting patterns
**Solutions**:
- Increase games per genome to 200+
- Manually review GA results JSON
- Look for variance patterns - high variance = noisy data
- Reject questionable proposals and re-run analysis

### Simulator Crashes

**Symptoms**: GA exits with errors mid-run
**Causes**: Code generation bugs, invalid parameter combinations
**Solutions**:
- Check `error.log` for stack trace
- Run single game with verbose mode
- Validate genome before full GA run
- Review last implemented proposals for bugs

## Future Enhancements

- Automated code generation (currently manual implementation)
- Multi-objective optimization (Pareto frontier)
- Transfer learning between cycles
- Ensemble methods (run multiple GAs in parallel)
- Adaptive mutation rates (higher early, lower late)
- Real-time progress streaming
- Human player testing integration

---

*Built following Universal Game Design Principles - optimizing for fun, not just metrics.*
