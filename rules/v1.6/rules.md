# Battalion - Complete Rulebook (v1.18)

**Game Design**: Strategic card game for 2-6 players
**Game Length**: 20-30 turns (15-30 minutes)
**Victory**: Last player standing or highest influence when troop deck depletes
**Simulator Version**: v1.18 (Meta-Evolution Stable)
**Date**: November 5, 2025

---

## Table of Contents

1. [Game Overview](#game-overview)
2. [Components](#components)
3. [Setup](#setup)
4. [Turn Structure](#turn-structure)
5. [Core Mechanics](#core-mechanics)
6. [Event Cards](#event-cards)
7. [Combat](#combat)
8. [Victory Conditions](#victory-conditions)
9. [Strategy Guide](#strategy-guide)

---

## Game Overview

Battalion is a strategic card game where players build armies, contract powerful leaders, and battle for supremacy. The game features a unique **two-deck system** with separate **Troop Deck** (combat power) and **Event Deck** (strategic actions), plus an **Unclaimed Pot** system where troops accumulate until players claim them.

### Key Features

- **Turn-based sequential play** - One player acts at a time (no simultaneous building)
- **Unclaimed Pot mechanic** - Troops accumulate in a communal pool, claimed via Standard Contract
- **ANTE system** - Every turn begins with 1 troop automatically added to the pot
- **Event card chaining** - Play multiple cards per turn (average 2-3 cards)
- **Multiple armies per player** - Strategic army positioning and selection
- **Two-deck system** - Troop Deck depletes (game timer), Event Deck reshuffles infinitely

---

## Components

### 1. Troop Deck (Combat Power)

**Contents**: 60-150 troops (configurable, GA-optimized)

**Troop Ranks** (Strength 1-5):
- **Rank 1**: 33% of deck - Weakest troops
- **Rank 2**: 25% of deck
- **Rank 3**: 20% of deck
- **Rank 4**: 15% of deck
- **Rank 5**: 7% of deck - Elite troops

**Captains** (40 unique):
- Represented as value `0` in the deck
- When drawn, converted to strength-10 troops ("Jackpot!")
- Mixed into the Troop Deck with regular troops

**Army Strength**: Sum of all troop ranks + leader bonuses
- Example: Army with [R3, R2, R5, R1] = 11 strength (not 4 separate attacks)

### 2. Event Deck (Strategic Actions)

**Contents**: 145 cards total (never depletes - reshuffles when empty)

**Card Types**:
- **Contract Cards** (25): Contract Mage, Contract Commander
- **Gather Troops** (30): Small (1-3), Medium (3-5), Large (5-7)
- **Attack Cards** (20): Basic, Tactical, Conditional, AOE, Risky
- **Economic Cards** (20): Gain influence, draw cards
- **Manipulation Cards** (15): Disrupt opponents
- **Utility Cards** (35): Timing, card draw, special effects

See [Event Cards](#event-cards) section for complete list.

### 3. Leader Markets (Draft System)

**Mage Market**: 3 face-up mages, 37 face-down in deck (40 total unique mages)
**Commander Market**: 3 face-up commanders, 37 face-down in deck (40 total unique commanders)

- Players can see all face-up leaders before contracting
- Markets auto-refill from decks when leaders drafted
- Strategic counter-picking and drafting decisions

**Leader Types**:
- **Captains** (40 unique): +1 attack, unit value 1, found in Troop Deck
- **Mages** (40 unique): +2 attack, unit value 1, drafted from market
- **Commanders** (40 unique): +3 attack, unit value 1, drafted from market

### 4. Player Components

Each player has:
- **3 Towers** (HP = 3-5, configurable)
- **Starting Influence**: 4-8 (configurable, default: 6)
- **Hand of event cards**: Size equals influence (floor of 2, ceiling of 10-12)
- **Multiple armies**: Each army has troops + optional leader

---

## Setup

### Game Setup

1. **Shuffle Decks**:
   - Shuffle Troop Deck (troops + 40 captains mixed together)
   - Shuffle Event Deck (145 cards)
   - Shuffle Mage Deck (40 mages)
   - Shuffle Commander Deck (40 commanders)

2. **Create Markets**:
   - Draw 3 mages face-up (Mage Market)
   - Draw 3 commanders face-up (Commander Market)

3. **Player Setup**:
   - Each player receives 3 towers
   - Each player receives starting influence (default: 6)
   - Each player draws starting hand (default: 6 event cards)

4. **Unclaimed Pot**:
   - Starts empty
   - Will fill naturally via ANTE and GATHER cards

5. **Determine Turn Order**:
   - Random starting player
   - Play proceeds clockwise (or anti-clockwise if Reverse Turn Order played)

---

## Turn Structure

Each turn follows this exact sequence:

### Phase 0: ANTE (Automatic)

**Every turn begins with the ANTE mechanic:**

1. Draw **1 troop** from the top of the Troop Deck
2. Automatically add it to the **Unclaimed Pot**
3. If the troop is a **Captain** (value 0):
   - Convert to strength-10 ("JACKPOT!")
   - Add to pot (does NOT auto-claim)

**Purpose**: Creates constant pot pressure and claiming decisions.

**Example**:
```
Turn 1: ANTE draws Rank 3 → Pot now: [3] (1 troop, strength 3)
Turn 2: ANTE draws Rank 2 → Pot now: [3, 2] (2 troops, strength 5)
Turn 3: ANTE draws CAPTAIN → Pot now: [3, 2, 10] (3 troops, strength 15) JACKPOT!
```

### Phase 1: Draw Event Card

1. Draw **1 event card** from the Event Deck
2. Add to your hand
3. If Event Deck is empty:
   - Shuffle discard pile
   - Reshuffle becomes new Event Deck
   - Continue drawing

### Phase 2: Event Card Chaining Loop

**This is the main action phase where you can play multiple cards:**

1. **Choose an event card** from your hand to play
   - Or use **Standard Contract** (free action, costs influence only)
2. **Pay the cost** (influence, discard cards, etc.)
3. **Resolve the card effect**
4. **Remove card from hand** (discard to Event Discard pile)
5. **Repeat** - Play another card if you want (up to 20 cards per turn, safety limit)

**Chain stops when**:
- No more playable cards in hand
- Not enough influence to play anything
- Turn-ending card played (e.g., Attack cards end your turn)
- Tower destroyed (immediately ends turn)
- Standard Contract attempted and failed (won't retry this turn)
- Strategy decides to stop chaining

**Average chain length**: 2-3 cards per turn

**Example Chain**:
```
Turn 5 - Player 1:
  1. Play "Gather Medium" → +4 troops to pot
  2. Play "Gather Small" → +2 troops to pot
  3. Standard Contract → Claim all 6 pot troops + draft Mage
  4. Play "Attack Basic" → Attack Player 2 (ENDS TURN)

Total: 4 actions in one turn
```

### Phase 3: Hand Refill

**At the end of your turn:**

1. Calculate target hand size: `max(2, your_influence)`
   - **Floor of 2**: You always draw to at least 2 cards (prevents death spiral)
   - **Ceiling**: Can't exceed max hand size (10-12 cards, configurable)
2. Draw event cards until hand size = target
3. If Event Deck empties, reshuffle discard pile

**Example**:
```
Player has 5 influence, 2 cards in hand
Target hand size = max(2, 5) = 5
Draw 3 cards → Now has 5 cards in hand
```

### Phase 4: Elimination Check

1. Check if any player has 0 towers remaining
2. Eliminate that player
3. Check if game is over (1 or 0 players remain)

### Phase 5: Next Player

1. Move to next active player (clockwise or anti-clockwise)
2. Begin their turn with ANTE

---

## Core Mechanics

### Standard Contract (Primary Claiming Mechanism)

**The most important action in the game - this is how you claim troops from the pot!**

**What is Standard Contract?**
- It's a **free action** (NOT an event card!)
- Costs **influence only** (typically 1-3 influence, GA-optimized)
- Available every turn if you meet the requirements

**Requirements**:
1. Have enough influence (typically 1-3)
2. Unclaimed pot has at least 1 troop
3. At least 1 leader available in markets (Mage or Commander)

**What it does**:
1. **Spend influence** (cost set by game configuration)
2. **Claim ALL troops** in the unclaimed pot
3. **Draft 1 leader** from either Mage or Commander market
4. **Create new army** immediately (troops + leader)
5. Market automatically refills with new leader

**Why it's important**: This is the primary way to build armies and claim troops before opponents do!

**Example**:
```
Unclaimed Pot: [3, 2, 10] (3 troops, total strength 15)
Player has 5 influence

Standard Contract:
  - Spend 2 influence → Now has 3 influence
  - Draft "Fire Mage" (+2 attack) from Mage Market
  - Claim all 3 troops: [3, 2, 10]
  - Create new army: [3, 2, 10] + Fire Mage = 17 total strength
  - New mage flipped to market
```

### Unclaimed Pot System

**What is the Unclaimed Pot?**
- A single communal pool of troops
- Visible to all players
- Grows via ANTE (1/turn) and GATHER cards (1-7/card)

**How troops enter the pot**:
1. **ANTE** (automatic): 1 troop per turn
2. **GATHER cards**: Small (1-3), Medium (3-5), Large (5-7)
3. **Failed claims**: If contract fails, troops return to pot
4. **Captain Jackpots**: When Captain drawn, becomes strength-10 troop

**How troops leave the pot**:
- **Standard Contract**: Claims ALL troops at once (all-or-nothing)
- That's it! No other way to claim pot troops

**Strategic Importance**:
- Pot grows rapidly (1/turn + gather cards)
- Players compete to claim at optimal timing
- Waiting = more troops, but opponents might claim first
- "Pot timing" is a core skill

**Example Pot Growth**:
```
Turn 1: ANTE → Pot: [3] (1 troop, strength 3)
Turn 2: ANTE → Pot: [3, 2] (2 troops, strength 5)
Turn 3: Player plays "Gather Medium" → Pot: [3, 2, 4, 5, 3, 2] (6 troops, strength 19)
Turn 4: Different player uses Standard Contract → Claims all 6 troops, pot now empty
Turn 5: ANTE → Pot: [1] (1 troop, strength 1) - cycle begins again
```

### Influence Economy

**What is Influence?**
- Your "currency" for playing cards and contracting leaders
- Determines your hand size (draw to influence each turn)
- Range: 2-12 typically

**Gaining Influence**:
- **Destroy enemy army**: +1-2 influence (configurable)
- **Eliminate player**: +2-4 influence (configurable)
- **Economic cards**: Various influence gains
- **Leader abilities**: Some leaders grant influence

**Spending Influence**:
- **Standard Contract**: 1-3 (configurable)
- **Event cards**: Various costs
- **Passive Tax**: -1 influence if you haven't attacked in X turns (configurable)

**Spending Lock**: You cannot spend influence below 2 (prevents lockout scenarios)

**Hand Size Rule**:
- Hand size = `max(2, influence)`
- Floor of 2 cards minimum
- Ceiling of 10-12 cards maximum (configurable)

**Example**:
```
Player starts with 6 influence
- Plays Standard Contract: -2 influence → Now 4 influence
- Draws to 4 cards at end of turn
- Destroys enemy army next turn: +1 influence → Now 5 influence
- Draws to 5 cards at end of turn
```

### Army Management

**Multiple Armies Per Player**:
- Each player can have 0-10+ armies simultaneously
- Each army is independent (own troops, own leader)
- Strategic positioning and army selection

**Army Composition**:
- **Troops**: List of ranks (1-5), strength = SUM of ranks
- **Leader** (optional): Adds attack bonus (+1/+2/+3)
- **Total Strength**: Sum of troop ranks + leader attack bonus

**Creating Armies**:
1. **Standard Contract**: Claim pot troops + draft leader → new army
2. **Contract Cards**: Various contract cards → new army
3. **Gather + Leader**: Gather troops, then contract leader separately

**Army Example**:
```
Army 1: [5, 4, 3, 2] + Commander (+3) = 17 strength
Army 2: [5, 5, 5] + Mage (+2) = 17 strength
Army 3: [3, 2, 1] + Captain (+1) = 7 strength

Total: 3 armies, 41 combined strength
```

**Army Destruction**:
- When army destroyed in combat, all troops discarded
- Leader returns to player's leader pool (can be reassigned)
- Net damage ÷ 5 = towers destroyed (if attacking towers)

---

## Event Cards

### Card Type Breakdown

#### Contract Cards (25 total)

**CONTRACT_MAGE (15 cards)**:
- **Cost**: leader_contract_cost influence (1-3, configurable)
- **Effect**: Choose 1 mage from 3-card Mage Market
- **Use**: Draft mages for +2 attack bonus

**CONTRACT_COMMANDER (10 cards)**:
- **Cost**: leader_contract_cost influence (1-3, configurable)
- **Effect**: Choose 1 commander from 3-card Commander Market
- **Use**: Draft commanders for +3 attack bonus

#### Gather Troops Cards (30 total)

**GATHER_SMALL (10 cards)**:
- **Effect**: Draw 1-3 troops from Troop Deck → Unclaimed Pot
- **Examples**: "Scout Patrol" (2 troops), "Recruitment Drive" (3 troops)

**GATHER_MEDIUM (10 cards)**:
- **Effect**: Draw 3-5 troops from Troop Deck → Unclaimed Pot
- **Examples**: "Army Muster" (4 troops), "War Levy" (5 troops)

**GATHER_LARGE (10 cards)**:
- **Effect**: Draw 5-7 troops from Troop Deck → Unclaimed Pot
- **Examples**: "Mass Conscription" (6 troops), "Total Mobilization" (7 troops)

**Important**: Gather cards add troops to the POT, not directly to you! You must claim via Standard Contract.

#### Attack Cards (20 total)

**ATTACK_BASIC (5 cards)**:
- **Effect**: Choose army, choose target, attack (ends turn)
- **Examples**: "Direct Assault", "Frontal Attack"

**ATTACK_TACTICAL (5 cards)**:
- **Effect**: Attack with bonuses (+2 to +5 strength)
- **Examples**: "Flanking Maneuver" (+3), "Overwhelming Force" (+5)

**ATTACK_CONDITIONAL (5 cards)**:
- **Effect**: Attack with conditions or situational bonuses
- **Examples**: "Ambush" (bonus vs larger army), "Revenge Strike" (bonus if towers lost)

**ATTACK_AOE (3 cards)**:
- **Effect**: Attack multiple targets or all players
- **Examples**: "Blitzkrieg", "Total War"

**ATTACK_RISKY (2 cards)**:
- **Effect**: High risk/high reward attacks
- **Examples**: "Pyrrhic Victory" (win combat, lose all troops), "Scorched Earth"

**All attack cards end your turn immediately when played.**

#### Economic Cards (20 total)

**ECONOMIC**:
- **Effects**: Gain influence, draw cards, resource management
- **Examples**:
  - "Diplomacy": +2 influence
  - "Trade Agreement": +1 influence, draw 1 card
  - "Tribute": +3 influence, discard 1 card
  - "War Economy": +1 influence per attack this turn

#### Manipulation Cards (15 total)

**MANIPULATION**:
- **Effects**: Disrupt opponents, steal troops, force actions
- **Examples**:
  - "Sabotage": Target discards 1 card
  - "Steal Troops": Take 1 troop from opponent army
  - "Forced March": Target must attack
  - "Reverse Turn Order": Reverse play order

#### Utility & Special Cards (35 total)

**Various effects**:
- **Battle Frenzy**: 0 casualties on next attack
- **Raiding Party**: Attack + gain 5 troops
- **Spoils of War**: After attack, draw 2 cards + 3 influence
- **Tactical Retreat**: 50% casualties this turn
- **Reinforcements**: Regain casualties after combat
- **Fortified Position**: 0 casualties when defending
- **Momentum**: -1 casualty per attack, stacks
- **Blitzkrieg**: Attack twice after army defeat
- **Raze**: Press attack after tower destruction
- **Chain Assault**: Tower destroyed → draw again
- **Siege Equipment**: Nullify ALL tower damage (next attack)
- **Protective Wards**: Reduce tower damage 50%
- **Plunder**: Tower → 3 influence + 1 card
- **Conscription**: 4 influence → 6 troops
- **Claim Army**: Claim unclaimed troops with available leader
- **Guerrilla Tactics**: Cap casualties at 5
- **Siege Attack**: Bypass armies, hit towers directly
- **Artillery Strike**: Bypass, 2x damage to towers

---

## Combat

### Combat Overview

Combat in Battalion is **player-directed** and **sum-based**:
- Attacker chooses which army attacks
- Attacker chooses target (enemy army or enemy towers)
- Defender chooses which army defends (if armies available)

### Army vs Army Combat

**Combat Resolution**:
1. **Calculate Strength**:
   - Attacker strength = sum of troop ranks + leader attack bonus
   - Defender strength = sum of troop ranks + leader attack bonus

2. **Determine Winner**:
   - Higher strength wins
   - Ties: Defender wins

3. **Casualties**:
   - **Winner**: Loses troops equal to loser's strength (mutual damage)
   - **Loser**: Army destroyed (all troops discarded, leader returns to pool)

4. **Influence Rewards**:
   - Winning player gains influence (configurable, typically +1-2)

**Example**:
```
Attacker: [5, 4, 3] + Commander (+3) = 15 strength
Defender: [5, 5, 2] + Mage (+2) = 14 strength

Attacker wins!
- Defender's army destroyed (troops discarded, Mage returns to hand)
- Attacker takes 14 casualties:
  - Remove 14 strength from [5, 4, 3] = Remove [5, 4, 3] + 2 more
  - Remove Rank 3 → [5, 4]
  - Remove Rank 4 → [5]
  - Remove 5 more → Army destroyed!

Both armies destroyed! (This happens often due to mutual damage)
Attacker gains +1 influence for destroying enemy army
```

### Army vs Towers Attack

**When no defender chosen (or no armies to defend)**:

1. **Tower Damage Calculation**:
   - Base tower damage = 5 per tower (configurable)
   - Total tower damage = 5 × remaining towers

2. **Combat Resolution**:
   - Army strength vs tower damage
   - Net damage = army strength - tower damage
   - If net positive: `net_damage ÷ 5 = towers destroyed`
   - Army takes casualties equal to tower damage

3. **Tower Destruction**:
   - Attacker gains influence (configurable)
   - Tower destruction **immediately ends turn** (v1.15+ mechanic)

**Example 1: Successful Tower Attack**:
```
Attacker: [5, 5, 5, 4, 3] + Commander (+3) = 25 strength
Defender: 3 towers (5 damage each = 15 total tower damage)

Net damage = 25 - 15 = 10
Towers destroyed = 10 ÷ 5 = 2 towers

Result:
- Defender loses 2 towers (now 1 tower remaining)
- Attacker's army takes 15 casualties → Reduced to [5, 5, 3] + Commander
- Turn ends immediately (tower destroyed)
```

**Example 2: Failed Tower Attack**:
```
Attacker: [5, 4, 3] + Mage (+2) = 14 strength
Defender: 3 towers (5 damage each = 15 total tower damage)

Net damage = 14 - 15 = -1 (negative, no towers destroyed)

Result:
- No towers destroyed
- Attacker's army takes 14 casualties → Army destroyed
- Wasted attack!
```

### Tower Damage Reduction Cards

**Some cards reduce tower damage**:
- **Siege Equipment**: Nullify ALL tower damage (next attack)
- **Protective Wards**: Reduce tower damage 50%
- **Vanguard Formation**: First attack ignores tower damage

**These are critical for successful tower attacks!**

### Bypass Attacks (v1.13+ Mechanic)

**Special attack cards that skip army combat**:

**SIEGE_ATTACK**:
- Bypass all armies
- Deal `bypass_damage` (configurable, typically 5-10) directly to towers

**ARTILLERY_STRIKE**:
- Bypass all armies
- Deal `2× bypass_damage` (typically 10-20) directly to towers

**Use**: Punish players who neglect armies, create direct pressure

---

## Victory Conditions

### 1. Conquest Victory (90% of games)

**Last player standing wins!**

- All other players eliminated (0 towers)
- Most common victory type

### 2. Troop Deck Depletion (10% of games)

**When Troop Deck runs out**:
1. Game ends immediately
2. Player with **highest influence** wins
3. Tiebreaker: Most armies → Most troops → Most towers

**Why this matters**: Troop Deck is the game timer (doesn't reshuffle like Event Deck)

### Elimination

**A player is eliminated when**:
- Towers reach 0
- Player removed from turn order
- All their armies, leaders, and hand discarded

---

## Strategy Guide

### 6 Viable Strategies (All 15-20% win rate)

#### 1. RUSH (Aggressive)
- **Goal**: Fast attacks, 3-troop armies, early pressure
- **Key Cards**: Gather Small, Attack Basic, Contract Cheap
- **Timing**: Claim pot early (3-5 troops), attack immediately
- **Wins**: 15-20% (fast games, high variance)

#### 2. SWARM (Army Count)
- **Goal**: Many small armies, overwhelm with numbers
- **Key Cards**: Contract Mage/Commander, Gather Medium
- **Timing**: Claim pot frequently, build 4-6 armies
- **Wins**: 15-20% (resilient, hard to eliminate)

#### 3. BUILDUP (Economic)
- **Goal**: Big armies, strong economy, late game power
- **Key Cards**: Gather Large, Economic cards, Contract Commander
- **Timing**: Wait for pot to grow (10-15 troops), massive claims
- **Wins**: 15-20% (slow start, strong finish)

#### 4. FORTRESS (Defensive)
- **Goal**: Patient defense, counter-attack, survive to end
- **Key Cards**: Protective Wards, Fortified Position, Reinforcements
- **Timing**: Block attacks, punish overextensions
- **Wins**: 15-20% (consistent, safe)

#### 5. TEMPO (Flexible)
- **Goal**: Opportunistic, adapt to board state
- **Key Cards**: All types, depends on situation
- **Timing**: Respond to threats, exploit openings
- **Wins**: 15-20% (requires skill, balanced)

#### 6. ADAPTIVE (Reactive)
- **Goal**: React to opponents, counter-strategies
- **Key Cards**: Manipulation, counter-plays
- **Timing**: Read opponents, disrupt plans
- **Wins**: 15-20% (highest skill ceiling)

### Key Strategic Concepts

**Pot Timing**:
- Small pot (3-5 troops): Rush strategy, fast armies
- Medium pot (6-10 troops): Standard timing, good value
- Large pot (10-15+ troops): Risk vs reward, opponents might claim first

**Influence Management**:
- Keep at least 3 influence (emergency contract)
- Spend aggressively when ahead
- Hoard when behind (economy recovery)

**Army Positioning**:
- Multiple small armies: Resilient, flexible
- Few large armies: Powerful, vulnerable
- Mix: Usually optimal

**Leader Drafting**:
- Commanders > Mages > Captains (generally)
- Counter-draft opponents (deny strong picks)
- Market visibility = strategic advantage

**Attack Timing**:
- Attack when net positive (army strength > tower damage + defender strength)
- Use tower damage reduction cards for tough attacks
- Tower destruction ends turn (plan accordingly)

**Card Chaining**:
- Gather → Gather → Contract → Attack (common chain)
- Economic → Gather → Gather → Contract (buildup chain)
- Attack early = fewer cards played (turn ends)
- Attack late = maximize card plays first

---

## Quick Reference

### Turn Order
1. **ANTE**: 1 troop → pot (automatic)
2. **DRAW**: 1 event card
3. **CHAIN**: Play 2-3 cards (Standard Contract available)
4. **REFILL**: Draw to influence (min 2, max 10-12)

### Standard Contract
- **Cost**: 1-3 influence (configurable)
- **Effect**: Claim ALL pot troops + draft 1 leader → new army
- **Frequency**: Most important action, use often

### Influence
- **Spending Lock**: Can't go below 2 (prevents lockout)
- **Hand Size**: Draw to influence each turn (floor of 2)
- **Gains**: Destroy army (+1-2), eliminate player (+2-4)

### Combat
- **Army Strength**: Sum of ranks + leader bonus
- **Mutual Damage**: Winner takes casualties equal to loser's strength
- **Tower Attack**: `(strength - tower_damage) ÷ 5 = towers destroyed`
- **Tower Damage**: 5 per tower (default)

### Victory
- **Conquest**: Last player standing (90% of games)
- **Depletion**: Highest influence when Troop Deck empty (10% of games)

---

## Designer Notes

This rulebook documents the **actual implementation** of Battalion simulator v1.18, which has been tested through 700,000+ simulated games across 14 meta-evolution cycles using genetic algorithms.

**Key Design Principles**:
- **Fun above all else**: The fun part (attacking) is also the winning strategy
- **Strategic agency > luck**: Contracts, not random draws; visible markets
- **Drama over balance**: Big swings, memorable moments, 90% conquest rate
- **20-30 turn games**: Achieved via game length optimization (v1.6 goal)
- **6 viable strategies**: All strategies win 15-20% (perfect balance)

**Version History**:
- **v1.5**: Simultaneous building (physical game, never implemented in simulator)
- **v1.6**: Game length optimization
- **v1.7**: Two-deck system, turn-based flow, sum-based combat
- **v1.8**: Event card chaining
- **v1.15**: Unclaimed pot system, tower destruction ends turn
- **v1.16**: Draft markets (3-card face-up)
- **v1.17**: ANTE mechanic, spending lock
- **v1.18**: Standard Contract fix, Captain jackpots, Ghost Cards removed

**For more information**:
- Simulator: `battalion_simulator_v1_18.py`
- Event Card Reference: See [CORRECTED_EVENT_CARDS_REFERENCE.md]
- Meta-Evolution Results: See `meta_evolution/EXECUTIVE_SUMMARY.md`

---

**Last Updated**: November 5, 2025
**Status**: ✅ Matches simulator v1.18 exactly
**Playtest Status**: 700,000+ simulated games, physical playtest TBD

