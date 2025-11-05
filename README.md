# Battalion

> *A strategic card game of territorial conquest, optimized through evolutionary algorithms*

[![Status](https://img.shields.io/badge/Status-Active%20Development-success)](https://github.com/yourusername/battalion)
[![Version](https://img.shields.io/badge/Version-1.6-blue)](https://github.com/yourusername/battalion/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)

---

## Overview

**Battalion** is a multiplayer card game (2-6 players) combining tactical combat, resource management, and territory control. What makes it unique is its **data-driven design process**: the game has been refined through 700,000+ simulated games using genetic algorithms guided by universal game design principles.

### Key Features

- **Fast-paced tactical combat**: 20-30 turn games with dynamic army building
- **Multiple viable strategies**: Rush, Adaptive, Swarm, Tempo, Buildup, Fortress
- **Leader-driven gameplay**: Commanders, Mages, and Captains with unique abilities
- **Rich deck composition**: 76-card main deck + 18 unique leaders + 26 tricks
- **Evolutionary optimization**: Meta-evolution system refines game balance
- **Complete Python simulator**: Test strategies, run tournaments, analyze gameplay

---

## Table of Contents

- [Quick Start](#quick-start)
- [Game Overview](#game-overview)
- [Project Structure](#project-structure)
- [Simulator Usage](#simulator-usage)
- [Meta-Evolution System](#meta-evolution-system)
- [Contributing](#contributing)
- [Version History](#version-history)
- [License](#license)

---

## Quick Start

### Play Your First Game

```bash
# Clone the repository
git clone https://github.com/yourusername/battalion.git
cd battalion

# Install dependencies (optional, for meta-evolution)
pip install -r requirements.txt

# Run a quick 4-player game
python examples/quick_start.py
```

### Read the Rules

👉 **[Complete Rulebook](docs/RULEBOOK.md)**
👉 **[Card Reference](docs/CARDS_REFERENCE.md)**
👉 **[Getting Started Guide](docs/GETTING_STARTED.md)**

---

## Game Overview

### Core Mechanics

**Objective**: Eliminate opponents by destroying their towers while building and commanding armies.

**Turn Structure**:
1. **Discard Phase**: Refresh hand to influence level (min 2 cards)
2. **Build Phase**: Play troops, use contracts, buy leaders
3. **Action Phase**: Play event cards, activate abilities
4. **Combat Phase**: Attack with armies (once per army)

**Win Conditions**:
- **Conquest Victory**: Eliminate all opponents' towers (primary, ~70% of games)
- **Deck Depletion**: Highest score when deck empties (secondary)

### Card Types

- **Troops** (40): Build army strength (ranks 1-5)
- **Leaders** (18): Claim armies + unique abilities
  - **Commanders** (10): Combat bonuses, special attacks
  - **Mages** (8): Instant abilities, support powers
- **Captains** (12): Basic leaders (strength 1, +1 trick)
- **Contracts** (12): Draft leaders from playbook (cost: 1 influence)
- **Tricks** (26): Instant effects (damage, buffs, control)
- **Towers** (3 per player): Your fortress (destroy = eliminate)

### Strategic Depth

**6 Viable Strategies** (15-20% win rates each):
- **Rush**: Fast aggression, claim at 2 troops
- **Adaptive**: Dynamic claiming based on game state
- **Swarm**: Multiple small armies
- **Tempo**: Balanced economic + combat
- **Buildup**: Economic engine, large armies
- **Fortress**: Defensive bonuses, patient gameplay

---

## Project Structure

```
battalion/
├── docs/                    # Complete documentation
│   ├── RULEBOOK.md         # Game rules
│   ├── CARDS_REFERENCE.md  # All cards
│   └── GETTING_STARTED.md  # Quick start
│
├── rules/                   # Version-specific rules
│   ├── v1.6/               # Current version
│   └── archive/            # Historical versions
│
├── simulator/               # Python game engine
│   ├── battalion_simulator.py  # Core simulator (v1.18)
│   └── tests/              # Unit tests
│
├── meta_evolution/          # Evolutionary optimization
│   ├── fitness_function.py # Universal principles scoring
│   ├── analyzer.py         # Results analysis
│   └── cycles/             # Evolution history
│
├── examples/                # Tutorial scripts
│   ├── quick_start.py      # Run your first game
│   └── custom_config.py    # Custom game setup
│
└── tools/                   # Utility scripts
    └── game_analyzer.py    # Analyze game logs
```

---

## Simulator Usage

### Basic Game Simulation

```python
from simulator.battalion_simulator import simulate_game, GameConfig

# Use default balanced configuration
config = GameConfig()

# Run a 4-player game with detailed logging
result = simulate_game(
    num_players=4,
    config=config,
    detailed_log=True
)

print(f"Winner: Player {result['winner']}")
print(f"Game Length: {result['turn_count']} turns")
print(f"Elimination Rate: {result['elimination_rate']*100}%")
```

### Custom Configuration

```python
# Create aggressive, fast-paced variant
config = GameConfig(
    tower_base_hp=3,              # Easier to eliminate (default: 4)
    starting_influence=8,         # More resources (default: 6)
    troop_deck_size=60,           # Smaller deck (default: 115)
    attack_chains_allowed=3,      # Multi-attacks (default: 1)
    leader_contract_cost=2,       # Cheaper contracts (default: 3)
)

result = simulate_game(4, config)
```

### Run Multiple Games

```python
# Tournament simulation
results = []
for i in range(100):
    result = simulate_game(num_players=4, config=config)
    results.append(result)

# Analyze results
avg_length = sum(r['turn_count'] for r in results) / len(results)
conquest_rate = sum(1 for r in results if r['elimination_victory']) / len(results)

print(f"Average Game Length: {avg_length:.1f} turns")
print(f"Conquest Victory Rate: {conquest_rate*100:.1f}%")
```

---

## Meta-Evolution System

### Overview

Battalion uses a **genetic algorithm** to evolve optimal game parameters guided by **20 Universal Game Design Principles**.

**Process**:
1. Generate 48 random game configurations
2. Simulate 100 games per configuration (~5,000 total games)
3. Score each configuration using comprehensive fitness function
4. Evolve best configurations over 150 generations
5. Analyze results and generate improvement proposals
6. Implement approved changes and repeat

### Fitness Function

**Total Score**: 0-1,100 points (up to 2,200 with elimination multiplier)

**Components**:
- **Core Fitness** (400 pts):
  - Playability (0-100): Game completes without errors
  - Strategic Depth (0-100): Multiple paths to victory
  - Pacing (0-100): Turn count in target range (20-30)
  - Engagement (0-100): Balanced player scores

- **Universal Principles** (500 pts):
  - 20 principles × 0-100 score, averaged × 5.0
  - Examples: Fun > Balance, Target Emotion, Leverage, Constraints

- **Exploration Bonus** (200 pts):
  - Novelty score: Unique parameter combinations
  - Extreme viability: Rare successful configurations

- **Variance Penalties** (-300 pts):
  - High variance: Unpredictable outcomes
  - Low differentiation: All games feel same
  - Runaway leader: Unstoppable advantage

- **Elimination Multiplier** (0.5× to 2.0×):
  - 0-30%: 0.5-0.9× (games too long)
  - 30-70%: 0.9-1.5× (optimal zone)
  - 70-100%: 1.5-2.0× (decisive victories)

### Evolution Results

**Cycle 9** (Latest stable):
- **Fitness**: 803.24
- **Elimination Rate**: 41%
- **Average Game Length**: 30 turns
- **Strategy Balance**: All 6 strategies 15-20% win rate

See [meta_evolution/results/EXECUTIVE_SUMMARY.md](meta_evolution/results/EXECUTIVE_SUMMARY.md) for full analysis.

### Run Your Own Evolution

```bash
cd meta_evolution
python run_cycle.py --cycles 1 --population 48 --generations 150 --games 100
```

**Warning**: Full cycle takes ~10-30 minutes and runs 720,000 simulations!

---

## Contributing

We welcome contributions from game designers, developers, and playtesters!

### Ways to Contribute

- **Playtesting**: Try the physical card game and provide feedback
- **Balance Suggestions**: Propose card changes or mechanic tweaks
- **Code**: Improve simulator, add features, fix bugs
- **Documentation**: Clarify rules, add examples, translate
- **Analysis**: Run evolution cycles, analyze data, find insights

### Getting Started

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
2. Check [Issues](https://github.com/yourusername/battalion/issues) for open tasks
3. Join discussions in [Discussions](https://github.com/yourusername/battalion/discussions)
4. Submit PRs with improvements!

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/battalion.git
cd battalion

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest simulator/tests/
```

---

## Version History

### Current: v1.6 (2025) - "Game Length Optimization"
- **Focus**: Reduced game length from 49 → 30 turns
- **Changes**: 1-influence contracts, deck depletion penalty
- **Status**: ✅ Stable, 30-turn games, 90% conquest rate

### v1.18 (Meta-Evolution) - "Bug Fixes + ANTE System"
- **Simulator version**: v1.18 (latest)
- **Changes**: Fixed Standard Contract, Ghost Cards removed, ANTE Captain jackpot
- **Cycles**: 8-14 (ongoing evolutionary optimization)

### Historical Versions

| Version | Year | Focus | Key Changes |
|---------|------|-------|-------------|
| v0.9 | 2019 | Original | Initial release, Fiverr art |
| v1.2 | 2025 | Playbook | Separate leader deck |
| v1.5 | 2025 | Balance | 40 troops (was 58), 12 captains (was 7) |
| v1.6 | 2025 | Pacing | Contract cost 1 inf, deck penalty |
| v1.17+ | 2025 | Evolution | Meta-evolution cycles 1-14 |

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## Research & Development

### Published Results

- **Total Games Simulated**: 700,000+
- **Evolution Cycles**: 14 (cycles 8-9 stable)
- **Parameters Optimized**: 54 game variables
- **Fitness Improvement**: 73.3% (Cycle 7 → 8 after bug fixes)

### Key Insights

1. **Elimination Rate Dominates Fitness**: 20% increase in elimination → 73% fitness boost
2. **Bug Fixes > Parameter Tuning**: Fixing broken mechanics matters more than optimization
3. **Multiple Equilibria Exist**: Different parameter sets achieve similar fitness
4. **Strategy Diversity Emerges**: GA naturally balances 6 distinct play styles

### Ongoing Research

- **Cycle 14** (In Progress): Balance fixes for bypass attacks and elimination rewards
- **Territory Control**: Exploring v1.7+ mechanics for area control gameplay
- **Reinforcement Learning**: Training AI agents to discover novel strategies

---

## Resources

### Documentation
- 📖 **[Complete Rulebook](docs/RULEBOOK.md)** - Full game rules
- 🃏 **[Card Reference](docs/CARDS_REFERENCE.md)** - All 114 cards
- 🚀 **[Getting Started](docs/GETTING_STARTED.md)** - Quick start guide
- 🤝 **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- 📊 **[Design Philosophy](docs/DESIGN_PHILOSOPHY.md)** - Core principles

### Community
- 💬 [Discussions](https://github.com/yourusername/battalion/discussions) - Ask questions, share ideas
- 🐛 [Issues](https://github.com/yourusername/battalion/issues) - Report bugs, request features
- 📈 [Project Board](https://github.com/yourusername/battalion/projects) - Development roadmap

### External Links
- 🎨 Card Art & Assets: [Link to assets repository or download]
- 📄 Printable Cards (PDF): [Link to print-ready files]
- 🎮 Online Playtest Platform: [Link if available]

---

## Credits

### Design & Development
- **Game Design**: Alex Dené (Original concept & evolution)
- **Meta-Evolution System**: Claude AI + Alex Dené (Collaborative development)
- **Card Art**: Fiverr Artists + Team Photos (v1.0 deck)
- **Simulation Engine**: Python implementation with genetic algorithms

### Special Thanks
- Nathan & Luke (Captain card models)
- Playtester community (feedback and balance suggestions)
- Contributors (see [CONTRIBUTORS.md](CONTRIBUTORS.md))

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**Summary**:
- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ✅ Attribution required
- ❌ No warranty provided

---

## Citation

If you use Battalion in research or academic work, please cite:

```bibtex
@software{battalion2025,
  title = {Battalion: A Data-Driven Card Game Design},
  author = {Dené, Alex},
  year = {2025},
  url = {https://github.com/yourusername/battalion},
  note = {Strategic card game optimized through evolutionary algorithms}
}
```

---

## Contact

- **Project Lead**: Alex Dené
- **Email**: [Your email or contact form]
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Issues**: [Report bugs or request features](https://github.com/yourusername/battalion/issues)

---

<p align="center">
  <b>Built with ❤️ using Python, Genetic Algorithms, and Universal Game Design Principles</b>
</p>

<p align="center">
  <i>"Fun above all else. 20-30 turn games. Strategic diversity. Linear experience 2P-6P."</i>
</p>
