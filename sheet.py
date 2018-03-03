from PIL import ImageFont, ImageDraw
from PIL import Image
import os
from functions import simplify_timestamp
import datetime
import textwrap


def print_hero(hero):
    im = Image.open("character_sheet.png")
    draw = ImageDraw.Draw(im)
    heroid_large = ImageFont.truetype("Heroid.ttf", 42)
    heroid = ImageFont.truetype("Heroid.ttf", 35)
    heroid_small = ImageFont.truetype("Heroid.ttf", 25)
    # heroid_large is 41px tall

    draw.text((333,119), hero['hero_name'], fill='grey', font=heroid_large)

    # print out the archetype(s)
    if len(hero['hero_archetype_list']) == 1:
        draw.text((522,205), hero['hero_archetype_list'][0]['archetype'], fill='grey', font=heroid_large)
    if len(hero['hero_archetype_list']) == 2:
        draw.text((522,205), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=heroid_large)
    if len(hero['hero_archetype_list']) == 3:
        draw.text((522,205), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=heroid_large)
        draw.text((522,205), hero['hero_archetype_list'][2]['archetype'], fill='grey', font=heroid_large)

    # print out the hero's move
    draw.text((294,290), str(hero['move']), fill='grey', font=heroid_large)

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



    # print out notes
    notes_height = 1400
    for note in hero['hero_notes']:
        notes_wrapped = textwrap.wrap(note, width=75)
        notes_height = notes_height + 10
        for line in notes_wrapped:
            draw.multiline_text((95,notes_height), line, fill='grey', font=heroid_small)
            notes_height = notes_height + 40





    temp_timestamp = str(datetime.datetime.now())
    sheet_timestamp = simplify_timestamp(temp_timestamp)

    suffix = '.png'
    im.save(os.path.join('static', 'hero_files', hero['hero_name'] + '_' + sheet_timestamp + suffix))
    # im.save('static/hero_files/text.png')

    # find height of fonts
    # width, height = draw.textsize(hero['hero_name'], font=heroid_large)
    # print('width: ' + str(width))
    # print('height: ' + str(height))
    return sheet_timestamp
