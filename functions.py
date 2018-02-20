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
