import os
import json


def simplify_timestamp(timestamp):
    chars = '-:. '
    for c in chars:
        timestamp = timestamp.replace(c, '')
    timestamp = timestamp[:-4]
    return(timestamp)

def arch_dict_adjustment(archetype_choice, arch_dict):
    for archetype in arch_dict:
        if archetype_choice == arch_dict[archetype]['power_name']:
            # set hero archetype/power to one chosen from list
            final = arch_dict.pop(archetype)
            break
    return(final, arch_dict)

def assign_base_points(hero_info, new):
    """ assigns base points from archetype to main dictionary """
    hero_info['body_points'] = new['body_points']
    hero_info['psych_points'] = new['psych_points']
    hero_info['move'] = new['move']
    if 'numbers' in new:
        hero_info['numbers'] = new['numbers']
    return(hero_info)

def assign_max_points(hero_info, new):
    """ assigns max points from archetype to main dictionary """
    hero_info['body_points'] = max(new['body_points'], hero_info['body_points'])
    hero_info['psych_points'] = max(new['psych_points'], hero_info['psych_points'])
    hero_info['move'] = max(new['move'], hero_info['move'])
    return(hero_info)

def hero_stat_adjust(base,adjusts):
    """retrun hero dict with adjusted stats"""
    for key in adjusts:
        base[key] = base.get(key, 4) + adjusts[key]
    return base

def temp_dump(hero, timestamp, datatype):
    """takes hero dict and turns it into a json file in the temp directory"""
    suffix = '.json'
    with open(os.path.join('temp', timestamp, datatype + suffix), 'w') as f:
        json.dump(hero, f, indent=2)

def grab_from_temp(timestamp, datatype):
    """grabs hero dict from json file in temp folder"""
    suffix = '.json'
    with open(os.path.join('temp', timestamp, datatype + suffix)) as f:
        hero = json.load(f)
    return hero
