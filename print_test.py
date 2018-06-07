import copy
from sheet import *


hero = {
  "melee_attack": 4,
  "melee_attack_rr": 0,
  "melee_defence": 4,
  "melee_defence_rr": 1,
  "ranged_attack_rr": 1,
  "ranged_defence": 4,
  "ranged_defence_rr": 1,
  "psyche_attack_rr": 0,
  "psyche_defence": 4,
  "psyche_defence_rr": 0,
  "hero_notes": [
    "Super-Agility - +1D on Knock down checks, move along verticle surfaces, and spend a Move action to move 15in",
    "Power Blasts (Minor) - You can make 15in ranged attacks that inflict Body Damage"
  ],
  "hero_type": "Street Level",
  "hero_archetype_list": [
    {
      "archetype": "Street Level",
      "power_name": "Street Level",
      "power_type": "Street Level",
      "description": "You are a hero or villain whose habits and powers keep you close to the streets. Protecting a neighborhood or small borough, or pulling small jobs like bank heists are your specialty.",
      "move": 6,
      "body_points": 5,
      "psych_points": 5,
      "maj-p": [],
      "min_p_num": 2,
      "minor_p_list": [
        "Armor",
        "Amphibious",
        "Barrier",
        "Burrowing",
        "Construct-Speed",
        "Construct-Tough",
        "Damage_Field",
        "Density_Decrease",
        "Density_Increase",
        "Dispel",
        "Duplicate",
        "Enhance_(Minor)",
        "Enhanced_Senses",
        "Entangle",
        "Explosion",
        "Flight",
        "Force-Field",
        "Fortune",
        "Gadgets",
        "Grenades",
        "Growth",
        "Giant",
        "Invisibility",
        "Iron_Will",
        "Leaping",
        "Magic_Artifact",
        "Massive",
        "Melee_Specialist",
        "Mimic",
        "Multiple_Limbes",
        "Obscurement",
        "Parasite",
        "Power_Blasts_(Minor)",
        "Rage",
        "Rapport",
        "Regen",
        "Resistance",
        "Reflection",
        "Savant",
        "Save",
        "Servitor-Sidekick",
        "Shield",
        "Shrinking",
        "Sonic_Blasts",
        "Stun",
        "Super-Agility",
        "Super-Strength_(Minor)",
        "Telekinesis",
        "Teleport",
        "Vampire",
        "X-Factor"
      ]
    }
  ],
  "hero_major_power_list": [],
  "hero_minor_power_list": [
    {
      "power_name": "Super-Agility",
      "power_type": "minor",
      "description": "You gain +2in to your move and +1 Re-roll on all defense checks against Body damaging attacks, and any check to avoid being knocked down. You can move up, hang from, and walk along vertical surfaces as if they were normal ground. You can also spend a Move action to move between structures or other vertical terrain pieces within 15in of each other.",
      "stat_changes": {
        "move": 2,
        "melee_defence_rr": 1,
        "ranged_defence_rr": 1
      },
      "notes": [
        "Super-Agility - +1D on Knock down checks, move along verticle surfaces, and spend a Move action to move 15in"
      ]
    },
    {
      "power_name": "Power Blasts (Minor)",
      "power_type": "minor",
      "description": "You shoot blasts of power (concussive force, cosmic energy, electricity, etc.) from your eyes or hands.",
      "stat_changes": {
        "ranged_attack": 1,
        "ranged_attack_rr": 1
      },
      "notes": [
        "Power Blasts (Minor) - You can make 15in ranged attacks that inflict Body Damage"
      ]
    }
  ],
  "hero_backgrounds": [
    "Arcane",
    "Athletics"
  ],
  "loops": 0,
  "power_house_loop": 0,
  "hero_name": "Test Guy",
  "body_points": 5,
  "psych_points": 5,
  "move": 8,
  "minor_power_loops": 0,
  "boost_loops": 1,
  "ranged_attack": 5,
  "tagline": "Fastest Mutant Alive"
}

hero2 = {
  "melee_attack": 4,
  "melee_attack_rr": 0,
  "melee_defence": 4,
  "melee_defence_rr": 0,
  "ranged_attack_rr": 0,
  "ranged_defence": 4,
  "ranged_defence_rr": 0,
  "psyche_attack_rr": 1,
  "psyche_defence": 4,
  "psyche_defence_rr": 0,
  "hero_notes": [
    "Sorcery - (Recharge 2+) You can access two powers from your grimoire each turn, but you must follow the normal rules for activating each power. Once you use one of these powers during a game, note it. You cannot use it again unless you make a 2+ Recharge roll for it. Any power you activate lasts until the beginning of your next turn.",
    "Sorcery - If a power in your grimoire has two Recharge rolls, one for Sorcery and one for the power itself, always use the harder of the two rolls to see if the power returns for use. Any power that also possesses some ability to push or extend its capabil- ities is +1 harder to Recharge with Sorcery.",
    "Power Blasts (Major)- 30in range, body damage",
    "Grimoire - Teleport - Teleporting costs a move action, and when you do so make a goal roll. You move up to 10in + 5in per goal scored. You can move to any point on the board whether you can see it or not. If you teleport out of melee combat, your foe still gets a free attack on you. If you are knocked back from a successful hit, measure your teleport distance from the point where your knockback ends.",
    "Grimoire - Entangle - 10in Range, 5D Body-based entangle attack that does no damage",
    "Grimoire - Dispel - Spend a combat action against a single foe in melee or up to 5in away and make a 5D opposed Psyche attack. This does no damage. On a success, each goal you win by cancels one of the target's powers or boosts of your choice (major powers require 2 goals). Your opponent loses access to the power(s) you choose to cancel until the start of your next turn.",
    "Grimoire - Force-Field - Decide when you acquire this power whether it shields against Body or Psyche damage. Your Force-Field grants you a separate 4D defense goal roll against incoming attacks. If an attack gets through, you must make a second defense goal roll against the full incoming attack.",
    "Grimoire - Force-Field - You may also protect additional characters within 10in of you. Use a special action and make a 4D check and note your goals - 2 goals = 1 character 3 goals = 2 characters 4 goals = 3 characters. Decide which characters to protect before making your check. Protected characters must remain within 10in of you to enjoy your Force-Fields benefits.",
    "Grimoire - Force-Field - (Recharge 2+) Maximum Protection - You can push your Force-Field to its limits, rolling 6D instead of 4D for its protection, but succeed or fail, the power shuts down after this one enhanced use. You must decide to push your field prior to your foes attack goal roll.",
    "Sonic Blasts - 15in Psyche-Damage ranged attack"
  ],
  "hero_type": "Standard",
  "hero_archetype_list": [
    {
      "archetype": "Sorcerer",
      "power_name": "Sorcerer",
      "power_type": "Standard",
      "description": "You practice the arts arcane. You use your magic to unlock mysteries and delve into new worlds, and your spells are a boon to your allies.",
      "move": 6,
      "body_points": 6,
      "psych_points": 8,
      "maj-p": [
        "Sorcery"
      ],
      "min_p_num": 1,
      "minor_p_list": [
        "Flight",
        "Entangle",
        "Iron_Will",
        "Jinx",
        "Rapport",
        "Sonic_Blasts",
        "Summoning",
        "Teleport"
      ]
    }
  ],
  "hero_major_power_list": [
    {
      "power_name": "Sorcery",
      "power_type": "major",
      "description": "Your knowledge of the arcane arts makes you a dangerous and versatile foe.",
      "additional_minor_powers": [],
      "additional_minor_power_restrictions": [
        "Magic_Artifact",
        "Shield"
      ],
      "additional_power_prefix": "Grimoire",
      "add_major_powers_number": 1,
      "add_minor_powers_number": 4,
      "stat_changes": {},
      "notes": [
        "Sorcery - (Recharge 2+) You can access two powers from your grimoire each turn, but you must follow the normal rules for activating each power. Once you use one of these powers during a game, note it. You cannot use it again unless you make a 2+ Recharge roll for it. Any power you activate lasts until the beginning of your next turn.",
        "Sorcery - If a power in your grimoire has two Recharge rolls, one for Sorcery and one for the power itself, always use the harder of the two rolls to see if the power returns for use. Any power that also possesses some ability to push or extend its capabil- ities is +1 harder to Recharge with Sorcery."
      ]
    },
    {
      "power_name": "Grimoire - Power Blasts",
      "power_type": "major",
      "description": "You shoot blasts of power (concussive force, cosmic energy, electricity, etc.) from your eyes or hands.  You can make 30in ranged attacks at +2D[1].  Your blasts are physical in nature and inflict Body Damage",
      "stat_changes": {
        "ranged_attack": 2,
        "ranged_attack_rr": 1
      },
      "notes": [
        "Power Blasts (Major)- 30in range, body damage"
      ]
    }
  ],
  "hero_minor_power_list": [
    {
      "power_name": "Grimoire - Teleport",
      "power_type": "minor",
      "description": "You can move from one point to another instantaneously!",
      "stat_changes": {},
      "notes": [
        "Grimoire - Teleport - Teleporting costs a move action, and when you do so make a goal roll. You move up to 10in + 5in per goal scored. You can move to any point on the board whether you can see it or not. If you teleport out of melee combat, your foe still gets a free attack on you. If you are knocked back from a successful hit, measure your teleport distance from the point where your knockback ends."
      ]
    },
    {
      "power_name": "Grimoire - Entangle",
      "power_type": "minor",
      "description": "You can entrap foes with a ranged attack up to 10in away. This could be summoned tentacles, plant vines, elastic limbs, telekinesis, or anything else you can think of.",
      "stat_changes": {},
      "notes": [
        "Grimoire - Entangle - 10in Range, 5D Body-based entangle attack that does no damage"
      ]
    },
    {
      "power_name": "Grimoire - Dispel",
      "power_type": "minor",
      "description": "You can nullify your opponent's powers or power effects.",
      "stat_changes": {},
      "notes": [
        "Grimoire - Dispel - Spend a combat action against a single foe in melee or up to 5in away and make a 5D opposed Psyche attack. This does no damage. On a success, each goal you win by cancels one of the target's powers or boosts of your choice (major powers require 2 goals). Your opponent loses access to the power(s) you choose to cancel until the start of your next turn."
      ]
    },
    {
      "power_name": "Grimoire - Force-Field",
      "power_type": "minor",
      "description": "You wield protective energies. Decide when you acquire this power whether it shields against Body or Psyche damage. Your Force-Field grants you a separate 4D defense goal roll against incoming attacks.",
      "stat_changes": {},
      "notes": [
        "Grimoire - Force-Field - Decide when you acquire this power whether it shields against Body or Psyche damage. Your Force-Field grants you a separate 4D defense goal roll against incoming attacks. If an attack gets through, you must make a second defense goal roll against the full incoming attack.",
        "Grimoire - Force-Field - You may also protect additional characters within 10in of you. Use a special action and make a 4D check and note your goals - 2 goals = 1 character 3 goals = 2 characters 4 goals = 3 characters. Decide which characters to protect before making your check. Protected characters must remain within 10in of you to enjoy your Force-Fields benefits.",
        "Grimoire - Force-Field - (Recharge 2+) Maximum Protection - You can push your Force-Field to its limits, rolling 6D instead of 4D for its protection, but succeed or fail, the power shuts down after this one enhanced use. You must decide to push your field prior to your foes attack goal roll."
      ]
    },
    {
      "power_name": "Sonic Blasts",
      "power_type": "minor",
      "description": "You possess sonic powers you can direct at foes with maddening force! This is a 4D[1], 15in Psyche-damage ranged attack.",
      "stat_changes": {
        "psyche_attack": 0,
        "psyche_attack_rr": 1
      },
      "notes": [
        "Sonic Blasts - 15in Psyche-Damage ranged attack"
      ]
    }
  ],
  "hero_backgrounds": [
    "Arcane",
    "Medicine"
  ],
  "loops": 0,
  "power_house_loop": 0,
  "hero_name": "Shaman",
  "body_points": 6,
  "psych_points": 8,
  "move": 6,
  "archery_sorcery_loops": 0,
  "minor_power_loops": 0,
  "boost_loops": 1,
  "psyche_attack": 4
}

basedir = os.path.abspath(os.path.dirname(__file__))

sheet_timestamp = print_hero(hero, basedir)
