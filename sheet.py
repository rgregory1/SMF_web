from PIL import ImageFont, ImageDraw
from PIL import Image
import os
from functions import simplify_timestamp
import datetime
import textwrap


def print_hero(hero, basedir):
    if hero['hero_archetype_list'][0]['archetype'] == 'Henchmen':
        im = Image.open(os.path.join(basedir,'character_sheet_hench.png'))
    else:
        im = Image.open(os.path.join(basedir,'character_sheet.png'))
    draw = ImageDraw.Draw(im)
    heroid_large = ImageFont.truetype(os.path.join(basedir,'Heroid.ttf'), 42)
    heroid = ImageFont.truetype(os.path.join(basedir,'Heroid.ttf'), 35)
    heroid_small = ImageFont.truetype(os.path.join(basedir,'Heroid.ttf'), 25)
    # heroid_large is 41px tall



    # print out the name and archetype(s)

    if len(hero['hero_archetype_list']) == 1:
        if hero['hero_archetype_list'][0]['archetype'] == 'Henchmen':
            henchman_name = hero['hero_name'] + ' (Henchmen)'
            draw.text((333,119), henchman_name, fill='grey', font=heroid_large)
        else:
            draw.text((333,119), hero['hero_name'], fill='grey', font=heroid_large)
        draw.text((522,205), hero['hero_archetype_list'][0]['archetype'], fill='grey', font=heroid_large)
    if len(hero['hero_archetype_list']) == 2:
        super_name = hero['hero_name'] + ' (Super)'
        draw.text((333,119), super_name, fill='grey', font=heroid_large)
        draw.text((522,205), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=heroid_large)
    if len(hero['hero_archetype_list']) == 3:
        powerhouse_name = hero['hero_name'] + ' (Powerhouse)'
        draw.text((333,119), powerhouse_name, fill='grey', font=heroid_large)
        draw.text((522,205), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=heroid_large)
        draw.text((522,246), hero['hero_archetype_list'][2]['archetype'], fill='grey', font=heroid_large)

    # print out the hero's move
    draw.text((294,290), str(hero['move']), fill='grey', font=heroid_large)

    if hero['hero_archetype_list'][0]['archetype'] == 'Henchmen':
        draw.text((408,367), str(hero['numbers']), fill='grey', font=heroid_large)
    else:
        # print out the hero's body
        draw.text((294,367), str(hero['body_points']), fill='grey', font=heroid_large)

        # print out the hero's psyche
        draw.text((348,473), str(hero['psych_points']), fill='grey', font=heroid_large)

    # print out the hero's melee attack and defence
    draw.text((515,585), str(hero['melee_attack']), fill='grey', font=heroid_large)
    if hero['melee_attack_rr'] > 0:
        draw.text((620,585), str(hero['melee_attack_rr']), fill='grey', font=heroid_large)
    draw.text((1222,585), str(hero['melee_defence']), fill='grey', font=heroid_large)
    if hero['melee_attack_rr'] > 0:
        draw.text((1327,585), str(hero['melee_defence_rr']), fill='grey', font=heroid_large)

    # print out the hero's ranged attack and defence
    if 'ranged_attack' in hero:
        draw.text((515,697), str(hero['ranged_attack']), fill='grey', font=heroid_large)
    if hero['ranged_attack_rr'] > 0:
        draw.text((620,697), str(hero['ranged_attack_rr']), fill='grey', font=heroid_large)
    draw.text((1222,697), str(hero['ranged_defence']), fill='grey', font=heroid_large)
    if hero['ranged_attack_rr'] > 0:
        draw.text((1327,697), str(hero['ranged_defence_rr']), fill='grey', font=heroid_large)

    # print out the hero's psyche attack and defence
    if 'psyche_attack' in hero:
        draw.text((515,811), str(hero['psyche_attack']), fill='grey', font=heroid_large)
    if hero['psyche_attack_rr'] > 0:
        draw.text((620,811), str(hero['psyche_attack_rr']), fill='grey', font=heroid_large)
    draw.text((1222,811), str(hero['psyche_defence']), fill='grey', font=heroid_large)
    if hero['psyche_attack_rr'] > 0:
        draw.text((1327,811), str(hero['psyche_defence_rr']), fill='grey', font=heroid_large)

    # if len(hero['hero_major_power_list']) > 1:
    majorpower_height = 1013
    for majorpower in hero['hero_major_power_list']:
        draw.text((119, majorpower_height), majorpower['power_name'], fill='grey', font=heroid_large)
        majorpower_height = majorpower_height + 40

    minorpower_height = 1013
    for minorpower in hero['hero_minor_power_list']:
        draw.text((797, minorpower_height), minorpower['power_name'], fill='grey', font=heroid_large)
        minorpower_height = minorpower_height + 40

    background_height = 1226
    for background in hero['hero_backgrounds']:
        draw.text((119, background_height), background, fill='grey', font=heroid_large)
        background_height = background_height + 40


    # print out notes
    notes_height = 1400
    for note in hero['hero_notes']:
        notes_wrapped = textwrap.wrap(note, width=75)
        notes_height = notes_height + 10
        for line in notes_wrapped:
            draw.multiline_text((95,notes_height), line, fill='grey', font=heroid_small)
            notes_height = notes_height + 35





    temp_timestamp = str(datetime.datetime.now())
    sheet_timestamp = simplify_timestamp(temp_timestamp)

    suffix = '.png'
    im.save(os.path.join(basedir,'static', 'hero_files', hero['hero_name'] + '_' + sheet_timestamp + suffix))
    # im.save('static/hero_files/text.png')

    # find height of fonts
    # width, height = draw.textsize(hero['hero_name'], font=heroid_large)
    # print('width: ' + str(width))
    # print('height: ' + str(height))
    return sheet_timestamp
