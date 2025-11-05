# Battalion - Complete Event Card Reference (v1.18)

**Total Cards**: 145 event cards (Event Deck reshuffles infinitely)
**Simulator Version**: v1.18 (Meta-Evolution Stable)
**Date**: November 5, 2025

---

## Table of Contents

1. [Contract Cards (25)](#contract-cards-25)
2. [Gather Troops Cards (30)](#gather-troops-cards-30)
3. [Attack Cards (35)](#attack-cards-35)
4. [Economic Cards (15)](#economic-cards-15)
5. [Manipulation Cards (15)](#manipulation-cards-15)
6. [Utility Cards (7)](#utility-cards-7)
7. [Special Combat Cards (18)](#special-combat-cards-18)

---

## Contract Cards (25)

### CONTRACT_MAGE (15 cards)

**Card Name**: "Contract Mage"
**Cost**: leader_contract_cost influence (1-3, configurable)
**Effect**: Choose 1 mage from 3-card Mage Market
**Use**: Draft mages for +2 attack bonus
**Timing**: Play during Event Card Chain phase
**Notes**: Market auto-refills from mage deck

**Quantity**: 15 cards (most common contract type)

---

### CONTRACT_COMMANDER (10 cards)

**Card Name**: "Contract Commander"
**Cost**: leader_contract_cost influence (1-3, configurable)
**Effect**: Choose 1 commander from 3-card Commander Market
**Use**: Draft commanders for +3 attack bonus
**Timing**: Play during Event Card Chain phase
**Notes**: Market auto-refills from commander deck

**Quantity**: 10 cards

---

## Gather Troops Cards (30)

**Important**: All GATHER cards add troops to the **Unclaimed Pot**, not directly to you! You must claim via Standard Contract.

### GATHER_SMALL (10 cards)

1. **Scout Patrol**
   - Effect: Draw 2 troops → pot
   - Cost: Free (0 influence)

2. **Recruitment Drive**
   - Effect: Draw 3 troops → pot
   - Cost: Free

3. **Muster Forces**
   - Effect: Draw 3 troops → pot, discard 1 troop
   - Cost: Free
   - Risk/Reward: More troops but lose 1

4. **Local Militia**
   - Effect: Draw 2 troops → pot, gain 1 influence
   - Cost: Free
   - Bonus: Economy + troops

5. **Volunteers**
   - Effect: Draw 2 troops → pot, draw 1 event card
   - Cost: Free
   - Bonus: Card draw

6. **Town Guard**
   - Effect: Draw 2 troops → pot, +1 rank bonus to troops
   - Cost: Free
   - Bonus: Quality improvement

7. **Quick Gather**
   - Effect: Draw 2 troops → pot, extra turn after
   - Cost: Free
   - Bonus: Action economy

8. **Selective Draft**
   - Effect: Look at top 5 troops, take 2 → pot
   - Cost: Free
   - Bonus: Quality control

9. **Cherry Pick**
   - Effect: Look at top 4 troops, take 1 → pot
   - Cost: Free
   - Bonus: Guaranteed best troop

10. **Scavenge**
    - Effect: Draw 2 troops from discard → pot
    - Cost: Free
    - Special: Recycles discarded troops

---

### GATHER_MEDIUM (10 cards)

1. **Call to Arms**
   - Effect: Draw 4 troops → pot
   - Cost: Free

2. **Rally the Troops**
   - Effect: Draw 5 troops → pot
   - Cost: Free

3. **Reinforcements**
   - Effect: Draw 4 troops → pot, optional: pay 1 influence for +2 troops
   - Cost: Free (optional upgrade: 1 influence)

4. **Army Muster**
   - Effect: Draw 5 troops → pot, must attack within 2 turns
   - Cost: Free
   - Condition: Forced attack timing

5. **Battle Preparation**
   - Effect: Draw 4 troops → pot, all become Rank 3
   - Cost: Free
   - Bonus: Consistent quality

6. **Mass Recruitment**
   - Effect: Draw 5 troops → pot, lose 1 influence
   - Cost: 1 influence (involuntary)
   - Drawback: Influence cost

7. **Fortify Ranks**
   - Effect: Draw 4 troops → pot, gain +2 permanent defense
   - Cost: Free
   - Bonus: Defense buff

8. **Tactical Gathering**
   - Effect: Draw 3 troops → pot, +2 if you have Commander
   - Cost: Free
   - Bonus: Commander synergy

9. **Elite Selection**
   - Effect: Draw 6 troops → pot, keep best 4
   - Cost: Free
   - Quality: High-value troops only

10. **Strategic Muster**
    - Effect: Draw 4 troops → pot, optional: discard 1 card for +2 troops
    - Cost: Free (optional: discard 1 event)

---

### GATHER_LARGE (5 cards)

1. **Mass Mobilization**
   - Effect: Draw 6 troops → pot
   - Cost: Free

2. **Full Muster**
   - Effect: Draw 7 troops → pot
   - Cost: Free

3. **Army Assembly**
   - Effect: Draw 8 troops → pot, discard 2 random troops
   - Cost: Free
   - Risk: Random discard

4. **Glorious Charge**
   - Effect: Draw 7 troops → pot, must attack this turn
   - Cost: Free
   - Condition: Forced attack

5. **War Machine**
   - Effect: Draw 6 troops → pot, all become Rank 5
   - Cost: Free
   - Bonus: All elite troops!

---

### GATHER_CONDITIONAL (5 cards)

1. **Gambit**
   - Effect: Draw random 3-7 troops → pot
   - Cost: Free
   - Risk: Variable outcome

2. **Desperation**
   - Effect: Draw (missing_towers × 2) troops → pot
   - Cost: Free
   - Scales: Better when losing

3. **Underdog Rally**
   - Effect: Draw 8 troops → pot if losing, else 3 troops
   - Cost: Free
   - Condition: Position-dependent

4. **Steal Recruits**
   - Effect: Draw 3 troops → pot, target discards 2 troops
   - Cost: Free
   - Bonus: Disrupts opponent

5. **Conscription**
   - Effect: All players draw 3 troops → pot, you draw 5
   - Cost: Free
   - Bonus: You get more

---

## Attack Cards (35)

**All attack cards end your turn immediately when played.**

### ATTACK_BASIC (8 cards)

1. **Assault**
   - Effect: Attack (no bonus)
   - Cost: Free
   - Ends Turn: Yes

2. **Strike**
   - Effect: Attack with +2 strength
   - Cost: Free
   - Ends Turn: Yes

3. **Charge**
   - Effect: Attack with +3 strength
   - Cost: Free
   - Ends Turn: Yes

4. **Ambush**
   - Effect: Attack with +5 strength, lose 2 troops after
   - Cost: Free
   - Risk: Post-combat loss
   - Ends Turn: Yes

5. **Raid**
   - Effect: Attack, steal 1 influence on win
   - Cost: Free
   - Bonus: Economy gain
   - Ends Turn: Yes

6. **Invasion**
   - Effect: Attack, +1 influence per tower destroyed
   - Cost: Free
   - Bonus: Tower rewards
   - Ends Turn: Yes

7. **Blitz**
   - Effect: Attack, attack again if win (second attack half strength)
   - Cost: Free
   - Bonus: Double attack
   - Ends Turn: Yes

8. **Relentless Assault**
   - Effect: Attack, can switch target if blocked
   - Cost: Free
   - Flexibility: Target switching
   - Ends Turn: Yes

---

### ATTACK_TACTICAL (8 cards)

1. **Pincer Attack**
   - Effect: Attack two targets, split army strength
   - Cost: Free
   - Special: Multi-target
   - Ends Turn: Yes

2. **Focused Strike**
   - Effect: Attack with +8 strength, discard 3 troops after
   - Cost: Free
   - Risk: High power, high cost
   - Ends Turn: Yes

3. **Surgical Strike**
   - Effect: Attack, ignore 5 defense
   - Cost: Free
   - Bonus: Defense penetration
   - Ends Turn: Yes

4. **Overwhelming Force**
   - Effect: Attack with 2× strength
   - Cost: Free
   - Bonus: Double power!
   - Ends Turn: Yes

5. **Calculated Assault**
   - Effect: Attack, draw 2 events after
   - Cost: Free
   - Bonus: Card draw
   - Ends Turn: Yes

6. **Strategic Strike**
   - Effect: Attack, gain 4 troops on win
   - Cost: Free
   - Bonus: Troop reward
   - Ends Turn: Yes

7. **Lightning Assault**
   - Effect: Attack with +3 strength, extra turn after
   - Cost: Free
   - Bonus: Action economy
   - Ends Turn: No (extra turn!)

8. **Siege Attack**
   - Effect: Attack, damage towers even if blocked
   - Cost: Free
   - Bonus: Guaranteed tower damage
   - Ends Turn: Yes

---

### ATTACK_CONDITIONAL (6 cards)

1. **Revenge**
   - Effect: Attack with +10 strength if damaged by target
   - Cost: Free
   - Condition: Must have been damaged
   - Ends Turn: Yes

2. **Underdog Strike**
   - Effect: Attack with +15 strength if losing, else +2
   - Cost: Free
   - Condition: Position-dependent
   - Ends Turn: Yes

3. **Challenger**
   - Effect: Attack with +7 strength vs player with most influence
   - Cost: Free
   - Target: Influence leader
   - Ends Turn: Yes

4. **Opportunistic Raid**
   - Effect: Attack with +5 strength vs player with most towers
   - Cost: Free
   - Target: Tower leader
   - Ends Turn: Yes

5. **Defensive Counter**
   - Effect: Attack with +8 strength vs last attacker (only if attacked)
   - Cost: Free
   - Condition: Retaliation only
   - Ends Turn: Yes

6. **Blood Feud**
   - Effect: Attack with +12 strength vs player who eliminated you before
   - Cost: Free
   - Condition: Revenge mechanic
   - Ends Turn: Yes

---

### ATTACK_AOE (5 cards)

1. **Rampage**
   - Effect: Deal 3 damage to all opponents
   - Cost: Free
   - Special: Multi-target
   - Ends Turn: Yes

2. **Scatter Attack**
   - Effect: Deal 5 damage split among chosen targets
   - Cost: Free
   - Flexibility: Choose distribution
   - Ends Turn: Yes

3. **Chaos Assault**
   - Effect: Deal random damage per tower to random targets
   - Cost: Free
   - Special: Chaotic targeting
   - Ends Turn: Yes

4. **Apocalypse**
   - Effect: Deal 2 damage to all players (including self)
   - Cost: Free
   - Risk: Self-damage
   - Ends Turn: Yes

5. **Rain of Fire**
   - Effect: Deal 1 damage to all players with 3 towers
   - Cost: Free
   - Condition: Targets leaders only
   - Ends Turn: Yes

---

### ATTACK_LEADER (5 cards)

1. **Commander's Fury**
   - Effect: Attack with +10 strength (requires Commander)
   - Cost: Free
   - Requirement: Commander leader
   - Ends Turn: Yes

2. **Mage Barrage**
   - Effect: Attack, ignore all defense (requires Mage)
   - Cost: Free
   - Requirement: Mage leader
   - Ends Turn: Yes

3. **Captain's Gambit**
   - Effect: Attack three times at half strength each (requires Captain)
   - Cost: Free
   - Requirement: Captain leader
   - Ends Turn: Yes

4. **Berserker Rage**
   - Effect: Attack all opponents (requires specific "Berserker Boss")
   - Cost: Free
   - Requirement: Specific leader
   - Ends Turn: Yes

5. **Zombie Horde**
   - Effect: Gather 5 troops, attack immediately (requires "Zombie Boss")
   - Cost: Free
   - Requirement: Specific leader
   - Ends Turn: Yes

---

### ATTACK_RISKY (3 cards)

1. **All-In Assault**
   - Effect: Attack with 3× strength, lose all troops after
   - Cost: Free
   - Risk: Army destroyed regardless
   - Ends Turn: Yes

2. **Kamikaze Strike**
   - Effect: Destroy own tower, deal 2 tower damage, ignore defense
   - Cost: 1 tower
   - Risk: Self-harm for massive damage
   - Ends Turn: Yes

3. **Reckless Charge**
   - Effect: Attack with +10 strength, take 1 tower damage if lose
   - Cost: Free
   - Risk: Tower loss if failed
   - Ends Turn: Yes

---

## Economic Cards (15)

1. **Tax Collection**
   - Effect: Gain 3 influence
   - Cost: Free

2. **Trade Route**
   - Effect: Gain 2 influence per tower you have
   - Cost: Free
   - Scales: Better with more towers

3. **Plunder**
   - Effect: Gain 4 influence, discard 3 troops
   - Cost: 3 troops
   - Trade: Troops for influence

4. **War Spoils**
   - Effect: Gain 1 influence per tower destroyed (ever)
   - Cost: Free
   - Scales: Rewards aggression

5. **Treasure Hunter**
   - Effect: Gain 5 influence, skip next turn
   - Cost: Next turn
   - Risk: Tempo loss

6. **Windfall**
   - Effect: Gain influence = towers × 2
   - Cost: Free
   - Scales: Position-dependent

7. **Extortion**
   - Effect: Steal 3 influence from richest player
   - Cost: Free
   - Target: Influence leader

8. **Pillage**
   - Effect: All lose 2 influence, you gain 1 per opponent
   - Cost: Free
   - Scales: Better with more players

9. **Steal Wealth**
   - Effect: Steal half of target's influence
   - Cost: Free
   - High Impact: Major swing

10. **Redistribute**
    - Effect: All give you 1 influence, you give back 2
    - Cost: Net -2 influence (usually)
    - Use: Emergency influence

11. **Sell Troops**
    - Effect: Discard troops for 1 influence each
    - Cost: Troops
    - Trade: Troops → influence

12. **Sell Leaders**
    - Effect: Discard leaders for 3 influence each
    - Cost: Leaders
    - Trade: Leaders → influence

13. **Emergency Funds**
    - Effect: Discard 2 events, gain 5 influence
    - Cost: 2 event cards
    - Trade: Cards → influence

14. **Underdog Bonus**
    - Effect: Gain 8 influence if losing, else 2
    - Cost: Free
    - Scales: Catch-up mechanic

15. **Momentum**
    - Effect: Gain 2 influence per tower destroyed last turn
    - Cost: Free
    - Scales: Rewards recent aggression

---

## Manipulation Cards (15)

1. **Sabotage**
   - Effect: Target discards 3 event cards
   - Cost: Free
   - Disruption: Hand size

2. **Raid Supplies**
   - Effect: Target discards 5 troops
   - Cost: Free
   - Disruption: Army size

3. **Espionage**
   - Effect: Look at target's hand, force discard 2 cards
   - Cost: Free
   - Disruption: Information + discard

4. **Snipe**
   - Effect: Destroy target's leader
   - Cost: Free
   - Disruption: Leader removal

5. **Earthquake**
   - Effect: Destroy half of target's army
   - Cost: Free
   - Disruption: Major army damage

6. **Poach**
   - Effect: Steal 3 troops from target's army
   - Cost: Free
   - Disruption: Troop theft

7. **Headhunt**
   - Effect: Steal target's leader (costs 2 influence)
   - Cost: 2 influence
   - Disruption: Leader theft

8. **Copy Tactics**
   - Effect: Copy last opponent card played
   - Cost: Free
   - Special: Card duplication

9. **Steal Secrets**
   - Effect: Look at top 5 of any deck, take 2
   - Cost: Free
   - Special: Deck manipulation

10. **Pickpocket**
    - Effect: Steal 1 random event from each opponent
    - Cost: Free
    - Disruption: Multi-target theft

11. **Famine**
    - Effect: All discard half their troops
    - Cost: Free
    - Disruption: Global army damage

12. **Plague**
    - Effect: All armies lose 2 troops
    - Cost: Free
    - Disruption: Army reduction

13. **Chaos Storm**
    - Effect: All discard 2 random events
    - Cost: Free
    - Disruption: Global hand damage

14. **Revolution**
    - Effect: Swap influence clockwise
    - Cost: Free
    - Special: Influence redistribution

15. **Apocalypse Now**
    - Effect: All discard all troops, all draw 5 events
    - Cost: Free
    - Special: Board reset

---

## Utility Cards (7)

**Note**: v1.18 removed 18 unimplemented "Ghost Cards" that always failed. Only implemented cards remain.

1. **Strategic Planning**
   - Effect: Draw 3 event cards
   - Cost: Free

2. **Deep Reserves**
   - Effect: Draw 5 events, discard 2
   - Cost: Free
   - Net: +3 cards with filtering

3. **Intelligence**
   - Effect: Look at top 5 events, take 2
   - Cost: Free
   - Quality: Selective draw

4. **Trade In**
   - Effect: Discard hand, draw (hand_size + 2) events
   - Cost: Entire hand
   - Use: Hand refresh

5. **Maximum Hand**
   - Effect: Draw to 8 cards
   - Cost: Free
   - Use: Fill hand

6. **Foresight**
   - Effect: Look at all opponent hands, draw 2 events
   - Cost: Free
   - Bonus: Information + cards

7. **Time Warp**
   - Effect: Extra turn after this one
   - Cost: Free
   - Bonus: Action economy

---

## Special Combat Cards (18)

**v1.12+ Attack-Focused Event Cards** (GA-optimized quantities)

### Attack Rewards (3 types)

**BATTLE_FRENZY** (quantity: configurable, typically 3-5):
- Effect: No attacker casualties on next attack
- Cost: 2 influence
- Duration: Next attack only
- Use: Safe aggression

**RAIDING_PARTY** (quantity: configurable, typically 2-4):
- Effect: Attack + gain 5 troops
- Cost: 1 influence
- Bonus: Troop reward
- Ends Turn: Yes

**SPOILS_OF_WAR** (quantity: configurable, typically 2-4):
- Effect: Passive - After any attack: draw 2 events + gain 3 influence
- Cost: 0 (passive effect)
- Timing: Triggers automatically
- Use: Passive economy engine

---

### Casualty Reduction (3 types)

**TACTICAL_RETREAT** (quantity: configurable, typically 2-4):
- Effect: Halve attacker casualties this turn
- Cost: 1 influence
- Duration: This turn
- Multiplier: 0.5×

**REINFORCEMENTS** (quantity: configurable, typically 2-3):
- Effect: Regain casualties after attack
- Cost: 2 influence
- Timing: After attack resolves
- Use: Casualty recovery

**FORTIFIED_POSITION** (quantity: configurable, typically 2-3):
- Effect: No defender casualties when defending
- Cost: 2 influence
- Duration: When defending
- Use: Defense nullification

---

### Combo/Chain (3 types)

**MOMENTUM** (quantity: configurable, typically 3-5):
- Effect: -1 casualty per attack, stacks
- Cost: 1 influence
- Stacking: Multiple cards = multiple stacks
- Use: Chains with attacks

**BLITZKRIEG** (quantity: configurable, typically 2-3):
- Effect: Attack twice this turn
- Cost: 2 influence
- Timing: Immediate
- Use: Double attack turns

**RAZE** (quantity: configurable, typically 1-2):
- Effect: Attack again after tower destruction
- Cost: 3 influence
- Timing: After tower destroyed
- Use: Press advantage

---

### Tower Damage Shields (3 types)

**SIEGE_EQUIPMENT** (quantity: configurable, typically 2-3):
- Effect: Nullify ALL tower damage on next attack
- Cost: 2 influence
- Duration: Next attack
- Use: Free tower attacks

**PROTECTIVE_WARDS** (quantity: configurable, typically 2-3):
- Effect: Reduce tower damage 50% on next attack
- Cost: 1 influence
- Duration: Next attack
- Multiplier: 0.5×

**VANGUARD_FORMATION** (quantity: configurable, typically 2-3):
- Effect: First attack this turn ignores tower damage
- Cost: 2 influence
- Duration: First attack only
- Use: Safe first strike

---

### Economy/Misc (3 types)

**PLUNDER** (quantity: configurable, typically 2-3):
- Effect: Tower destroyed → gain 3 influence + 1 card
- Cost: Free
- Timing: After tower destruction
- Use: Tower rewards

**WAR_ECONOMY** (quantity: configurable, typically 2-3):
- Effect: +1 influence per attack this turn
- Cost: Free
- Duration: This turn
- Use: Multi-attack economy

**CONSCRIPTION** (quantity: configurable, typically 1-2):
- Effect: Spend 4 influence → gain 6 troops
- Cost: 4 influence
- Trade: Influence → troops

---

### Wild Cards (3 types)

**GUERRILLA_TACTICS** (quantity: configurable, typically 1-2):
- Effect: Cap casualties at 5 (attacker or defender)
- Cost: 2 influence
- Duration: This turn
- Use: Casualty mitigation

**SCORCHED_EARTH** (quantity: configurable, typically 1):
- Effect: Destroy tower → gain 10 troops + 5 influence
- Cost: Free
- Reward: Massive tower destruction bonus
- Ends Turn: Yes

**PYRRHIC_VICTORY** (quantity: configurable, typically 1):
- Effect: Auto-win combat, lose all troops
- Cost: Entire army
- Use: Guaranteed victory at high cost
- Ends Turn: Yes

**REVERSE_TURN_ORDER** (quantity: configurable, typically 1):
- Effect: Reverse play order (clockwise ↔ anti-clockwise)
- Cost: Free
- Duration: Rest of game
- Use: Strategic positioning

---

### Bypass Attacks (2 types) - v1.13+

**SIEGE_ATTACK** (quantity: configurable, typically 2-3):
- Effect: Bypass armies, deal bypass_damage to towers
- Cost: Free
- Damage: Configurable (typically 5-10)
- Ends Turn: Yes

**ARTILLERY_STRIKE** (quantity: configurable, typically 1-2):
- Effect: Bypass armies, deal 2× bypass_damage to towers
- Cost: Free
- Damage: Configurable (typically 10-20)
- Ends Turn: Yes

---

### Unclaimed Troops Mechanic - v1.15+

**CLAIM_ARMY** (quantity: configurable, typically 2-3):
- Effect: Claim unclaimed troops with available leader
- Cost: Free
- Requirement: Have leader without army
- Use: Alternative to Standard Contract

---

## Card Composition Summary

| Category | Quantity | Percentage |
|----------|----------|------------|
| Contract Cards | 25 | 17.2% |
| Gather Troops | 30 | 20.7% |
| Attack Cards | 35 | 24.1% |
| Economic Cards | 15 | 10.3% |
| Manipulation Cards | 15 | 10.3% |
| Utility Cards | 7 | 4.8% |
| Special Combat | 18 | 12.4% |
| **Total** | **145** | **100%** |

---

## Card Frequency Notes

**Fixed Cards** (always same quantity):
- Contract Mage: 15
- Contract Commander: 10
- Gather Small: 10
- Gather Medium: 10
- Gather Large: 5
- Gather Conditional: 5
- Attack Basic: 8
- Attack Tactical: 8
- Attack Conditional: 6
- Attack AOE: 5
- Attack Leader: 5
- Attack Risky: 3
- Economic: 15
- Manipulation: 15
- Utility: 7

**Variable Cards** (GA-optimized quantities):
- Battle Frenzy: 3-5
- Raiding Party: 2-4
- Spoils of War: 2-4
- Tactical Retreat: 2-4
- Reinforcements: 2-3
- Fortified Position: 2-3
- Momentum: 3-5
- Blitzkrieg: 2-3
- Raze: 1-2
- Siege Equipment: 2-3
- Protective Wards: 2-3
- Vanguard Formation: 2-3
- Plunder: 2-3
- War Economy: 2-3
- Conscription: 1-2
- Others: 1-2 each

The exact quantities of variable cards are optimized by the genetic algorithm across 14+ meta-evolution cycles.

---

## Designer Notes

This card reference documents the **actual 145-card Event Deck** implemented in Battalion simulator v1.18.

**v1.18 Changes**:
- ❌ Removed 18 "Ghost Cards" (unimplemented utility cards that always failed)
- ✅ All 145 cards are fully implemented and functional
- ✅ Card quantities optimized via genetic algorithm (700K+ games)

**Card Design Principles**:
- **Attack cards end turn** (prevents infinite chains)
- **Gather cards feed pot** (not direct gains - strategic timing)
- **Economic cards provide resource management** (influence economy)
- **Manipulation cards create interaction** (disrupt opponents)
- **Special combat cards reward aggression** (90% conquest rate goal)

**For more information**:
- Complete Rules: See [CORRECTED_RULEBOOK_V1_18.md]
- Simulator: `battalion_simulator_v1_18.py`
- Meta-Evolution Results: See `meta_evolution/EXECUTIVE_SUMMARY.md`

---

**Last Updated**: November 5, 2025
**Status**: ✅ Matches simulator v1.18 exactly
**Total Cards**: 145 (Event Deck reshuffles infinitely)

