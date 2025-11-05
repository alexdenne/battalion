# Changelog - Version 1.6 (2025)

## Version 1.6.0 - Game Length Optimization (In Development)

**Release Date:** TBD  
**Parent Version:** v1.5 (2025)  
**Testing Status:** Phase 1 - Initial Development

---

### 🎯 Primary Goal: Reduce Game Length

**Problem Statement:**
- v1.5 games averaged 26-49 turns (target: 20-30)
- 4P games worst offender: 49 turns (145% over target)
- Caused by 2-influence contract cost (corrected simulator bug)
- 42% of games end by deck depletion (should be <20%)

**Solution:**
- Revert contract cost to 1 influence
- Add deck depletion penalty to force conclusions
- Rebalance weak strategies to increase aggression

---

### ⚡ Breaking Changes

#### 1. Contract Cost Reduction
**Changed:** Contracts cost **1 influence** (was 2 influence in v1.5)

**Before (v1.5):**
```
Use Contract: Discard Contract + 1 card + 2 influence → Get leader
```

**After (v1.6):**
```
Use Contract: Discard Contract + 1 card + 1 influence → Get leader
```

**Impact:**
- Faster leader acquisition
- More influence available for other actions
- Expected 20-30% reduction in game length
- Risk: May make contracts too dominant (monitor buying rate)

**Rationale:**
The 2-influence cost in v1.5 was correct per rules, but testing showed it slowed games excessively (33→49 turns in 4P). The 1-influence cost represents a deliberate design change to prioritize game length over exact cost parity with buying.

---

#### 2. Deck Depletion Penalty (NEW MECHANIC)
**Added:** When main deck is empty, all players lose 1 tower per round

**Mechanic Details:**
- Triggers at **start of each round** after deck empties
- Affects **all players** simultaneously
- Continues until game ends by conquest or mutual elimination

**Example Timeline:**
```
Turn 38: Main deck has 5 cards
Turn 40: Main deck empties (0 cards)
Turn 41: Round starts → All players lose 1 tower
Turn 46: Round starts → All players lose 1 tower (again)
Turn 51: Round starts → All players lose 1 tower (game ends if anyone eliminated)
```

**Impact:**
- Forces games to conclude within ~5-10 turns of deck depletion
- Increases conquest win rate (target: 70%+ vs current 58%)
- Creates late-game urgency ("rush to eliminate before towers fall")
- Prevents 49-turn marathons

**Rationale:**
Without this, players can stalemate indefinitely once deck empties, leading to point-counting games that violate "fun above all else" principle.

---

### 🔧 Strategy Adjustments

#### 3. Buildup Strategy Buff
**Changed:** Claiming and attacking thresholds

**Before (v1.5):**
- Claim at: 4+ troops (quality armies)
- Attack with: 2+ armies (combined forces)
- Win rate: 9-14% (severely underpowered)

**After (v1.6):**
- Claim at: 3+ troops (competitive speed)
- Attack with: 1+ army (maintains tempo)
- Still focuses on economic advantage
- Expected win rate: 15-20%

**Rationale:**
Buildup's 4+ claiming threshold was too slow. By time it claimed, aggressive strategies had 2-3 armies. New 3+ threshold keeps economic theme while competing on speed.

---

#### 4. Fortress Strategy Buff
**Changed:** Claiming threshold + new defensive ability

**Before (v1.5):**
- Claim at: 5+ troops (massive armies)
- Attack with: 2+ armies
- Win rate: 5-12% (nearly unviable, especially 6P at 5%)

**After (v1.6):**
- Claim at: 3+ troops (matches aggro speed)
- Attack with: 1+ army
- **NEW ABILITY:** "First attack received each turn deals -2 damage to your armies"
- Expected win rate: 15-20%

**Defensive Bonus Explanation:**
- First incoming attack each turn reduced by 2 damage
- Represents defensive positioning/fortifications
- Allows Fortress to claim faster while maintaining defensive identity
- Subsequent attacks same turn deal full damage

**Example:**
```
Fortress has 5-troop army
Player 1 attacks with 4 power → Reduced to 2 → Army takes 2 damage (now 3 troops)
Player 2 attacks with 4 power → Full damage → Army takes 4 damage (eliminated)
```

**Rationale:**
Waiting for 5+ troops was a death sentence. New threshold with defensive bonus maintains theme ("hard to kill") without sacrificing tempo.

---

### 🛠️ Implementation Changes

#### 5. Buying Behavior Fix (All Strategies)
**Changed:** All strategies now buy leaders opportunistically

**Before (v1.5):**
- Only Tempo strategy bought leaders (4% rate)
- All others: 0% buying
- Total buying rate: 3-12% across player counts

**After (v1.6):**
- ALL strategies buy when influence ≥ 5
- Maintains contract preference when influence < 5
- Expected buying rate: 30-40%

**Strategy-Specific Behavior:**
```python
# Pseudocode for all strategies
if influence >= 5 and has_leader_available:
    buy_leader()  # Get +1 attack bonus
elif has_contract:
    use_contract()  # Save influence
else:
    take_other_action()
```

**Rationale:**
Low buying rate in v1.5 was simulator implementation issue, not player behavior issue. Real players would buy when they have excess influence. This makes strategies more realistic.

---

### 📊 Expected Impacts

#### Game Length Prediction
| Player Count | v1.5 Actual | v1.6 Target | Expected |
|--------------|-------------|-------------|----------|
| 2P | 26 turns | 20-25 | 22 turns |
| 3P | 36 turns | 25-30 | 28 turns |
| 4P | 49 turns | 25-30 | 30 turns |
| 5P | 40 turns | 25-30 | 28 turns |
| 6P | 36 turns | 25-30 | 26 turns |

**Key Changes:**
- 1-influence contracts: -20% game length
- Deck depletion penalty: Forces conclusion
- Faster strategies: +10% aggression

---

#### Strategy Balance Prediction
| Strategy | v1.5 Win % | v1.6 Target | Expected |
|----------|------------|-------------|----------|
| Rush | 19-22% | 16-20% | 18% ✅ |
| Adaptive | 20-22% | 16-20% | 19% ✅ |
| Swarm | 18-21% | 16-20% | 18% ✅ |
| Tempo | 17-20% | 16-20% | 17% ✅ |
| Buildup | 10-14% | 16-20% | 17% 🎯 |
| Fortress | 5-12% | 16-20% | 16% 🎯 |

**Key Improvements:**
- Buildup: +5% from faster claiming
- Fortress: +8% from defensive bonus + tempo
- Top 4: Slight decrease from stronger competition

---

#### Resource Usage Prediction
| Metric | v1.5 | v1.6 Target | Expected |
|--------|------|-------------|----------|
| Contract Usage | 97-100% | 60-70% | 65% |
| Buying Usage | 3-12% | 30-40% | 35% |
| Conquest Rate | 58% | 70-80% | 72% |
| Avg Influence | 2.5-5.8 | 3.0-4.5 | 3.5 |

**Key Changes:**
- Lower contract cost → more frequent usage
- Buying at 5+ influence → healthy mix
- Deck penalty → more conquest wins

---

### 🧪 Testing Plan

#### Phase 1: Core Mechanics (Current)
- [x] Reduce contract cost to 1 influence
- [x] Implement deck depletion penalty
- [ ] Run 10,000 games at 4P
- [ ] Validate: Game length 25-35 turns, conquest 65%+

#### Phase 2: Strategy Balance
- [ ] Update Buildup (claim 3+, attack 1+)
- [ ] Update Fortress (claim 3+, defensive bonus)
- [ ] Run 10,000 games at 5P-6P
- [ ] Validate: Both strategies 15-20% win rate

#### Phase 3: Economic Balance
- [ ] Update all strategies to buy at 5+ influence
- [ ] Run 10,000 games across all player counts
- [ ] Validate: 30-40% buying rate, balanced wins

#### Phase 4: Comprehensive Validation
- [ ] Run 50,000 games (10k per player count)
- [ ] Validate all metrics within target ranges
- [ ] Document final results
- [ ] Close v1.6 or iterate

---

### 🔄 Migration Guide (v1.5 → v1.6)

#### For Players
**What You'll Notice:**
- Games are **shorter** (20-30 turns vs 30-50)
- **More aggressive** play in late game (deck depletion pressure)
- **More buying** (players saving influence for bought leaders)
- **Buildup/Fortress viable** (can compete with rush strategies)

**Strategy Adjustments:**
- **Buildup players:** Claim at 3+ now (not 4+)
- **Fortress players:** Claim at 3+, use defensive bonus tactically
- **All players:** Consider buying at 5+ influence
- **Late game:** Push for elimination when deck low (tower penalty coming)

#### For Developers
**Simulator Changes:**
1. `try_use_contract()`: Change influence cost 2 → 1
2. `play_game()`: Add deck depletion penalty check
3. `action_economy()`: Update Buildup claiming (4+ → 3+)
4. `action_economy_patient()`: Update Fortress claiming (5+ → 3+) + defensive bonus
5. All action functions: Add buying behavior at 5+ influence

**Testing Checklist:**
- [ ] Contract cost correctly applied (1 influence)
- [ ] Deck depletion penalty triggers per round
- [ ] Buildup claims at 3+ troops
- [ ] Fortress defensive bonus works (-2 damage first attack)
- [ ] All strategies buy at 5+ influence
- [ ] Game length statistics tracked
- [ ] Conquest rate calculated correctly

---

### 📝 Notes

**Design Philosophy:**
This version prioritizes **fun** (20-30 turn games) over perfect balance. The deck depletion penalty is a deliberate "forcing function" to prevent marathons that violate working principles.

**Risk Assessment:**
- **Low Risk:** Contract cost reduction (tested at 1 inf in early v1.5)
- **Medium Risk:** Deck depletion penalty (new mechanic, may feel arbitrary)
- **Low Risk:** Strategy buffs (incremental changes)

**Rollback Plan:**
If v1.6 testing shows games too short (<20 turns) or conquest too high (>85%), can increase contract cost to 1.5 influence (effective cost via other mechanism) or adjust deck depletion timing.

---

**Last Updated:** October 30, 2025  
**Status:** Phase 1 Development  
**Next Milestone:** Implement simulator changes and run 10k test
