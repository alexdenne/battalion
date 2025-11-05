# CRITICAL: Rulebook vs Simulator v1.18 Discrepancies

**Date**: November 5, 2025
**Status**: 🔴 MAJOR ISSUES FOUND - DO NOT DEPLOY CURRENT RULEBOOK

---

## Executive Summary

The rulebook at `Rules version 1.6 (2025)/rules/index.md` describes **v1.5 mechanics that DO NOT EXIST** in simulator v1.18. This is a **critical blocker** for GitHub deployment.

### Severity: CRITICAL

- **Completely wrong game flow**: Simultaneous building vs Turn-based with ANTE
- **Wrong economy mechanics**: No communal pot system described
- **Missing core mechanics**: ANTE system, Standard Contract, Event card chaining
- **Wrong card system**: Describes old v1.5 physical deck, not v1.17+ two-deck system

---

## Major Discrepancies Found

### 1. ❌ SIMULTANEOUS BUILDING (DOES NOT EXIST)

**Rulebook Says (WRONG)**:
- "Phase 1: PLANNING (Hidden) - All players plan simultaneously"
- "Phase 2: READY CHECK - Wait for all players"
- "Phase 3: REVEAL - Flip all cards simultaneously"
- "Phase 4: VALIDATION - Check legality"
- "Inspired by 7 Wonders, Robo Rally, Diplomacy"

**Simulator v1.18 Actually Does**:
- **Turn-based sequential play** (one player at a time)
- **No simultaneous anything**
- **No communal build piles**
- **No face-down planning**

**Impact**: The entire core mechanic description is fictional!

---

### 2. ❌ MISSING: ANTE SYSTEM (CORE MECHANIC)

**Rulebook Says**: Nothing - not mentioned at all

**Simulator v1.18 Actually Does** (lines 4492-4516):
```python
# ANTE MECHANIC - Mandatory pot contribution at turn start
# Every turn begins with 1 troop added to the unclaimed pot
if game_state.troop_deck:
    ante_troop = game_state.troop_deck.pop(0)

    if ante_troop == 0:  # Captain
        captain_value = 10  # JACKPOT!
        game_state.unclaimed_troops.append(captain_value)
    else:
        game_state.unclaimed_troops.append(ante_troop)
```

**What This Means**:
- Every turn starts with 1 troop card drawn from troop deck
- Automatically added to the **unclaimed pot** (communal pool)
- If it's a Captain (value 0), it becomes a 10-strength "JACKPOT"
- This is THE central mechanic creating pot pressure

**Impact**: The ENTIRE pot economy is undocumented!

---

### 3. ❌ WRONG: TWO-DECK SYSTEM

**Rulebook Says**:
- Main deck with troops, captains, contracts mixed together
- 76-card main deck total

**Simulator v1.18 Actually Does** (header lines 76-100):
```
1. TROOP DECK (Ranks 1-5 only): Combat power, SUM-based strength
   - Troops + Captains mixed in
   - Depletes = game over

2. EVENT DECK (145 cards): Strategic actions, never depletes
   - Contracts, Gather Troops, Attacks, Economic, Manipulation
   - Shuffles when empty (infinite gameplay)
```

**Impact**: Players would have no idea there are two separate decks!

---

### 4. ❌ MISSING: STANDARD CONTRACT (CORE ACTION)

**Rulebook Says**: Contracts cost "2 influence" and require discarding a contract card

**Simulator v1.18 Actually Does** (lines 2313-2344):
```python
def resolve_standard_contract(player, card, game_state, playbook):
    """
    v1.18: Resolve Standard Contract action
    - Costs leader_contract_cost influence (GA-optimized: 1-3)
    - Claims ALL unclaimed troops in pot
    - Drafts a leader from market
    - Creates new army immediately
    - Does NOT consume a card from hand
    """
```

**What This Means**:
- **Standard Contract** is a FREE ACTION (no card required!)
- You spend influence to claim the unclaimed pot + draft a leader
- This is the PRIMARY claiming mechanism
- Cost is configurable (1-3 influence), not fixed at 2

**Impact**: The most important game action is completely undocumented!

---

### 5. ❌ WRONG: "GATHER TROOPS" SYSTEM

**Rulebook Says**: Players place troop cards face-down on communal piles

**Simulator v1.18 Actually Does** (EventCardType enum + resolve functions):
- **GATHER_SMALL**: Event card that draws 1-3 troops from troop deck → unclaimed pot
- **GATHER_MEDIUM**: Event card that draws 3-5 troops from troop deck → unclaimed pot
- **GATHER_LARGE**: Event card that draws 5-7 troops from troop deck → unclaimed pot

**What "Gather Troops" Really Means**:
- It's an EVENT CARD you play from your hand
- It draws troops from the troop deck
- Those troops go to the unclaimed pot (not to you directly)
- Anyone can claim them with Standard Contract

**Impact**: The pot-building mechanic is completely wrong!

---

### 6. ❌ WRONG: TURN STRUCTURE

**Rulebook Says**:
1. Simultaneous Build Phase
2. Action Phase (sequential)
3. Draw Step

**Simulator v1.18 Actually Does** (lines 4492-4650):
1. **ANTE**: Draw 1 troop → unclaimed pot
2. **DRAW**: Draw 1 event card from event deck
3. **CHAIN LOOP** (play up to 20 event cards in sequence):
   - Choose event card to play
   - Resolve card effect
   - Repeat until no more playable cards or end turn triggered
4. **INFLUENCE REFILL**: Draw event cards until hand = influence (min 2)

**Impact**: Turn structure is completely different!

---

### 7. ❌ MISSING: EVENT CARD CHAINING (v1.8 MECHANIC)

**Rulebook Says**: Players take ONE action per turn

**Simulator v1.18 Actually Does** (lines 4536-4650):
- Players can play **multiple event cards per turn** (up to 20)
- Chain stops when:
  - No more playable cards
  - Influence depleted
  - End turn card played (e.g., attacks)
  - Standard Contract attempted and failed

**What This Means**:
- You might play "Gather Medium" → "Gather Small" → "Standard Contract" → "Attack" all in one turn
- Chains create explosive turns (2-3 cards per turn average)
- This is WHY games are fast (30 turns average)

**Impact**: The entire action economy is wrong!

---

### 8. ❌ WRONG: HAND SIZE MECHANICS

**Rulebook Says**:
- "Your maximum hand size equals your influence"
- "Draw until hand size equals influence"

**Simulator v1.18 Actually Does** (lines 4647-4663 + config):
```python
# INFLUENCE REFILL (with FLOOR and CEILING)
hand_target = max(2, player.influence)  # Floor of 2
hand_target = min(hand_target, config.max_hand_size)  # Ceiling (default: 10-12)

while len(player.hand) < hand_target and event_deck:
    player.draw_event_card(event_deck)
```

**What This Means**:
- **Floor**: You always draw to at least 2 cards (prevents death spiral)
- **Ceiling**: You can't exceed max_hand_size (prevents hoarding)
- **Spending lock**: You can't spend influence below 2 (prevents lockout)

**Impact**: Critical economy safety features are undocumented!

---

### 9. ❌ WRONG: LEADER ACQUISITION

**Rulebook Says**:
- **Buy**: "Discard 1 card + reduce influence by 1"
- **Contract**: "Discard contract card + 1 card + reduce influence by 2"

**Simulator v1.18 Actually Does**:
- **Standard Contract**: Spend influence (1-3), claim unclaimed pot + draft leader (NO CARD COST)
- **Contract Mage**: Event card (in event deck), spend influence, draft mage from 3-card market
- **Contract Commander**: Event card (in event deck), spend influence, draft commander from 3-card market
- **Captain in Ante/Gather**: Captains are in troop deck, appear during ANTE or GATHER cards

**Impact**: The entire leader economy is wrong!

---

### 10. ❌ MISSING: DRAFT MARKETS

**Rulebook Says**: Generic "playbook" with leaders

**Simulator v1.18 Actually Does** (v1.16+ feature, lines 1-60):
- **3-card face-up Mage market**
- **3-card face-up Commander market**
- Visible to all players before contracting
- Auto-refills from deck when leader drafted
- Strategic counter-picking

**Impact**: Major strategic layer completely missing!

---

### 11. ❌ COMPLETELY WRONG: CARD QUANTITIES

**Rulebook Says** (v1.5):
- 40 troops (4 of each rank 1-5, two colors)
- 12 captains
- 12 contracts
- 76-card main deck

**Simulator v1.18 Actually Uses**:
- **Troop Deck** (GA-optimized, configurable):
  - troop_deck_size: 60-150 (varies by cycle)
  - Distribution: R1=33%, R2=25%, R3=20%, R4=15%, R5=7%
  - Captains mixed in (40 unique captains)

- **Event Deck** (145 cards):
  - 30 Gather Troops cards (Small/Medium/Large)
  - 20 Attack cards (Basic/Tactical/Conditional/AOE/Risky)
  - 10 Contract cards (Mage/Commander)
  - 20 Economic cards
  - 15 Manipulation cards
  - 50 Utility/Chaotic cards

**Impact**: Card counts are completely fictional!

---

### 12. ❌ MISSING: UNCLAIMED POT VISUALIZATION

**Rulebook Says**: 4 communal build piles

**Simulator v1.18 Actually Does**:
- **Single unclaimed troops list** (game_state.unclaimed_troops)
- All players can see pot size and strength
- Pot grows via:
  - ANTE (1 troop per turn)
  - GATHER cards (1-7 troops)
  - Failed claims (troops return to pot)
- Pot is claimed via Standard Contract (all-or-nothing)

**Impact**: Physical game setup is completely wrong!

---

## Additional Minor Issues

### 13. Missing: Spending Lock
- Simulator prevents spending influence below 2
- Not mentioned in rulebook

### 14. Missing: Passive Tax
- Configurable penalty for not attacking
- Not mentioned in rulebook

### 15. Wrong: Influence Gains
- Rulebook says "+1 for destroying army"
- Simulator has complex elimination-based rewards

### 16. Missing: Tower Destruction Mechanics
- Net damage ÷ 5 = towers destroyed
- Not clearly explained in rulebook

### 17. Missing: Deck Depletion Mechanics
- Troop deck depletion = game over
- Event deck never depletes (shuffles)
- Not mentioned in rulebook

---

## Files Affected

### Must Be Completely Rewritten:
1. `Rules version 1.6 (2025)/rules/index.md` - **100% wrong**
2. `Rules version 1.6 (2025)/cards/index.md` - **Wrong card list**

### Must Be Created:
3. Correct rulebook for v1.17+ mechanics
4. Correct event card reference
5. Turn structure diagram

---

## Action Required

**STOP DEPLOYMENT** until we create:

1. **NEW RULEBOOK** matching simulator v1.18 exactly
2. **EVENT CARD REFERENCE** listing all 145 event cards
3. **TURN STRUCTURE GUIDE** showing ANTE → DRAW → CHAIN → REFILL
4. **POT MECHANICS GUIDE** explaining unclaimed troops system
5. **QUICK REFERENCE CARD** for physical playability

---

## Why This Happened

Looking at file history:
- v1.5 rules describe a physical simultaneous-building game
- v1.7 simulator introduced two-deck system
- v1.17 simulator added unclaimed pot + ANTE
- v1.18 simulator added Standard Contract fix
- **But the rulebook was never updated past v1.5!**

The simulator evolved through 13+ versions while the rulebook stayed frozen at v1.5.

---

## Recommendation

**Option A - Write New Rulebook (RECOMMENDED)**:
- Extract mechanics directly from simulator v1.18 source code
- Document actual turn flow, card types, pot mechanics
- Create playable physical rules
- Time: 2-3 hours

**Option B - Wait for Physical Playtest**:
- Don't deploy until you've played v1.17+ physically
- Validate that simulator mechanics translate to fun physical game
- Document rules from actual play experience
- Time: 1 week+

**I recommend Option A** - We can create accurate documentation right now from the simulator code.

---

**Status**: 🔴 BLOCKING GITHUB DEPLOYMENT
**Next Step**: Create corrected rulebook matching simulator v1.18
