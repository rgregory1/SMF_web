import copy
from sheet import *


hero = {
  "melee_attack": 5,
  "melee_attack_rr": 1,
  "melee_defence": 5,
  "melee_defence_rr": 1,
  "ranged_attack_rr": 0,
  "ranged_defence": 4,
  "ranged_defence_rr": 0,
  "psyche_attack_rr": 0,
  "psyche_defence": 4,
  "psyche_defence_rr": 0,
  "hero_notes": [
    "Scrapper - reduce melee gang-up by -1D, and reflection minor power",
    "Scrapper - Anytime you successfully defend against a Body-damaging attack you can choose to make a Chance roll. On a 2+, your attack- er suffers 2 Body damage.",
    "Fortune - Recharge 2+, Gain +1D[1] on a defense roll against any attack. You can decide to use this ability after you have made your initial defense roll!",
    "Melee Speicialist - +2D on any checks to break objects or escape entangles."
  ],
  "hero_type": "Standard",
  "hero_archetype_list": [
    {
      "archetype": "Brawler",
      "power_name": "Brawler",
      "power_type": "Standard",
      "description": "You are a close in fighter who relies on sheer bravado,...",
      "move": 7,
      "body_points": 7,
      "psych_points": 6,
      "maj-p": [
        "Scrapper"
      ],
      "min_p_num": 2,
      "minor_p_list": [
        "Enhanced_Senses",
        "Fortune",
        "Iron_Will",
        "Melee_Specialist",
        "Regen",
        "Resistance",
        "Shield",
        "Super-Agility"
      ]
    }
  ],
  "hero_major_power_list": [
    {
      "power_name": "Scrapper",
      "power_type": "major",
      "description": "You're a resourceful, tenacious close-in fighter.  You possess the following abilities: +1D on melee attack rolls, +1D on melee defence rolls, reduce an melee gang-up bonus foes gain against you by -1D, and Counterattack: You posses the Reflection minor power limited to melee attacks.",
      "stat_changes": {
        "melee_attack": 1,
        "melee_defence": 1
      },
      "notes": [
        "Scrapper - reduce melee gang-up by -1D, and reflection minor power",
        "Scrapper - Anytime you successfully defend against a Body-damaging attack you can choose to make a Chance roll. On a 2+, your attack- er suffers 2 Body damage."
      ]
    }
  ],
  "hero_minor_power_list": [
    {
      "power_name": "Fortune",
      "power_type": "minor",
      "description": "You are darn lucky or capable of manipulating probabilities in your favor when it counts the most.",
      "stat_changes": {},
      "notes": [
        "Fortune - Recharge 2+, Gain +1D[1] on a defense roll against any attack. You can decide to use this ability after you have made your initial defense roll!"
      ]
    },
    {
      "power_name": "Melee Specialist",
      "power_type": "minor",
      "description": "+1 Re-roll on melee attack rolls, +1 Re-roll on melee defense rolls, and +2D on any checks to break objects or escape entangles.",
      "stat_changes": {
        "melee_attack_rr": 1,
        "melee_defence_rr": 1
      },
      "notes": [
        "Melee Speicialist - +2D on any checks to break objects or escape entangles."
      ]
    }
  ],
  "hero_backgrounds": [
    "Blue Collar",
    "Business"
  ],
  "loops": 0,
  "power_house_loop": 0,
  "hero_name": "Joe",
  "body_points": 7,
  "psych_points": 6,
  "move": 7,
  "minor_power_loops": 0,
  "boost_loops": 1
}

sheet_timestamp = print_hero(hero)