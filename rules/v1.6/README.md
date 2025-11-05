# Battalion - Rules Version 1.6 (2025)

**Status:** ✅ Core Mechanics Validated - Economic Analysis Complete  
**Parent Version:** v1.5 (2025)  
**Focus:** Game Length Optimization, Strategy Balance & Economic Dynamics  
**Latest Update:** October 30, 2025

---

## Version 1.6 Goals

Based on comprehensive 50,000-game testing of v1.5, version 1.6 addresses critical issues:

### Primary Objectives

1. **Reduce Game Length** ⏱️
   - Current: 26-49 turns (4P worst at 49 turns)
   - Target: 20-30 turns consistently
   - Solution: Contract cost reduction + deck depletion penalty

2. **Balance Buildup & Fortress Strategies** ⚖️
   - Current: 5-14% win rates (unviable)
   - Target: 15-20% win rates (competitive)
   - Solution: Faster claiming thresholds + strategic bonuses

3. **Encourage Buying Leaders** 💰
   - Current: 3-12% buying rate
   - Target: 30-40% buying rate
   - Solution: Buff bought leaders + strategy fixes

---

## Key Changes from v1.5

### 1. Contract Cost Reduction (Priority 1)

**Change:** Contracts cost **1 influence** (was 2 influence)

**Rationale:**
- v1.5 testing showed 2-influence contracts slowed games from 33→49 turns
- 1-influence balances speed vs. buying incentive
- Maintains contract viability while encouraging faster gameplay

**Impact:**
- Expected: 30-35 turn games (down from 49)
- Faster leader acquisition
- More aggressive early gameplay

---

### 2. Deck Depletion Penalty (Priority 1)

**NEW RULE:** When the main deck is empty, all players lose 1 tower at the start of each round.

**Rationale:**
- Prevents 49-turn marathons from deck depletion
- Creates urgency when deck runs low
- Forces conclusion within ~5 turns of deck empty
- Rewards efficient play over stalling

**Impact:**
- Games end by conquest more often (target: 70%+)
- Eliminates ultra-long stalemates
- Adds strategic pressure in late game

**Example:**
- Turn 40: Deck empties, 3 players remain (all 3 towers)
- Turn 41: All players lose 1 tower (now 2 towers each)
- Turn 46: All players lose another tower (now 1 tower each)
- Turn 51: All players lose final tower (game ends, highest score wins)

---

### 3. Strategy Rebalancing (Priority 2)

**Buildup Strategy Changes:**
- **OLD:** Claim at 4+ troops, attack with 2+ armies
- **NEW:** Claim at 3+ troops, attack with 1+ army
- Maintains economic focus but competes on speed

**Fortress Strategy Changes:**
- **OLD:** Claim at 5+ troops, attack with 2+ armies
- **NEW:** Claim at 3+ troops, defensive bonus active
- **NEW ABILITY:** "First attack received each turn deals -2 damage to your armies"
- Trades offense for defense while maintaining tempo

---

### 4. Buying Incentives (Priority 3)

**Strategy Implementation Fix:**
- ALL strategies now buy leaders when influence ≥ 5
- Previously only Tempo bought (4% rate)
- Encourages mixed economy (contracts + buying)

**Future Consideration:**
- If buying remains low, increase bought leader bonus: +1 attack → +2 attack
- Monitor in testing before implementing

---

## Testing Plan

### Phase 1: Contract Cost + Deck Depletion (NOW)
1. Implement 1-influence contracts
2. Implement deck depletion penalty
3. Run 10,000 games at 4P (worst offender in v1.5)
4. **Success Criteria:**
   - Game length: 25-35 turns
   - Conquest rate: 65%+
   - No strategy above 25% or below 12%

### Phase 2: Strategy Buffs
1. Update Buildup strategy (claim 3+, attack 1+)
2. Update Fortress strategy (claim 3+, defensive bonus)
3. Run 10,000 games at 5P-6P (where they're weakest)
4. **Success Criteria:**
   - Buildup: 15-20% win rate
   - Fortress: 15-20% win rate
   - Balanced across all player counts

### Phase 3: Buying Encouragement
1. Update all strategies to buy at 5+ influence
2. Run 10,000 games across 2P-6P
3. **Success Criteria:**
   - Buying rate: 30-40%
   - Contracts: 60-70% (still dominant but not exclusive)
   - Win rates remain balanced

### Phase 4: Comprehensive Validation
1. Run 50,000 games (10k per player count)
2. Validate all metrics meet targets
3. If successful, close v1.6 and finalize

---

## v1.5 Testing Results Summary

**Total Games:** 50,000 (10,000 per player count)

**Critical Issues Found:**
- ❌ Game length 50-145% over target (worst: 4P at 49 turns)
- ❌ Buildup & Fortress severely underpowered (5-14% win rates)
- ❌ Buying virtually unused (3-12% vs 40% target)
- ❌ Conquest rate too low (58% vs 80% target)

**What Worked:**
- ✅ Adaptive claiming system (prevents getting stuck)
- ✅ Excellent balance among 4 aggressive strategies
- ✅ Contract system provides consistent gameplay
- ✅ No crashes or edge cases

**Why v1.6 Is Necessary:**
v1.5's 2-influence contract fix (correcting simulator bug) inadvertently made games too long. v1.6 reverts this while adding deck depletion penalty to prevent marathons.

---

## File Structure

```
Rules version 1.6 (2025)/
├── README.md (this file)
├── CHANGELOG.md
├── cards/
│   └── index.md
├── rules/
│   └── index.md
└── testing/
    ├── battalion_simulator.py (v1.6)
    └── [test results will go here]
```

---

## Working Principles Alignment

**From WORKING-PRINCIPLES.md:**

1. ✅ **Fun above all else** - Shorter games = more fun, less drag
2. 🎯 **20-30 turn games** - Primary focus of v1.6!
3. 🎯 **Strategic diversity** - Fixing Buildup/Fortress for 6 viable strategies
4. ✅ **Linear experience 2P-6P** - Deck depletion penalty scales naturally

---

## Development Status

- [x] Create v1.6 folder structure
- [x] Copy v1.5 rules and cards
- [x] Document v1.6 changes
- [x] Update simulator with contract cost reduction (1 influence)
- [x] Implement deck depletion penalty (-1 tower/round when deck empty)
- [x] Update Buildup strategy (claim 3+, attack 1+)
- [x] Update Fortress strategy (claim 3+, defensive bonus -2 damage)
- [x] Update buying behavior (all strategies buy at 5+ influence)
- [x] Run Phase 1 testing (10k games at 4P) - ✅ 30 turns avg, 90% pure conquest
- [x] Run Phase 3 testing (buying behavior) - ⚠️ 7% buying rate (below target)
- [x] Implement comprehensive tracking (tower sources, influence variation, deck consumption)
- [x] Validate conquest mechanics (94.6% combat-driven, 90% pure conquest)
- [ ] Run genetic algorithm to explore mechanic improvements
- [ ] Address economic stagnation (increase contract costs or add economic pressure)
- [ ] Achieve 20-30% buying rate target
- [ ] Run final comprehensive 50k testing
- [ ] Finalize v1.6 and create v1.7 proposals

---

## Current Findings (October 30, 2025)

**✅ SUCCESSES:**
- 🎯 Game length: 30 turns (within 20-30 target)
- 🏆 90% pure conquest (target: 70%+)
- ⚖️ Balanced strategies: 15-20% win rates across all 6 strategies
- 🏰 94.6% tower destruction from combat (proves conquest is real)
- ⚡ Deck depletion creates pressure without forcing (only 5% forced endings)

**⚠️ REMAINING ISSUES:**
- 💰 Buying rate: 7% (target: 20-30%)
- 📊 Influence variation: 0.7 stddev (target: 1.5+, shows "LOW FLEX")
- 🛡️ Contracts: 100% usage (no trade-offs at 1 influence cost)
- 🔄 Only 16% of players "flex" (drop to ≤2, recover to 5+)

**🎯 ROOT CAUSE:**
Contract cost of 1 influence is too cheap. Players maintain steady 3-4 influence without strategic decisions.

**📈 NEXT STEP:** 
Use genetic algorithm to test contract cost variations (2-3 influence) and explore economic pressure mechanics (progressive costs, influence decay, etc.) to achieve target buying rates and influence variation.

---
