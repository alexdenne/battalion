"""
Battalion Game Simulator - Version 1.17 - UNCLAIMED ARMY POT SYSTEM
Simulates full Battalion games with strategic bots for balance testing

=============================================================================
VERSION 1.17 - UNCLAIMED ARMY POT SYSTEM
=============================================================================

🔥 CORE MECHANICS (UNCHANGEABLE):
- Multiple armies per player ✅
- Strategic army selection (attacker & defender choose) ✅
- Leader return to hand when army destroyed ✅

🎯 v1.16 NEW MECHANICS - Epic Leader Draft System:
**120 UNIQUE EPIC LEADERS** with individual abilities and personalities:
- 40 Captains: Combat specialists, ambush tactics, rallying armies (IN TROOP DECK)
- 40 Mages: Elemental powers, area effects, tower bombardment (DRAFT MARKET)
- 40 Commanders: Strategic masterminds, economy boosts, army manipulation (DRAFT MARKET)

**CAPTAINS (40) - TROOP DECK SYSTEM:**
- Captains remain in troop deck mixed with troops (NO CHANGE from v1.15)
- Drawn naturally during gameplay when gathering troops
- Weaker abilities, mostly stat bonuses (+1 attack, unit value 1)
- No separate market or contract system needed

**MAGES & COMMANDERS - 3-CARD FACE-UP DRAFT MARKETS:**
- Mages: 40 unique mages, 3 face-up in market, 37 face-down in deck
- Commanders: 40 unique commanders, 3 face-up in market, 37 face-down in deck
- Players can see what's available before contracting
- Market refills automatically from deck when leader contracted

**CONTRACT MAGE / CONTRACT COMMANDER EVENT CARDS:**
- Cost: leader_contract_cost influence (GA-optimized, range 0-3)
- Player chooses from 3 face-up leaders in appropriate market
- Leader MUST be assigned immediately to:
  1. Unclaimed troops (from cards drawn this turn) - MOST COMMON
  2. Leaderless army already deployed - RARE
  3. If no valid target: contract blocked/invalid
- New leader immediately flipped to market from deck
- Creates strategic drafting decisions and counter-picks

**LEADER ABILITIES** (Phase 5+ - Not Yet Implemented):
- Passive abilities (always active)
- Triggered abilities (combat/event-based)
- Activated abilities (cost influence to use)
- Each of 120 leaders has unique, themed ability

🎯 v1.16 DESIGN GOALS:
- Massive replayability: 120 unique leaders vs 19 generic leaders
- Strategic depth: Draft counter-picks, ability combos, timing
- Thematic richness: Named heroes with lore-appropriate powers
- Market visibility: Players make informed choices, not blind draws
- Scalable implementation: Start with draft, add abilities incrementally

🎯 v1.16 KEY CHANGES FROM v1.15:
1. **120 EPIC LEADERS** - 40 captains (troop deck), 40 mages (market), 40 commanders (market)
2. **DRAFT MARKETS** - Mages & Commanders have 3-card face-up markets (Captains stay in troop deck)
3. **CONTRACT_MAGE & CONTRACT_COMMANDER** - New event cards (cost: leader_contract_cost influence)
4. **MARKET REFILL** - Automatic deck→market when mage/commander contracted
5. **LEADER ASSIGNMENT RULES** - Must have unclaimed troops or leaderless army to contract

v1.8 had: Event card chaining (2-3 cards/turn average)

Based on v1.7, which had:
=============================================================================
VERSION 1.7 - TWO-DECK SYSTEM (Major Restructure)
=============================================================================

DESIGN PHILOSOPHY (from WORKING-PRINCIPLES.md Universal Principles):
- Fun above all else - Make the fun part also the winning strategy
- 20-30 turn games (maintain from v1.6)
- Strategic agency > luck (contracts not random draws)
- Early elimination protection (90% survive to Round 3)
- Drama over balance - Big swings, memorable moments

🆕 v1.7 FUNDAMENTAL CHANGES FROM v1.6:

1. **TWO-DECK SYSTEM** - Separates combat from strategy
   - TROOP DECK (Ranks 1-5 only): Combat power, SUM-based strength
     * Distribution: R1=33%, R2=25%, R3=20%, R4=15%, R5=7%
     * Depletes = game over (pressure mechanic)
   - EVENT DECK (145 cards): Strategic actions, never depletes
     * Contracts, Gather Troops, Attacks, Economic, Manipulation, Utility/Chaotic
     * Shuffles when empty (infinite gameplay)

2. **TURN-BASED FLOW** - Not round-based
   - Each player: Draw event → Play event → Resolve → Next player
   - Continuous action (no waiting for simultaneous reveals)
   - More engaging, less downtime

3. **SUM-BASED ARMY STRENGTH** - Simpler combat math
   - Army strength = SUM of all troop ranks + leader bonuses
   - Example: [R3, R2, R5, R1] = 11 strength (not 4 separate attacks)
   - Net damage ÷ 5 = towers destroyed
   - Clearer power levels, easier to understand

4. **CONTRACT EVENT CARDS** - Strategic choice, not random
   - Leaders acquired via Contract event cards
   - Multiple cost tiers: 1 inf (Captain), 2 inf (Mage), 2 inf+card (Commander)
   - Reduced captain dependency: 5-10 in playbook (was 17 in deck)

5. **EARLY ELIMINATION PROTECTION** - First 2 rounds
   - Damage cap: Max 1 tower loss per round in Rounds 1-2
   - Round 3+: Normal combat
   - Target: 90% of 3P+ games, all players survive to Round 3

6. **EVENT_CARD_POWER MULTIPLIER** - Dial the madness
   - Scales all event card effects (troops, attack bonuses, influence, damage)
   - Range: 0.25 (grindy) → 3.0 (broken)
   - Recommended: 0.5 (moderate) for initial testing
   - Formula: scaled_value = max(1, round(base_value * event_card_power))

WHAT'S REMOVED FROM v1.6:
- ❌ Round-based simultaneous building (replaced with turn-based events)
- ❌ Communal build piles (replaced with individual army areas)
- ❌ Rank 6-10 troops (simplified to Ranks 1-5)
- ❌ Random captain draws from deck (replaced with contracts)
- ❌ Individual attack resolution (replaced with SUM-based)
- ❌ Tower plunder rewards (simplified for v1.7 focus)
- ❌ Attrition mechanics (removed in v1.5, staying gone)

=============================================================================
"""

import random
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from collections import defaultdict

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class EventCardType(Enum):
    """Types of event cards in the Event Deck"""
    # 🔥 v1.16: NEW draft contract system for Mages & Commanders
    CONTRACT_MAGE = "contract_mage"             # leader_contract_cost inf: Choose mage from 3-card market
    CONTRACT_COMMANDER = "contract_commander"   # leader_contract_cost inf: Choose commander from 3-card market
    # Legacy contract types (deprecated in v1.16, kept for compatibility)
    CONTRACT_LEADER = "contract_leader"         # 1 inf: Choose from 3-card market (legacy)
    CONTRACT_CHEAP = "contract_cheap"           # 1 inf: Captain (legacy)
    CONTRACT_STANDARD = "contract_standard"     # 2 inf: Mage (legacy)
    CONTRACT_PREMIUM = "contract_premium"       # 2 inf + 1 card: Commander (legacy)
    CONTRACT_EXPENSIVE = "contract_expensive"   # 3 inf: Multi-leader (legacy)
    GATHER_SMALL = "gather_small"              # 2-3 troops
    GATHER_MEDIUM = "gather_medium"            # 4-5 troops
    GATHER_LARGE = "gather_large"              # 6-8 troops
    ATTACK_BASIC = "attack_basic"              # Base attack
    ATTACK_TACTICAL = "attack_tactical"        # Bonus attack
    ATTACK_CONDITIONAL = "attack_conditional"  # Situational
    ATTACK_AOE = "attack_aoe"                  # Multi-target
    ATTACK_RISKY = "attack_risky"              # High risk/reward
    ECONOMIC = "economic"                       # Gain influence
    MANIPULATION = "manipulation"               # Disrupt opponents
    UTILITY = "utility"                         # Card draw, timing
    
    # v1.12 ATTACK-FOCUSED CARDS (Compensate for mutual damage)
    # Attack Rewards
    BATTLE_FRENZY = "battle_frenzy"            # 0 attacker casualties next attack
    RAIDING_PARTY = "raiding_party"            # Attack + gain 5 troops
    SPOILS_OF_WAR = "spoils_of_war"            # After attack: draw 2 + 3 inf
    # Casualty Reduction
    TACTICAL_RETREAT = "tactical_retreat"       # 50% casualties this turn
    REINFORCEMENTS = "reinforcements"           # Regain casualties after combat
    FORTIFIED_POSITION = "fortified_position"   # 0 casualties when defending
    # Combo/Chain
    MOMENTUM = "momentum"                       # -1 casualty per attack, stacks
    BLITZKRIEG = "blitzkrieg"                  # Attack twice after army defeat
    RAZE = "raze"                              # 🔥 v1.15: Press attack after tower destruction
    CHAIN_ASSAULT = "chain_assault"            # Tower destroyed → draw again
    # 🔥 v1.15: Tower Damage Shields
    SIEGE_EQUIPMENT = "siege_equipment"        # Nullify ALL tower damage (next attack)
    PROTECTIVE_WARDS = "protective_wards"      # Reduce tower damage 50% (next attack)
    VANGUARD_FORMATION = "vanguard_formation"  # First attack ignores tower damage (this turn)
    # Economy
    PLUNDER = "plunder"                        # Tower → 3 inf + 1 card
    WAR_ECONOMY = "war_economy"                # +1 inf per attack this turn
    CONSCRIPTION = "conscription"              # 4 inf → 6 troops
    # 🔥 v1.15: Unclaimed Troops Mechanic
    CLAIM_ARMY = "claim_army"                  # Claim unclaimed troops with available leader
    # Wild Cards
    GUERRILLA_TACTICS = "guerrilla_tactics"    # Cap casualties at 5
    SCORCHED_EARTH = "scorched_earth"          # Destroy tower → 10 troops + 5 inf
    PYRRHIC_VICTORY = "pyrrhic_victory"        # Win auto, lose all troops
    REVERSE_TURN_ORDER = "reverse_turn_order"  # 🔥 v1.15: Reverse play order (clockwise ↔ anti-clockwise)
    
    # v1.13 BYPASS ATTACKS (Hearthstone-style: skip army combat, hit towers directly)
    SIEGE_ATTACK = "siege_attack"              # Bypass: deal bypass_damage to towers
    ARTILLERY_STRIKE = "artillery_strike"      # Bypass: deal 2× bypass_damage to towers

class LeaderType(Enum):
    """Types of leaders available"""
    CAPTAIN = "captain"
    MAGE = "mage"
    COMMANDER = "commander"

class StrategyType(Enum):
    """Player strategies (from v1.6)"""
    RUSH = "rush"           # Fast aggro, 3-troop armies
    SWARM = "swarm"         # Many small armies
    BUILDUP = "buildup"     # Economic, bigger armies
    FORTRESS = "fortress"   # Defensive, patient
    TEMPO = "tempo"         # Flexible, opportunistic
    ADAPTIVE = "adaptive"   # Responds to board state
    WILDCARD = "wildcard"   # 🎲 Randomized behavior each game (usually loses, but interesting when it wins!)

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class EventCard:
    """Represents an event card"""
    card_type: EventCardType
    name: str
    base_effect: Dict[str, any]  # Effect values at 1.0 power
    
    def get_scaled_effect(self, event_card_power: float) -> Dict[str, any]:
        """Scale card effects by event_card_power multiplier"""
        scaled = {}
        for key, value in self.base_effect.items():
            if isinstance(value, int):
                if 'troops' in key or 'draw' in key or 'influence' in key or 'damage' in key:
                    # Additive values
                    scaled[key] = max(1, round(value * event_card_power))
                elif 'bonus' in key or 'attack_plus' in key:
                    # Attack bonuses
                    scaled[key] = round(value * event_card_power)
                elif 'multiplier' in key:
                    # Multiplicative values: 1 + ((base - 1) * power)
                    scaled[key] = 1 + ((value - 1) * event_card_power)
                else:
                    scaled[key] = value
            elif isinstance(value, float) and 'multiplier' in key:
                # Handle multipliers like 2.0, 3.0
                scaled[key] = 1 + ((value - 1) * event_card_power)
            else:
                scaled[key] = value
        return scaled

@dataclass
class Leader:
    """Represents a leader (Captain/Mage/Commander)"""
    leader_type: LeaderType
    name: str
    attack_bonus: int
    unit_value: int
    ability: Optional[str] = None  # Legacy field for compatibility
    # v1.16 Phase 5: Full ability system
    ability_id: str = ""
    ability_type: str = "passive"  # "passive", "triggered", "activated"
    ability_cost: int = 0  # Influence cost (0 for passive/triggered)
    ability_description: str = ""

@dataclass
class Army:
    """Represents a player's army"""
    troops: List[int] = field(default_factory=list)  # List of troop ranks (1-5)
    leader: Optional[Leader] = None
    trick: Optional[str] = None  # 🔥 v1.17: Trick card (assigned when Captain claimed)

    def get_strength(self) -> int:
        """Calculate total army strength = SUM of ranks + leader bonus"""
        troop_sum = sum(self.troops)
        leader_bonus = self.leader.attack_bonus if self.leader else 0
        return troop_sum + leader_bonus

    def get_unit_count(self) -> int:
        """Get total unit count (troops + leader)"""
        return len(self.troops) + (1 if self.leader else 0)

@dataclass
class Player:
    """Represents a player in the game"""
    player_id: int
    strategy: StrategyType
    towers: int = 3
    influence: int = 4  # Starting influence in v1.7
    armies: List[Army] = field(default_factory=list)  # 🔥 v1.9: MULTIPLE ARMIES!
    hand: List[EventCard] = field(default_factory=list)
    leaders: List[Leader] = field(default_factory=list)
    eliminated: bool = False
    towers_destroyed: int = 0  # Towers this player destroyed (total)
    towers_destroyed_this_turn: int = 0  # 🔥 v1.15: Towers destroyed THIS turn (max 1, resets)
    end_turn_now: bool = False  # 🔥 v1.15: Flag to end turn immediately (tower destroyed)
    armies_destroyed: int = 0  # Armies this player destroyed

    # 🔥 v1.11: Attack tracking for incentives
    turns_since_last_attack: int = 0  # Passive tax tracker
    attacked_last_turn: bool = False  # Momentum bonus tracker
    attacks_this_game: int = 0  # Total attacks for glory rewards
    
    # 🔥 v1.12: Active card effects tracking
    active_effects: Dict[str, Any] = field(default_factory=dict)  # Track card effects (battle_frenzy, momentum_stacks, etc.)
    attacks_this_turn: int = 0  # For momentum stacking (-1/-2/-3)
    
    # 🎲 Wildcard strategy randomization (set at game start)
    wildcard_aggression: float = 0.5  # 0.0 = passive, 1.0 = hyper-aggressive
    wildcard_chain_length: int = 3    # Max cards to chain per turn
    wildcard_risk_tolerance: float = 0.5  # 0.0 = safe, 1.0 = risky
    
    def draw_event_card(self, event_deck: List[EventCard], max_hand_size: int = 10) -> Optional[EventCard]:
        """
        Draw an event card from the deck

        🔥 v1.19: Added hand size limit (default 10, prevents runaway card draw)
        """
        if not event_deck:
            return None

        # 🔥 v1.19: Enforce hand size limit (prevent runaway card accumulation)
        if len(self.hand) >= max_hand_size:
            return None  # Hand is full, can't draw more

        card = event_deck.pop(0)
        self.hand.append(card)
        return card
    
    def can_spend_influence(self, amount: int) -> bool:
        """
        🔥 v1.17 SPENDING LOCK: Check if player can spend influence without going below floor of 2
        Player's influence can never drop below 2 (prevents death spiral)
        """
        return self.influence - amount >= 2

    def can_afford_card(self, card: EventCard, event_card_power: float) -> bool:
        """Check if player can afford to play this card (with spending lock)"""
        effect = card.get_scaled_effect(event_card_power)
        cost_influence = effect.get('cost_influence', 0)
        cost_cards = effect.get('cost_cards', 0)
        # 🔥 v1.17 SPENDING LOCK: Check spending lock as well as raw affordability
        can_afford_influence = self.influence >= cost_influence and self.can_spend_influence(cost_influence)
        can_afford_cards = len(self.hand) >= cost_cards + 1  # +1 for the card itself
        return can_afford_influence and can_afford_cards
    
    # 🔥 v1.9: MULTIPLE ARMIES MANAGEMENT
    def get_strongest_army(self) -> Optional[Army]:
        """Get the strongest army (for attacking)"""
        if not self.armies:
            return None
        return max(self.armies, key=lambda a: a.get_strength())
    
    def get_weakest_army(self) -> Optional[Army]:
        """Get the weakest army (for sacrificing in defense)"""
        if not self.armies:
            return None
        return min(self.armies, key=lambda a: a.get_strength())
    
    def get_total_army_strength(self) -> int:
        """Get combined strength of ALL armies"""
        return sum(army.get_strength() for army in self.armies)
    
    def get_total_troop_count(self) -> int:
        """Get total number of troops across ALL armies"""
        return sum(len(army.troops) for army in self.armies)
    
    def create_new_army(self) -> Army:
        """Create a new empty army and add it to player's armies"""
        new_army = Army()
        self.armies.append(new_army)
        return new_army
    
    def remove_army(self, army: Army):
        """Remove an army (when destroyed)"""
        if army in self.armies:
            self.armies.remove(army)
    
    def add_troop_to_strongest_army(self, troop_rank: int):
        """Add a troop to the strongest army (default behavior for gathering troops)"""
        if not self.armies:
            self.create_new_army()
        strongest = self.get_strongest_army()
        strongest.troops.append(troop_rank)

# =============================================================================
# DETAILED LOGGING
# =============================================================================

class GameLogger:
    """Handles detailed turn-by-turn game logging for analysis."""

    def __init__(self, log_file: str):
        self.log_file = log_file
        self.file_handle = open(log_file, 'w')

    def close(self):
        """Close the log file."""
        if self.file_handle:
            self.file_handle.close()

    def write(self, text: str):
        """Write text to log file."""
        self.file_handle.write(text + '\n')
        self.file_handle.flush()  # Ensure it's written immediately

    def log_header(self, text: str):
        """Write a major section header."""
        self.write('=' * 80)
        self.write(text)
        self.write('=' * 80)
        self.write('')

    def log_subheader(self, text: str):
        """Write a minor section header."""
        self.write('')
        self.write('-' * 80)
        self.write(text)
        self.write('-' * 80)

    def log_game_start(self, player_count: int, players: List['Player'], config: 'GameConfig'):
        """Log game initialization."""
        self.log_header('GAME START')
        self.write(f'Players: {player_count}')
        self.write('')
        for p in players:
            self.write(f'Player {p.player_id}:')
            self.write(f'  Strategy: {p.strategy.value}')
            self.write(f'  Towers: {p.towers}')
            self.write(f'  Influence: {p.influence}')
            self.write(f'  Hand: {len(p.hand)} cards')
            if p.strategy.value == 'WILDCARD':
                self.write(f'  Wildcard Aggression: {p.wildcard_aggression:.2f}')
                self.write(f'  Wildcard Chain Length: {p.wildcard_chain_length}')
                self.write(f'  Wildcard Risk Tolerance: {p.wildcard_risk_tolerance:.2f}')
        self.write('')

    def log_turn_start(self, turn: int, player: 'Player', round_num: int, game_state: 'GameState' = None):
        """Log the start of a player's turn."""
        self.log_header(f'TURN {turn} - Player {player.player_id} ({player.strategy.value}) - Round {round_num}')

        # Player state
        self.write('PLAYER STATE:')
        self.write(f'  Towers: {player.towers}')
        self.write(f'  Influence: {player.influence}')
        self.write(f'  Hand Size: {len(player.hand)} cards')

        # Show hand contents
        if player.hand:
            self.write(f'  Hand Cards:')
            for card in player.hand:
                self.write(f'    - {card.name}')

        # Army state
        self.write(f'  Armies: {len(player.armies)}')
        for i, army in enumerate(player.armies):
            troop_count = len(army.troops)
            total_strength = sum(army.troops)
            self.write(f'    Army {i+1}: {troop_count} troops, strength {total_strength}')
            if army.troops:
                self.write(f'      Troops: {sorted(army.troops, reverse=True)}')
            if army.leader:
                self.write(f'      Leader: {army.leader.name} (Attack: +{army.leader.attack_bonus})')

        # 🔥 v1.15 Phase 3: Show available leaders in player's hand
        if player.leaders:
            self.write(f'  Available Leaders: {len(player.leaders)}')
            for leader in player.leaders:
                self.write(f'    - {leader.name} (+{leader.attack_bonus} attack)')

        # 🔥 v1.16: Show leader draft markets (3-card face-up for Mages & Commanders only)
        if game_state:
            self.write('')
            self.write('LEADER DRAFT MARKETS (Mages & Commanders):')
            if game_state.mage_market:
                mage_names = [m.name for m in game_state.mage_market]
                self.write(f'  Mage Market: [{", ".join(mage_names)}] (Deck: {len(game_state.mage_deck)} remaining)')
            if game_state.commander_market:
                commander_names = [c.name for c in game_state.commander_market]
                self.write(f'  Commander Market: [{", ".join(commander_names)}] (Deck: {len(game_state.commander_deck)} remaining)')
            self.write('  Note: Captains are in troop deck (not shown here)')

        # 🔥 v1.15 Phase 3: Show unclaimed troops pool
        if game_state and game_state.unclaimed_troops:
            self.write('')
            self.write('UNCLAIMED TROOPS (Center Pool):')
            troop_count = len(game_state.unclaimed_troops)
            total_strength = sum(game_state.unclaimed_troops)
            troop_breakdown = sorted(game_state.unclaimed_troops, reverse=True)
            self.write(f'  {troop_count} troops, strength {total_strength}')
            self.write(f'  Troops: {troop_breakdown}')

        # Active effects
        if player.active_effects:
            self.write('')
            self.write(f'  Active Effects:')
            for effect, value in player.active_effects.items():
                self.write(f'    - {effect}: {value}')

        self.write('')

    def log_card_play(self, player_id: int, card_name: str, action_num: int):
        """Log a card being played."""
        self.write(f'ACTION {action_num}: Play "{card_name}"')

    def log_card_effect(self, effect_text: str):
        """Log the result of a card effect."""
        self.write(f'  → {effect_text}')

    def log_combat(self, combat_data: dict):
        """Log detailed combat information."""
        self.write('')
        self.write('⚔️' * 40)
        self.write(f"COMBAT: Player {combat_data['attacker_id']} attacks Player {combat_data['defender_id']}")
        self.write('⚔️' * 40)

        # Card played
        if 'card_name' in combat_data:
            self.write(f"Card: {combat_data['card_name']}")

        # Bypass attack (direct tower damage)
        if combat_data.get('bypass_attack'):
            self.write(f"Type: BYPASS ATTACK (direct tower damage)")
            self.write(f"  Bypass Damage: {combat_data.get('bypass_damage', 0)}")
            self.write(f"  Towers Destroyed: {combat_data.get('towers_destroyed', 0)}")
            self.write(f"  Defender Towers: {combat_data['defender_towers_before']} → {combat_data['defender_towers_after']}")
            if combat_data.get('influence_gained', 0) > 0:
                self.write(f"  Attacker Gained: {combat_data['influence_gained']} influence")
            return

        # Army selection
        self.write('')
        self.write('ARMY SELECTION:')
        attacker_army = combat_data.get('attacker_army', {})
        self.write(f"  Attacker chose Army #{attacker_army.get('index', 0)}")
        self.write(f"    Troops: {attacker_army.get('troop_count', 0)} (strength {attacker_army.get('troop_strength', 0)})")
        if attacker_army.get('troops'):
            self.write(f"    Ranks: {attacker_army['troops']}")
        if attacker_army.get('leader'):
            leader_bonus = attacker_army.get('leader_bonus', 0)
            self.write(f"    Leader: {attacker_army['leader']} (+{leader_bonus} attack)")
            # 🔥 v1.16: Show leader ability if present
            if attacker_army.get('leader_ability'):
                self.write(f"      💫 Ability: {attacker_army['leader_ability']}")
        elif not attacker_army.get('has_leader'):
            self.write(f"    Leader: None ⚠️  (no leader bonus)")

        defender_army = combat_data.get('defender_army', {})
        self.write(f"  Defender chose Army #{defender_army.get('index', 0)}")
        self.write(f"    Troops: {defender_army.get('troop_count', 0)} (strength {defender_army.get('troop_strength', 0)})")
        if defender_army.get('troops'):
            self.write(f"    Ranks: {defender_army['troops']}")
        if defender_army.get('leader'):
            leader_bonus = defender_army.get('leader_bonus', 0)
            self.write(f"    Leader: {defender_army['leader']} (+{leader_bonus} defense)")
            # 🔥 v1.16: Show leader ability if present
            if defender_army.get('leader_ability'):
                self.write(f"      💫 Ability: {defender_army['leader_ability']}")
        elif not defender_army.get('has_leader'):
            self.write(f"    Leader: None (no leader bonus)")

        # Combat calculation
        self.write('')
        self.write('COMBAT CALCULATION:')

        # 🔥 v1.15 Phase 3: Show tower damage and shield effects
        tower_damage_config = combat_data.get('tower_damage_config', 0)
        tower_damage_taken = combat_data.get('tower_damage_taken', 0)
        shield_effect = combat_data.get('shield_effect')

        if tower_damage_config > 0:
            original_strength = combat_data.get('attack_base', 0) + tower_damage_taken
            self.write(f"  Army Strength (before tower damage): {original_strength}")

            # Show shield effects
            if shield_effect == 'siege_equipment':
                self.write(f"  🛡️  SIEGE EQUIPMENT: Tower damage nullified!")
                self.write(f"  - Tower Damage: {tower_damage_config} → 0 (shielded)")
            elif shield_effect == 'protective_wards':
                self.write(f"  🛡️  PROTECTIVE WARDS: Tower damage reduced 50%")
                self.write(f"  - Tower Damage: {tower_damage_config} → {tower_damage_taken} (reduced)")
            elif shield_effect == 'vanguard_formation':
                self.write(f"  🛡️  VANGUARD FORMATION: First attack shielded!")
                self.write(f"  - Tower Damage: {tower_damage_config} → 0 (first attack)")
            elif tower_damage_taken > 0:
                self.write(f"  - Tower Damage: {tower_damage_taken}")
            else:
                self.write(f"  - Tower Damage: 0 (no towers)")

            self.write(f"  = Attacker Base: {combat_data.get('attack_base', 0)}")
        else:
            self.write(f"  Attacker Base: {combat_data.get('attack_base', 0)}")

        if combat_data.get('attack_bonus', 0) > 0:
            bonus_source = combat_data.get('bonus_source', 'Unknown')
            self.write(f"  + Card Bonus: {combat_data['attack_bonus']} (from {bonus_source})")
        if combat_data.get('attack_multiplier', 1.0) != 1.0:
            self.write(f"  × Multiplier: {combat_data['attack_multiplier']}x")
        self.write(f"  = Total Attack: {combat_data.get('total_attack', 0)}")
        self.write(f"  Defender: {combat_data.get('defense_strength', 0)}")

        # Blocking decision (if applicable)
        if 'blocking_enabled' in combat_data and combat_data['blocking_enabled']:
            blocked = combat_data.get('defender_blocked', True)
            self.write('')
            self.write('BLOCKING DECISION:')
            if blocked:
                self.write(f"  Defender CHOSE TO BLOCK")
                self.write(f"    Reasoning: {combat_data.get('block_reason', 'Strategic decision')}")
            else:
                self.write(f"  Defender CHOSE NOT TO BLOCK")
                self.write(f"    Reasoning: {combat_data.get('block_reason', 'Preserving army')}")

        # Combat outcome
        self.write('')
        self.write('OUTCOME:')

        if not combat_data.get('defender_blocked', True) and combat_data.get('blocking_enabled'):
            # Didn't block - tower damage, armies survive
            self.write(f"  No blocking: Attack goes through to towers")
            self.write(f"  Towers Destroyed: {combat_data.get('towers_destroyed', 0)}")
            self.write(f"  Defender Towers: {combat_data['defender_towers_before']} → {combat_data['defender_towers_after']}")
            self.write(f"  Both armies survive intact")
        else:
            # Normal combat with casualties
            # 🔥 v1.15: Show asymmetric strength-based casualties
            attacker_casualties = combat_data.get('attacker_casualties', 0)
            defender_casualties = combat_data.get('defender_casualties', 0)
            attacker_removed = combat_data.get('attacker_strength_removed', 0)
            defender_removed = combat_data.get('defender_strength_removed', 0)
            net_damage = combat_data.get('net_damage', 0)

            self.write(f"  Attacker takes: {attacker_casualties} strength casualties (removed: {attacker_removed})")
            self.write(f"  Defender takes: {defender_casualties} strength casualties (removed: {defender_removed})")
            self.write(f"  Net Damage to Towers: {net_damage}")
            self.write(f"  Towers Destroyed: {combat_data.get('towers_destroyed', 0)}")
            self.write(f"  Defender Towers: {combat_data['defender_towers_before']} → {combat_data['defender_towers_after']}")

            if combat_data.get('attacker_army_destroyed'):
                self.write(f"  💀 Attacker's army DESTROYED")
            elif attacker_removed > 0:
                self.write(f"  ✅ Attacker's army SURVIVES (lost {attacker_removed} strength)")

            if combat_data.get('defender_army_destroyed'):
                self.write(f"  💀 Defender's army DESTROYED")

        # Rewards
        if combat_data.get('towers_destroyed', 0) > 0:
            self.write('')
            self.write('REWARDS:')
            if combat_data.get('influence_gained', 0) > 0:
                self.write(f"  Influence: +{combat_data['influence_gained']}")
                if combat_data.get('momentum_bonus'):
                    self.write(f"    (includes momentum bonus!)")
            if combat_data.get('cards_drawn', 0) > 0:
                self.write(f"  Cards Drawn: {combat_data['cards_drawn']}")
            if combat_data.get('glory_bonus', 0) > 0:
                self.write(f"  Glory Bonus: +{combat_data['glory_bonus']} influence")

        # Elimination
        if combat_data.get('defender_eliminated'):
            self.write('')
            self.write(f"  💀💀💀 PLAYER {combat_data['defender_id']} ELIMINATED! 💀💀💀")

        self.write('')

    def log_elimination(self, player_id: int, turn: int):
        """Log a player elimination."""
        self.write('')
        self.write('💀' * 40)
        self.write(f'PLAYER {player_id} ELIMINATED (Turn {turn})')
        self.write('💀' * 40)
        self.write('')

    def log_turn_end(self, cards_played: int, troops_drawn: int):
        """Log turn summary."""
        self.write('')
        self.write(f'TURN END: {cards_played} cards played, {troops_drawn} troops drawn')
        self.write('')

    def log_game_end(self, winner_id: int, turns: int, reason: str):
        """Log game conclusion."""
        self.log_header('GAME END')
        self.write(f'Winner: Player {winner_id}')
        self.write(f'Win Type: {reason}')
        self.write(f'Total Turns: {turns}')
        self.write('')

# =============================================================================
# GAME STATE
# =============================================================================

@dataclass
class GameConfig:
    """Configuration for game parameters"""
    # Troop Deck composition (Ranks 1-5 only)
    troops_rank_1: int = 17  # 33% of 50
    troops_rank_2: int = 13  # 25%
    troops_rank_3: int = 10  # 20%
    troops_rank_4: int = 7   # 15%
    troops_rank_5: int = 3   # 7%
    
    # Event Deck composition (145 cards total)
    # 🔥 v1.16: NEW draft contract system (Mages & Commanders only)
    contracts_mage: int = 15        # leader_contract_cost inf: Draft mage from 3-card market
    contracts_commander: int = 10   # leader_contract_cost inf: Draft commander from 3-card market
    # Legacy contracts (kept for backwards compatibility, reduce counts)
    contracts_leader: int = 0       # Deprecated: replaced by CONTRACT_MAGE & CONTRACT_COMMANDER
    contracts_cheap: int = 2        # 1 influence: Captain (legacy)
    contracts_standard: int = 2     # 2 influence: Mage (legacy)
    contracts_premium: int = 2      # 2 inf + 1 card: Commander (legacy)
    contracts_expensive: int = 1    # 3 influence: Multi-leader (legacy)
    contracts_chaotic: int = 0      # Deprecated
    
    # Gather Troops (30)
    gather_small: int = 10          # 2-3 troops
    gather_medium: int = 10         # 4-5 troops
    gather_large: int = 5           # 6-8 troops
    gather_conditional: int = 5     # Varies
    
    # Attacks (35)
    attacks_basic: int = 8
    attacks_tactical: int = 8
    attacks_conditional: int = 6
    attacks_aoe: int = 5
    attacks_leader_enhanced: int = 5
    attacks_risky: int = 3
    
    # Other (55)
    economic: int = 15
    manipulation: int = 15
    utility_chaotic: int = 25
    
    # Game mechanics (v1.8.1 TUNING - Target: 2-3 cards/turn)
    event_card_power: float = 1.148        # GA optimized for chaining
    early_protection_rounds: int = 2        # GA optimal (damage cap rounds)
    early_protection_max_towers: int = 2    # GA optimal (max towers per attack)
    early_attack_block_rounds: int = 0      # 🔥 v1.15: Rounds where NO attacks allowed (0=disabled)
    tower_damage_threshold: int = 6         # GA: slightly tankier (was 5 in v1.7)
    tower_attack_damage: int = 3            # 🔥 v1.15: Tower damage to attacker BEFORE combat (0-10 range)
    claim_army_cost: int = 2                # 🔥 v1.15: Influence cost to claim unclaimed troops (0-5 range)
    starting_influence: int = 6             # 🔥 v1.8.1: INCREASED for 2-3 cards/turn (was 5)
    starting_hand_size: int = 6             # 🔥 v1.8.1: INCREASED for sustained chaining (was 5)
    
    # v1.11 ATTACK INCENTIVE PARAMETERS (kept for backwards compatibility)
    influence_per_tower: int = 2            # Influence gained per tower destroyed (1-5 range)
    passive_tax_amount: int = 1             # Influence lost when passive (0-4 range)
    passive_tax_threshold: int = 2          # Turns without attack before tax (1-4 range)
    momentum_multiplier: float = 2.0        # Influence multiplier for consecutive attacks (1.0-5.0)
    glory_divisor: int = 3                  # Bonus = towers_destroyed // X (2-6 range)
    bonus_cards_per_tower: int = 1          # Extra cards drawn per tower destroyed (0-3)
    
    # v1.12 ATTACK-FOCUSED EVENT CARDS (GA optimizes composition!)
    # Attack Rewards (30% of deck)
    battle_frenzy_count: int = 2            # 0 attacker casualties next attack (0-5 range)
    raiding_party_count: int = 4            # Attack + gain 5 troops (0-8 range)
    spoils_of_war_count: int = 6            # After attack: draw 2 + 3 influence (0-10 range)
    
    # Casualty Reduction (20% of deck)
    tactical_retreat_count: int = 4         # 50% casualties this turn (0-8 range)
    reinforcements_count: int = 2           # Regain casualties after combat (0-4 range)
    fortified_position_count: int = 2       # 0 casualties when defending (0-4 range)
    
    # Combo/Chain (25% of deck)
    momentum_card_count: int = 4            # -1 casualty per attack, stacks (0-8 range)
    blitzkrieg_count: int = 3               # Attack twice after army defeat (0-6 range)
    raze_count: int = 1                     # 🔥 v1.15: Press attack after tower (0-3 range)
    chain_assault_count: int = 3            # Tower destroyed → draw again (0-6 range)

    # 🔥 v1.15: Tower Damage Shields (Phase 2)
    siege_equipment_count: int = 2          # Nullify tower damage next attack (0-4 range)
    protective_wards_count: int = 3         # Reduce tower damage 50% next attack (0-6 range)
    vanguard_formation_count: int = 2       # First attack ignores tower damage (0-4 range)
    
    # Economy (20% of deck)
    plunder_count: int = 4                  # Tower → 3 inf + 1 card (0-8 range)
    war_economy_count: int = 3              # +1 inf per attack this turn (0-6 range)
    conscription_count: int = 3             # 4 inf → 6 troops (0-6 range)
    claim_army_count: int = 3               # 🔥 v1.15: Claim unclaimed troops (0-6 range)
    
    # Wild Cards (5% of deck)
    guerrilla_tactics_count: int = 1        # Cap casualties at 5 (0-3 range)
    scorched_earth_count: int = 1           # Destroy tower → 10 troops + 5 inf (0-3 range)
    pyrrhic_victory_count: int = 0          # Win auto, lose all troops (0-2 range)
    reverse_turn_order_count: int = 1       # 🔥 v1.15: Reverse play direction (0-3 range)
    
    # 🔥 v1.13 NEW: CORE MECHANIC ALTERNATIVES (GA optimizes!)
    # Inspired by MTG (opt-in blocking) + Hearthstone (bypass attacks)
    enable_optional_blocking: bool = False  # Defender chooses whether to block (MTG-style)
    enable_bypass_attacks: bool = False     # Some cards attack towers directly (Hearthstone-style)
    bypass_damage_amount: int = 2           # Tower damage for bypass attacks (1-4 range)
    
    # Core game parameters (v1.9+)
    troop_deck_size: int = 143              # Total troops available (v1.8.3 optimal)
    starting_troops_per_player: int = 15    # Starting army size
    tower_income: int = 2                   # Income per tower per round
    troops_per_tower: int = 5               # Troops gained from destroying tower
    
    # Leader Playbook (v1.16: 40 captains in troop deck, 40 mages/commanders in draft markets)
    captains_available: int = 40  # All 40 captains in TROOP DECK (no market)
    mages_available: int = 40     # All 40 mages in draft market (3 face-up, 37 face-down)
    commanders_available: int = 40  # All 40 commanders in draft market (3 face-up, 37 face-down)
    leader_contract_cost: int = 1  # 🔥 v1.16: Influence cost to contract mage/commander from market (GA range 0-3)

    # 🔥 v1.14 NEW CARDS: Endgame/Elimination (4 cards)
    death_blow_count: int = 2              # Event: If opp has 1 tower, deal 3 damage (0-3 range)
    coup_de_grace_count: int = 1           # Event: Eliminated player this turn? Draw 3 (0-2 range)
    vulture_count: int = 2                 # Troop: 2 + (2 × elim players) strength (0-4 range)
    elimination_bounty_count: int = 1      # Passive: Eliminate player → +5 inf (0-2 range)

    # 🔥 v1.14 NEW CARDS: Comeback/Desperation (4 cards)
    pyrrhic_assault_count: int = 1         # Event: Destroy your tower → 4 damage to enemy tower (0-2 range)
    final_rally_count: int = 2             # Enhancement: At 1 tower, troop deals double (0-3 range)
    nothing_to_lose_count: int = 1         # Passive: At 1 tower, +1 card/turn (0-2 range)
    desperate_gambit_count: int = 2        # Event: Discard hand, draw 5 (0-3 range)

    # 🔥 v1.14 NEW CARDS: Leader Synergy (3 cards)
    inspire_troops_count: int = 1          # Captain: All troops +2 this turn, once/game (0-2 range)
    arcane_bombardment_count: int = 2      # Mage: Pay 4 inf → 2 damage to tower (0-3 range)
    war_council_count: int = 2             # Event: Draw 1 per leader you have (0-3 range)

    # 🔥 v1.14 NEW CARDS: Position/Dominance (3 cards)
    overwhelming_numbers_count: int = 1    # Event: 2+ tower advantage → 1 damage all enemies (0-2 range)
    defensive_pact_count: int = 2          # Event: Fewest towers → +3 inf (0-3 range)
    territory_control_count: int = 1       # Passive: Each tower beyond 3 → +1 income (0-2 range)

    # 🔥 v1.14 NEW PARAMETERS: Leader Powers (6 params)
    captain_combat_bonus: int = 1          # +X strength to troops when captain present (0-3 range)
    mage_ability_cost: int = 4             # Influence cost for mage abilities (2-5 range)
    commander_defense_value: int = 1       # Damage prevention per commander (0-3 range)
    leader_health: int = 3                 # Leader HP, 0=invincible (1-5 range)
    captain_troop_limit: int = 5           # Max troops captain can boost (0-10 range)
    mage_range: int = 2                    # How many towers mage can affect (1-5 range)

    # 🔥 v1.14 NEW PARAMETERS: Combat/Pacing (5 params)
    tower_base_hp: int = 6                 # Damage to destroy tower (3-10 range)
    max_hand_size: int = 10                # 🔥 v1.19: Hand limit (prevents runaway card draw)
    troop_strength_variance: float = 1.0   # Multiply all troop strength (0.5-2.0 range)
    attack_chains_allowed: int = 3         # Max consecutive attacks (1-5 range)
    income_multiplier: float = 1.0         # Scale all income (0.5-2.0 range)

    # Verbosity control (for GA runs)
    verbose: bool = False                  # Set to False to suppress per-game output
    detailed_log: bool = False             # Enable turn-by-turn detailed logging
    log_file: str = None                   # File path for detailed log (if detailed_log=True)

@dataclass
class GameState:
    """Current state of the game"""
    players: List[Player]
    troop_deck: List[int]  # List of ranks (1-5)
    event_deck: List[EventCard]
    event_discard: List[EventCard]
    config: GameConfig
    current_round: int = 1
    current_turn: int = 0
    game_over: bool = False
    winner: Optional[int] = None

    # 🔥 v1.15: Unclaimed troops pool (shared center pile)
    unclaimed_troops: List[int] = field(default_factory=list)  # Troops waiting to be claimed

    # 🔥 v1.16: EPIC LEADER DRAFT SYSTEM - Mages & Commanders only (Captains in troop deck)
    mage_deck: List[Leader] = field(default_factory=list)  # Mage deck (face-down, 37 cards after initial deal)
    mage_market: List[Leader] = field(default_factory=list)  # Mage market (face-up, 3 cards)
    commander_deck: List[Leader] = field(default_factory=list)  # Commander deck (face-down, 37 cards)
    commander_market: List[Leader] = field(default_factory=list)  # Commander market (face-up, 3 cards)

    # 🔥 v1.17: Captain pool (40 captains, drawn when Captain card appears in troop deck)
    captain_pool: List[Leader] = field(default_factory=list)

    # 🔥 v1.17: Trick Playbook deck (26 cards, drawn when Captain claimed)
    trick_deck: List[str] = field(default_factory=list)

    play_direction: int = 1  # 🔥 v1.15: 1 = clockwise, -1 = anti-clockwise

    # Tracking metrics
    total_turns: int = 0
    contract_plays: int = 0
    attack_plays: int = 0
    towers_destroyed_total: int = 0
    cards_played_per_turn: List[int] = field(default_factory=list)  # Track event cards played each turn
    cards_drawn_per_turn: List[int] = field(default_factory=list)   # Track event cards drawn each turn
    troops_drawn_per_turn: List[int] = field(default_factory=list)  # Track troop cards drawn each turn
    
    def get_active_players(self) -> List[Player]:
        """Get list of non-eliminated players"""
        return [p for p in self.players if not p.eliminated]
    
    def check_game_over(self) -> bool:
        """Check if game should end"""
        active = self.get_active_players()

        # Win by elimination
        if len(active) == 1:
            self.game_over = True
            self.winner = active[0].player_id
            return True

        # All players eliminated (shouldn't happen but handle it)
        if len(active) == 0:
            self.game_over = True
            # Pick last eliminated player's eliminator or just player 0
            self.winner = 0
            return True

        # Loss by troop deck depletion
        if not self.troop_deck:
            self.game_over = True
            # Winner is player with most towers
            self.winner = max(active, key=lambda p: p.towers).player_id
            return True

        return False

    def log_action(self, message: str):
        """
        🔥 v1.18: Helper to log actions to file (not console)
        Only logs if detailed_log is enabled and logger exists
        """
        if self.config.detailed_log and hasattr(self, '_logger') and self._logger:
            self._logger.write(message)

# =============================================================================
# DECK CREATION
# =============================================================================

def create_troop_deck(config: GameConfig) -> List[int]:
    """
    Create the Troop Deck with Ranks 1-5 + Captain cards

    🔥 v1.17: Captains are now in the troop deck (represented as value 0)
    When a Captain (0) is drawn, it auto-claims unclaimed troops + draws trick
    """
    deck = []
    deck.extend([1] * config.troops_rank_1)
    deck.extend([2] * config.troops_rank_2)
    deck.extend([3] * config.troops_rank_3)
    deck.extend([4] * config.troops_rank_4)
    deck.extend([5] * config.troops_rank_5)
    # 🔥 v1.17: Add Captain cards (value 0 = special marker)
    deck.extend([0] * config.captains_available)
    random.shuffle(deck)
    return deck

def create_trick_deck() -> List[str]:
    """
    Create the Trick Playbook deck (26 cards from 2020 version)

    🔥 v1.17: Tricks are drawn when Captain is claimed
    Each Captain army gets ONE trick card
    """
    tricks = []
    tricks.extend(['Spyglass'] * 4)
    tricks.extend(['Fireball'] * 4)
    tricks.extend(['Poison'] * 3)
    tricks.extend(['Rocket'] * 2)
    tricks.extend(['Counter'] * 2)
    tricks.extend(['Rage'] * 2)
    tricks.extend(['Tactics'] * 2)
    tricks.extend(['Resupply'] * 2)
    tricks.extend(['Snipe', 'Fog', 'Dodge', 'Earthquake', 'Plague'])
    random.shuffle(tricks)
    return tricks

def create_event_deck(config: GameConfig) -> List[EventCard]:
    """Create the massive 145-card Event Deck"""
    cards = []

    # 🔥 v1.16: NEW CONTRACT_MAGE & CONTRACT_COMMANDER cards (25 cards total)
    # Contract Mage (15 cards) - Draft from 3-card mage market
    for i in range(config.contracts_mage):
        cards.append(EventCard(
            EventCardType.CONTRACT_MAGE,
            f"Contract Mage",
            {'cost_influence': config.leader_contract_cost}
        ))

    # Contract Commander (10 cards) - Draft from 3-card commander market
    for i in range(config.contracts_commander):
        cards.append(EventCard(
            EventCardType.CONTRACT_COMMANDER,
            f"Contract Commander",
            {'cost_influence': config.leader_contract_cost}
        ))

    # LEGACY CONTRACT_LEADER (deprecated in v1.16, kept for backwards compatibility)
    for i in range(config.contracts_leader):
        cards.append(EventCard(
            EventCardType.CONTRACT_LEADER,
            f"Contract Leader (Legacy)",
            {'cost_influence': config.leader_contract_cost}
        ))

    # LEGACY CONTRACTS (8 cards total, reduced from 25)
    # Cheap Captain contracts (1 influence) - uses config.contracts_cheap
    cheap_contracts = [
        ("Recruit Captain", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN}),
        ("Mercenary Deal", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'bonus_attack': 1}),
        ("Draft Notice", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'gather_troops': 2}),
        ("Emergency Hire", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'influence_penalty_next': 1}),
        ("Conscription", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'draw_events': 1}),
        ("Battlefield Promotion", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'can_attack_twice': True}),
        ("Quick Hire", {'cost_influence': 1, 'leader_type': LeaderType.CAPTAIN, 'extra_turn': True}),
        ("Desperate Recruitment", {'cost_influence': 0, 'leader_type': LeaderType.CAPTAIN, 'condition': 'fewest_towers'}),
    ]
    for i, (name, effect) in enumerate(cheap_contracts[:config.contracts_cheap]):
        cards.append(EventCard(EventCardType.CONTRACT_CHEAP, name, effect))
    
    # Standard Mage contracts (2 influence) - uses config.contracts_standard
    standard_contracts = [
        ("Hire Mage", {'cost_influence': 2, 'leader_type': LeaderType.MAGE}),
        ("Magical Binding", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'bonus_attack': 2}),
        ("Arcane Alliance", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'gain_influence': 1}),
        ("Spellcaster Pact", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'draw_events': 2}),
        ("Mystic Recruitment", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'gather_troops': 3}),
        ("Sorcerer's Bargain", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'steal_troops': 1}),
        ("Wizards Council", {'cost_influence': 2, 'leader_type': LeaderType.MAGE, 'can_get_two': True}),
    ]
    for i, (name, effect) in enumerate(standard_contracts[:config.contracts_standard]):
        cards.append(EventCard(EventCardType.CONTRACT_STANDARD, name, effect))
    
    # Premium Commander contracts (2 inf + 1 card) - uses config.contracts_premium
    premium_contracts = [
        ("Warlord Summons", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER}),
        ("Legendary Hero", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER, 'bonus_attack': 3}),
        ("Generals Call", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER, 'gather_troops': 4}),
        ("Supreme Commander", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER, 'gain_influence': 2}),
        ("Battle Tactician", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER, 'destroy_troop': 1}),
        ("Champion's Arrival", {'cost_influence': 2, 'cost_cards': 1, 'leader_type': LeaderType.COMMANDER, 'can_attack_immediately': True}),
    ]
    for i, (name, effect) in enumerate(premium_contracts[:config.contracts_premium]):
        cards.append(EventCard(EventCardType.CONTRACT_PREMIUM, name, effect))
    
    # Expensive multi-leader contracts (3 influence) - uses config.contracts_expensive
    expensive_contracts = [
        ("War Council", {'cost_influence': 3, 'get_commander': True, 'get_mage': True}),
        ("Elite Task Force", {'cost_influence': 3, 'get_any_two': True}),
        ("Army of One", {'cost_influence': 3, 'leader_type': LeaderType.COMMANDER, 'counts_as_three': True}),
    ]
    for i, (name, effect) in enumerate(expensive_contracts[:config.contracts_expensive]):
        cards.append(EventCard(EventCardType.CONTRACT_EXPENSIVE, name, effect))
    
    # Chaotic contract - 1 card
    cards.append(EventCard(EventCardType.CONTRACT_EXPENSIVE, "Mystery Mercenary", 
                          {'cost_influence': 1, 'random_leader': True}))
    
    # GATHER TROOPS (30 cards)
    # Small (2-3 troops) - 10 cards
    gather_small_cards = [
        ("Scout Patrol", {'gather_troops': 2}),
        ("Recruitment Drive", {'gather_troops': 3}),
        ("Muster Forces", {'gather_troops': 3, 'discard_troops': 1}),
        ("Local Militia", {'gather_troops': 2, 'gain_influence': 1}),
        ("Volunteers", {'gather_troops': 2, 'draw_events': 1}),
        ("Town Guard", {'gather_troops': 2, 'rank_bonus': 1}),
        ("Quick Gather", {'gather_troops': 2, 'extra_turn': True}),
        ("Selective Draft", {'look_troops': 5, 'take_troops': 2}),
        ("Cherry Pick", {'look_troops': 4, 'take_troops': 1}),
        ("Scavenge", {'gather_from_discard': 2}),
    ]
    for name, effect in gather_small_cards:
        cards.append(EventCard(EventCardType.GATHER_SMALL, name, effect))
    
    # Medium (4-5 troops) - 10 cards  
    gather_medium_cards = [
        ("Call to Arms", {'gather_troops': 4}),
        ("Rally the Troops", {'gather_troops': 5}),
        ("Reinforcements", {'gather_troops': 4, 'optional_pay_influence': 1, 'optional_get_troops': 2}),
        ("Army Muster", {'gather_troops': 5, 'must_attack_within': 2}),
        ("Battle Preparation", {'gather_troops': 4, 'all_become_rank': 3}),
        ("Mass Recruitment", {'gather_troops': 5, 'lose_influence': 1}),
        ("Fortify Ranks", {'gather_troops': 4, 'gain_permanent_defense': 2}),
        ("Tactical Gathering", {'gather_troops': 3, 'bonus_if_commander': 2}),
        ("Elite Selection", {'gather_troops': 6, 'keep_best': 4}),
        ("Strategic Muster", {'gather_troops': 4, 'optional_discard_card': 1, 'optional_get_troops': 2}),
    ]
    for name, effect in gather_medium_cards:
        cards.append(EventCard(EventCardType.GATHER_MEDIUM, name, effect))
    
    # Large (6-8 troops) - 5 cards
    gather_large_cards = [
        ("Mass Mobilization", {'gather_troops': 6}),
        ("Full Muster", {'gather_troops': 7}),
        ("Army Assembly", {'gather_troops': 8, 'discard_random_troops': 2}),
        ("Glorious Charge", {'gather_troops': 7, 'must_attack_this_turn': True}),
        ("War Machine", {'gather_troops': 6, 'all_become_rank': 5}),
    ]
    for name, effect in gather_large_cards:
        cards.append(EventCard(EventCardType.GATHER_LARGE, name, effect))
    
    # Conditional/Interactive - 5 cards
    gather_conditional_cards = [
        ("Gambit", {'gather_troops_random': (3, 7)}),
        ("Desperation", {'gather_troops_formula': 'missing_towers * 2'}),
        ("Underdog Rally", {'gather_troops_if_losing': 8, 'gather_troops_else': 3}),
        ("Steal Recruits", {'gather_troops': 3, 'target_discards_troops': 2}),
        ("Conscription", {'all_players_gather': 3, 'you_gather': 5}),
    ]
    for name, effect in gather_conditional_cards:
        cards.append(EventCard(EventCardType.GATHER_SMALL, name, effect))
    
    # ATTACK CARDS (35 cards)
    # Basic attacks - 8 cards
    attack_basic_cards = [
        ("Assault", {'attack_bonus': 0}),
        ("Strike", {'attack_bonus': 2}),
        ("Charge", {'attack_bonus': 3}),
        ("Ambush", {'attack_bonus': 5, 'lose_troops_after': 2}),
        ("Raid", {'attack_bonus': 0, 'steal_influence_on_win': 1}),
        ("Invasion", {'attack_bonus': 0, 'bonus_influence_on_tower': 1}),
        ("Blitz", {'attack_bonus': 0, 'attack_again_if_win': True, 'second_attack_half': True}),
        ("Relentless Assault", {'attack_bonus': 0, 'can_switch_target_if_blocked': True}),
    ]
    for name, effect in attack_basic_cards:
        cards.append(EventCard(EventCardType.ATTACK_BASIC, name, effect))
    
    # Tactical attacks - 8 cards
    attack_tactical_cards = [
        ("Pincer Attack", {'attack_two_targets': True, 'split_army': True}),
        ("Focused Strike", {'attack_bonus': 8, 'discard_troops_after': 3}),
        ("Surgical Strike", {'attack_bonus': 0, 'ignore_defense': 5}),
        ("Overwhelming Force", {'attack_multiplier': 2.0}),
        ("Calculated Assault", {'attack_bonus': 0, 'draw_events_after': 2}),
        ("Strategic Strike", {'attack_bonus': 0, 'gather_troops_on_win': 4}),
        ("Lightning Assault", {'attack_bonus': 3, 'extra_turn_after': True}),
        ("Siege Attack", {'attack_bonus': 0, 'damage_towers_even_if_blocked': True}),
    ]
    for name, effect in attack_tactical_cards:
        cards.append(EventCard(EventCardType.ATTACK_TACTICAL, name, effect))
    
    # Conditional attacks - 6 cards
    attack_conditional_cards = [
        ("Revenge", {'attack_bonus_if_damaged_by': 10}),
        ("Underdog Strike", {'attack_bonus_if_losing': 15, 'attack_bonus_else': 2}),
        ("Challenger", {'attack_bonus_vs_most_influence': 7}),
        ("Opportunistic Raid", {'attack_bonus_vs_most_towers': 5}),
        ("Defensive Counter", {'attack_bonus_vs_attacker': 8, 'only_if_attacked': True}),
        ("Blood Feud", {'attack_bonus_vs_eliminator': 12}),
    ]
    for name, effect in attack_conditional_cards:
        cards.append(EventCard(EventCardType.ATTACK_CONDITIONAL, name, effect))
    
    # AoE attacks - 5 cards
    attack_aoe_cards = [
        ("Rampage", {'damage_all_opponents': 3}),
        ("Scatter Attack", {'damage_split': 5, 'choose_targets': True}),
        ("Chaos Assault", {'damage_random_per_tower': True}),
        ("Apocalypse", {'damage_all_including_self': 2}),
        ("Rain of Fire", {'damage_all_with_3_towers': 1}),
    ]
    for name, effect in attack_aoe_cards:
        cards.append(EventCard(EventCardType.ATTACK_AOE, name, effect))
    
    # Leader-enhanced attacks - 5 cards
    attack_leader_cards = [
        ("Commander's Fury", {'requires': LeaderType.COMMANDER, 'attack_bonus': 10}),
        ("Mage Barrage", {'requires': LeaderType.MAGE, 'ignore_all_defense': True}),
        ("Captain's Gambit", {'requires': LeaderType.CAPTAIN, 'attack_three_times': True, 'each_half_strength': True}),
        ("Berserker Rage", {'requires_specific': 'Berserker Boss', 'attack_all_opponents': True}),
        ("Zombie Horde", {'requires_specific': 'Zombie Boss', 'gather_troops': 5, 'attack_immediately': True}),
    ]
    for name, effect in attack_leader_cards:
        cards.append(EventCard(EventCardType.ATTACK_TACTICAL, name, effect))
    
    # Risky attacks - 3 cards
    attack_risky_cards = [
        ("All-In Assault", {'attack_multiplier': 3.0, 'lose_all_troops_after': True}),
        ("Kamikaze Strike", {'destroy_own_tower': 1, 'deal_tower_damage': 2, 'ignore_defense': True}),
        ("Reckless Charge", {'attack_bonus': 10, 'take_tower_damage_if_lose': 1}),
    ]
    for name, effect in attack_risky_cards:
        cards.append(EventCard(EventCardType.ATTACK_RISKY, name, effect))
    
    # ECONOMIC CARDS (15 cards)
    economic_cards = [
        ("Tax Collection", {'gain_influence': 3}),
        ("Trade Route", {'gain_influence_per_tower': 2}),
        ("Plunder", {'gain_influence': 4, 'discard_troops': 3}),
        ("War Spoils", {'gain_influence_per_tower_destroyed': 1}),
        ("Treasure Hunter", {'gain_influence': 5, 'skip_next_turn': True}),
        ("Windfall", {'gain_influence_formula': 'towers * 2'}),
        ("Extortion", {'steal_influence_from_richest': 3}),
        ("Pillage", {'all_lose_influence': 2, 'you_gain_per_opponent': 1}),
        ("Steal Wealth", {'steal_half_influence': True}),
        ("Redistribute", {'all_give_you': 1, 'you_give_back': 2}),
        ("Sell Troops", {'discard_troops_for_influence': True, 'rate': 1}),
        ("Sell Leaders", {'discard_leaders_for_influence': True, 'rate': 3}),
        ("Emergency Funds", {'discard_events': 2, 'gain_influence': 5}),
        ("Underdog Bonus", {'gain_influence_if_losing': 8, 'gain_influence_else': 2}),
        ("Momentum", {'gain_influence_per_tower_destroyed_last_turn': 2}),
    ]
    for name, effect in economic_cards:
        cards.append(EventCard(EventCardType.ECONOMIC, name, effect))
    
    # MANIPULATION CARDS (15 cards)
    manipulation_cards = [
        ("Sabotage", {'target_discards_events': 3}),
        ("Raid Supplies", {'target_discards_troops': 5}),
        ("Espionage", {'look_at_hand': True, 'force_discard': 2}),
        ("Snipe", {'destroy_target_leader': True}),
        ("Earthquake", {'destroy_half_target_army': True}),
        ("Poach", {'steal_troops_from_target': 3}),
        ("Headhunt", {'steal_target_leader': True, 'cost_influence': 2}),
        ("Copy Tactics", {'copy_last_opponent_card': True}),
        ("Steal Secrets", {'look_top_any_deck': 5, 'take': 2}),
        ("Pickpocket", {'steal_random_event_from_each': True}),
        ("Famine", {'all_discard_half_troops': True}),
        ("Plague", {'all_armies_lose_troops': 2}),
        ("Chaos Storm", {'all_discard_random_events': 2}),
        ("Revolution", {'swap_influence_clockwise': True}),
        ("Apocalypse Now", {'all_discard_all_troops': True, 'all_draw': 5}),
    ]
    for name, effect in manipulation_cards:
        cards.append(EventCard(EventCardType.MANIPULATION, name, effect))
    
    # 🔥 v1.18: UTILITY CARDS - Only implemented cards included
    # Removed 18 unimplemented cards that always failed (Double Time, Random Luck, Choose Your Destiny, etc.)
    utility_cards = [
        ("Strategic Planning", {'draw_events': 3}),
        ("Deep Reserves", {'draw_events': 5, 'discard_events': 2}),
        ("Intelligence", {'look_top_events': 5, 'take': 2}),
        ("Trade In", {'discard_hand': True, 'draw_events': 'hand_size + 2'}),
        ("Maximum Hand", {'draw_to': 8}),
        ("Foresight", {'look_all_opponent_hands': True, 'draw_events': 2}),
        ("Time Warp", {'extra_turn': True}),
    ]
    for name, effect in utility_cards:
        cards.append(EventCard(EventCardType.UTILITY, name, effect))
    
    # v1.12 ATTACK-FOCUSED EVENT CARDS (GA optimizes composition!)
    # Attack Rewards (30% of new cards)
    for _ in range(config.battle_frenzy_count):
        cards.append(EventCard(
            EventCardType.BATTLE_FRENZY,
            "Battle Frenzy",
            {'effect': 'no_attacker_casualties', 'cost_influence': 2, 'duration': 'next_attack'}
        ))
    
    for _ in range(config.raiding_party_count):
        cards.append(EventCard(
            EventCardType.RAIDING_PARTY,
            "Raiding Party",
            {'effect': 'attack_and_gain_troops', 'troops_gained': 5, 'cost_influence': 1}
        ))
    
    for _ in range(config.spoils_of_war_count):
        cards.append(EventCard(
            EventCardType.SPOILS_OF_WAR,
            "Spoils of War",
            {'effect': 'passive_after_any_attack', 'draw_events': 2, 'gain_influence': 3, 'cost_cards': 0}
        ))
    
    # Casualty Reduction (20% of new cards)
    for _ in range(config.tactical_retreat_count):
        cards.append(EventCard(
            EventCardType.TACTICAL_RETREAT,
            "Tactical Retreat",
            {'effect': 'halve_attacker_casualties', 'multiplier': 0.5, 'cost_influence': 1, 'duration': 'this_turn'}
        ))
    
    for _ in range(config.reinforcements_count):
        cards.append(EventCard(
            EventCardType.REINFORCEMENTS,
            "Reinforcements",
            {'effect': 'regain_casualties', 'cost_influence': 2, 'timing': 'after_attack'}
        ))
    
    for _ in range(config.fortified_position_count):
        cards.append(EventCard(
            EventCardType.FORTIFIED_POSITION,
            "Fortified Position",
            {'effect': 'no_defender_casualties', 'cost_influence': 2, 'duration': 'when_defending'}
        ))
    
    # Combo/Chain (25% of new cards)
    for _ in range(config.momentum_card_count):
        cards.append(EventCard(
            EventCardType.MOMENTUM,
            "Momentum",
            {'effect': 'stacking_casualty_reduction', 'reduction_per_attack': 1, 'cost_influence': 1, 'stacks': True}
        ))
    
    for _ in range(config.blitzkrieg_count):
        cards.append(EventCard(
            EventCardType.BLITZKRIEG,
            "Blitzkrieg",
            {'effect': 'attack_twice', 'cost_influence': 2, 'timing': 'immediate'}
        ))

    # 🔥 v1.15: Raze - Press attack after tower destruction
    for _ in range(config.raze_count):
        cards.append(EventCard(
            EventCardType.RAZE,
            "Raze",
            {'effect': 'attack_after_tower', 'cost_influence': 3, 'timing': 'immediate'}
        ))

    # 🔥 v1.15: Tower Damage Shield Cards
    for _ in range(config.siege_equipment_count):
        cards.append(EventCard(
            EventCardType.SIEGE_EQUIPMENT,
            "Siege Equipment",
            {'effect': 'nullify_tower_damage', 'cost_influence': 2, 'duration': 'next_attack'}
        ))

    for _ in range(config.protective_wards_count):
        cards.append(EventCard(
            EventCardType.PROTECTIVE_WARDS,
            "Protective Wards",
            {'effect': 'reduce_tower_damage_50', 'cost_influence': 1, 'duration': 'next_attack'}
        ))

    for _ in range(config.vanguard_formation_count):
        cards.append(EventCard(
            EventCardType.VANGUARD_FORMATION,
            "Vanguard Formation",
            {'effect': 'first_attack_no_tower', 'cost_influence': 1, 'duration': 'this_turn'}
        ))

    for _ in range(config.chain_assault_count):
        cards.append(EventCard(
            EventCardType.CHAIN_ASSAULT,
            "Chain Assault",
            {'effect': 'redraw_on_tower_destroy', 'cost_influence': 1, 'timing': 'after_attack'}
        ))
    
    # Economy (20% of new cards)
    for _ in range(config.plunder_count):
        cards.append(EventCard(
            EventCardType.PLUNDER,
            "Plunder",
            {'effect': 'tower_destroy_bonus', 'gain_influence': 3, 'draw_events': 1, 'cost_cards': 0}
        ))
    
    for _ in range(config.war_economy_count):
        cards.append(EventCard(
            EventCardType.WAR_ECONOMY,
            "War Economy",
            {'effect': 'gain_influence_per_attack', 'influence_per_attack': 1, 'cost_influence': 1, 'duration': 'this_turn'}
        ))
    
    for _ in range(config.conscription_count):
        cards.append(EventCard(
            EventCardType.CONSCRIPTION,
            "Conscription",
            {'effect': 'buy_troops_with_influence', 'cost_influence': 4, 'troops_gained': 6}
        ))

    # 🔥 v1.17: CLAIM_ARMY removed - claiming now via Standard Contract or Captain draws

    # Wild Cards (5% of new cards)
    for _ in range(config.guerrilla_tactics_count):
        cards.append(EventCard(
            EventCardType.GUERRILLA_TACTICS,
            "Guerrilla Tactics",
            {'effect': 'cap_casualties', 'max_casualties': 5, 'cost_influence': 1, 'duration': 'this_turn'}
        ))
    
    for _ in range(config.scorched_earth_count):
        cards.append(EventCard(
            EventCardType.SCORCHED_EARTH,
            "Scorched Earth",
            {'effect': 'destroy_tower_gain_troops', 'cost_tower': 1, 'troops_gained': 10}
        ))
    
    for _ in range(config.reverse_turn_order_count):
        cards.append(EventCard(
            EventCardType.REVERSE_TURN_ORDER,
            "Chaos Reversal",
            {'effect': 'reverse_play_order', 'cost_influence': 2}
        ))

    for _ in range(config.pyrrhic_victory_count):
        cards.append(EventCard(
            EventCardType.PYRRHIC_VICTORY,
            "Pyrrhic Victory",
            {'effect': 'auto_win_lose_all', 'cost_influence': 3, 'auto_win': True, 'lose_all_troops': True}
        ))
    
    # 🔥 v1.13: BYPASS ATTACKS (Hearthstone-style: skip army combat, hit towers directly)
    if config.enable_bypass_attacks:
        # Add 5 Siege Attacks (basic bypass)
        for _ in range(5):
            cards.append(EventCard(
                EventCardType.SIEGE_ATTACK,
                "Siege Attack",
                {'effect': 'bypass_attack', 'cost_influence': 2, 'bypass_damage': 'config.bypass_damage_amount'}
            ))
        
        # Add 3 Artillery Strikes (2× bypass damage)
        for _ in range(3):
            cards.append(EventCard(
                EventCardType.ARTILLERY_STRIKE,
                "Artillery Strike",
                {'effect': 'bypass_attack', 'cost_influence': 3, 'bypass_damage': 'config.bypass_damage_amount * 2'}
            ))
    
    random.shuffle(cards)
    return cards

def create_leader_playbook(config: GameConfig) -> Dict[LeaderType, List[Leader]]:
    """Create the Leader Playbook (leaders available via contracts)"""
    playbook = {
        LeaderType.CAPTAIN: [],
        LeaderType.MAGE: [],
        LeaderType.COMMANDER: []
    }
    
    # Captains (40 epic leaders from v1.16 with unique abilities)
    playbook[LeaderType.CAPTAIN].extend([
        Leader(LeaderType.CAPTAIN, "Marcus the Swift", attack_bonus=1, unit_value=1,
               ability_id="first_strike", ability_type="passive", ability_cost=0,
               ability_description="+2 attack this combat"),
        Leader(LeaderType.CAPTAIN, "Helena Shadowstep", attack_bonus=1, unit_value=1,
               ability_id="blink", ability_type="triggered", ability_cost=0,
               ability_description="When this army would take casualties, 50% chance to take 0 instead"),
        Leader(LeaderType.CAPTAIN, "Brutus Vanguard", attack_bonus=1, unit_value=1,
               ability_id="rally_cry", ability_type="activated", ability_cost=1,
               ability_description="All your armies gain +1 strength this round"),
        Leader(LeaderType.CAPTAIN, "Quintus Scout", attack_bonus=1, unit_value=1,
               ability_id="reconnaissance", ability_type="activated", ability_cost=1,
               ability_description="Look at 1 card from opponent's hand"),
        Leader(LeaderType.CAPTAIN, "Aria the Raider", attack_bonus=1, unit_value=1,
               ability_id="pillage", ability_type="triggered", ability_cost=0,
               ability_description="Gain +1 influence on successful tower damage"),
        Leader(LeaderType.CAPTAIN, "Maximus Outrider", attack_bonus=1, unit_value=1,
               ability_id="flank", ability_type="triggered", ability_cost=0,
               ability_description="Remove 1 troop from defending army before combat"),
        Leader(LeaderType.CAPTAIN, "Titus Pathfinder", attack_bonus=1, unit_value=1,
               ability_id="terrain_master", ability_type="triggered", ability_cost=0,
               ability_description="Gather 1 extra troop when recruiting"),
        Leader(LeaderType.CAPTAIN, "Cassia Skirmisher", attack_bonus=1, unit_value=1,
               ability_id="hit_and_run", ability_type="triggered", ability_cost=0,
               ability_description="After attacking, this army cannot be attacked this round"),
        Leader(LeaderType.CAPTAIN, "Lucius Ghost", attack_bonus=1, unit_value=1,
               ability_id="ambush", ability_type="passive", ability_cost=0,
               ability_description="+2 attack if opponent has no leader"),
        Leader(LeaderType.CAPTAIN, "Octavia Nightblade", attack_bonus=1, unit_value=1,
               ability_id="assassinate", ability_type="activated", ability_cost=1,
               ability_description="Deal 1 damage to enemy leader HP"),
        Leader(LeaderType.CAPTAIN, "Ajax the Brave", attack_bonus=1, unit_value=1,
               ability_id="fearless", ability_type="passive", ability_cost=0,
               ability_description="Cannot be killed by leader abilities"),
        Leader(LeaderType.CAPTAIN, "Ragnar Bloodaxe", attack_bonus=1, unit_value=1,
               ability_id="berserker_rage", ability_type="passive", ability_cost=0,
               ability_description="+1 attack for each troop lost this game"),
        Leader(LeaderType.CAPTAIN, "Spartacus Ironclad", attack_bonus=1, unit_value=1,
               ability_id="unbreakable", ability_type="passive", ability_cost=0,
               ability_description="This army takes -2 damage (minimum 1)"),
        Leader(LeaderType.CAPTAIN, "Achilles Champion", attack_bonus=1, unit_value=1,
               ability_id="legendary_duel", ability_type="activated", ability_cost=2,
               ability_description="Double your attack and defense this combat"),
        Leader(LeaderType.CAPTAIN, "Fenrir Warhound", attack_bonus=1, unit_value=1,
               ability_id="pursuit", ability_type="triggered", ability_cost=0,
               ability_description="Can attack the same opponent twice per turn"),
        Leader(LeaderType.CAPTAIN, "Hector Dreadnought", attack_bonus=1, unit_value=1,
               ability_id="overwhelming_force", ability_type="passive", ability_cost=0,
               ability_description="+3 attack, -1 defense"),
        Leader(LeaderType.CAPTAIN, "Theron Siegemaster", attack_bonus=1, unit_value=1,
               ability_id="ram", ability_type="passive", ability_cost=0,
               ability_description="Deal +2 damage to towers"),
        Leader(LeaderType.CAPTAIN, "Xena Ravager", attack_bonus=1, unit_value=1,
               ability_id="devastate", ability_type="triggered", ability_cost=0,
               ability_description="Destroy 1 troop in opposing army before combat"),
        Leader(LeaderType.CAPTAIN, "Leonidas Crimsonfang", attack_bonus=1, unit_value=1,
               ability_id="last_stand", ability_type="passive", ability_cost=0,
               ability_description="+2 attack when you have only 1 tower"),
        Leader(LeaderType.CAPTAIN, "Thor Unyielding", attack_bonus=1, unit_value=1,
               ability_id="immovable", ability_type="passive", ability_cost=0,
               ability_description="Cannot be targeted by enemy abilities"),
        Leader(LeaderType.CAPTAIN, "Sun Tzu the Cunning", attack_bonus=1, unit_value=1,
               ability_id="art_of_war", ability_type="triggered", ability_cost=0,
               ability_description="Draw 1 card after combat"),
        Leader(LeaderType.CAPTAIN, "Alexander Strategos", attack_bonus=1, unit_value=1,
               ability_id="conqueror", ability_type="triggered", ability_cost=0,
               ability_description="Gain +1 influence per tower destroyed"),
        Leader(LeaderType.CAPTAIN, "Hannibal Deceptor", attack_bonus=1, unit_value=1,
               ability_id="feint", ability_type="activated", ability_cost=1,
               ability_description="Swap your attack and defense values"),
        Leader(LeaderType.CAPTAIN, "Scipio Ambusher", attack_bonus=1, unit_value=1,
               ability_id="trap", ability_type="triggered", ability_cost=0,
               ability_description="Deal 2 damage to attacker when you're attacked"),
        Leader(LeaderType.CAPTAIN, "Caesar Elite", attack_bonus=1, unit_value=1,
               ability_id="divide_and_conquer", ability_type="activated", ability_cost=2,
               ability_description="Reduce enemy army to half strength (rounded down)"),
        Leader(LeaderType.CAPTAIN, "Cyrus Veteran", attack_bonus=1, unit_value=1,
               ability_id="battle_hardened", ability_type="passive", ability_cost=0,
               ability_description="+1 attack, +1 defense (passive)"),
        Leader(LeaderType.CAPTAIN, "Odysseus Bold", attack_bonus=1, unit_value=1,
               ability_id="gambit", ability_type="activated", ability_cost=1,
               ability_description="Sacrifice 2 troops to gain +4 attack"),
        Leader(LeaderType.CAPTAIN, "Boudica Supreme", attack_bonus=1, unit_value=1,
               ability_id="perfect_execution", ability_type="triggered", ability_cost=0,
               ability_description="Take no casualties when you win combat"),
        Leader(LeaderType.CAPTAIN, "Vercingetorix Trickster", attack_bonus=1, unit_value=1,
               ability_id="misdirect", ability_type="activated", ability_cost=1,
               ability_description="Redirect incoming attack to adjacent player (multiplayer only)"),
        Leader(LeaderType.CAPTAIN, "Pompey Warlord", attack_bonus=1, unit_value=1,
               ability_id="command", ability_type="activated", ability_cost=3,
               ability_description="Take control of opponent's army for one attack"),
        Leader(LeaderType.CAPTAIN, "Siegfried Stormborn", attack_bonus=1, unit_value=1,
               ability_id="call_lightning", ability_type="activated", ability_cost=2,
               ability_description="Deal 3 damage to any army"),
        Leader(LeaderType.CAPTAIN, "Beowulf Dragonslayer", attack_bonus=1, unit_value=1,
               ability_id="slay_monster", ability_type="activated", ability_cost=2,
               ability_description="Destroy target commander"),
        Leader(LeaderType.CAPTAIN, "Perseus Phoenix", attack_bonus=1, unit_value=1,
               ability_id="rebirth", ability_type="triggered", ability_cost=0,
               ability_description="When destroyed, return to your available leaders (can re-assign)"),
        Leader(LeaderType.CAPTAIN, "Roland Silvertongue", attack_bonus=1, unit_value=1,
               ability_id="inspire", ability_type="activated", ability_cost=1,
               ability_description="All your armies get +1 attack this round"),
        Leader(LeaderType.CAPTAIN, "Gilgamesh Immortal", attack_bonus=1, unit_value=1,
               ability_id="eternal", ability_type="passive", ability_cost=0,
               ability_description="This leader's HP cannot drop below 1"),
        Leader(LeaderType.CAPTAIN, "Hercules Lionheart", attack_bonus=1, unit_value=1,
               ability_id="twelve_labors", ability_type="passive", ability_cost=0,
               ability_description="+1 to all stats for each eliminated player"),
        Leader(LeaderType.CAPTAIN, "Samson Steelfist", attack_bonus=1, unit_value=1,
               ability_id="mighty_blow", ability_type="passive", ability_cost=0,
               ability_description="Deal double damage to towers"),
        Leader(LeaderType.CAPTAIN, "Rostam Warhawk", attack_bonus=1, unit_value=1,
               ability_id="dive_strike", ability_type="activated", ability_cost=1,
               ability_description="+3 attack, lose 1 troop from this army"),
        Leader(LeaderType.CAPTAIN, "Miyamoto Blademaster", attack_bonus=1, unit_value=1,
               ability_id="iaijutsu", ability_type="activated", ability_cost=2,
               ability_description="If you have 5+ cards in hand, destroy opposing army"),
        Leader(LeaderType.CAPTAIN, "Vlad Shadowbane", attack_bonus=1, unit_value=1,
               ability_id="impale", ability_type="activated", ability_cost=2,
               ability_description="Destroy 3 troops in target army"),
    ])
    
    # Mages (40 epic leaders from v1.16 with unique abilities)
    playbook[LeaderType.MAGE].extend([
        Leader(LeaderType.MAGE, "Pyros Flamecaller", attack_bonus=2, unit_value=1,
               ability_id="fireball", ability_type="activated", ability_cost=2,
               ability_description="Deal 4 damage to target army"),
        Leader(LeaderType.MAGE, "Ember the Scorched", attack_bonus=2, unit_value=1,
               ability_id="ignite", ability_type="activated", ability_cost=2,
               ability_description="Target army takes 1 damage per turn (ongoing)"),
        Leader(LeaderType.MAGE, "Vulcan Infernus", attack_bonus=2, unit_value=1,
               ability_id="volcanic_eruption", ability_type="activated", ability_cost=3,
               ability_description="Deal 2 damage to all armies"),
        Leader(LeaderType.MAGE, "Ignis Firelord", attack_bonus=2, unit_value=1,
               ability_id="phoenix_fire", ability_type="activated", ability_cost=2,
               ability_description="Claim 3 troops from unclaimed pool"),
        Leader(LeaderType.MAGE, "Seraphina Ashbringer", attack_bonus=2, unit_value=1,
               ability_id="cremation", ability_type="activated", ability_cost=1,
               ability_description="Sacrifice troops for cards (1 troop = 1 card)"),
        Leader(LeaderType.MAGE, "Prometheus Eternal Flame", attack_bonus=2, unit_value=1,
               ability_id="undying_fire", ability_type="passive", ability_cost=0,
               ability_description="All your attacks deal +1 damage"),
        Leader(LeaderType.MAGE, "Helios Sunforge", attack_bonus=2, unit_value=1,
               ability_id="solar_flare", ability_type="activated", ability_cost=0,
               ability_description="Spend X influence, deal X damage to any target"),
        Leader(LeaderType.MAGE, "Agni Burnmaster", attack_bonus=2, unit_value=1,
               ability_id="scorch_earth", ability_type="activated", ability_cost=2,
               ability_description="Target opponent discards 1 card"),
        Leader(LeaderType.MAGE, "Glacius Frostborn", attack_bonus=2, unit_value=1,
               ability_id="freeze", ability_type="activated", ability_cost=2,
               ability_description="Target army cannot attack next turn"),
        Leader(LeaderType.MAGE, "Skadi Winter Queen", attack_bonus=2, unit_value=1,
               ability_id="blizzard", ability_type="activated", ability_cost=3,
               ability_description="All armies lose 1 strength"),
        Leader(LeaderType.MAGE, "Boreas Icewind", attack_bonus=2, unit_value=1,
               ability_id="shatter", ability_type="activated", ability_cost=2,
               ability_description="Destroy all 1-strength troops on board"),
        Leader(LeaderType.MAGE, "Elsa Crystal Heart", attack_bonus=2, unit_value=1,
               ability_id="ice_wall", ability_type="activated", ability_cost=1,
               ability_description="+3 defense this turn"),
        Leader(LeaderType.MAGE, "Nix Permafrost", attack_bonus=2, unit_value=1,
               ability_id="deep_freeze", ability_type="activated", ability_cost=5,
               ability_description="Remove target leader from game permanently"),
        Leader(LeaderType.MAGE, "Ymir Glacier", attack_bonus=2, unit_value=1,
               ability_id="icebound", ability_type="activated", ability_cost=2,
               ability_description="Enemy event cards cost +1 influence this turn"),
        Leader(LeaderType.MAGE, "Khione Snowdrift", attack_bonus=2, unit_value=1,
               ability_id="avalanche", ability_type="activated", ability_cost=2,
               ability_description="Deal damage equal to your troop count"),
        Leader(LeaderType.MAGE, "Ullr Frostbite", attack_bonus=2, unit_value=1,
               ability_id="numb", ability_type="activated", ability_cost=2,
               ability_description="Target leader cannot use ability this turn"),
        Leader(LeaderType.MAGE, "Zeus Stormfather", attack_bonus=2, unit_value=1,
               ability_id="chain_lightning", ability_type="activated", ability_cost=3,
               ability_description="Deal 2 damage to 3 different targets"),
        Leader(LeaderType.MAGE, "Thor Thundergod", attack_bonus=2, unit_value=1,
               ability_id="mjolnir", ability_type="activated", ability_cost=5,
               ability_description="Destroy target tower"),
        Leader(LeaderType.MAGE, "Raijin Tempest", attack_bonus=2, unit_value=1,
               ability_id="thunder_clap", ability_type="activated", ability_cost=4,
               ability_description="All enemy leaders cannot activate abilities this turn"),
        Leader(LeaderType.MAGE, "Perun Lightning Lord", attack_bonus=2, unit_value=1,
               ability_id="static_shock", ability_type="passive", ability_cost=0,
               ability_description="Deal 1 damage to attacker when attacked"),
        Leader(LeaderType.MAGE, "Aeolus Windcaller", attack_bonus=2, unit_value=1,
               ability_id="tornado", ability_type="activated", ability_cost=3,
               ability_description="Return all troops from one army to unclaimed pool"),
        Leader(LeaderType.MAGE, "Enlil Sky Sovereign", attack_bonus=2, unit_value=1,
               ability_id="hurricane", ability_type="activated", ability_cost=4,
               ability_description="Redistribute all troops randomly"),
        Leader(LeaderType.MAGE, "Indra Monsoon", attack_bonus=2, unit_value=1,
               ability_id="deluge", ability_type="activated", ability_cost=3,
               ability_description="Deal 1 damage to each enemy tower"),
        Leader(LeaderType.MAGE, "Taranis Stormcrash", attack_bonus=2, unit_value=1,
               ability_id="overload", ability_type="activated", ability_cost=2,
               ability_description="Deal damage equal to cards in hand"),
        Leader(LeaderType.MAGE, "Nyx Shadowborn", attack_bonus=2, unit_value=1,
               ability_id="shadowmeld", ability_type="activated", ability_cost=2,
               ability_description="Cannot be attacked for 1 turn"),
        Leader(LeaderType.MAGE, "Erebus Voidwalker", attack_bonus=2, unit_value=1,
               ability_id="banish", ability_type="activated", ability_cost=4,
               ability_description="Remove target army from game"),
        Leader(LeaderType.MAGE, "Morrigan Deathsinger", attack_bonus=2, unit_value=1,
               ability_id="soul_drain", ability_type="activated", ability_cost=3,
               ability_description="Steal 2 troops from opponent"),
        Leader(LeaderType.MAGE, "Hades Gravekeeper", attack_bonus=2, unit_value=1,
               ability_id="raise_dead", ability_type="activated", ability_cost=3,
               ability_description="Claim 5 troops from unclaimed pool"),
        Leader(LeaderType.MAGE, "Anubis Reaper", attack_bonus=2, unit_value=1,
               ability_id="harvest_souls", ability_type="passive", ability_cost=0,
               ability_description="Gain +1 troop per enemy troop killed this turn"),
        Leader(LeaderType.MAGE, "Charon Bonecaller", attack_bonus=2, unit_value=1,
               ability_id="ferry_souls", ability_type="activated", ability_cost=3,
               ability_description="Swap two armies (yours and opponent's)"),
        Leader(LeaderType.MAGE, "Thanatos Gravewarden", attack_bonus=2, unit_value=1,
               ability_id="mark_of_death", ability_type="activated", ability_cost=2,
               ability_description="Target army takes double damage this turn"),
        Leader(LeaderType.MAGE, "Hecate Dark Priestess", attack_bonus=2, unit_value=1,
               ability_id="hex", ability_type="activated", ability_cost=2,
               ability_description="Target opponent cannot play event cards next turn"),
        Leader(LeaderType.MAGE, "Merlin Archmage", attack_bonus=2, unit_value=1,
               ability_id="arcane_blast", ability_type="activated", ability_cost=2,
               ability_description="Deal damage equal to event cards played this turn"),
        Leader(LeaderType.MAGE, "Gandalf Starweaver", attack_bonus=2, unit_value=1,
               ability_id="cosmic_ray", ability_type="activated", ability_cost=0,
               ability_description="Destroy 1 tower (cost: all influence)"),
        Leader(LeaderType.MAGE, "Morgan Oracle", attack_bonus=2, unit_value=1,
               ability_id="scry", ability_type="activated", ability_cost=1,
               ability_description="Look at top 3 cards, rearrange them"),
        Leader(LeaderType.MAGE, "Circe Enchantress", attack_bonus=2, unit_value=1,
               ability_id="polymorph", ability_type="activated", ability_cost=4,
               ability_description="Change all troops to 1-strength"),
        Leader(LeaderType.MAGE, "Thoth Runemaster", attack_bonus=2, unit_value=1,
               ability_id="ancient_runes", ability_type="activated", ability_cost=2,
               ability_description="Double influence income this turn"),
        Leader(LeaderType.MAGE, "Athena Warsage", attack_bonus=2, unit_value=1,
               ability_id="tactical_insight", ability_type="activated", ability_cost=1,
               ability_description="Look at opponent's hand"),
        Leader(LeaderType.MAGE, "Odin Allfather", attack_bonus=2, unit_value=1,
               ability_id="gungnir", ability_type="activated", ability_cost=3,
               ability_description="Your next attack ignores blocking (defender must block)"),
        Leader(LeaderType.MAGE, "Ra Sunking", attack_bonus=2, unit_value=1,
               ability_id="divine_judgement", ability_type="activated", ability_cost=8,
               ability_description="Eliminate player with 1 tower"),
    ])
    
    # Commanders (40 epic leaders from v1.16 with unique abilities)
    playbook[LeaderType.COMMANDER].extend([
        Leader(LeaderType.COMMANDER, "Julius Caesar", attack_bonus=3, unit_value=2,
               ability_id="veni_vidi_vici", ability_type="triggered", ability_cost=0,
               ability_description="If you destroy a tower this turn, gain +3 influence"),
        Leader(LeaderType.COMMANDER, "Augustus Imperator", attack_bonus=3, unit_value=2,
               ability_id="pax_romana", ability_type="activated", ability_cost=2,
               ability_description="Gain 3 influence, draw 2 cards"),
        Leader(LeaderType.COMMANDER, "Trajan Optimus", attack_bonus=3, unit_value=2,
               ability_id="legion_march", ability_type="activated", ability_cost=3,
               ability_description="Deploy 2 armies this turn"),
        Leader(LeaderType.COMMANDER, "Marcus Aurelius", attack_bonus=3, unit_value=2,
               ability_id="stoic_resolve", ability_type="activated", ability_cost=2,
               ability_description="Immune to enemy event cards this turn"),
        Leader(LeaderType.COMMANDER, "Constantine Great", attack_bonus=3, unit_value=2,
               ability_id="divine_mandate", ability_type="activated", ability_cost=2,
               ability_description="All leader contracts cost -1 influence this turn"),
        Leader(LeaderType.COMMANDER, "Hadrian Fortifier", attack_bonus=3, unit_value=2,
               ability_id="wall_builder", ability_type="activated", ability_cost=4,
               ability_description="All your towers gain +2 HP permanently"),
        Leader(LeaderType.COMMANDER, "Nero Tyrant", attack_bonus=3, unit_value=2,
               ability_id="great_fire", ability_type="activated", ability_cost=0,
               ability_description="Destroy 1 of your towers, gain 5 influence"),
        Leader(LeaderType.COMMANDER, "Caligula Mad", attack_bonus=3, unit_value=2,
               ability_id="chaos_reign", ability_type="activated", ability_cost=2,
               ability_description="Reverse turn order for 1 round"),
        Leader(LeaderType.COMMANDER, "Leonidas Spartan", attack_bonus=3, unit_value=2,
               ability_id="300_warriors", ability_type="activated", ability_cost=4,
               ability_description="Spawn 5 troops (3-strength each)"),
        Leader(LeaderType.COMMANDER, "Pericles Strategos", attack_bonus=3, unit_value=2,
               ability_id="golden_age", ability_type="passive", ability_cost=0,
               ability_description="Income doubled this round"),
        Leader(LeaderType.COMMANDER, "Themistocles Admiral", attack_bonus=3, unit_value=2,
               ability_id="naval_superiority", ability_type="activated", ability_cost=2,
               ability_description="Negate 1 attack this turn"),
        Leader(LeaderType.COMMANDER, "Alcibiades Tactician", attack_bonus=3, unit_value=2,
               ability_id="betrayal", ability_type="activated", ability_cost=5,
               ability_description="Steal 1 leader from opponent"),
        Leader(LeaderType.COMMANDER, "Philip Macedon", attack_bonus=3, unit_value=2,
               ability_id="phalanx", ability_type="activated", ability_cost=2,
               ability_description="All your captains get +2 defense this turn"),
        Leader(LeaderType.COMMANDER, "Pyrrhus Warlord", attack_bonus=3, unit_value=2,
               ability_id="costly_victory", ability_type="activated", ability_cost=3,
               ability_description="Deal 10 damage to target, destroy your army"),
        Leader(LeaderType.COMMANDER, "Epaminondas", attack_bonus=3, unit_value=2,
               ability_id="oblique_order", ability_type="activated", ability_cost=2,
               ability_description="Rearrange combat resolution order"),
        Leader(LeaderType.COMMANDER, "Agesilaus", attack_bonus=3, unit_value=2,
               ability_id="laconic_wit", ability_type="activated", ability_cost=2,
               ability_description="Draw cards equal to towers you control"),
        Leader(LeaderType.COMMANDER, "Genghis Khan", attack_bonus=3, unit_value=2,
               ability_id="mongol_horde", ability_type="passive", ability_cost=0,
               ability_description="+2 attack per army you control"),
        Leader(LeaderType.COMMANDER, "Attila Hun", attack_bonus=3, unit_value=2,
               ability_id="scourge_of_god", ability_type="activated", ability_cost=4,
               ability_description="Deal 5 damage to any target"),
        Leader(LeaderType.COMMANDER, "Tamerlane", attack_bonus=3, unit_value=2,
               ability_id="iron_conqueror", ability_type="activated", ability_cost=3,
               ability_description="Your towers cannot be damaged this turn"),
        Leader(LeaderType.COMMANDER, "Saladin", attack_bonus=3, unit_value=2,
               ability_id="jihad", ability_type="activated", ability_cost=2,
               ability_description="All your armies gain +2 attack vs towers this turn"),
        Leader(LeaderType.COMMANDER, "Richard Lionheart", attack_bonus=3, unit_value=2,
               ability_id="crusader_king", ability_type="passive", ability_cost=0,
               ability_description="Gain 1 influence per attack made this turn"),
        Leader(LeaderType.COMMANDER, "Charlemagne", attack_bonus=3, unit_value=2,
               ability_id="holy_roman_empire", ability_type="activated", ability_cost=3,
               ability_description="Contract 2 leaders for free"),
        Leader(LeaderType.COMMANDER, "William Conqueror", attack_bonus=3, unit_value=2,
               ability_id="norman_invasion", ability_type="activated", ability_cost=4,
               ability_description="Deploy 2 commanders this turn"),
        Leader(LeaderType.COMMANDER, "Suleiman Magnificent", attack_bonus=3, unit_value=2,
               ability_id="ottoman_power", ability_type="activated", ability_cost=3,
               ability_description="+3 to all your stats this turn"),
        Leader(LeaderType.COMMANDER, "Hannibal Barca", attack_bonus=3, unit_value=2,
               ability_id="cannae", ability_type="activated", ability_cost=6,
               ability_description="Destroy all enemy armies"),
        Leader(LeaderType.COMMANDER, "Belisarius", attack_bonus=3, unit_value=2,
               ability_id="byzantine_strategy", ability_type="activated", ability_cost=2,
               ability_description="Redirect 1 attack to different player"),
        Leader(LeaderType.COMMANDER, "Khalid Sword of Allah", attack_bonus=3, unit_value=2,
               ability_id="undefeated", ability_type="passive", ability_cost=0,
               ability_description="Win all ties in combat"),
        Leader(LeaderType.COMMANDER, "Subutai", attack_bonus=3, unit_value=2,
               ability_id="master_tactician", ability_type="activated", ability_cost=2,
               ability_description="Play any event card from discard pile"),
        Leader(LeaderType.COMMANDER, "Scipio Africanus", attack_bonus=3, unit_value=2,
               ability_id="zama", ability_type="passive", ability_cost=0,
               ability_description="Counter-attack with full strength when attacked"),
        Leader(LeaderType.COMMANDER, "Yi Sun-sin", attack_bonus=3, unit_value=2,
               ability_id="turtle_ships", ability_type="activated", ability_cost=3,
               ability_description="Towers cannot be damaged this turn"),
        Leader(LeaderType.COMMANDER, "Boudica Iceni", attack_bonus=3, unit_value=2,
               ability_id="celtic_fury", ability_type="passive", ability_cost=0,
               ability_description="+1 attack per tower you've lost"),
        Leader(LeaderType.COMMANDER, "Vercingetorix Gaul", attack_bonus=3, unit_value=2,
               ability_id="last_stand_defense", ability_type="passive", ability_cost=0,
               ability_description="When you have 1 tower, all your armies have +3 defense"),
        Leader(LeaderType.COMMANDER, "Gilgamesh Uruk", attack_bonus=3, unit_value=2,
               ability_id="epic_of_kings", ability_type="activated", ability_cost=3,
               ability_description="Draw 5 cards"),
        Leader(LeaderType.COMMANDER, "Hammurabi Lawgiver", attack_bonus=3, unit_value=2,
               ability_id="code", ability_type="activated", ability_cost=4,
               ability_description="Target opponent discards hand, draws 3"),
        Leader(LeaderType.COMMANDER, "Cyrus Great", attack_bonus=3, unit_value=2,
               ability_id="persian_empire", ability_type="activated", ability_cost=4,
               ability_description="Take control of all unclaimed troops"),
        Leader(LeaderType.COMMANDER, "Ramses Pharaoh", attack_bonus=3, unit_value=2,
               ability_id="plague", ability_type="activated", ability_cost=4,
               ability_description="Reduce all enemy troops by 1 strength"),
        Leader(LeaderType.COMMANDER, "Darius", attack_bonus=3, unit_value=2,
               ability_id="immortals", ability_type="passive", ability_cost=0,
               ability_description="Your troops cannot be reduced below 1 strength"),
        Leader(LeaderType.COMMANDER, "Nebuchadnezzar", attack_bonus=3, unit_value=2,
               ability_id="hanging_gardens", ability_type="activated", ability_cost=2,
               ability_description="Gain influence equal to towers controlled"),
        Leader(LeaderType.COMMANDER, "Alexander", attack_bonus=3, unit_value=2,
               ability_id="macedonian_phalanx", ability_type="activated", ability_cost=3,
               ability_description="All your armies gain +3 attack this turn"),
        Leader(LeaderType.COMMANDER, "Ashoka", attack_bonus=3, unit_value=2,
               ability_id="dharma", ability_type="activated", ability_cost=5,
               ability_description="End combat phase, all armies return to full strength"),
    ])
    
    return playbook

# =============================================================================
# LEADER ABILITY RESOLUTION SYSTEM (v1.16 Phase 5)
# =============================================================================

def resolve_leader_ability_passive(leader: Leader, context: dict, game_state: GameState) -> dict:
    """
    Resolve passive abilities (always active).

    Args:
        leader: The leader with the ability
        context: Dictionary containing:
            - phase: str (combat_start, combat_calc, tower_damage, etc.)
            - army: Army (the army with this leader)
            - opponent_army: Army (optional, opponent's army)
            - player: Player (the owning player)
            - opponent: Player (optional, the opponent player)
        game_state: Current game state

    Returns:
        Dictionary of modifications to apply:
            - attack_bonus: int (additional attack)
            - defense_bonus: int (additional defense)
            - damage_reduction: int (reduce incoming damage)
            - tower_damage_bonus: int (extra tower damage)
            - etc.
    """
    ability_id = leader.ability_id
    modifications = {
        'attack_bonus': 0,
        'defense_bonus': 0,
        'damage_reduction': 0,
        'tower_damage_bonus': 0,
        'damage_multiplier': 1.0
    }

    if not ability_id:
        return modifications

    phase = context.get('phase', '')
    army = context.get('army')
    opponent_army = context.get('opponent_army')
    player = context.get('player')
    opponent = context.get('opponent')

    # CAPTAIN PASSIVE ABILITIES
    if ability_id == "first_strike":  # Marcus the Swift
        modifications['attack_bonus'] = 2

    elif ability_id == "ambush":  # Lucius Ghost
        if opponent_army and not opponent_army.leader:
            modifications['attack_bonus'] = 2

    elif ability_id == "berserker_rage":  # Ragnar Bloodaxe
        if player:
            # Count troops lost (would need tracking in Player class)
            # For now, approximate based on starting deck size vs current
            modifications['attack_bonus'] = player.attacks_this_game // 3  # Rough approximation

    elif ability_id == "unbreakable":  # Spartacus Ironclad
        modifications['damage_reduction'] = 2

    elif ability_id == "overwhelming_force":  # Hector Dreadnought
        modifications['attack_bonus'] = 3
        modifications['defense_bonus'] = -1

    elif ability_id == "ram":  # Theron Siegemaster
        modifications['tower_damage_bonus'] = 2

    elif ability_id == "last_stand":  # Leonidas Crimsonfang
        if player and player.towers == 1:
            modifications['attack_bonus'] = 2

    elif ability_id == "battle_hardened":  # Cyrus Veteran
        modifications['attack_bonus'] = 1
        modifications['defense_bonus'] = 1

    elif ability_id == "mighty_blow":  # Samson Steelfist
        modifications['tower_damage_bonus'] = modifications.get('tower_damage_bonus', 0) * 2
        modifications['damage_multiplier'] = 2.0  # Double tower damage

    # MAGE PASSIVE ABILITIES
    elif ability_id == "undying_fire":  # Prometheus Eternal Flame
        modifications['attack_bonus'] = 1  # All attacks deal +1

    elif ability_id == "static_shock":  # Perun Lightning Lord
        # Handled in combat as counter-damage
        pass

    elif ability_id == "harvest_souls":  # Anubis Reaper
        # Handled post-combat to collect killed troops
        pass

    # COMMANDER PASSIVE ABILITIES
    elif ability_id == "golden_age":  # Pericles Strategos
        # Income doubled (handled in income phase)
        pass

    elif ability_id == "mongol_horde":  # Genghis Khan
        if player:
            modifications['attack_bonus'] = len(player.armies) * 2

    elif ability_id == "crusader_king":  # Richard Lionheart
        # Handled in attack phase (gain influence per attack)
        pass

    elif ability_id == "undefeated":  # Khalid Sword of Allah
        # Win ties (handled in combat resolution)
        pass

    elif ability_id == "zama":  # Scipio Africanus
        # Counter-attack (handled in combat resolution)
        pass

    elif ability_id == "celtic_fury":  # Boudica Iceni
        if player:
            towers_lost = 3 - player.towers
            modifications['attack_bonus'] = towers_lost

    elif ability_id == "last_stand_defense":  # Vercingetorix Gaul
        if player and player.towers == 1:
            modifications['defense_bonus'] = 3

    elif ability_id == "immortals":  # Darius
        # Troops can't go below 1 strength (handled in damage calculation)
        pass

    return modifications


def resolve_leader_ability_triggered(leader: Leader, trigger: str, context: dict,
                                     game_state: GameState, logger: GameLogger) -> dict:
    """
    Resolve triggered abilities (on specific events).

    Args:
        leader: The leader with the ability
        trigger: Trigger type (combat_start, combat_end, tower_destroyed, casualties, etc.)
        context: Dictionary with relevant game objects
        game_state: Current game state
        logger: Game logger for output

    Returns:
        Dictionary of effects applied
    """
    ability_id = leader.ability_id
    results = {'success': False, 'effect': ''}

    if not ability_id or leader.ability_type != "triggered":
        return results

    player = context.get('player')
    opponent = context.get('opponent')
    army = context.get('army')
    opponent_army = context.get('opponent_army')

    # TRIGGERED ABILITIES

    # Combat triggers
    if trigger == "casualties" and ability_id == "blink":  # Helena Shadowstep
        if random.random() < 0.5:
            results['success'] = True
            results['effect'] = "Blink activated! No casualties taken."
            results['negate_casualties'] = True
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Blink: Avoided all casualties!")

    elif trigger == "tower_damaged" and ability_id == "pillage":  # Aria the Raider
        if player:
            player.influence += 1
            results['success'] = True
            results['effect'] = "+1 influence from Pillage"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Pillage: +1 influence")

    elif trigger == "combat_start" and ability_id == "flank":  # Maximus Outrider
        if opponent_army and len(opponent_army.troops) > 0:
            opponent_army.troops.pop()
            results['success'] = True
            results['effect'] = "Removed 1 troop from defender"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Flank: Removed 1 defending troop")

    elif trigger == "gather_troops" and ability_id == "terrain_master":  # Titus Pathfinder
        results['success'] = True
        results['effect'] = "+1 extra troop when gathering"
        results['bonus_troops'] = 1

    elif trigger == "combat_end" and ability_id == "hit_and_run":  # Cassia Skirmisher
        if army and player:
            # Mark army as untargetable
            if not hasattr(player, 'untargetable_armies'):
                player.untargetable_armies = []
            player.untargetable_armies.append(army)
            results['success'] = True
            results['effect'] = "Army cannot be attacked this round"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Hit and Run: Army cannot be attacked")

    elif trigger == "combat_end" and ability_id == "art_of_war":  # Sun Tzu the Cunning
        if player and game_state.event_deck:
            player.draw_event_card(game_state.event_deck)
            results['success'] = True
            results['effect'] = "Drew 1 card"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Art of War: Drew 1 card")

    elif trigger == "tower_destroyed" and ability_id == "conqueror":  # Alexander Strategos
        if player:
            player.influence += 1
            results['success'] = True
            results['effect'] = "+1 influence per tower destroyed"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Conqueror: +1 influence")

    elif trigger == "combat_start" and ability_id == "trap":  # Scipio Ambusher (defender)
        # Deal 2 damage to attacker when attacked
        results['success'] = True
        results['effect'] = "Deal 2 damage to attacker"
        results['counter_damage'] = 2
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Trap: 2 damage to attacker")

    elif trigger == "combat_end" and ability_id == "perfect_execution":  # Boudica Supreme
        if context.get('combat_won'):
            results['success'] = True
            results['effect'] = "No casualties when winning"
            results['negate_casualties'] = True
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Perfect Execution: No casualties!")

    elif trigger == "leader_destroyed" and ability_id == "rebirth":  # Perseus Phoenix
        if player:
            player.leaders.append(leader)
            results['success'] = True
            results['effect'] = "Leader returned to available leaders"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Rebirth: Returned to leader pool!")

    elif trigger == "tower_destroyed" and ability_id == "veni_vidi_vici":  # Julius Caesar
        if player:
            player.influence += 3
            results['success'] = True
            results['effect'] = "+3 influence for destroying tower"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Veni Vidi Vici: +3 influence")

    elif trigger == "combat_start" and ability_id == "devastate":  # Xena Ravager
        if opponent_army and len(opponent_army.troops) > 0:
            opponent_army.troops.pop()
            results['success'] = True
            results['effect'] = "Destroyed 1 troop in opposing army"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Devastate: Destroyed 1 enemy troop")

    return results


def resolve_leader_ability_activated(leader: Leader, player: Player, context: dict,
                                     game_state: GameState, logger: GameLogger) -> dict:
    """
    Resolve activated abilities (player chooses to use, costs influence).

    Args:
        leader: The leader with the ability
        player: The player activating the ability
        context: Dictionary with targets and parameters
        game_state: Current game state
        logger: Game logger for output

    Returns:
        Dictionary with success status and effects
    """
    ability_id = leader.ability_id
    ability_cost = leader.ability_cost
    results = {'success': False, 'effect': '', 'cost': ability_cost}

    if not ability_id or leader.ability_type != "activated":
        return results

    # 🔥 v1.17 SPENDING LOCK: Check if player can afford (with spending lock)
    if player.influence < ability_cost:
        results['effect'] = f"Not enough influence (need {ability_cost}, have {player.influence})"
        return results

    if not player.can_spend_influence(ability_cost):
        results['effect'] = f"Cannot spend influence (would drop below minimum of 2)"
        return results

    # Pay the cost
    player.influence -= ability_cost

    target_player = context.get('target_player')
    target_army = context.get('target_army')

    # ACTIVATED ABILITIES (Simplified implementations - full logic would be more complex)

    # Direct damage abilities
    if ability_id == "fireball":  # Pyros Flamecaller
        if target_army:
            damage = min(4, len(target_army.troops))
            for _ in range(damage):
                if target_army.troops:
                    target_army.troops.pop()
            results['success'] = True
            results['effect'] = f"Dealt {damage} damage to army"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Fireball: {damage} damage!")

    elif ability_id == "call_lightning":  # Siegfried Stormborn
        if target_army:
            damage = min(3, len(target_army.troops))
            for _ in range(damage):
                if target_army.troops:
                    target_army.troops.pop()
            results['success'] = True
            results['effect'] = f"Dealt {damage} damage to army"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Call Lightning: {damage} damage!")

    elif ability_id == "chain_lightning":  # Zeus Stormfather
        # Deal 2 damage to 3 different targets (simplified)
        results['success'] = True
        results['effect'] = "Deal 2 damage to 3 targets"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Chain Lightning!")

    # Utility abilities
    elif ability_id == "rally_cry":  # Brutus Vanguard
        for army in player.armies:
            army.troops.append(1)  # Add 1 strength to each army
        results['success'] = True
        results['effect'] = f"All armies +1 strength"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Rally Cry: All armies +1 strength")

    elif ability_id == "inspire":  # Roland Silvertongue
        # All armies +1 attack this round (would need turn-based tracking)
        results['success'] = True
        results['effect'] = "All armies +1 attack this round"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Inspire: All armies +1 attack")

    elif ability_id == "pax_romana":  # Augustus Imperator
        player.influence += 3
        for _ in range(2):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        results['success'] = True
        results['effect'] = "+3 influence, draw 2 cards"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Pax Romana: +3 inf, +2 cards")

    elif ability_id == "epic_of_kings":  # Gilgamesh Uruk
        for _ in range(5):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        results['success'] = True
        results['effect'] = "Draw 5 cards"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Epic of Kings: Drew 5 cards!")

    # Board manipulation
    elif ability_id == "divide_and_conquer":  # Caesar Elite
        if target_army:
            original_size = len(target_army.troops)
            new_size = original_size // 2
            target_army.troops = target_army.troops[:new_size]
            results['success'] = True
            results['effect'] = f"Reduced army from {original_size} to {new_size} troops"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Divide and Conquer: Army halved!")

    elif ability_id == "freeze":  # Glacius Frostborn
        if target_army:
            # Mark army as frozen (can't attack next turn)
            results['success'] = True
            results['effect'] = "Army cannot attack next turn"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Freeze: Army frozen!")

    elif ability_id == "mjolnir":  # Thor Thundergod
        if target_player and target_player.towers > 0:
            target_player.towers -= 1
            results['success'] = True
            results['effect'] = "Destroyed 1 tower"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Mjolnir: Tower destroyed!")

    elif ability_id == "cannae":  # Hannibal Barca
        # Destroy all enemy armies
        destroyed = 0
        for p in game_state.players:
            if p != player:
                destroyed += len(p.armies)
                p.armies.clear()
        results['success'] = True
        results['effect'] = f"Destroyed {destroyed} enemy armies"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - Cannae: {destroyed} armies destroyed!")

    elif ability_id == "divine_judgement":  # Ra Sunking
        if target_player and target_player.towers == 1:
            target_player.towers = 0
            target_player.eliminated = True
            results['success'] = True
            results['effect'] = "Eliminated player with 1 tower"
            if logger:
                logger.write(f"  [ABILITY] {leader.name} - Divine Judgement: Player eliminated!")

    # More abilities can be added incrementally
    else:
        # Placeholder for unimplemented abilities
        results['success'] = True
        results['effect'] = f"{leader.ability_description} (not fully implemented yet)"
        if logger:
            logger.write(f"  [ABILITY] {leader.name} - {leader.ability_description}")

    return results


def get_leader_ability_passive_bonus(leader: Leader, phase: str, context: dict,
                                     game_state: GameState) -> dict:
    """
    Helper function to quickly get passive bonuses during combat calculation.

    Args:
        leader: The leader
        phase: Combat phase
        context: Context dictionary
        game_state: Game state

    Returns:
        Modifications dictionary
    """
    if not leader or leader.ability_type != "passive":
        return {'attack_bonus': 0, 'defense_bonus': 0, 'damage_reduction': 0,
                'tower_damage_bonus': 0, 'damage_multiplier': 1.0}

    context['phase'] = phase
    return resolve_leader_ability_passive(leader, context, game_state)


# =============================================================================
# EVENT CARD RESOLUTION
# =============================================================================

def can_contract_leader(player: Player, game_state: GameState) -> bool:
    """
    🔥 v1.16: Check if player can validly contract a leader

    Leader MUST be assigned immediately to:
    1. Unclaimed troops (from cards drawn this turn) - MOST COMMON
    2. Leaderless army already deployed - RARE

    Returns:
        True if player has unclaimed troops OR leaderless army
    """
    # Check for unclaimed troops
    if game_state.unclaimed_troops:
        return True

    # Check for leaderless armies
    for army in player.armies:
        if not army.leader and len(army.troops) > 0:
            return True

    return False


def contract_leader_from_market(player: Player, game_state: GameState, leader_type: LeaderType) -> Optional[Leader]:
    """
    🔥 v1.16: Contract a leader from the 3-card face-up market
    🔥 v1.18 BUG FIX: Removed overly restrictive validation - leaders can create empty armies

    Args:
        player: The player contracting the leader
        game_state: Current game state (contains markets and decks)
        leader_type: Type of leader to contract (MAGE or COMMANDER only)

    Returns:
        The contracted leader, or None if market is empty
    """
    # 🔥 v1.18: Removed can_contract_leader() check - leaders can always be contracted
    # The function handles all cases: unclaimed troops, leaderless army, OR create new empty army

    # Get the appropriate market and deck (MAGE or COMMANDER only)
    if leader_type == LeaderType.MAGE:
        market = game_state.mage_market
        deck = game_state.mage_deck
    elif leader_type == LeaderType.COMMANDER:
        market = game_state.commander_market
        deck = game_state.commander_deck
    else:
        return None  # Captains not in market system

    if not market:
        return None  # No leaders available in market

    # AI/Player selects a leader from the 3-card market
    # For now, simple AI: pick first leader (index 0)
    # TODO Phase 10+: Implement smarter AI selection based on abilities/strategy
    selected_leader = market.pop(0)

    # Refill market from deck (if deck has cards left)
    if deck:
        new_leader = deck.pop()
        market.append(new_leader)

    # 🔥 v1.16 ASSIGNMENT PRIORITY:
    # 1. Assign to unclaimed troops (create new army)
    # 2. Assign to existing leaderless army

    if game_state.unclaimed_troops:
        # MOST COMMON: Claim unclaimed troops with this leader
        new_army = player.create_new_army()
        new_army.leader = selected_leader
        # Move unclaimed troops to this new army
        new_army.troops = game_state.unclaimed_troops[:]
        game_state.unclaimed_troops.clear()
    else:
        # RARE: Assign to existing leaderless army
        assigned = False
        for army in player.armies:
            if not army.leader and len(army.troops) > 0:
                army.leader = selected_leader
                assigned = True
                break

        if not assigned:
            # Safety fallback: create empty army (shouldn't happen with validation)
            new_army = player.create_new_army()
            new_army.leader = selected_leader

    return selected_leader


def resolve_standard_contract(player: Player, card: EventCard, game_state: GameState, playbook: Dict[LeaderType, List[Leader]] = None) -> bool:
    """
    🔥 v1.18: Resolve Standard Contract action (non-card action to claim unclaimed troops pot)

    🐛 BUG FIX: contract_leader_from_market() already claims troops, so we must NOT do it again
    The bug was creating duplicate armies and causing contract failures in late-game rounds.

    Standard Contract: Spend influence to draft mage/commander AND claim all unclaimed troops
    Requirements:
    - Player has enough influence (leader_contract_cost)
    - Unclaimed troops exist in pot
    - Mage or Commander available in market
    """
    cost = card.base_effect.get('cost_influence', game_state.config.leader_contract_cost)

    # 🔥 v1.18 SPENDING LOCK: Check affordability (with spending lock)
    if player.influence < cost:
        return False

    if not player.can_spend_influence(cost):
        return False  # Cannot spend - would drop below minimum

    # Check if unclaimed troops exist
    if len(game_state.unclaimed_troops) == 0:
        return False

    # Check if any leaders available
    if len(game_state.mage_market) == 0 and len(game_state.commander_market) == 0:
        return False

    # Pay the cost BEFORE drafting (prevents issues if spending check changes state)
    player.influence -= cost

    # Try to draft a leader (prefer commander, fallback to mage)
    # 🔥 v1.18 FIX: contract_leader_from_market() handles troop claiming internally!
    # Do NOT claim troops again or we create duplicate armies
    leader = None
    if game_state.commander_market:
        leader = contract_leader_from_market(player, game_state, LeaderType.COMMANDER)
    elif game_state.mage_market:
        leader = contract_leader_from_market(player, game_state, LeaderType.MAGE)

    if not leader:
        # Refund the cost if leader draft failed
        player.influence += cost
        return False  # Failed to draft leader

    # Track contract (troops already claimed by contract_leader_from_market)
    game_state.contract_plays += 1

    return True

def resolve_contract_card(player: Player, card: EventCard, game_state: GameState, playbook: Dict[LeaderType, List[Leader]] = None) -> bool:
    """Resolve contract event cards (acquire leaders)"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)

    # 🔥 v1.16: Handle CONTRACT_MAGE (draft from 3-card mage market)
    if card.card_type == EventCardType.CONTRACT_MAGE:
        cost = effect.get('cost_influence', game_state.config.leader_contract_cost)

        # 🔥 v1.17 SPENDING LOCK: Check affordability (with spending lock)
        if player.influence < cost or not player.can_spend_influence(cost):
            return False  # Can't afford or would drop below minimum

        # 🔥 v1.18 BUG FIX: Removed can_contract_leader() check - leaders can create empty armies
        # The contract_leader_from_market() function handles all cases

        leader = contract_leader_from_market(player, game_state, LeaderType.MAGE)

        if leader:
            player.influence -= cost
            game_state.contract_plays += 1
            return True
        else:
            return False  # No mages available in market

    # 🔥 v1.16: Handle CONTRACT_COMMANDER (draft from 3-card commander market)
    if card.card_type == EventCardType.CONTRACT_COMMANDER:
        cost = effect.get('cost_influence', game_state.config.leader_contract_cost)

        # 🔥 v1.17 SPENDING LOCK: Check affordability (with spending lock)
        if player.influence < cost or not player.can_spend_influence(cost):
            return False  # Can't afford or would drop below minimum

        # 🔥 v1.18 BUG FIX: Removed can_contract_leader() check - leaders can create empty armies
        # The contract_leader_from_market() function handles all cases

        leader = contract_leader_from_market(player, game_state, LeaderType.COMMANDER)

        if leader:
            player.influence -= cost
            game_state.contract_plays += 1
            return True
        else:
            return False  # No commanders available in market

    # 🔥 v1.16 LEGACY: Handle old CONTRACT_LEADER card type (deprecated)
    if card.card_type == EventCardType.CONTRACT_LEADER:
        cost = effect.get('cost_influence', 1)

        # 🔥 v1.17 SPENDING LOCK: Check affordability (with spending lock)
        if player.influence < cost or not player.can_spend_influence(cost):
            return False  # Can't afford or would drop below minimum

        # AI chooses which market to draft from based on strategy
        # For now, simple priority: Commander > Mage
        leader = None
        if game_state.commander_market:
            leader = contract_leader_from_market(player, game_state, LeaderType.COMMANDER)
        elif game_state.mage_market:
            leader = contract_leader_from_market(player, game_state, LeaderType.MAGE)

        if leader:
            player.influence -= cost
            game_state.contract_plays += 1
            return True
        else:
            return False  # No leaders available in any market

    # 🔥 LEGACY CONTRACT CARDS (v1.15 and earlier)
    # Check if player can afford
    cost_influence = effect.get('cost_influence', 0)
    cost_cards = effect.get('cost_cards', 0)

    # 🔥 v1.17 SPENDING LOCK: Check affordability (with spending lock)
    can_afford_influence = player.influence >= cost_influence and player.can_spend_influence(cost_influence)
    can_afford_cards = len(player.hand) >= cost_cards + 1

    if not can_afford_influence or not can_afford_cards:
        return False  # Can't afford or would drop below minimum

    # Pay costs
    player.influence -= cost_influence
    for _ in range(cost_cards):
        if player.hand:
            player.hand.pop()  # Discard random card

    # 🔥 v1.16: Use game_state markets (Mages & Commanders only, no captain market)
    playbook_map = {
        LeaderType.MAGE: game_state.mage_market,
        LeaderType.COMMANDER: game_state.commander_market,
    }

    # Get leader(s)
    leader_type = effect.get('leader_type')
    if leader_type and leader_type in playbook_map and playbook_map[leader_type]:
        leader = playbook_map[leader_type].pop(0)
        player.leaders.append(leader)

        # 🔥 v1.15 FIX: AUTO-ASSIGN leader to army without one
        assigned = False
        for army in player.armies:
            if not army.leader:
                army.leader = leader
                player.leaders.remove(leader)  # Remove from pool once assigned
                assigned = True
                break

        # If all armies have leaders, create new army for this leader
        if not assigned:
            new_army = player.create_new_army()
            new_army.leader = leader
            player.leaders.remove(leader)

        game_state.contract_plays += 1
        return True

    # Handle special contracts
    if effect.get('get_commander') and effect.get('get_mage'):
        if playbook_map[LeaderType.COMMANDER] and playbook_map[LeaderType.MAGE]:
            commander = playbook_map[LeaderType.COMMANDER].pop(0)
            mage = playbook_map[LeaderType.MAGE].pop(0)
            player.leaders.extend([commander, mage])

            # 🔥 v1.15 FIX: AUTO-ASSIGN both leaders
            for leader in [commander, mage]:
                assigned = False
                for army in player.armies:
                    if not army.leader:
                        army.leader = leader
                        player.leaders.remove(leader)
                        assigned = True
                        break
                if not assigned:
                    new_army = player.create_new_army()
                    new_army.leader = leader
                    player.leaders.remove(leader)

            game_state.contract_plays += 2
            return True

    if effect.get('random_leader'):
        available_types = [lt for lt in LeaderType if lt in playbook_map and playbook_map[lt]]
        if available_types:
            random_type = random.choice(available_types)
            leader = playbook_map[random_type].pop(0)
            player.leaders.append(leader)

            # 🔥 v1.15 FIX: AUTO-ASSIGN leader
            assigned = False
            for army in player.armies:
                if not army.leader:
                    army.leader = leader
                    player.leaders.remove(leader)
                    assigned = True
                    break
            if not assigned:
                new_army = player.create_new_army()
                new_army.leader = leader
                player.leaders.remove(leader)

            game_state.contract_plays += 1
            return True

    return False

def resolve_gather_card(player: Player, card: EventCard, game_state: GameState, troops_drawn_counter: Optional[List[int]] = None) -> bool:
    """Resolve gather troops event cards"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)
    troops_drawn = 0

    # 🔥 v1.15: Basic gather - add to UNCLAIMED POOL (not directly to army)
    gather_count = effect.get('gather_troops', 0)
    if gather_count > 0:
        for _ in range(gather_count):
            if game_state.troop_deck:
                troop = game_state.troop_deck.pop(0)

                # 🔥 v1.17: Check if Captain was drawn (value 0)
                if troop == 0:
                    # CAPTAIN DRAWN! Auto-claim unclaimed troops + draw trick
                    if game_state.captain_pool:
                        captain = game_state.captain_pool.pop(0)

                        # Create new army with captain
                        new_army = player.create_new_army()
                        new_army.leader = captain

                        # Add all unclaimed troops to this army
                        new_army.troops = game_state.unclaimed_troops[:]
                        game_state.unclaimed_troops.clear()

                        # Draw trick from trick deck
                        if game_state.trick_deck:
                            trick = game_state.trick_deck.pop(0)
                            new_army.trick = trick
                            # Log to file only (not console spam)
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} + {trick}")
                        else:
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} (no tricks left)")
                    else:
                        if game_state.config.detailed_log:
                            game_state.log_action(f"  ⚠️ CAPTAIN DRAWN but no captains left in pool!")
                else:
                    # Regular troop - add to unclaimed pool
                    game_state.unclaimed_troops.append(troop)
                    troops_drawn += 1
        if troops_drawn_counter is not None:
            troops_drawn_counter[0] += troops_drawn
        return True
    
    # 🔥 v1.15: Conditional gather - add to UNCLAIMED POOL
    if effect.get('gather_troops_if_losing'):
        # Check if player is losing (fewest towers)
        active_players = game_state.get_active_players()
        min_towers = min(p.towers for p in active_players)
        if player.towers == min_towers:
            gather_count = effect['gather_troops_if_losing']
        else:
            gather_count = effect.get('gather_troops_else', 0)

        for _ in range(gather_count):
            if game_state.troop_deck:
                troop = game_state.troop_deck.pop(0)

                # 🔥 v1.17: Check if Captain was drawn (value 0)
                if troop == 0:
                    if game_state.captain_pool:
                        captain = game_state.captain_pool.pop(0)
                        new_army = player.create_new_army()
                        new_army.leader = captain
                        new_army.troops = game_state.unclaimed_troops[:]
                        game_state.unclaimed_troops.clear()
                        if game_state.trick_deck:
                            trick = game_state.trick_deck.pop(0)
                            new_army.trick = trick
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} + {trick}")
                        else:
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} (no tricks left)")
                    else:
                        if game_state.config.detailed_log:
                            game_state.log_action(f"  ⚠️ CAPTAIN DRAWN but no captains left in pool!")
                else:
                    game_state.unclaimed_troops.append(troop)
                    troops_drawn += 1
        if troops_drawn_counter is not None:
            troops_drawn_counter[0] += troops_drawn
        return True

    # 🔥 v1.15: Random gather - add to UNCLAIMED POOL
    if effect.get('gather_troops_random'):
        min_troops, max_troops = effect['gather_troops_random']
        gather_count = random.randint(min_troops, max_troops)
        for _ in range(gather_count):
            if game_state.troop_deck:
                troop = game_state.troop_deck.pop(0)

                # 🔥 v1.17: Check if Captain was drawn (value 0)
                if troop == 0:
                    if game_state.captain_pool:
                        captain = game_state.captain_pool.pop(0)
                        new_army = player.create_new_army()
                        new_army.leader = captain
                        new_army.troops = game_state.unclaimed_troops[:]
                        game_state.unclaimed_troops.clear()
                        if game_state.trick_deck:
                            trick = game_state.trick_deck.pop(0)
                            new_army.trick = trick
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} + {trick}")
                        else:
                            if game_state.config.detailed_log:
                                game_state.log_action(f"  🎖️ CAPTAIN DRAWN! Auto-claimed {len(new_army.troops)} troops with {captain.name} (no tricks left)")
                    else:
                        if game_state.config.detailed_log:
                            game_state.log_action(f"  ⚠️ CAPTAIN DRAWN but no captains left in pool!")
                else:
                    game_state.unclaimed_troops.append(troop)
                    troops_drawn += 1
        if troops_drawn_counter is not None:
            troops_drawn_counter[0] += troops_drawn
        return True
    
    return False

def decide_whether_to_block(defender: Player, defending_army: 'Army', attack_strength: int, game_state: GameState) -> bool:
    """
    🔥 v1.13: Defender AI decides whether to block attack (MTG-style)
    If blocks: mutual damage as normal
    If doesn't block: tower takes damage, army survives
    """
    defense_strength = defending_army.get_strength()
    
    # WILDCARD uses aggression parameter
    if defender.strategy == StrategyType.WILDCARD:
        # High aggression = always block (fight back)
        # Low aggression = preserve army (don't block unless forced)
        if defender.towers == 1:
            return True  # Must defend last tower
        return defender.wildcard_aggression > 0.6
    
    # Strategy-specific heuristics
    # Block if: strong enough to win/survive OR must defend last tower
    if defense_strength > attack_strength * 1.2:
        return True  # Strong army, can win trade
    
    if defender.towers == 1:
        return True  # Must defend last tower (no choice)
    
    # Don't block if: weak army AND have multiple towers (preserve army for later)
    if defense_strength < attack_strength * 0.8 and defender.towers > 1:
        # FORTRESS: More likely to preserve army (defensive)
        if defender.strategy == StrategyType.FORTRESS:
            return defense_strength > attack_strength * 0.5  # Only block if not totally outmatched
        # RUSH: More aggressive, blocks more often
        elif defender.strategy == StrategyType.RUSH:
            return defense_strength > attack_strength * 0.6
        # TEMPO: Mathematical decision
        elif defender.strategy == StrategyType.TEMPO:
            return defense_strength >= attack_strength * 0.75
        # Default: don't block if very weak
        return False
    
    # Default: block (when in doubt, defend)
    return True

def remove_strength_from_army(army: Army, target_strength: int) -> int:
    """
    Remove troops from army to match target_strength as closely as possible.
    Uses greedy algorithm to find optimal combination.
    Returns actual strength removed.

    🔥 v1.15: Asymmetric combat - armies lose STRENGTH, not troop count
    """
    total_strength = sum(army.troops)

    if total_strength <= target_strength:
        # Army completely destroyed
        strength_removed = total_strength
        army.troops.clear()
        return strength_removed

    # Find optimal combination of troops to remove
    # Strategy: Try to match target exactly using greedy subset sum
    troops_sorted_desc = sorted(army.troops, reverse=True)

    # Greedy approach: Take largest troops that fit
    strength_to_remove = 0
    troops_to_remove = []

    for troop in troops_sorted_desc:
        if strength_to_remove + troop <= target_strength:
            troops_to_remove.append(troop)
            strength_to_remove += troop
            if strength_to_remove == target_strength:
                break  # Perfect match!

    # If we haven't removed enough, add one more troop (slight overkill acceptable)
    if strength_to_remove < target_strength:
        remaining = [t for t in troops_sorted_desc if t not in troops_to_remove]
        if remaining:
            troops_to_remove.append(remaining[0])
            strength_to_remove += remaining[0]

    # Remove the selected troops from army
    for troop in troops_to_remove:
        army.troops.remove(troop)

    return strength_to_remove

def resolve_attack_card(player: Player, card: EventCard, game_state: GameState, target: Optional[Player] = None, logger: Optional['GameLogger'] = None):
    """Resolve attack event cards"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)

    # Prepare combat data for logging
    combat_data = {
        'attacker_id': player.player_id,
        'card_name': card.name,
    }
    
    # 🔥 v1.13: BYPASS ATTACKS - Skip army combat, hit towers directly (Hearthstone-style)
    if card.card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE]:
        if game_state.config.enable_bypass_attacks:
            if not target:
                active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
                if not active_opponents:
                    return False
                target = random.choice(active_opponents)
            
            # 🔥 v1.20 BALANCE FIX: Bypass attacks are for chipping, not instant-win
            # Siege Attack = 1 damage (chip damage), Artillery Strike = 2 damage (stronger chip)
            # These are tactical tools, not elimination buttons
            if card.card_type == EventCardType.ARTILLERY_STRIKE:
                bypass_damage = 2  # Artillery: stronger chip damage
            else:  # SIEGE_ATTACK
                bypass_damage = 1  # Siege: basic chip damage
            
            # Apply early elimination protection
            if game_state.current_round <= game_state.config.early_protection_rounds:
                bypass_damage = min(bypass_damage, game_state.config.early_protection_max_towers)
            
            # Deal direct tower damage (skip army combat entirely)
            towers_before = target.towers
            target.towers -= min(bypass_damage, target.towers)
            towers_destroyed = towers_before - target.towers

            # Log bypass attack
            combat_data.update({
                'defender_id': target.player_id,
                'bypass_attack': True,
                'bypass_damage': bypass_damage,
                'towers_destroyed': towers_destroyed,
                'defender_towers_before': towers_before,
                'defender_towers_after': target.towers,
            })

            if towers_destroyed > 0:
                player.towers_destroyed += towers_destroyed
                game_state.towers_destroyed_total += towers_destroyed

                # 🔥 v1.19 BUG FIX: Bypass attacks should NOT get momentum multiplier
                # They already skip combat entirely - momentum is for consecutive COMBAT wins
                # This prevents runaway influence from siege/artillery spam
                base_influence_reward = towers_destroyed * game_state.config.influence_per_tower
                # Removed momentum multiplier for bypass attacks (was causing +30 influence bugs)
                player.influence += base_influence_reward

                cards_drawn = 0
                for _ in range(game_state.config.bonus_cards_per_tower):
                    if game_state.event_deck:
                        player.draw_event_card(game_state.event_deck)
                        cards_drawn += 1

                glory_bonus = player.towers_destroyed // game_state.config.glory_divisor
                player.influence += glory_bonus

                combat_data.update({
                    'influence_gained': base_influence_reward + glory_bonus,
                    'cards_drawn': cards_drawn,
                    'glory_bonus': glory_bonus,
                })

                if target.towers <= 0:
                    target.eliminated = True
                    combat_data['defender_eliminated'] = True

                    # 🔥 v1.20 ELIMINATION REWARD: Flat +3 influence, +2 cards (balanced, not game-ending)
                    player.influence += 3
                    elimination_cards_drawn = 0
                    for _ in range(2):
                        if game_state.event_deck:
                            player.draw_event_card(game_state.event_deck)
                            elimination_cards_drawn += 1
                    combat_data['elimination_bonus'] = {'influence': 3, 'cards': elimination_cards_drawn}

            # Log the combat
            if logger:
                logger.log_combat(combat_data)

            # Attacker takes NO casualties (that's the point of bypass!)
            player.attacks_this_turn += 1
            player.attacked_last_turn = True
            game_state.attack_plays += 1
            return True
    
    # 🔥 v1.9: MULTIPLE ARMIES COMBAT SYSTEM

    if not target:
        # Choose target (random opponent)
        active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
        if not active_opponents:
            return False
        target = random.choice(active_opponents)

    # 🔥 v1.15: EARLY ATTACK BLOCK - No attacks allowed in first N rounds
    if game_state.config.early_attack_block_rounds > 0:
        if game_state.current_round <= game_state.config.early_attack_block_rounds:
            if logger:
                logger.write('')
                logger.write('❌ ATTACK BLOCKED: Early protection active')
                logger.write(f'   Attacks not allowed until Round {game_state.config.early_attack_block_rounds + 1}')
            return False

    # 🔥 v1.10: STRATEGIC ARMY SELECTION
    # For now, AI uses heuristics (can be improved with more sophisticated logic)
    # Attacker: Use strongest army (aggressive)
    # Defender: Use weakest army that can survive OR strongest to tank (defensive)

    attacking_army = player.get_strongest_army()  # Attacker chooses (for now: strongest)
    defending_army = target.get_weakest_army()    # Defender chooses (for now: sacrificial)

    if not attacking_army or not defending_army:
        return False  # No armies to fight!

    # 🔥 v1.15: LEADER REQUIREMENT - Armies MUST have leaders to attack
    if not attacking_army.leader:
        if logger:
            logger.write('')
            logger.write('❌ ATTACK BLOCKED: Army has no leader')
            logger.write(f'   Attacking armies must have a leader (Captain/Mage/Commander)')
        return False

    # Get army indices for logging
    attacker_army_idx = player.armies.index(attacking_army) + 1
    defender_army_idx = target.armies.index(defending_army) + 1

    # 🔥 v1.16: LEADER ABILITIES - Apply passive abilities for both armies
    attacker_mods = resolve_leader_ability_passive(
        attacking_army.leader,
        {
            'phase': 'combat_start',
            'army': attacking_army,
            'opponent_army': defending_army,
            'player': player,
            'opponent': target
        },
        game_state
    ) if attacking_army.leader else {
        'attack_bonus': 0,
        'defense_bonus': 0,
        'damage_reduction': 0,
        'tower_damage_bonus': 0,
        'damage_multiplier': 1.0
    }

    defender_mods = resolve_leader_ability_passive(
        defending_army.leader,
        {
            'phase': 'combat_start',
            'army': defending_army,
            'opponent_army': attacking_army,
            'player': target,
            'opponent': player
        },
        game_state
    ) if defending_army.leader else {
        'attack_bonus': 0,
        'defense_bonus': 0,
        'damage_reduction': 0,
        'tower_damage_bonus': 0,
        'damage_multiplier': 1.0
    }

    # Calculate strengths
    attack_strength = attacking_army.get_strength()
    attack_bonus = effect.get('attack_bonus', 0) + attacker_mods.get('attack_bonus', 0)  # 🔥 v1.16: Add leader bonus
    attack_multiplier = effect.get('attack_multiplier', 1.0) * attacker_mods.get('damage_multiplier', 1.0)  # 🔥 v1.16: Apply leader multiplier

    # 🔥 v1.15: TOWER ATTACK DAMAGE - Towers damage attacker BEFORE combat
    tower_damage_config = game_state.config.tower_attack_damage
    tower_damage = tower_damage_config + attacker_mods.get('tower_damage_bonus', 0)  # 🔥 v1.16: Apply leader tower damage bonus
    shield_effect_used = None  # 🔥 v1.15 Phase 3: Track for logging

    # Check for tower damage shield effects
    if player.active_effects.get('siege_equipment'):
        tower_damage = 0  # Nullify tower damage
        shield_effect_used = 'siege_equipment'  # 🔥 v1.15 Phase 3
        player.active_effects['siege_equipment'] = False  # Consumed
    elif player.active_effects.get('protective_wards'):
        tower_damage = tower_damage // 2  # Reduce by 50%
        shield_effect_used = 'protective_wards'  # 🔥 v1.15 Phase 3
        player.active_effects['protective_wards'] = False  # Consumed
    elif player.active_effects.get('vanguard_formation') and player.attacks_this_turn == 0:
        tower_damage = 0  # First attack ignores tower damage
        shield_effect_used = 'vanguard_formation'  # 🔥 v1.15 Phase 3
        # Don't consume - lasts whole turn

    # Apply tower damage to attacking army
    attack_strength = max(0, attack_strength - tower_damage)

    total_attack = int((attack_strength + attack_bonus) * attack_multiplier)

    defense_strength = defending_army.get_strength() + defender_mods.get('defense_bonus', 0)  # 🔥 v1.16: Add leader defense bonus

    # Track bonus source for logging
    bonus_source = None
    if attack_bonus > 0:
        bonus_source = card.name  # The card itself provides the bonus

    # Calculate leader contributions separately for detailed logging
    attacker_troop_strength = sum(attacking_army.troops)
    attacker_leader_bonus = attacking_army.leader.attack_bonus if attacking_army.leader else 0
    defender_troop_strength = sum(defending_army.troops)
    defender_leader_bonus = defending_army.leader.attack_bonus if defending_army.leader else 0  # 🔥 Leaders use attack_bonus for defense too

    # Prepare combat data for logging
    combat_data.update({
        'defender_id': target.player_id,
        'tower_damage_config': tower_damage_config,  # 🔥 v1.15 Phase 3: Base tower damage
        'tower_damage_taken': tower_damage,  # 🔥 v1.15: Actual tower damage after shields
        'shield_effect': shield_effect_used,  # 🔥 v1.15 Phase 3: Shield used (if any)
        'attacker_army': {
            'index': attacker_army_idx,
            'troop_count': len(attacking_army.troops),
            'troop_strength': attacker_troop_strength,
            'leader_bonus': attacker_leader_bonus,
            'base_strength': sum(attacking_army.troops),
            'troops': sorted(attacking_army.troops, reverse=True),
            'leader': attacking_army.leader.name if attacking_army.leader else None,
            'has_leader': attacking_army.leader is not None,
            'leader_ability': attacking_army.leader.ability_description if attacking_army.leader else None,  # 🔥 v1.16
        },
        'defender_army': {
            'index': defender_army_idx,
            'troop_count': len(defending_army.troops),
            'troop_strength': defender_troop_strength,
            'leader_bonus': defender_leader_bonus,
            'base_strength': sum(defending_army.troops),
            'troops': sorted(defending_army.troops, reverse=True),
            'leader': defending_army.leader.name if defending_army.leader else None,
            'has_leader': defending_army.leader is not None,
            'leader_ability': defending_army.leader.ability_description if defending_army.leader else None,  # 🔥 v1.16
        },
        'attack_base': attack_strength,  # After tower damage applied
        'attack_bonus': attack_bonus,
        'bonus_source': bonus_source,
        'attack_multiplier': attack_multiplier,
        'total_attack': total_attack,
        'defense_strength': defense_strength,
        'defender_towers_before': target.towers,
    })

    # 🔥 v1.16: LEADER ABILITIES - Triggered abilities at combat start
    if attacking_army.leader and attacking_army.leader.ability_type == "triggered":
        attacker_trigger_result = resolve_leader_ability_triggered(
            attacking_army.leader,
            'combat_start',
            {
                'army': attacking_army,
                'opponent_army': defending_army,
                'player': player,
                'opponent': target
            },
            game_state,
            logger
        )
        # Some triggered abilities modify combat stats (like flank removing troops)
        if attacker_trigger_result.get('success'):
            # Recalculate defense strength if defender troops were modified
            defense_strength = defending_army.get_strength() + defender_mods.get('defense_bonus', 0)

    if defending_army.leader and defending_army.leader.ability_type == "triggered":
        defender_trigger_result = resolve_leader_ability_triggered(
            defending_army.leader,
            'combat_start',
            {
                'army': defending_army,
                'opponent_army': attacking_army,
                'player': target,
                'opponent': player
            },
            game_state,
            logger
        )
        # Some triggered abilities (like trap) deal damage to attacker
        if defender_trigger_result.get('counter_damage'):
            counter_damage = defender_trigger_result['counter_damage']
            attack_strength = max(0, attack_strength - counter_damage)
            total_attack = int((attack_strength + attack_bonus) * attack_multiplier)

    # 🔥 v1.13: OPT-IN BLOCKING - Defender chooses (MTG-style)
    if game_state.config.enable_optional_blocking:
        should_block = decide_whether_to_block(target, defending_army, total_attack, game_state)

        combat_data['blocking_enabled'] = True
        combat_data['defender_blocked'] = should_block

        if not should_block:
            combat_data['block_reason'] = "Preserving army"

            # Defender chooses NOT to block: take tower damage, army survives
            net_damage = total_attack
            towers_destroyed = net_damage // game_state.config.tower_damage_threshold

            # Apply early elimination protection
            if game_state.current_round <= game_state.config.early_protection_rounds:
                towers_destroyed = min(towers_destroyed, game_state.config.early_protection_max_towers)

            # 🔥 v1.15: MAX 1 TOWER PER TURN
            towers_destroyed = min(towers_destroyed, 1 - player.towers_destroyed_this_turn)

            combat_data.update({
                'towers_destroyed': towers_destroyed,
                'defender_towers_after': target.towers - towers_destroyed,
            })

            # Deal tower damage
            if towers_destroyed > 0:
                target.towers -= towers_destroyed
                player.towers_destroyed += towers_destroyed
                player.towers_destroyed_this_turn += towers_destroyed  # 🔥 v1.15
                player.end_turn_now = True  # 🔥 v1.15: Tower destruction ends turn!
                game_state.towers_destroyed_total += towers_destroyed

                # Give attack rewards
                base_influence_reward = towers_destroyed * game_state.config.influence_per_tower
                momentum_bonus = player.attacked_last_turn
                if momentum_bonus:
                    base_influence_reward = int(base_influence_reward * game_state.config.momentum_multiplier)
                player.influence += base_influence_reward

                cards_drawn = 0
                for _ in range(game_state.config.bonus_cards_per_tower):
                    if game_state.event_deck:
                        player.draw_event_card(game_state.event_deck)
                        cards_drawn += 1

                glory_bonus = player.towers_destroyed // game_state.config.glory_divisor
                player.influence += glory_bonus

                combat_data.update({
                    'influence_gained': base_influence_reward + glory_bonus,
                    'momentum_bonus': momentum_bonus,
                    'cards_drawn': cards_drawn,
                    'glory_bonus': glory_bonus,
                })

                if target.towers <= 0:
                    target.eliminated = True
                    combat_data['defender_eliminated'] = True

                    # 🔥 v1.20 ELIMINATION REWARD: Flat +3 influence, +2 cards (balanced, not game-ending)
                    player.influence += 3
                    elimination_cards_drawn = 0
                    for _ in range(2):
                        if game_state.event_deck:
                            player.draw_event_card(game_state.event_deck)
                            elimination_cards_drawn += 1
                    combat_data['elimination_bonus'] = {'influence': 3, 'cards': elimination_cards_drawn}

            # Log the combat
            if logger:
                logger.log_combat(combat_data)

            # No casualties for either side (defender didn't block)
            player.attacks_this_turn += 1
            player.attacked_last_turn = True
            game_state.attack_plays += 1
            return True
        else:
            combat_data['block_reason'] = "Defending towers"
    
    # If blocking (or blocking disabled), proceed with mutual damage as normal
    # 🔥 v1.15: ASYMMETRIC CASUALTIES - Each side loses opponent's total strength
    attacker_casualties_strength = defense_strength  # Attacker loses defender's strength
    defender_casualties_strength = total_attack      # Defender loses attacker's strength

    # Calculate net damage for tower destruction
    net_damage = max(0, total_attack - defense_strength)
    towers_destroyed = net_damage // game_state.config.tower_damage_threshold

    # Apply early elimination protection
    if game_state.current_round <= game_state.config.early_protection_rounds:
        towers_destroyed = min(towers_destroyed, game_state.config.early_protection_max_towers)

    # 🔥 v1.15: MAX 1 TOWER PER TURN - Cap based on towers already destroyed this turn
    towers_destroyed = min(towers_destroyed, 1 - player.towers_destroyed_this_turn)

    # Deal tower damage
    if towers_destroyed > 0:
        target.towers -= towers_destroyed
        player.towers_destroyed += towers_destroyed
        player.towers_destroyed_this_turn += towers_destroyed  # 🔥 v1.15: Track this turn
        player.end_turn_now = True  # 🔥 v1.15: Tower destruction ends turn!
        game_state.towers_destroyed_total += towers_destroyed
        
        # 🔥 v1.11: AGGRESSIVE ATTACK INCENTIVES!
        # 1. Influence per tower destroyed (configurable: 1-5)
        base_influence_reward = towers_destroyed * game_state.config.influence_per_tower
        
        # 4. MOMENTUM BONUS: Multiplier if attacked last turn (configurable: 1.0-5.0x)
        if player.attacked_last_turn:
            base_influence_reward = int(base_influence_reward * game_state.config.momentum_multiplier)
        
        player.influence += base_influence_reward
        
        # 2. BONUS CARDS: Draw extra event cards on tower destruction (configurable: 0-3)
        for _ in range(game_state.config.bonus_cards_per_tower):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        
        # 5. GLORY REWARDS: Bonus based on total towers destroyed (configurable divisor: 2-6)
        glory_bonus = player.towers_destroyed // game_state.config.glory_divisor
        player.influence += glory_bonus
        
        if target.towers <= 0:
            target.eliminated = True
    
    # 🔥 v1.15: Apply ASYMMETRIC STRENGTH-BASED casualties to BOTH armies
    # 🔥 v1.12: Check for card effects that modify casualties!

    # Attacker takes casualties (defender's strength)
    attacker_casualties = attacker_casualties_strength

    # BATTLE FRENZY: No attacker casualties on next attack
    if player.active_effects.get('battle_frenzy', False):
        attacker_casualties = 0
        player.active_effects['battle_frenzy'] = False  # Consumed

    # TACTICAL RETREAT: Halve attacker casualties this turn
    elif player.active_effects.get('tactical_retreat', False):
        attacker_casualties = int(attacker_casualties * 0.5)

    # MOMENTUM: -1/-2/-3 casualties per attack this turn
    if player.active_effects.get('momentum', False):
        momentum_reduction = min(player.attacks_this_turn, 3)  # Cap at -3
        attacker_casualties = max(0, attacker_casualties - momentum_reduction)

    # GUERRILLA TACTICS: Cap casualties at 5 this turn
    if player.active_effects.get('guerrilla_tactics', False):
        attacker_casualties = min(attacker_casualties, 5)

    # 🔥 v1.16: LEADER ABILITIES - Apply damage reduction
    attacker_casualties = max(0, attacker_casualties - attacker_mods.get('damage_reduction', 0))

    # 🔥 v1.16: LEADER ABILITIES - Check for casualty-negating triggered abilities (Blink, Perfect Execution)
    if attacking_army.leader and attacking_army.leader.ability_type == "triggered":
        casualty_trigger_result = resolve_leader_ability_triggered(
            attacking_army.leader,
            'casualties',
            {
                'army': attacking_army,
                'opponent_army': defending_army,
                'player': player,
                'opponent': target
            },
            game_state,
            logger
        )
        if casualty_trigger_result.get('negate_casualties'):
            attacker_casualties = 0

    # 🔥 v1.15: Remove troops by STRENGTH, not count
    attacker_troops_before = len(attacking_army.troops)
    attacker_strength_removed = remove_strength_from_army(attacking_army, attacker_casualties)
    attacker_troops_lost = attacker_troops_before - len(attacking_army.troops)  # Count of troops removed

    # Defender takes casualties (attacker's strength)
    defender_casualties = defender_casualties_strength

    # FORTIFIED POSITION: No defender casualties when defending
    if target.active_effects.get('fortified_position', False):
        defender_casualties = 0

    # GUERRILLA TACTICS: Cap casualties at 5 this turn
    if target.active_effects.get('guerrilla_tactics', False):
        defender_casualties = min(defender_casualties, 5)

    # 🔥 v1.16: LEADER ABILITIES - Apply damage reduction
    defender_casualties = max(0, defender_casualties - defender_mods.get('damage_reduction', 0))

    # 🔥 v1.15: Remove troops by STRENGTH, not count
    defender_troops_before = len(defending_army.troops)
    defender_strength_removed = remove_strength_from_army(defending_army, defender_casualties)
    defender_troops_lost = defender_troops_before - len(defending_army.troops)  # Count of troops removed
    
    # 🔥 v1.10: Check if armies are destroyed and handle leaders
    attacker_army_destroyed = (len(attacking_army.troops) == 0)
    defender_army_destroyed = (len(defending_army.troops) == 0)
    
    # Attacker's leader returns to hand if army destroyed (tie/loss)
    if attacker_army_destroyed and attacking_army.leader:
        player.hand.append(EventCard(
            EventCardType.CONTRACT_CHEAP,
            f"Returned {attacking_army.leader.name}",
            {'cost_influence': 1, 'leader_type': attacking_army.leader.leader_type}
        ))
        # Note: This adds a contract card representing the leader back to hand
        # In a full implementation, we'd have a proper leader card system
    
    # Remove destroyed armies
    if attacker_army_destroyed:
        player.remove_army(attacking_army)
        if defender_army_destroyed:
            # Tie: both destroyed
            target.remove_army(defending_army)
            player.armies_destroyed += 1
            target.armies_destroyed += 1
            player.influence += 1
            target.influence += 1
        # else: Attacker lost (army destroyed, defender survived)
    elif defender_army_destroyed:
        # Attacker won: defender destroyed, attacker survived
        target.remove_army(defending_army)
        player.armies_destroyed += 1
        player.influence += 1  # 🔥 +1 influence for killing enemy army!

    # Prepare final combat data for logging
    total_influence_gained = 0
    cards_drawn_combat = 0
    glory_bonus_combat = 0

    if towers_destroyed > 0:
        base_reward = towers_destroyed * game_state.config.influence_per_tower
        momentum_bonus = player.attacked_last_turn
        if momentum_bonus:
            base_reward = int(base_reward * game_state.config.momentum_multiplier)

        cards_drawn_combat = game_state.config.bonus_cards_per_tower * towers_destroyed
        glory_bonus_combat = player.towers_destroyed // game_state.config.glory_divisor
        total_influence_gained = base_reward + glory_bonus_combat

    combat_data.update({
        'attacker_casualties': attacker_casualties,  # 🔥 v1.15: Strength casualties
        'defender_casualties': defender_casualties,  # 🔥 v1.15: Strength casualties
        'attacker_strength_removed': attacker_strength_removed,  # 🔥 v1.15: Actual strength removed
        'defender_strength_removed': defender_strength_removed,  # 🔥 v1.15: Actual strength removed
        'net_damage': net_damage,
        'towers_destroyed': towers_destroyed,
        'defender_towers_after': target.towers,
        'attacker_army_destroyed': attacker_army_destroyed,
        'defender_army_destroyed': defender_army_destroyed,
        'influence_gained': total_influence_gained,
        'momentum_bonus': player.attacked_last_turn if towers_destroyed > 0 else False,
        'cards_drawn': cards_drawn_combat,
        'glory_bonus': glory_bonus_combat,
    })

    if target.towers <= 0:
        combat_data['defender_eliminated'] = True

    # Log the combat
    if logger:
        logger.log_combat(combat_data)

    # 🔥 v1.16: LEADER ABILITIES - Post-combat triggered abilities
    # Determine who won combat (for Perfect Execution, etc.)
    attacker_won = not attacker_army_destroyed and defender_army_destroyed
    defender_won = attacker_army_destroyed and not defender_army_destroyed

    # Attacker's post-combat abilities
    if attacking_army.leader and attacking_army.leader.ability_type == "triggered":
        combat_end_result = resolve_leader_ability_triggered(
            attacking_army.leader,
            'combat_end',
            {
                'army': attacking_army,
                'opponent_army': defending_army,
                'player': player,
                'opponent': target,
                'combat_won': attacker_won
            },
            game_state,
            logger
        )

        # Trigger tower_destroyed abilities (Conqueror, Veni Vidi Vici, Pillage)
        if towers_destroyed > 0:
            tower_result = resolve_leader_ability_triggered(
                attacking_army.leader,
                'tower_destroyed',
                {
                    'player': player,
                    'opponent': target,
                    'towers_destroyed': towers_destroyed
                },
                game_state,
                logger
            )

        # Trigger tower_damaged for Pillage
        if towers_destroyed > 0:
            tower_damage_result = resolve_leader_ability_triggered(
                attacking_army.leader,
                'tower_damaged',
                {
                    'player': player,
                    'opponent': target,
                    'towers_destroyed': towers_destroyed
                },
                game_state,
                logger
            )

    # Defender's post-combat abilities
    if defending_army.leader and defending_army.leader.ability_type == "triggered":
        combat_end_result = resolve_leader_ability_triggered(
            defending_army.leader,
            'combat_end',
            {
                'army': defending_army,
                'opponent_army': attacking_army,
                'player': target,
                'opponent': player,
                'combat_won': defender_won
            },
            game_state,
            logger
        )

    # 🔥 v1.11: Track attack for incentives
    game_state.attack_plays += 1
    player.attacks_this_game += 1
    player.turns_since_last_attack = 0
    player.attacked_last_turn = True  # Will be reset at end of turn

    # 🔥 v1.12: Apply card effects AFTER attack resolves
    
    # RAIDING PARTY: Attack + gain 5 troops
    if player.active_effects.get('raiding_party', False):
        for _ in range(5):
            if game_state.troop_deck:
                troop_rank = game_state.troop_deck.pop(0)
                attacking_army.troops.append(troop_rank)
        player.active_effects['raiding_party'] = False  # Consumed
    
    # SPOILS OF WAR: Draw 2 cards + gain 3 influence after ANY attack (passive)
    if player.active_effects.get('spoils_of_war', False):
        for _ in range(2):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        player.influence += 3
        # Note: Spoils of War is NOT consumed (passive effect for entire turn)
    
    # REINFORCEMENTS: Regain casualties from this attack
    if player.active_effects.get('reinforcements', False):
        for _ in range(attacker_troops_lost):
            if game_state.troop_deck:
                troop_rank = game_state.troop_deck.pop(0)
                attacking_army.troops.append(troop_rank)
        player.active_effects['reinforcements'] = False  # Consumed
    
    # PLUNDER: Tower destroyed → gain 3 influence + 1 card
    if towers_destroyed > 0 and player.active_effects.get('plunder', False):
        player.influence += 3 * towers_destroyed
        for _ in range(towers_destroyed):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        # Note: Plunder is NOT consumed (passive effect)
    
    # CHAIN ASSAULT: Tower destroyed → draw another event card to potentially chain
    if towers_destroyed > 0 and player.active_effects.get('chain_assault', False):
        if game_state.event_deck:
            player.draw_event_card(game_state.event_deck)
        player.active_effects['chain_assault'] = False  # Consumed after first trigger
    
    # WAR ECONOMY: Gain 1 influence per attack this turn
    if player.active_effects.get('war_economy', False):
        player.influence += 1
        # Note: War Economy is NOT consumed (passive effect for entire turn)
    
    # PYRRHIC VICTORY: Auto-win attack, but lose all troops in attacking army
    if player.active_effects.get('pyrrhic_victory', False):
        # Note: This would be handled during attack calculation (auto-win logic)
        # For now, just clear the army after attack
        attacking_army.troops.clear()
        player.active_effects['pyrrhic_victory'] = False  # Consumed
    
    # Increment attacks this turn (for Momentum stacking)
    player.attacks_this_turn += 1

    # 🔥 v1.15: Return combat results for press attack mechanics
    return {
        'success': True,
        'army_defeated': defender_army_destroyed,  # For Blitzkrieg (press after army defeat)
        'tower_destroyed': towers_destroyed > 0,   # For Raze (press after tower)
        'end_turn': player.end_turn_now,           # Tower destruction ends turn
    }

def resolve_economic_card(player: Player, card: EventCard, game_state: GameState) -> bool:
    """Resolve economic event cards (gain/steal influence)"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)
    
    # Basic gain influence
    gain_influence = effect.get('gain_influence', 0)
    if gain_influence > 0:
        player.influence += gain_influence
        return True
    
    # Per-tower influence
    gain_per_tower = effect.get('gain_influence_per_tower', 0)
    if gain_per_tower > 0:
        player.influence += player.towers * gain_per_tower
        return True
    
    # Steal from richest
    # 🔥 v1.17 SPENDING LOCK: Stealing respects the influence floor of 2
    if effect.get('steal_influence_from_richest'):
        active_players = game_state.get_active_players()
        richest = max(active_players, key=lambda p: p.influence if p.player_id != player.player_id else 0)
        steal_amount = effect['steal_influence_from_richest']
        # Can only steal down to the floor of 2
        max_stealable = max(0, richest.influence - 2)
        stolen = min(steal_amount, max_stealable)
        if stolen > 0:
            richest.influence -= stolen
            player.influence += stolen
        return True
    
    # Conditional gain
    if effect.get('gain_influence_if_losing'):
        active_players = game_state.get_active_players()
        min_towers = min(p.towers for p in active_players)
        if player.towers == min_towers:
            player.influence += effect['gain_influence_if_losing']
        else:
            player.influence += effect.get('gain_influence_else', 0)
        return True
    
    return False

def resolve_manipulation_card(player: Player, card: EventCard, game_state: GameState, target: Optional[Player] = None) -> bool:
    """Resolve manipulation event cards (disrupt opponents)"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)
    
    if not target:
        # Choose target
        active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
        if not active_opponents:
            return False
        target = random.choice(active_opponents)
    
    # Discard events
    discard_events = effect.get('target_discards_events', 0)
    if discard_events > 0:
        for _ in range(min(discard_events, len(target.hand))):
            target.hand.pop()
        return True
    
    # Discard troops - target strongest army
    discard_troops = effect.get('target_discards_troops', 0)
    if discard_troops > 0:
        strongest = target.get_strongest_army()
        if strongest:
            for _ in range(min(discard_troops, len(strongest.troops))):
                strongest.troops.pop()
        return True
    
    # Destroy leader - target strongest army's leader
    if effect.get('destroy_target_leader'):
        strongest = target.get_strongest_army()
        if strongest and strongest.leader:
            strongest.leader = None
        return True
    
    # Steal troops - from target's strongest to player's strongest
    steal_troops = effect.get('steal_troops_from_target', 0)
    if steal_troops > 0:
        target_strongest = target.get_strongest_army()
        if target_strongest and target_strongest.troops:
            for _ in range(min(steal_troops, len(target_strongest.troops))):
                if target_strongest.troops:
                    troop = target_strongest.troops.pop()
                    player.add_troop_to_strongest_army(troop)
        return True
    
    # AOE effects - affect all armies
    if effect.get('all_discard_half_troops'):
        for p in game_state.get_active_players():
            if p.player_id != player.player_id:
                for army in p.armies:
                    troops_to_discard = len(army.troops) // 2
                    for _ in range(troops_to_discard):
                        if army.troops:
                            army.troops.pop()
        return True
    
    return False

def resolve_utility_card(player: Player, card: EventCard, game_state: GameState) -> bool:
    """Resolve utility event cards (draw, timing, special effects)"""
    effect = card.get_scaled_effect(game_state.config.event_card_power)
    
    # Draw events
    draw_events = effect.get('draw_events', 0)
    if isinstance(draw_events, int) and draw_events > 0:
        for _ in range(draw_events):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        return True
    elif isinstance(draw_events, str):
        # Handle formulas like 'hand_size + 2'
        # For now, just draw 3
        for _ in range(3):
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        return True
    
    # Look at top cards
    if effect.get('look_top_events'):
        # For now, just draw (can be enhanced for strategic play)
        look_count = effect['look_top_events']
        take_count = effect.get('take', 1)
        if isinstance(look_count, int) and isinstance(take_count, int):
            for _ in range(min(take_count, look_count, len(game_state.event_deck))):
                player.draw_event_card(game_state.event_deck)
        return True
    
    # Extra turn
    if effect.get('extra_turn'):
        # Flag for game loop to handle
        return True
    
    # Draw to maximum
    if effect.get('draw_to'):
        draw_to = effect['draw_to']
        if isinstance(draw_to, int):
            while len(player.hand) < draw_to and game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        return True
    
    # Discard and redraw
    if effect.get('discard_hand'):
        hand_size = len(player.hand)
        player.hand.clear()
        # Draw new hand
        for _ in range(hand_size + 2):  # +2 bonus
            if game_state.event_deck:
                player.draw_event_card(game_state.event_deck)
        return True
    
    return False

def resolve_v12_card(player: Player, card: EventCard, game_state: GameState,
                     target: Optional[Player] = None, logger: Optional['GameLogger'] = None) -> bool:
    """
    🔥 v1.12: Resolve new attack-focused event cards
    These cards compensate for mutual damage by:
    - Reducing/negating casualties
    - Generating troops after attacks
    - Providing economic rewards
    - Enabling combo chains
    """
    effect = card.get_scaled_effect(game_state.config.event_card_power)
    cost_influence = effect.get('cost_influence', 0)
    cost_cards = effect.get('cost_cards', 0)

    # 🔥 v1.17 SPENDING LOCK: Check affordability (with spending lock)
    if player.influence < cost_influence or not player.can_spend_influence(cost_influence):
        return False  # Can't afford or would drop below minimum
    if len(player.hand) < cost_cards + 1:  # +1 for the card itself
        return False

    # Pay costs
    player.influence -= cost_influence
    for _ in range(cost_cards):
        if player.hand:
            player.hand.pop(random.randrange(len(player.hand)))
    
    card_type = card.card_type
    
    # Attack Rewards (30%)
    if card_type == EventCardType.BATTLE_FRENZY:
        player.active_effects['battle_frenzy'] = True  # Next attack: no attacker casualties
        return True
    
    elif card_type == EventCardType.RAIDING_PARTY:
        player.active_effects['raiding_party'] = True  # Attack + gain 5 troops
        # Also play attack immediately (hybrid card)
        return resolve_attack_card(player, EventCard(EventCardType.ATTACK_BASIC, "Raid", {'attack_bonus': 0}), 
                                   game_state, target)
    
    elif card_type == EventCardType.SPOILS_OF_WAR:
        player.active_effects['spoils_of_war'] = True  # Passive: draw 2 + gain 3 inf after ANY attack
        return True
    
    # Casualty Reduction (20%)
    elif card_type == EventCardType.TACTICAL_RETREAT:
        player.active_effects['tactical_retreat'] = True  # This turn: 50% attacker casualties
        return True
    
    elif card_type == EventCardType.REINFORCEMENTS:
        player.active_effects['reinforcements'] = True  # After next attack: regain casualties
        return True
    
    elif card_type == EventCardType.FORTIFIED_POSITION:
        player.active_effects['fortified_position'] = True  # When defending: 0 casualties
        return True
    
    # Combo/Chain (25%)
    elif card_type == EventCardType.MOMENTUM:
        player.active_effects['momentum'] = True  # -1/-2/-3 casualties per attack this turn
        return True
    
    elif card_type == EventCardType.BLITZKRIEG:
        # 🔥 v1.15: Attack twice, but ONLY if first attack defeats enemy ARMY
        if not target:
            active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
            if not active_opponents:
                return False
            target = random.choice(active_opponents)

        attack_card = EventCard(EventCardType.ATTACK_BASIC, "Blitz Attack", {'attack_bonus': 0})
        result = resolve_attack_card(player, attack_card, game_state, target, logger)

        # Only press attack if enemy army was defeated (not just tower)
        if isinstance(result, dict) and result.get('army_defeated'):
            if logger:
                logger.write("  ⚡ BLITZKRIEG: Army defeated, pressing the attack!")
            # Second attack allowed
            resolve_attack_card(player, attack_card, game_state, target, logger)
        elif isinstance(result, dict) and not result.get('army_defeated'):
            if logger:
                logger.write("  ❌ BLITZKRIEG BLOCKED: Must defeat enemy army to press attack")
        else:
            # Old return format (boolean) - allow second attack for backward compatibility
            resolve_attack_card(player, attack_card, game_state, target, logger)
        return True

    # 🔥 v1.15: Raze - Press attack after tower destruction
    elif card_type == EventCardType.RAZE:
        if not target:
            active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
            if not active_opponents:
                return False
            target = random.choice(active_opponents)

        attack_card = EventCard(EventCardType.ATTACK_BASIC, "Raze Attack", {'attack_bonus': 0})
        result = resolve_attack_card(player, attack_card, game_state, target, logger)

        # Only press attack if tower was destroyed (not just army)
        if isinstance(result, dict) and result.get('tower_destroyed'):
            if logger:
                logger.write("  🔥 RAZE: Tower destroyed, pressing the attack!")
            # Second attack allowed
            resolve_attack_card(player, attack_card, game_state, target, logger)
        elif isinstance(result, dict) and not result.get('tower_destroyed'):
            if logger:
                logger.write("  ❌ RAZE BLOCKED: Must destroy tower to press attack")
        else:
            # Old return format (boolean) - allow second attack for backward compatibility
            resolve_attack_card(player, attack_card, game_state, target, logger)
        return True

    elif card_type == EventCardType.CHAIN_ASSAULT:
        player.active_effects['chain_assault'] = True  # Tower destroyed → draw card
        return True

    # 🔥 v1.15: Tower Damage Shield Cards
    elif card_type == EventCardType.SIEGE_EQUIPMENT:
        player.active_effects['siege_equipment'] = True  # Nullify ALL tower damage next attack
        if logger:
            logger.write("  🛡️ SIEGE EQUIPMENT: Next attack ignores ALL tower damage")
        return True

    elif card_type == EventCardType.PROTECTIVE_WARDS:
        player.active_effects['protective_wards'] = True  # Reduce tower damage 50% next attack
        if logger:
            logger.write("  🛡️ PROTECTIVE WARDS: Next attack takes 50% tower damage")
        return True

    elif card_type == EventCardType.VANGUARD_FORMATION:
        player.active_effects['vanguard_formation'] = True  # First attack ignores tower damage this turn
        if logger:
            logger.write("  🛡️ VANGUARD FORMATION: First attack this turn ignores tower damage")
        return True

    # Economy (20%)
    elif card_type == EventCardType.PLUNDER:
        player.active_effects['plunder'] = True  # Tower destroyed → 3 inf + 1 card
        return True
    
    elif card_type == EventCardType.WAR_ECONOMY:
        player.active_effects['war_economy'] = True  # +1 influence per attack this turn
        return True
    
    elif card_type == EventCardType.CONSCRIPTION:
        # Buy 6 troops for 4 influence (already paid above)
        army = player.get_strongest_army()
        if not army and player.armies:
            army = player.armies[0]
        elif not army:
            army = player.create_new_army()

        for _ in range(6):
            if game_state.troop_deck:
                troop_rank = game_state.troop_deck.pop(0)
                army.troops.append(troop_rank)
        return True

    # 🔥 v1.15: Claim Army - Assign leader to unclaimed troops
    # 🔥 v1.17: CLAIM_ARMY removed - claiming now via Standard Contract or Captain draws

    # Wild Cards (5%)
    elif card_type == EventCardType.GUERRILLA_TACTICS:
        player.active_effects['guerrilla_tactics'] = True  # Cap casualties at 5 this turn
        return True

    # 🔥 v1.15: Reverse Turn Order
    elif card_type == EventCardType.REVERSE_TURN_ORDER:
        game_state.play_direction *= -1  # Flip direction
        direction_name = "anti-clockwise" if game_state.play_direction == -1 else "clockwise"
        if logger:
            logger.write(f"  🔄 CHAOS REVERSAL: Play order reversed to {direction_name}!")
        return True

    elif card_type == EventCardType.SCORCHED_EARTH:
        # Destroy own tower, gain 10 troops
        if player.towers > 0:
            player.towers -= 1
            army = player.get_strongest_army()
            if not army and player.armies:
                army = player.armies[0]
            elif not army:
                army = player.create_new_army()
            
            for _ in range(10):
                if game_state.troop_deck:
                    troop_rank = game_state.troop_deck.pop(0)
                    army.troops.append(troop_rank)
            return True
        return False
    
    elif card_type == EventCardType.PYRRHIC_VICTORY:
        player.active_effects['pyrrhic_victory'] = True  # Auto-win next attack, lose all troops
        # Also attack immediately
        return resolve_attack_card(player, EventCard(EventCardType.ATTACK_BASIC, "Pyrrhic Attack", 
                                                     {'attack_bonus': 999}), game_state, target)
    
    return False

def resolve_event_card(player: Player, card: EventCard, game_state: GameState,
                      playbook: Dict[LeaderType, List[Leader]],
                      target: Optional[Player] = None,
                      troops_drawn_counter: Optional[List[int]] = None,
                      logger: Optional['GameLogger'] = None) -> bool:
    """
    Master function to resolve any event card based on its type
    Returns True if card was successfully played
    """
    card_type = card.card_type

    # 🔥 v1.18: VERBOSE LOGGING - Log card effect details
    if logger:
        logger.write(f"  💭 Resolving: {card.name} (Type: {card_type.value})")
        logger.write(f"     Pre-state: Influence={player.influence}, Hand={len(player.hand)}, Armies={len(player.armies)}, Unclaimed={len(game_state.unclaimed_troops)}")
        if card.base_effect:
            effects_str = ", ".join([f"{k}={v}" for k, v in card.base_effect.items() if not k.startswith('_')])
            if effects_str:
                logger.write(f"     Effects: {effects_str}")

    # 🔥 v1.17: Handle Standard Contract (special non-card action)
    if card.name == "STANDARD_CONTRACT" and card.base_effect.get('is_standard_contract', False):
        result = resolve_standard_contract(player, card, game_state, playbook)
        if logger:
            logger.write(f"     Result: {'✅ Success' if result else '❌ Failed'}")
            logger.write(f"     Post-state: Influence={player.influence}, Armies={len(player.armies)}, Unclaimed={len(game_state.unclaimed_troops)}")
        return result

    if card_type in [EventCardType.CONTRACT_CHEAP, EventCardType.CONTRACT_STANDARD,
                     EventCardType.CONTRACT_PREMIUM, EventCardType.CONTRACT_EXPENSIVE,
                     EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_COMMANDER]:
        result = resolve_contract_card(player, card, game_state, playbook)
        if logger:
            logger.write(f"     Result: {'✅ Contract success' if result else '❌ Contract failed'}")
            logger.write(f"     Post-state: Influence={player.influence}, Armies={len(player.armies)}")
        return result

    elif card_type in [EventCardType.GATHER_SMALL, EventCardType.GATHER_MEDIUM,
                       EventCardType.GATHER_LARGE]:
        troops_before = len(game_state.unclaimed_troops)
        result = resolve_gather_card(player, card, game_state, troops_drawn_counter)
        if logger:
            troops_added = len(game_state.unclaimed_troops) - troops_before
            logger.write(f"     Result: {'✅ Gathered troops' if result else '❌ Failed'}")
            logger.write(f"     Troops gathered: {troops_added}, Unclaimed pot now: {len(game_state.unclaimed_troops)}")
        return result

    elif card_type in [EventCardType.ATTACK_BASIC, EventCardType.ATTACK_TACTICAL,
                       EventCardType.ATTACK_CONDITIONAL, EventCardType.ATTACK_AOE,
                       EventCardType.ATTACK_RISKY,
                       EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE]:  # 🔥 v1.18: Added bypass attacks
        result = resolve_attack_card(player, card, game_state, target, logger)
        if logger:
            logger.write(f"     Result: {'✅ Attack resolved' if result else '❌ Attack failed'}")
            if target:
                logger.write(f"     Target post-state: Towers={target.towers}, Armies={len(target.armies)}")
        return result

    elif card_type == EventCardType.ECONOMIC:
        inf_before = player.influence
        result = resolve_economic_card(player, card, game_state)
        if logger:
            inf_change = player.influence - inf_before
            logger.write(f"     Result: {'✅ Economic effect applied' if result else '❌ Failed'}")
            logger.write(f"     Influence change: {inf_change:+d} (now {player.influence})")
        return result

    elif card_type == EventCardType.MANIPULATION:
        result = resolve_manipulation_card(player, card, game_state, target)
        if logger:
            logger.write(f"     Result: {'✅ Manipulation success' if result else '❌ Failed'}")
        return result

    elif card_type == EventCardType.UTILITY:
        result = resolve_utility_card(player, card, game_state)
        if logger:
            logger.write(f"     Result: {'✅ Utility effect applied' if result else '❌ Failed'}")
        return result
    
    # 🔥 v1.12: ATTACK-FOCUSED EVENT CARDS
    elif card_type in [EventCardType.BATTLE_FRENZY, EventCardType.RAIDING_PARTY,
                       EventCardType.SPOILS_OF_WAR, EventCardType.TACTICAL_RETREAT,
                       EventCardType.REINFORCEMENTS, EventCardType.FORTIFIED_POSITION,
                       EventCardType.MOMENTUM, EventCardType.BLITZKRIEG,
                       EventCardType.RAZE,  # 🔥 v1.15: Press attack after tower
                       EventCardType.SIEGE_EQUIPMENT, EventCardType.PROTECTIVE_WARDS,
                       EventCardType.VANGUARD_FORMATION,  # 🔥 v1.15: Tower shields
                       EventCardType.CHAIN_ASSAULT, EventCardType.PLUNDER,
                       EventCardType.WAR_ECONOMY, EventCardType.CONSCRIPTION,
                       EventCardType.CLAIM_ARMY,  # 🔥 v1.15: Claim unclaimed troops
                       EventCardType.GUERRILLA_TACTICS, EventCardType.SCORCHED_EARTH,
                       EventCardType.REVERSE_TURN_ORDER,  # 🔥 v1.15: Reverse play direction
                       EventCardType.PYRRHIC_VICTORY]:
        result = resolve_v12_card(player, card, game_state, target, logger)
        if logger:
            logger.write(f"     Result: {'✅ Special card effect applied' if result else '❌ Failed'}")
            effects = []
            if 'momentum' in player.active_effects:
                effects.append("Momentum active")
            if 'fortified_position' in player.active_effects:
                effects.append("Fortified")
            if 'spoils_of_war' in player.active_effects:
                effects.append("Spoils active")
            if effects:
                logger.write(f"     Active effects: {', '.join(effects)}")
        return result

    if logger:
        logger.write(f"     ❌ Unknown card type, card not resolved")
    return False

# =============================================================================
# AI STRATEGY (Choose which card to play + Chain management)
# =============================================================================

def should_continue_chaining(player: Player, game_state: GameState, cards_played: int) -> bool:
    """
    🔥 v1.8 NEW: Decide if player should continue playing cards or stop
    
    Strategy logic:
    - RUSH: Chain aggressively (play all attack cards, target 4-6 cards/turn)
    - SWARM: Chain gathering, stop before committing to attack (target 3-5 cards/turn)
    - BUILDUP: Conservative chaining (target 2-3 cards/turn)
    - FORTRESS: Very conservative (target 1-2 cards/turn, save resources)
    - TEMPO: Moderate chaining (target 2-4 cards/turn)
    - ADAPTIVE: Flexible, responds to board state (target 2-4 cards/turn)
    
    Target overall average: 2-5 cards/turn across all strategies
    """
    
    # Always play at least 1 card if possible
    if cards_played == 0:
        return True
    
    # Stop if out of cards or influence
    if len(player.hand) == 0 or player.influence < 1:
        return False
    
    # Strategy-specific limits (v1.8.1: MORE AGGRESSIVE for 2-3 avg)
    if player.strategy == StrategyType.RUSH:
        # RUSH: Very aggressive chaining, play 6-10 cards
        return cards_played < 10
    
    elif player.strategy == StrategyType.SWARM:
        # SWARM: Aggressive gathering (5-7 cards)
        return cards_played < 7
    
    elif player.strategy == StrategyType.BUILDUP:
        # BUILDUP: Moderate, 4-5 cards per turn
        return cards_played < 5
    
    elif player.strategy == StrategyType.FORTRESS:
        # FORTRESS: Still conservative but increased, 3-4 cards per turn
        return cards_played < 4
    
    elif player.strategy == StrategyType.TEMPO:
        # TEMPO: More flexible, 4-6 cards per turn
        return cards_played < 6
    
    elif player.strategy == StrategyType.ADAPTIVE:
        # ADAPTIVE: Responds to board state, 4-8 cards per turn (v1.8.1: more aggressive)
        # More aggressive when behind, more conservative when ahead
        my_towers = next(p for p in game_state.players if p.player_id == player.player_id).towers
        avg_enemy_towers = sum(p.towers for p in game_state.players if p.player_id != player.player_id) / (len(game_state.players) - 1)
        
        if my_towers < avg_enemy_towers:
            # Behind: chain very aggressively (up to 8 cards)
            return cards_played < 8
        else:
            # Ahead: still moderate (4-5 cards)
            return cards_played < 5
    
    elif player.strategy == StrategyType.WILDCARD:
        # 🎲 WILDCARD: Uses randomized parameters set at game start
        # Usually loses, but when it wins, we log its behavior!
        return cards_played < player.wildcard_chain_length
    
    # Default: keep chaining (up to 5 cards for unknown strategies)
    return cards_played < 5

def can_player_play_card(player: Player, card: EventCard, game_state: GameState, target: Optional[Player] = None) -> bool:
    """
    🔥 v1.19: Validate if player can actually play this card (beyond just affording it)

    Checks:
    1. Leader type requirements (Mage Barrage needs Mage, Captain's Gambit needs Captain, etc.)
    2. Attack viability (can we break through defense?)
    3. Card-specific preconditions (has army, has troops, etc.)

    Returns True if card can be played, False otherwise
    """
    effect = card.get_scaled_effect(game_state.config.event_card_power)

    # Check 1: Leader type requirements for attack cards
    required_leader_type = effect.get('requires')
    if required_leader_type:
        # Check if player has ANY army with the required leader type
        has_required_leader = any(
            army.leader and army.leader.leader_type == required_leader_type
            for army in player.armies
        )
        if not has_required_leader:
            return False  # Can't play this card without the required leader type

    # Check 2: Attack cards need at least one army with a leader (except bypass attacks)
    is_bypass_attack = card.card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE]

    if not is_bypass_attack and card.card_type in [EventCardType.ATTACK_BASIC, EventCardType.ATTACK_TACTICAL,
                          EventCardType.ATTACK_CONDITIONAL, EventCardType.ATTACK_AOE,
                          EventCardType.ATTACK_RISKY]:
        has_leader = any(army.leader is not None for army in player.armies)
        if not has_leader:
            return False  # Can't attack without a leader

        # Check 3: Zero-damage attack prevention (don't attack if we can't break defense)
        if target and not effect.get('ignore_all_defense'):  # Mage Barrage ignores defense
            attacking_army = player.get_strongest_army()
            defending_army = target.get_weakest_army() if target.armies else None

            if attacking_army and defending_army:
                attack_strength = attacking_army.get_strength()
                attack_bonus = effect.get('attack_bonus', 0)
                total_attack = attack_strength + attack_bonus

                defense_strength = defending_army.get_strength()
                defense_bonus = effect.get('defense_bonus', 0)
                total_defense = defense_strength + defense_bonus

                # 🔥 v1.20: Prevent zero-damage "pillow fight" attacks
                # If we can't break through defense, this attack will deal 0 tower damage
                if total_attack <= total_defense:
                    if game_state.config.detailed_log and hasattr(game_state, '_logger') and game_state._logger:
                        game_state.log_action(f"   ❌ Rejected {card.name}: Zero-damage attack (ATK {total_attack} vs DEF {total_defense})")
                    return False  # Waste of turn - don't attack

    # Check 4: Specific card preconditions (can add more as needed)
    if card.name == "Rally the Troops" and not player.armies:
        return False  # Some cards might need existing armies

    return True  # Card can be played

def choose_card_to_play(player: Player, game_state: GameState, playbook: Dict[LeaderType, List[Leader]],
                       standard_contract_failed: bool = False, verbose: bool = False) -> Tuple[Optional[EventCard], Optional[Player]]:
    """
    AI chooses which event card to play based on strategy
    Returns (card_to_play, target) or (None, None) if no playable cards

    🔥 v1.17: Can also return a special "STANDARD_CONTRACT" marker to trigger non-card contract

    Args:
        standard_contract_failed: If True, skip Standard Contract check (already failed this turn)
        verbose: If True, print detailed Standard Contract failure reasons
    """
    if not player.hand:
        return None, None

    # 🔥 v1.18: Log AI decision-making process
    if game_state.config.detailed_log:
        game_state.log_action(f"\n🧠 AI DECISION-MAKING ({player.strategy.name.upper()} strategy):")
        game_state.log_action(f"   Hand: {len(player.hand)} cards | Influence: {player.influence} | Armies: {len(player.armies)}")
        game_state.log_action(f"   Has Leader: {any(army.leader for army in player.armies)}")
        game_state.log_action(f"   Unclaimed Troops: {len(game_state.unclaimed_troops)} (strength {sum(game_state.unclaimed_troops)})")
        game_state.log_action(f"   Leaders Available: Mages={len(game_state.mage_market)}, Commanders={len(game_state.commander_market)}")

    # 🔥 v1.17 ANTI-FEEDER LOGIC: Determine if we can claim the pot
    # If we CAN'T claim, we should NOT play pot-building cards (avoid feeding opponents)
    can_claim_pot = False

    # Check #1: Can we use Standard Contract?
    if not standard_contract_failed:
        cost = game_state.config.leader_contract_cost
        has_influence = player.influence >= cost and player.can_spend_influence(cost)  # 🔥 v1.18: Added spending lock check
        has_leaders_in_market = len(game_state.mage_market) > 0 or len(game_state.commander_market) > 0
        can_claim_pot = has_influence and has_leaders_in_market

    # Check #2: Do we have a claim card in hand? (Mystery Mercenary, Warlord Summons, etc.)
    if not can_claim_pot:
        for card in player.hand:
            if card.name in ["Mystery Mercenary", "Warlord Summons", "Magical Binding", "Hire Mage", "War Council"]:
                can_claim_pot = True
                break

    # Check #3: Might we draw a captain from a GATHER card this turn?
    # This is probabilistic, but if we have GATHER cards, there's a chance
    # For now, we'll be conservative and assume NO (prevents accidental feeding)
    # Future: Could calculate probability based on remaining captains in deck

    # 🔥 v1.17: Check if "Standard Contract" action is available (non-card action)
    # Skip if already failed this turn to prevent infinite loops
    if not standard_contract_failed:
        # Conditions: (a) enough influence AND spending lock, (b) unclaimed troops exist, (c) leaders available in markets
        cost = game_state.config.leader_contract_cost
        has_influence = player.influence >= cost and player.can_spend_influence(cost)  # 🔥 v1.18: Added spending lock check
        has_unclaimed_troops = len(game_state.unclaimed_troops) > 0
        has_leaders_in_market = len(game_state.mage_market) > 0 or len(game_state.commander_market) > 0

        can_standard_contract = has_influence and has_unclaimed_troops and has_leaders_in_market

        # AI decision: Should we use Standard Contract instead of playing a card?
        # Priority: If we have unclaimed troops and can afford it, do it!
        # This is MORE valuable than most cards because it's FREE (no card cost)
        if can_standard_contract:
            # 🔥 v1.18: Log why Standard Contract is chosen
            if game_state.config.detailed_log:
                game_state.log_action(f"   ✅ STANDARD CONTRACT available: {len(game_state.unclaimed_troops)} unclaimed troops, {game_state.config.leader_contract_cost} influence cost")
                game_state.log_action(f"   → AI chose Standard Contract (free army creation, better than playing a card)")

            # Create a special marker to indicate Standard Contract
            from dataclasses import dataclass
            standard_contract_marker = EventCard(
                EventCardType.CONTRACT_MAGE,  # Reuse CONTRACT_MAGE type
                "STANDARD_CONTRACT",  # Special name to identify it
                {'cost_influence': game_state.config.leader_contract_cost, 'is_standard_contract': True}
            )
            return standard_contract_marker, None
        elif verbose and (has_unclaimed_troops or has_influence):
            # Report why Standard Contract is unavailable (for debugging)
            if not has_influence:
                print(f"    ⚠️  Standard Contract unavailable: Not enough influence ({player.influence} < {game_state.config.leader_contract_cost})")
            elif not has_unclaimed_troops:
                print(f"    ⚠️  Standard Contract unavailable: No unclaimed troops (pot empty)")
            elif not has_leaders_in_market:
                print(f"    ⚠️  Standard Contract unavailable: No leaders in market (Mages: {len(game_state.mage_market)}, Commanders: {len(game_state.commander_market)})")

    # 🔥 v1.19: Determine target BEFORE card validation (needed for zero-damage attack check)
    active_opponents = [p for p in game_state.get_active_players() if p.player_id != player.player_id]
    target = None
    if active_opponents:
        # Target player with most towers
        target = max(active_opponents, key=lambda p: p.towers)

    # 🔥 v1.19: Build playable cards list with FULL validation (not just affordability)
    playable_cards = []
    for card in player.hand:
        # Check 1: Can afford?
        if not player.can_afford_card(card, game_state.config.event_card_power):
            continue

        # Check 2: Can actually play? (leader requirements, zero-damage attacks, etc.)
        if not can_player_play_card(player, card, game_state, target):
            if game_state.config.detailed_log:
                effect = card.get_scaled_effect(game_state.config.event_card_power)
                required = effect.get('requires')
                if required:
                    game_state.log_action(f"   ❌ Filtered out {card.name}: requires {required.name}")
            continue

        playable_cards.append(card)

    if not playable_cards:
        return None, None

    # 🔥 v1.17 ANTI-FEEDER FILTER: Remove pot-building cards if we can't claim
    # Only apply filter if:
    # 1. We CAN'T claim the pot, AND
    # 2. There ARE unclaimed troops (no point feeding an empty pot)
    if not can_claim_pot and len(game_state.unclaimed_troops) > 0:
        # Identify pot-building cards (GATHER cards that add troops to unclaimed pot)
        pot_building_types = [
            EventCardType.GATHER_SMALL,   # Rally the Troops, Quick Gather, etc.
            EventCardType.GATHER_MEDIUM,  # Strategic Muster, etc.
            EventCardType.GATHER_LARGE    # Conscription, etc.
        ]

        # Filter out pot-building cards
        non_feeder_cards = [card for card in playable_cards
                           if card.card_type not in pot_building_types]

        # If we have other cards to play, use those instead
        # If ONLY pot-building cards exist, allow them (edge case: better to feed than waste turn)
        if non_feeder_cards:
            playable_cards = non_feeder_cards
            if verbose:
                print(f"    🧠 Anti-Feeder: Filtered out pot-building cards (can't claim pot)")

    # 🔥 v1.19: Removed duplicate target selection (now done earlier for validation)
    # 🔥 v1.19: Keep has_leader check for strategy prioritization (still needed)
    has_leader = any(army.leader is not None for army in player.armies)

    # Strategy-based card selection
    strategy = player.strategy
    
    if strategy == StrategyType.RUSH:
        # 🔥 v1.16 AI FIX: RUSH needs leader before attacking!
        if not has_leader:
            # No leader: prioritize getting one FIRST (captains from troop deck OR contract)
            for card_type in [EventCardType.GATHER_SMALL, EventCardType.GATHER_MEDIUM,
                             EventCardType.CONTRACT_COMMANDER, EventCardType.CONTRACT_MAGE,
                             EventCardType.CONTRACT_CHEAP]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target

        # Has leader: prioritize bypass > attacks > gather > commanders > mages > economic
        for card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE,
                         EventCardType.ATTACK_BASIC, EventCardType.ATTACK_TACTICAL,
                         EventCardType.GATHER_SMALL, EventCardType.GATHER_MEDIUM,
                         EventCardType.CONTRACT_COMMANDER, EventCardType.CONTRACT_MAGE,
                         EventCardType.CONTRACT_CHEAP]:
            for card in playable_cards:
                if card.card_type == card_type:
                    if game_state.config.detailed_log:
                        game_state.log_action(f"   → RUSH chose: {card.name} (Has leader, aggressive play)")
                    return card, target
    
    elif strategy == StrategyType.SWARM:
        # 🔥 v1.16 AI FIX: Can't attack without leader
        if not has_leader:
            # Gather troops to find captain OR contract a leader
            for card_type in [EventCardType.GATHER_MEDIUM, EventCardType.GATHER_LARGE,
                             EventCardType.GATHER_SMALL, EventCardType.CONTRACT_MAGE]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        # Has leader: prioritize gather > attacks > contracts
        for card_type in [EventCardType.GATHER_MEDIUM, EventCardType.GATHER_LARGE,
                         EventCardType.GATHER_SMALL, EventCardType.ATTACK_BASIC]:
            for card in playable_cards:
                if card.card_type == card_type:
                    return card, target
    
    elif strategy == StrategyType.BUILDUP:
        # 🔥 v1.16: BUILDUP prioritizes commanders (economy/strategy) over mages
        # Prioritize: economic > commanders > mages > gather > utility
        for card_type in [EventCardType.ECONOMIC, EventCardType.CONTRACT_COMMANDER,
                         EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_STANDARD,
                         EventCardType.CONTRACT_PREMIUM, EventCardType.GATHER_MEDIUM]:
            for card in playable_cards:
                if card.card_type == card_type:
                    return card, target
    
    elif strategy == StrategyType.FORTRESS:
        # 🔥 v1.16 AI FIX: Can't attack without leader
        if not has_leader:
            # Get leader first (commanders for defense, or gather for captain)
            for card_type in [EventCardType.CONTRACT_COMMANDER, EventCardType.GATHER_LARGE,
                             EventCardType.CONTRACT_MAGE, EventCardType.GATHER_MEDIUM]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target

        # Has leader: if losing (fewer towers than average), use bypass to catch up
        avg_towers = sum(p.towers for p in game_state.get_active_players()) / len(game_state.get_active_players())
        if player.towers < avg_towers:
            # Behind: use bypass to catch up quickly
            for card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        # Prioritize: gather > commanders > economic > mages > defensive
        for card_type in [EventCardType.GATHER_LARGE, EventCardType.CONTRACT_COMMANDER,
                         EventCardType.ECONOMIC, EventCardType.CONTRACT_MAGE,
                         EventCardType.CONTRACT_PREMIUM, EventCardType.UTILITY]:
            for card in playable_cards:
                if card.card_type == card_type:
                    return card, target
    
    elif strategy == StrategyType.TEMPO:
        # 🔥 v1.16 AI FIX: TEMPO must prioritize getting a leader FIRST!
        if not has_leader:
            # No leader: GET ONE IMMEDIATELY (highest priority!)
            # Try to contract leaders OR gather troops to find captain
            for card_type in [EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_COMMANDER,
                             EventCardType.GATHER_MEDIUM, EventCardType.GATHER_SMALL]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target

        # Has leader: balanced approach - adapt to situation
        if player.influence > 5:
            # High influence: invest in mages first (flexible abilities), then contracts
            for card_type in [EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_COMMANDER]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
            for card in playable_cards:
                if 'contract' in card.card_type.value:
                    return card, target
        elif player.get_total_troop_count() < 5:  # 🔥 v1.9: Check total troops across armies
            # Low troops: gather
            for card in playable_cards:
                if 'gather' in card.card_type.value:
                    return card, target
        else:
            # Attack when ready: prefer bypass (no casualties = efficient)
            for card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
            for card in playable_cards:
                if 'attack' in card.card_type.value:
                    return card, target
    
    elif strategy == StrategyType.ADAPTIVE:
        # 🔥 v1.16 AI FIX: Can't attack without leader
        if not has_leader:
            # Get leader first (contract OR gather for captain)
            for card_type in [EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_COMMANDER,
                             EventCardType.GATHER_LARGE, EventCardType.GATHER_MEDIUM]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target

        # Has leader: respond to board state
        if player.towers < 2:
            # Desperate: use bypass to catch up quickly OR build up
            for card_type in [EventCardType.ARTILLERY_STRIKE, EventCardType.SIEGE_ATTACK,
                             EventCardType.GATHER_LARGE, EventCardType.ATTACK_TACTICAL]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        elif player.towers == 3:
            # Winning: maintain pressure with bypass (no casualties to preserve lead)
            for card_type in [EventCardType.SIEGE_ATTACK, EventCardType.ARTILLERY_STRIKE,
                             EventCardType.ATTACK_BASIC, EventCardType.GATHER_MEDIUM]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        else:
            # Even: be flexible
            for card_type in [EventCardType.GATHER_MEDIUM, EventCardType.ECONOMIC]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
    
    elif strategy == StrategyType.WILDCARD:
        # 🔥 v1.16 AI FIX: Can't attack without leader
        if not has_leader:
            # Get leader before attacking (gather OR contract)
            for card_type in [EventCardType.GATHER_MEDIUM, EventCardType.GATHER_SMALL,
                             EventCardType.CONTRACT_MAGE, EventCardType.CONTRACT_COMMANDER]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target

        # Has leader: use risk_tolerance for bypass frequency
        # High risk = use bypass more (aggressive, risky play)
        # Low risk = traditional attacks (conservative)
        if player.wildcard_risk_tolerance > 0.7:
            # High risk: prioritize bypass attacks
            for card_type in [EventCardType.ARTILLERY_STRIKE, EventCardType.SIEGE_ATTACK]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        elif player.wildcard_risk_tolerance < 0.3:
            # Low risk: avoid bypass, prefer traditional
            for card_type in [EventCardType.ATTACK_BASIC, EventCardType.GATHER_MEDIUM]:
                for card in playable_cards:
                    if card.card_type == card_type:
                        return card, target
        # Medium risk: fallthrough to default (any card)
    
    # Default: play first affordable card
    return playable_cards[0], target

# =============================================================================
# GAME SIMULATION
# =============================================================================

def simulate_game(player_count: int, config: GameConfig, strategies: Optional[List[StrategyType]] = None, verbose: bool = False) -> Dict:
    """
    Simulate a full game of Battalion v1.7

    Args:
        player_count: Number of players (2-4)
        config: Game configuration
        strategies: List of strategies for each player (random if None)
        verbose: Print game events

    Returns:
        Dict with game statistics
    """
    # Initialize detailed logger if requested
    logger = None
    if config.detailed_log and config.log_file:
        logger = GameLogger(config.log_file)

    # Initialize decks
    troop_deck = create_troop_deck(config)
    event_deck = create_event_deck(config)
    playbook = create_leader_playbook(config)
    
    # Initialize players
    # 🎲 v1.8: Fully randomize strategies - could have 6 turtles!
    if strategies is None:
        all_strategies = list(StrategyType)
        strategies = [random.choice(all_strategies) for _ in range(player_count)]
    
    players = []
    for i in range(player_count):
        player = Player(
            player_id=i,
            strategy=strategies[i],
            towers=3,
            influence=config.starting_influence
        )
        
        # 🎲 Initialize wildcard randomization
        if player.strategy == StrategyType.WILDCARD:
            player.wildcard_aggression = random.uniform(0.0, 1.0)
            player.wildcard_chain_length = random.randint(1, 8)
            player.wildcard_risk_tolerance = random.uniform(0.0, 1.0)
            if verbose:
                print(f"  🎲 Player {i} WILDCARD params: aggr={player.wildcard_aggression:.2f}, chain={player.wildcard_chain_length}, risk={player.wildcard_risk_tolerance:.2f}")
        
        # Draw starting hand
        for _ in range(config.starting_hand_size):
            if event_deck:
                player.draw_event_card(event_deck)

        # 🔥 v1.9: Give each player ONE starting army
        # 🔥 v1.17: Players start with ZERO armies and ZERO troops
        # Armies are created via Captain draws (troop deck) or contracts (mage/commander markets)

        players.append(player)
    
    # 🔥 v1.16: Initialize leader decks and markets (Mages & Commanders only)
    # Captains stay in troop deck (no market system)

    # Mage market: 3 face-up, rest face-down
    mage_deck = playbook[LeaderType.MAGE][:]
    random.shuffle(mage_deck)
    mage_market = [mage_deck.pop() for _ in range(min(3, len(mage_deck)))]

    # Commander market: 3 face-up, rest face-down
    commander_deck = playbook[LeaderType.COMMANDER][:]
    random.shuffle(commander_deck)
    commander_market = [commander_deck.pop() for _ in range(min(3, len(commander_deck)))]

    # 🔥 v1.17: Initialize Captain pool (shuffled)
    captain_pool = playbook[LeaderType.CAPTAIN][:]
    random.shuffle(captain_pool)

    # 🔥 v1.17: Initialize Trick Playbook deck
    trick_deck = create_trick_deck()

    # Initialize game state
    game_state = GameState(
        players=players,
        troop_deck=troop_deck,
        event_deck=event_deck,
        event_discard=[],
        config=config,
        current_round=1,
        current_turn=0,
        # 🔥 v1.16: Initialize leader draft system (Mages & Commanders only)
        mage_deck=mage_deck,
        mage_market=mage_market,
        commander_deck=commander_deck,
        commander_market=commander_market,
        # 🔥 v1.17: Initialize captain pool and trick deck
        captain_pool=captain_pool,
        trick_deck=trick_deck,
        unclaimed_troops=[]
    )

    # 🔥 v1.18: Attach logger to game_state for verbose AI logging
    game_state._logger = logger
    
    if verbose:
        print(f"🎮 Game Start: {player_count} players")
        for p in players:
            print(f"  Player {p.player_id}: {p.strategy.value}")
        print()

    # Log game start
    if logger:
        logger.log_game_start(player_count, players, config)

    # Main game loop (turn-based)
    max_turns = 500  # Safety limit
    turn_count = 0
    current_player_idx = 0
    
    while not game_state.game_over and turn_count < max_turns:
        turn_count += 1
        game_state.total_turns = turn_count
        
        # Get active players
        active_players = game_state.get_active_players()
        if len(active_players) <= 1:
            break
        
        # Current player
        player = active_players[current_player_idx % len(active_players)]
        
        # 🔥 v1.11: PASSIVE TAX - Configurable penalty for not attacking
        # 🔥 v1.17 SPENDING LOCK: Passive tax respects the influence floor of 2
        player.turns_since_last_attack += 1
        if player.turns_since_last_attack >= game_state.config.passive_tax_threshold and player.influence > 2:
            # Tax can reduce influence, but not below the floor of 2
            max_tax = player.influence - 2
            tax = min(game_state.config.passive_tax_amount, max_tax)
            if tax > 0:
                player.influence -= tax
                if verbose:
                    print(f"  💸 PASSIVE TAX: Player {player.player_id} loses {tax} influence (haven't attacked in {player.turns_since_last_attack} turns)")
        
        if verbose:
            print(f"Turn {turn_count} - Player {player.player_id} ({player.strategy.value})")
            print(f"  Towers: {player.towers}, Influence: {player.influence}, Hand: {len(player.hand)}, Armies: {len(player.armies)} ({player.get_total_troop_count()} troops total)")

        # Log turn start
        if logger:
            logger.log_turn_start(turn_count, player, game_state.current_round, game_state)  # 🔥 v1.15 Phase 3: Pass game_state

        # Track cards for this turn
        cards_drawn_this_turn = 0
        cards_played_this_turn = 0
        troops_drawn_this_turn = [0]  # Use list to pass by reference
        attacked_this_turn = False  # Track if player attacked

        # 🔥 v1.15: Reset per-turn counters and flags
        player.towers_destroyed_this_turn = 0
        player.end_turn_now = False

        # 🔥 v1.18: ANTE MECHANIC - Mandatory pot contribution at turn start
        # Every turn begins with 1 troop added to the unclaimed pot
        # This makes the pot central and forces constant claiming decisions
        if game_state.troop_deck:
            ante_troop = game_state.troop_deck.pop(0)

            # Check if it's a Captain (value 0)
            if ante_troop == 0:
                # 🔥 v1.18 FIX: Captain during ANTE creates "JACKPOT POT" - does NOT auto-claim!
                # Auto-claim ONLY triggers when playing GATHER cards from hand (like Army Muster)
                captain_value = 10  # Captain represents a high-value troop
                game_state.unclaimed_troops.append(captain_value)
                troops_drawn_this_turn[0] += 1
                if logger:
                    logger.write(f"ACTION 0: ANTE - 🎖️ CAPTAIN card drawn! Added as strength-{captain_value} troop to pot (JACKPOT!). Pot now: {len(game_state.unclaimed_troops)} troops, strength {sum(game_state.unclaimed_troops)}")
                if verbose:
                    print(f"  🎲 ANTE: CAPTAIN JACKPOT! Added strength-{captain_value} to pot (now {len(game_state.unclaimed_troops)} troops, total strength {sum(game_state.unclaimed_troops)})")
            else:
                # Regular troop - add to unclaimed pot
                game_state.unclaimed_troops.append(ante_troop)
                troops_drawn_this_turn[0] += 1
                if logger:
                    logger.write(f"ACTION 0: ANTE - 1 troop (strength {ante_troop}) added to pot. Pot now: {len(game_state.unclaimed_troops)} troops, strength {sum(game_state.unclaimed_troops)}")
                if verbose:
                    print(f"  🎲 ANTE: 1 troop added to pot (now {len(game_state.unclaimed_troops)} troops, total strength {sum(game_state.unclaimed_troops)})")

        # PHASE 1: Draw event card
        if event_deck:
            drawn_card = player.draw_event_card(event_deck)
            if drawn_card:
                cards_drawn_this_turn += 1
                if verbose:
                    print(f"  Drew: {drawn_card.name}")
                if logger:
                    logger.log_card_effect(f"Drew card: {drawn_card.name}")
        else:
            # Event deck empty: shuffle discard pile
            if game_state.event_discard:
                game_state.event_deck = game_state.event_discard[:]
                random.shuffle(game_state.event_deck)
                game_state.event_discard.clear()
                if verbose:
                    print(f"  📚 Event deck reshuffled!")
        
        # PHASE 2: 🔥 EVENT CARD CHAINING LOOP (v1.8 NEW!)
        max_cards_per_turn = 20  # Safety limit
        chain_number = 0

        # 🔥 v1.17: Flag to prevent infinite Standard Contract loops
        standard_contract_failed_this_turn = False

        if verbose and len(player.hand) > 0:
            print(f"  🔗 CHAIN START (hand: {len(player.hand)} cards, influence: {player.influence})")

        while chain_number < max_cards_per_turn:
            # Choose card to play (pass flag to prevent infinite Standard Contract loops)
            card_to_play, target = choose_card_to_play(player, game_state, playbook,
                                                       standard_contract_failed=standard_contract_failed_this_turn,
                                                       verbose=verbose)

            if not card_to_play:
                break  # No more playable cards

            chain_number += 1

            # 🔥 v1.17: Check if this is a Standard Contract (non-card action)
            is_standard_contract = (card_to_play.name == "STANDARD_CONTRACT" and
                                   card_to_play.base_effect.get('is_standard_contract', False))

            if verbose:
                if is_standard_contract:
                    print(f"    Action #{chain_number}: Standard Contract (no card)", end="")
                else:
                    print(f"    Card #{chain_number}: {card_to_play.name}", end="")

            # Log card play
            if logger:
                if is_standard_contract:
                    logger.log_card_play(player.player_id, "Standard Contract", chain_number)
                else:
                    logger.log_card_play(player.player_id, card_to_play.name, chain_number)

            # 🔥 v1.17: Remove from hand ONLY if it's NOT a Standard Contract
            if not is_standard_contract:
                player.hand.remove(card_to_play)

            # Resolve card (pass troops counter for gather cards)
            success = resolve_event_card(player, card_to_play, game_state, playbook, target, troops_drawn_this_turn, logger)

            # 🔥 v1.17: If Standard Contract failed, set flag to prevent retrying
            if is_standard_contract and not success:
                standard_contract_failed_this_turn = True
                if verbose:
                    print(" ❌ FAILED - will not retry")
                if logger:
                    logger.write("  ❌ Standard Contract FAILED")
                    # Log detailed failure reasons
                    if player.influence < game_state.config.leader_contract_cost:
                        logger.write(f"     Reason: Insufficient influence ({player.influence} < {game_state.config.leader_contract_cost})")
                    elif len(game_state.unclaimed_troops) == 0:
                        logger.write(f"     Reason: No unclaimed troops in pot")
                    elif len(game_state.mage_market) == 0 and len(game_state.commander_market) == 0:
                        logger.write(f"     Reason: No leaders available in markets")
                    else:
                        logger.write(f"     Reason: Contract resolution failed (unknown)")

            if success:
                cards_played_this_turn += 1
                # 🔥 v1.17: Add to discard ONLY if it's NOT a Standard Contract
                if not is_standard_contract:
                    game_state.event_discard.append(card_to_play)

                # Log card effects
                if logger:
                    if 'attack' in card_to_play.card_type.value and target:
                        logger.log_card_effect(f"Attacked Player {target.player_id} (Towers: {target.towers})")
                    elif 'contract' in card_to_play.card_type.value:
                        logger.log_card_effect("Leader acquired!")
                    elif 'gather' in card_to_play.card_type.value:
                        troops_gained = troops_drawn_this_turn[0] - sum(game_state.troops_drawn_per_turn)
                        logger.log_card_effect(f"+{troops_gained} troops ({player.get_total_troop_count()} total)")
                    elif 'economic' in card_to_play.card_type.value:
                        logger.log_card_effect(f"Influence now: {player.influence}")

                if verbose:
                    if 'attack' in card_to_play.card_type.value and target:
                        print(f" → Attacked P{target.player_id} (Towers: {target.towers})")
                    elif 'contract' in card_to_play.card_type.value:
                        print(f" → Leader acquired!")
                    elif 'gather' in card_to_play.card_type.value:
                        print(f" → +{troops_drawn_this_turn[0] - sum(game_state.troops_drawn_per_turn)} troops ({player.get_total_troop_count()} total)")
                    elif 'economic' in card_to_play.card_type.value:
                        print(f" → Influence now: {player.influence}")
                    else:
                        print()  # Newline for other cards

            # 🔥 v1.15: TOWER DESTRUCTION ENDS TURN - Check if turn should end immediately
            if player.end_turn_now:
                if verbose:
                    print(f"  🛑 TURN ENDED: Tower destroyed (no more cards can be played)")
                if logger:
                    logger.write("🛑 TURN ENDED: Tower destroyed (no more cards can be played)")
                break

            # 🎯 STRATEGY DECISION: Continue chaining or stop?
            if not should_continue_chaining(player, game_state, cards_played_this_turn):
                if verbose:
                    print(f"  🛑 Chain stopped by strategy ({player.strategy.value})")
                break
        
        if verbose and cards_played_this_turn > 0:
            print(f"  ✅ CHAIN END: {cards_played_this_turn} cards played, {troops_drawn_this_turn[0]} troops drawn")
        elif verbose:
            print(f"  No playable cards")

        # Log turn end
        if logger:
            logger.log_turn_end(cards_played_this_turn, troops_drawn_this_turn[0])

        # 🔥 v1.17 HAND SIZE FLOOR: Hand refill mechanic - draw to INFLUENCE at end of turn
        # Hand size = current influence (tracks your power/economy)
        # Minimum 2 cards to prevent death spiral
        target_hand_size = max(2, player.influence)  # Minimum 2 cards (Hand Size Floor)
        if len(player.hand) < target_hand_size and event_deck:
            cards_to_draw = target_hand_size - len(player.hand)
            refilled = 0
            for _ in range(cards_to_draw):
                if event_deck:
                    drawn = player.draw_event_card(event_deck)
                    if drawn:
                        refilled += 1
                else:
                    # Reshuffle if deck empty
                    if game_state.event_discard:
                        game_state.event_deck = game_state.event_discard[:]
                        random.shuffle(game_state.event_deck)
                        game_state.event_discard.clear()
                        # Try drawing again
                        if event_deck:
                            drawn = player.draw_event_card(event_deck)
                            if drawn:
                                refilled += 1
            if refilled > 0 and verbose:
                print(f"  ♻️ HAND REFILL: Drew {refilled} cards to match influence (now {len(player.hand)} in hand, influence: {player.influence})")
            if refilled > 0 and logger:
                logger.write(f"♻️ HAND REFILL: Drew {refilled} cards to match influence (now {len(player.hand)} in hand, influence: {player.influence})")

        # Record metrics for this turn
        game_state.cards_drawn_per_turn.append(cards_drawn_this_turn)
        game_state.cards_played_per_turn.append(cards_played_this_turn)
        game_state.troops_drawn_per_turn.append(troops_drawn_this_turn[0])

        # PHASE 3: Check eliminations and game end
        for p in active_players:
            if p.towers <= 0 and not p.eliminated:
                p.eliminated = True
                if verbose:
                    print(f"  💀 Player {p.player_id} eliminated!")
                if logger:
                    logger.log_elimination(p.player_id, turn_count)
        
        if game_state.check_game_over():
            break
        
        # Check round progression (every player_count turns = 1 round)
        if turn_count % player_count == 0:
            game_state.current_round += 1
            if verbose:
                print(f"\n🔄 Round {game_state.current_round}")
                for p in game_state.get_active_players():
                    print(f"  Player {p.player_id}: {p.towers} towers, {p.influence} influence")
                print()
        
        # 🔥 v1.11: Reset momentum tracker for ALL players at end of round cycle
        # (attacked_last_turn only lasts one full turn cycle)
        if turn_count % len(active_players) == 0:
            for p in active_players:
                p.attacked_last_turn = False
        
        # 🔥 v1.12: Reset turn-based card effects at END of player's turn
        player.attacks_this_turn = 0  # Reset momentum stacking counter
        
        # Clear single-turn effects
        player.active_effects.pop('tactical_retreat', None)
        player.active_effects.pop('spoils_of_war', None)
        player.active_effects.pop('momentum', None)
        player.active_effects.pop('war_economy', None)
        player.active_effects.pop('guerrilla_tactics', None)
        player.active_effects.pop('vanguard_formation', None)  # 🔥 v1.15: Vanguard lasts whole turn

        # Note: fortified_position, plunder, chain_assault persist across turns until triggered/consumed
        # Note: siege_equipment, protective_wards consumed on use (next attack only)
        
        # Next player (🔥 v1.15: Respects play_direction)
        current_player_idx += game_state.play_direction
        
        # Safety check: troop deck depletion
        if not troop_deck:
            if verbose:
                print("🏁 Troop deck depleted!")
            
            # 🔥 v1.9.1: PUNISH DECK DEPLETION - Kill player with fewest towers!
            active_players = game_state.get_active_players()
            if len(active_players) > 1:
                # Find player(s) with fewest towers
                min_towers = min(p.towers for p in active_players)
                weakest_players = [p for p in active_players if p.towers == min_towers]
                
                # If there are multiple with same towers, eliminate the one with fewest armies
                if len(weakest_players) > 1:
                    victim = min(weakest_players, key=lambda p: len(p.armies))
                else:
                    victim = weakest_players[0]
                
                # ELIMINATE THE WEAKEST!
                victim.eliminated = True
                victim.towers = 0
                if verbose:
                    print(f"💀 Player {victim.player_id} eliminated by deck depletion (weakest player)!")
            
            game_state.check_game_over()
            break
    
    # Game over - collect results
    active_players = game_state.get_active_players()
    if active_players:
        winner = max(active_players, key=lambda p: (p.towers, p.towers_destroyed))
        game_state.winner = winner.player_id
    
    # Count early eliminations (eliminated in first 2 rounds)
    early_eliminations = sum(1 for p in players 
                           if p.eliminated and game_state.current_round <= 2)
    
    # Calculate card play/draw averages (EVENT + TROOP cards)
    avg_cards_played = sum(game_state.cards_played_per_turn) / len(game_state.cards_played_per_turn) if game_state.cards_played_per_turn else 0
    avg_event_cards_drawn = sum(game_state.cards_drawn_per_turn) / len(game_state.cards_drawn_per_turn) if game_state.cards_drawn_per_turn else 0
    avg_troop_cards_drawn = sum(game_state.troops_drawn_per_turn) / len(game_state.troops_drawn_per_turn) if game_state.troops_drawn_per_turn else 0
    avg_total_cards_drawn = avg_event_cards_drawn + avg_troop_cards_drawn  # TOTAL CHURN!
    max_cards_played_turn = max(game_state.cards_played_per_turn) if game_state.cards_played_per_turn else 0
    
    if verbose:
        print(f"\n🏆 GAME OVER")
        print(f"Winner: Player {game_state.winner}")
        print(f"Total turns: {turn_count}")
        print(f"Rounds: {game_state.current_round}")
        print(f"Contract plays: {game_state.contract_plays}")
        print(f"Attack plays: {game_state.attack_plays}")
        print(f"Early eliminations: {early_eliminations}")
        print(f"Avg event cards played/turn: {avg_cards_played:.2f}")
        print(f"Avg event cards drawn/turn: {avg_event_cards_drawn:.2f}")
        print(f"Avg troop cards drawn/turn: {avg_troop_cards_drawn:.2f}")
        print(f"Avg TOTAL cards drawn/turn: {avg_total_cards_drawn:.2f}")
        print(f"Max cards in one turn: {max_cards_played_turn}")
        print()
    
    # Build result dict
    result = {
        'winner': game_state.winner,
        'turns': turn_count,
        'rounds': game_state.current_round,
        'player_count': player_count,
        'contract_usage': game_state.contract_plays,
        'attack_frequency': game_state.attack_plays,
        'early_eliminations': early_eliminations,
        'early_elimination_rate': early_eliminations / player_count,
        'troop_deck_depleted': len(troop_deck) == 0,
        'towers_destroyed_total': game_state.towers_destroyed_total,
        'avg_cards_played_per_turn': avg_cards_played,
        'avg_cards_drawn_per_turn': avg_total_cards_drawn,  # TOTAL (event + troop)
        'avg_event_cards_drawn_per_turn': avg_event_cards_drawn,
        'avg_troop_cards_drawn_per_turn': avg_troop_cards_drawn,
        'max_cards_played_single_turn': max_cards_played_turn,
        'cards_played_per_turn': game_state.cards_played_per_turn,  # Full list for analysis
        'cards_drawn_per_turn': game_state.cards_drawn_per_turn,
        'troops_drawn_per_turn': game_state.troops_drawn_per_turn,
        'players': [
            {
                'player_id': p.player_id,
                'strategy': p.strategy.value,
                'towers': p.towers,
                'eliminated': p.eliminated,
                'towers_destroyed': p.towers_destroyed,
                'armies_destroyed': p.armies_destroyed,  # 🔥 v1.9: Track army kills
                'final_influence': p.influence,
                'final_army_count': len(p.armies),  # 🔥 v1.9: Number of armies
                'final_army_size': p.get_total_troop_count(),  # 🔥 v1.9: Total troops across all armies
                # 🎲 Include wildcard params for analysis
                'wildcard_aggression': p.wildcard_aggression if p.strategy == StrategyType.WILDCARD else None,
                'wildcard_chain_length': p.wildcard_chain_length if p.strategy == StrategyType.WILDCARD else None,
                'wildcard_risk_tolerance': p.wildcard_risk_tolerance if p.strategy == StrategyType.WILDCARD else None,
            }
            for p in players
        ]
    }
    
    # 🎲 Log wildcard wins (only if verbose mode enabled)
    winner = next((p for p in players if p.player_id == game_state.winner), None)
    if config.verbose and winner and winner.strategy == StrategyType.WILDCARD:
        print()
        print("="*80)
        print("🎲🏆 WILDCARD WIN! 🏆🎲")
        print("="*80)
        print(f"Player {winner.player_id} won with WILDCARD strategy!")
        print(f"  Aggression: {winner.wildcard_aggression:.2f} (0.0=passive, 1.0=hyper-aggressive)")
        print(f"  Chain Length: {winner.wildcard_chain_length} cards/turn max")
        print(f"  Risk Tolerance: {winner.wildcard_risk_tolerance:.2f} (0.0=safe, 1.0=risky)")
        print(f"  Actual avg cards/turn: {avg_cards_played:.2f}")
        print(f"  Final towers: {winner.towers}")
        print(f"  Towers destroyed: {winner.towers_destroyed}")
        print("This configuration should be studied! 🔬")
        print("="*80)
        print()

    # Log game end and close logger
    if logger:
        win_type = "TOWER_ADVANTAGE" if winner else "TIMEOUT"
        logger.log_game_end(game_state.winner, turn_count, win_type)
        logger.write('')
        logger.write('FINAL STATISTICS:')
        logger.write(f'  Total Turns: {turn_count}')
        logger.write(f'  Total Rounds: {game_state.current_round}')
        logger.write(f'  Avg Cards Played/Turn: {avg_cards_played:.2f}')
        logger.write(f'  Avg Cards Drawn/Turn: {avg_total_cards_drawn:.2f}')
        logger.write(f'  Total Eliminations: {sum(1 for p in players if p.eliminated)}')
        logger.write('')
        logger.close()

    return result

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("Battalion v1.7 Simulator - Two-Deck Revolution")
    print("=" * 60)
    print()
    
    # Test deck creation
    print("Testing deck creation...")
    config = GameConfig()
    
    # Test troop deck
    troop_deck = create_troop_deck(config)
    print(f"✅ Troop Deck: {len(troop_deck)} cards")
    print(f"  Rank 1: {troop_deck.count(1)} (33%), Rank 2: {troop_deck.count(2)} (25%), Rank 3: {troop_deck.count(3)} (20%)")
    print(f"  Rank 4: {troop_deck.count(4)} (15%), Rank 5: {troop_deck.count(5)} (7%)")
    
    # Test event deck
    event_deck = create_event_deck(config)
    print(f"✅ Event Deck: {len(event_deck)} cards")
    
    # Test event_card_power scaling
    print(f"✅ Event card power scaling: 0.5 default (moderate)")
    
    print()
    print("=" * 60)
    print("Running test game (verbose)...")
    print("=" * 60)
    print()
    
    # Run a single verbose game
    result = simulate_game(
        player_count=3,
        config=config,
        strategies=[StrategyType.RUSH, StrategyType.BUILDUP, StrategyType.TEMPO],
        verbose=True
    )
    
    print("=" * 60)
    print("Test game completed!")
    print("=" * 60)
    print()
    print("Running quick batch test (10 games)...")
    
    # Run batch of games silently
    results = []
    for i in range(10):
        result = simulate_game(player_count=3, config=config, verbose=False)
        results.append(result)
    
    # Analyze results
    avg_turns = sum(r['turns'] for r in results) / len(results)
    avg_rounds = sum(r['rounds'] for r in results) / len(results)
    total_early_elims = sum(r['early_eliminations'] for r in results)
    total_players = sum(r['player_count'] for r in results)
    early_elim_rate = (total_early_elims / total_players) * 100
    
    avg_contracts = sum(r['contract_usage'] for r in results) / len(results)
    avg_attacks = sum(r['attack_frequency'] for r in results) / len(results)
    
    print(f"✅ 10 games completed")
    print(f"   Average game length: {avg_turns:.1f} turns, {avg_rounds:.1f} rounds")
    print(f"   Early elimination rate: {early_elim_rate:.1f}% (Target: <10%)")
    print(f"   Average contracts per game: {avg_contracts:.1f}")
    print(f"   Average attacks per game: {avg_attacks:.1f}")
    print()
    
    if early_elim_rate <= 10.0:
        print("🎉 Early elimination protection WORKING!")
    else:
        print("⚠️ Early elimination rate too high - needs tuning")
    
    print()
    print("=" * 60)
    print("v1.7 Simulator Ready!")
    print("=" * 60)
    print()
    print("To run more comprehensive tests:")
    print("  python3 battalion_simulator_v17.py")
    print()
    print("To adjust event_card_power:")
    print("  config.event_card_power = 0.33  # Grindy")
    print("  config.event_card_power = 0.5   # Moderate (default)")
    print("  config.event_card_power = 1.0   # Wild")
    print("  config.event_card_power = 2.0   # Chaos")
