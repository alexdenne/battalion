# Contributing to Battalion

Thank you for your interest in contributing to Battalion! This guide will help you get started with contributing to the project, whether you're a game designer, developer, playtester, or data analyst.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Submission Guidelines](#submission-guidelines)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We expect:

- **Respectful communication**: Disagree professionally, focus on ideas not people
- **Constructive feedback**: Offer solutions, not just criticism
- **Collaboration**: Work together to improve the game
- **Patience**: Remember everyone is learning

### Reporting Issues

If you experience harassment or unacceptable behavior, please contact the project maintainers at [your-email].

---

## How Can I Contribute?

### 🎮 Playtesting

**Best for**: Game designers, casual players

**What you do**:
- Print and play the physical card game
- Run games with 2-6 players
- Document your experience (game length, strategy viability, fun moments)
- Report balance issues or confusing rules

**How to start**:
1. Download printable cards from [assets repository link]
2. Read the [rulebook](docs/RULEBOOK.md)
3. Play 3-5 games
4. Submit feedback via [Playtest Feedback Form](link) or create an issue

**Example feedback**:
```markdown
## Playtest Report

**Date**: 2025-11-05
**Players**: 4
**Game Length**: 28 turns
**Winner Strategy**: Rush

**Observations**:
- Captains feel too weak compared to Commanders
- Fortress strategy couldn't keep up with aggression
- Trick cards were decisive in final combat
- Overall: Fun, but needs balance tweaks

**Suggestions**:
- Increase Captain strength to 2?
- Add defensive bonuses for Fortress players
```

### 🎨 Game Design

**Best for**: Game designers, balance experts

**What you do**:
- Propose new cards or mechanics
- Suggest balance changes
- Design alternative game modes
- Contribute to design philosophy

**How to start**:
1. Read [DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md)
2. Review current [balance issues](link-to-issues)
3. Submit proposals via GitHub Issues with tag `design-proposal`

**Proposal template**:
```markdown
## Design Proposal: [Title]

**Problem**: What gameplay issue does this address?
**Solution**: Your proposed change
**Expected Impact**: How will this improve the game?
**Trade-offs**: What are the downsides?
**Testing Plan**: How can we validate this works?
```

### 💻 Code Contributions

**Best for**: Python developers, algorithm enthusiasts

**What you do**:
- Fix bugs in the simulator
- Add new features
- Improve performance
- Write unit tests

**How to start**:
1. Set up development environment (see below)
2. Find an issue tagged `good-first-issue` or `help-wanted`
3. Comment on the issue to claim it
4. Submit a pull request

### 📊 Data Analysis

**Best for**: Data scientists, researchers

**What you do**:
- Run evolution cycles
- Analyze game balance
- Visualize fitness landscapes
- Identify parameter correlations

**How to start**:
1. Read [meta_evolution/README.md](meta_evolution/README.md)
2. Run your own evolution cycle
3. Share findings in [Discussions](link)
4. Submit analysis reports via pull request

### 📝 Documentation

**Best for**: Technical writers, educators

**What you do**:
- Clarify confusing rules
- Add code examples
- Create tutorials
- Translate documentation

**How to start**:
1. Identify unclear documentation
2. Submit improvements via pull request
3. Tag with `documentation` label

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of card games (for game design)
- Basic Python knowledge (for code contributions)

### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/battalion.git
cd battalion

# 3. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install development dependencies
pip install -r requirements-dev.txt  # pytest, black, mypy, etc.

# 6. Create a feature branch
git checkout -b feature/your-feature-name

# 7. Run tests to verify setup
python -m pytest simulator/tests/
```

### Project Structure (Quick Reference)

```
battalion/
├── simulator/          # Core game engine
│   ├── battalion_simulator.py
│   └── tests/
├── meta_evolution/     # Genetic algorithm system
│   ├── fitness_function.py
│   └── cycles/
├── docs/               # Documentation
├── examples/           # Tutorial scripts
└── tools/              # Utility scripts
```

---

## Development Workflow

### 1. Choose an Issue

- Browse [open issues](link)
- Look for tags: `good-first-issue`, `help-wanted`, `bug`, `enhancement`
- Comment to claim: "I'd like to work on this"
- Wait for maintainer confirmation

### 2. Create a Branch

```bash
# Branch naming conventions:
# - feature/description-of-feature
# - fix/description-of-bug
# - docs/description-of-update
# - refactor/description-of-refactor

git checkout -b feature/add-new-card-type
```

### 3. Make Changes

- Write clean, readable code
- Follow style guidelines (see below)
- Add tests for new features
- Update documentation

### 4. Test Your Changes

```bash
# Run all tests
python -m pytest simulator/tests/

# Run specific test file
python -m pytest simulator/tests/test_combat.py

# Run with coverage
python -m pytest --cov=simulator simulator/tests/

# Test a quick game simulation
python examples/quick_start.py
```

### 5. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new Territory Control card type

- Implement Territory card class
- Add territory claiming mechanic
- Update game state to track territories
- Add tests for territory mechanics"
```

**Commit message format**:
```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/add-new-card-type

# Go to GitHub and create a pull request
# Fill out the PR template (see below)
```

---

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some project-specific conventions:

**Formatting**:
```bash
# Use Black for automatic formatting
black simulator/ meta_evolution/ tools/

# Check with flake8
flake8 simulator/ meta_evolution/
```

**Key conventions**:
- **Line length**: 100 characters (not 80)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings `"like this"`
- **Imports**: Grouped (standard library, third-party, local)

**Example**:
```python
from typing import List, Optional
import random

from dataclasses import dataclass
import numpy as np

from simulator.game_state import GameState


@dataclass
class Card:
    """Represents a game card.

    Attributes:
        name: Card name (e.g., "Captain")
        card_type: Type of card (TROOP, LEADER, EVENT)
        strength: Combat strength (0-5)
    """
    name: str
    card_type: str
    strength: int = 0

    def can_attack(self, game_state: GameState) -> bool:
        """Check if card can initiate an attack."""
        return self.strength > 0 and not game_state.attacked_this_turn
```

### Documentation Style

**Docstrings**: Google style
```python
def calculate_fitness(game_result: dict, config: GameConfig) -> float:
    """Calculate comprehensive fitness score for a game configuration.

    Args:
        game_result: Dictionary containing game outcome data
        config: Game configuration that was tested

    Returns:
        Fitness score between 0-1100 (before multiplier)

    Raises:
        ValueError: If game_result missing required keys

    Example:
        >>> result = simulate_game(4, config)
        >>> fitness = calculate_fitness(result, config)
        >>> print(f"Fitness: {fitness:.2f}")
    """
    pass
```

**Comments**: Explain "why", not "what"
```python
# GOOD: Explains reasoning
# Use influence floor of 2 to prevent death spiral where players
# can't draw cards, can't gain influence, can't recover
hand_size = max(2, player.influence)

# BAD: Just repeats the code
# Set hand size to max of 2 or player influence
hand_size = max(2, player.influence)
```

### Markdown Documentation

- Use **ATX headers** (`# Header` not underlines)
- **One sentence per line** for easy diffing
- **Code blocks**: Always specify language
- **Links**: Use reference-style for repeated URLs
- **Tables**: Use for structured data

---

## Testing Guidelines

### Unit Tests

**Coverage requirement**: 80% minimum for new code

**Test structure**:
```python
# simulator/tests/test_combat.py
import pytest
from simulator.battalion_simulator import resolve_combat, Army

class TestCombat:
    """Tests for combat resolution mechanics."""

    def test_basic_combat_attacker_wins(self):
        """Attacker with higher strength should win combat."""
        attacker = Army(strength=5, leader="Captain")
        defender = Army(strength=3, leader=None)

        result = resolve_combat(attacker, defender)

        assert result['winner'] == 'attacker'
        assert result['damage_dealt'] == 2
        assert defender.strength == 1

    def test_combat_with_equal_strength(self):
        """Equal strength combat should result in mutual damage."""
        attacker = Army(strength=4, leader="Captain")
        defender = Army(strength=4, leader="Mage")

        result = resolve_combat(attacker, defender)

        assert result['winner'] == 'tie'
        assert attacker.strength < 4
        assert defender.strength < 4

    @pytest.mark.parametrize("attacker_str,defender_str,expected", [
        (5, 3, 'attacker'),
        (3, 5, 'defender'),
        (4, 4, 'tie'),
    ])
    def test_combat_outcomes(self, attacker_str, defender_str, expected):
        """Test various combat strength combinations."""
        attacker = Army(strength=attacker_str)
        defender = Army(strength=defender_str)
        result = resolve_combat(attacker, defender)
        assert result['winner'] == expected
```

### Integration Tests

Test complete game flows:
```python
def test_full_game_completes_successfully():
    """A standard 4-player game should complete without errors."""
    config = GameConfig()
    result = simulate_game(num_players=4, config=config)

    assert result['winner'] in range(4)
    assert result['turn_count'] > 0
    assert result['turn_count'] < 100  # Reasonable upper limit
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest simulator/tests/test_combat.py

# Specific test
pytest simulator/tests/test_combat.py::TestCombat::test_basic_combat_attacker_wins

# With coverage report
pytest --cov=simulator --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

## Submission Guidelines

### Pull Request Template

```markdown
## Description
Brief description of your changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123
Related to #456

## Changes Made
- Detailed list of what you changed
- Why you made these changes
- Any trade-offs or design decisions

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Tested manually (describe how)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No new warnings generated
- [ ] Added tests with good coverage

## Screenshots (if applicable)
[Add screenshots for UI/visual changes]

## Additional Context
Any other information reviewers should know.
```

### Review Process

1. **Automated Checks**: CI/CD runs tests and style checks
2. **Maintainer Review**: Code review by project maintainer
3. **Feedback**: Address any requested changes
4. **Approval**: Maintainer approves PR
5. **Merge**: Squash and merge into main branch

**Timeline**: Expect response within 48-72 hours

### What Makes a Good PR?

✅ **Good PR**:
- Single focused change
- Clear description
- Tests included
- Documentation updated
- Small diff (<300 lines preferred)

❌ **Avoid**:
- Multiple unrelated changes
- No tests
- Breaking changes without discussion
- Massive refactors (>1000 lines)
- Formatting-only changes mixed with logic changes

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Design discussions, questions, showcases
- **Pull Requests**: Code review, technical discussion

### Getting Help

- Check [FAQ](docs/FAQ.md)
- Search [existing issues](link)
- Ask in [Discussions](link)
- Tag `@maintainer` for urgent questions

### Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes
- Project README

---

## Advanced Topics

### Running Meta-Evolution Cycles

```bash
cd meta_evolution
python run_cycle.py \
    --cycles 1 \
    --population 48 \
    --generations 150 \
    --games 100 \
    --output cycles/cycle_test/
```

**Warning**: Takes 10-30 minutes and runs 720,000 simulations!

### Custom Fitness Functions

To experiment with different fitness criteria:

1. Copy `meta_evolution/fitness_function.py`
2. Modify scoring components
3. Run test cycle
4. Compare results with baseline
5. Submit as research contribution

### Adding New Card Types

1. Update `EventCardType` enum
2. Add card effect in `resolve_event_card()`
3. Add AI logic in `choose_card_to_play()`
4. Create tests
5. Update card documentation

---

## License

By contributing to Battalion, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

**Project Lead**: Alex Dené
**Email**: [your-email]
**Issues**: [GitHub Issues](link)

**Thank you for contributing to Battalion!** 🎮🃏

