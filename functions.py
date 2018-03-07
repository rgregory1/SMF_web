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

def temp_dump(hero, timestamp, datatype, basedir):
    """takes hero dict and turns it into a json file in the temp directory"""
    suffix = '.json'
    with open(os.path.join(basedir,'static','temp', timestamp, datatype + suffix), 'w') as f:
        json.dump(hero, f, indent=2)

def grab_from_temp(timestamp, datatype):
    """grabs hero dict from json file in temp folder"""
    suffix = '.json'
    with open(os.path.join('static','temp', timestamp, datatype + suffix)) as f:
        hero = json.load(f)
    return hero

def make_dict_from_list(power_list, power_dict):
    """give a list of power names, compare to a dict of powers, return dict of powers from the list"""
    current_power_dict = {}
    for complete_power in power_dict:
        for power_name in power_list:
            if complete_power == power_name:
                current_power_dict[complete_power] = power_dict[complete_power].copy()
    return current_power_dict

def assign_power_from_dict(current_power_name, current_dict):
    """give power name and dict of powers, return variable with only one dictionary"""
    current_power_dict = {}
    for power in current_dict:
        if current_power_name == current_dict[power]['power_name']:
            current_power_dict = current_dict[power].copy()
    return current_power_dict


def pop_dict_from_dicts(current_power_name, current_dict):
    for power in current_dict:
        if current_power_name == current_dict[power]['power_name']:
            final = current_dict.pop(power)
            break
    return(final, current_dict)

def henchman_stat_redux(henchmen_group):
    redux_stats = ['melee_attack', 'melee_defence', 'ranged_attack', 'ranged_defence', 'psyche_attack', 'psyche_defence']
    for redux_stat in redux_stats:
        for hero_key, hero_value in henchmen_group.items():
            if hero_key == redux_stat:
                if hero_value == 4:
                    henchmen_group[hero_key] = 2
                if hero_value == 5 or hero_value == 6:
                    henchmen_group[hero_key] = 3
    return(henchmen_group)
