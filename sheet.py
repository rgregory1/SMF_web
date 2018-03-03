from PIL import ImageFont, ImageDraw
from PIL import Image
import os
from functions import simplify_timestamp
import datetime


def print_hero(hero):
    im = Image.open("blank_sheet.png")
    draw = ImageDraw.Draw(im)
    avengerFont = ImageFont.truetype("AMA.ttf", 36)
    draw.text((395,319), hero['hero_name'], fill='grey', font=avengerFont)


    if len(hero['hero_archetype_list']) == 1:
        draw.text((500,400), hero['hero_archetype_list'][0]['archetype'], fill='grey', font=avengerFont)
    if len(hero['hero_archetype_list']) == 2:
        draw.text((500,400), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=avengerFont)
    if len(hero['hero_archetype_list']) == 3:
        draw.text((500,400), hero['hero_archetype_list'][1]['archetype'], fill='grey', font=avengerFont)
        draw.text((500,400), hero['hero_archetype_list'][2]['archetype'], fill='grey', font=avengerFont)
    draw.text((200,1600), hero['hero_notes'][1], fill='grey', font=avengerFont)

    temp_timestamp = str(datetime.datetime.now())
    sheet_timestamp = simplify_timestamp(temp_timestamp)

    suffix = '.png'
    im.save(os.path.join('static', 'hero_files', hero['hero_name'] + '_' + sheet_timestamp + suffix))
    # im.save('static/hero_files/text.png')
    return sheet_timestamp
