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
  "hero_name": "Little Guy",
  "body_points": 5,
  "psych_points": 5,
  "move": 8,
  "minor_power_loops": 0,
  "boost_loops": 1,
  "ranged_attack": 5
}

basedir = os.path.abspath(os.path.dirname(__file__))

sheet_timestamp = print_hero(hero, basedir)
