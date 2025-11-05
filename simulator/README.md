# Battalion Simulator

Python implementation of Battalion game rules for simulation and analysis.

## Quick Start

```python
from simulator.battalion_simulator import simulate_game, GameConfig

# Run a 4-player game
config = GameConfig()
result = simulate_game(num_players=4, config=config, detailed_log=True)

print(f"Winner: Player {result['winner']}")
print(f"Game Length: {result['turn_count']} turns")
```

## Version

**Current**: v1.18 (Meta-Evolution)

**Changes in v1.18**:
- ✅ Standard Contract bug fix (100% reliability)
- ✅ ANTE Captain jackpot system
- ✅ Ghost Cards removed (18 unimplemented cards)
- ✅ Hand size limit (10 cards max)
- ✅ AI anti-feeder logic

See [examples/](../examples/) for more usage examples.
