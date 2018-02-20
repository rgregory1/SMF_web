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
