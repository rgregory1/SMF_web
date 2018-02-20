from flask import Flask, render_template, request, redirect, escape, jsonify, Response
import json
import os
import datetime
from functions import simplify_timestamp, arch_dict_adjustment, assign_base_points, assign_max_points


app = Flask(__name__)

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

# load information into dictionaries ---------------------------------------------------------------
with open('data/archetype_data.json') as f:
    arch_dict = json.load(f)



@app.route('/')
def entry_page():
    # first page, get hero name
    # temp_timestamp = str(datetime.datetime.now())
    # timestamp = simplify_timestamp(temp_timestamp)
    timestamp = '180220'
    try:
        os.makedirs(os.path.join('temp', timestamp))
    except:
        pass

    # grab hero dict
    with open('data/hero_start.json') as f:
        hero = json.load(f)
    with open('data/archetype_data.json') as f:
        arch_dict = json.load(f)

    temp_dump(hero, timestamp, 'hero')
    temp_dump(arch_dict, timestamp, 'arch_dict')

    return render_template('home.html', the_title='SMF Character Creator', timestamp=timestamp)

@app.route('/archetype_picker', methods=['POST'])
def archetype_page():
    timestamp = request.form['timestamp']
    # grab dictionaries for use
    hero = grab_from_temp(timestamp, 'hero')
    arch_dict = grab_from_temp(timestamp, 'arch_dict')

    # get hero name from last page/form
    heroname = request.form['heroname']

    #create and assign hero name in dict
    hero['hero_name'] = heroname

    temp_dump(hero, timestamp, 'hero')
    return render_template('archetype_picker.html', the_title='Archetype Picker Page', arch_dict=arch_dict, heroname=heroname, timestamp=timestamp)



@app.route('/setup_arch', methods=['POST'])
def setup_arch():


    timestamp = request.form['timestamp']
    archetype_choice = request.form['current_arch']

    # get hero stats from temp folder
    hero = grab_from_temp(timestamp, 'hero')
    arch_dict = grab_from_temp(timestamp, 'arch_dict')

    current_archetype, arch_dict = arch_dict_adjustment(archetype_choice, arch_dict)
    hero['hero_archetype_list'].append(current_archetype)
    hero['hero_type'] = hero['hero_archetype_list'][0]['power_type']

    # if chosen archetype is standard, set stats
    if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
        hero = assign_base_points(hero, hero['hero_archetype_list'][0])
    elif hero['hero_archetype_list'][0]['power_type'] == 'Super' or hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
        # creat new dict without alt power levels in it
        new_arch_dict = {}
        for d in arch_dict:
            if arch_dict[d]['power_type'] == 'Standard':
                new_arch_dict[d] = arch_dict[d].copy()
        hero['loops'] = hero['hero_archetype_list'][0]['archetype_number']
        temp_dump(new_arch_dict, timestamp, 'new_arch_dict')


    temp_dump(arch_dict, timestamp, 'arch_dict')
    temp_dump(hero, timestamp, 'hero')
    title = 'Here are your results for Henchmen and standard archetypes:'
    title2 = 'Here are your results for Powerhouse and Super archetypes:'
    loops = hero['loops']
    if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
        return render_template('results.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title)
    if hero['hero_archetype_list'][0]['power_type'] == 'Super' or hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
        return render_template('alt_power_arch_picker.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title2, loops=loops, new_arch_dict=new_arch_dict)
    # if hero['hero_archetype_list'][0]['power_type'] == 'Super' or hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
    #     return render_template('alt_power_arch_picker.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title2)

@app.route('/not_sure', methods=['POST'])
def not_sure():
    # grab info from form
    timestamp = request.form['timestamp']
    archetype_choice = request.form['current_arch']

    # get hero stats from temp folder
    hero = grab_from_temp(timestamp, 'hero')
    new_arch_dict = grab_from_temp(timestamp, 'new_arch_dict')
    current_archetype, new_arch_dict = arch_dict_adjustment(archetype_choice, new_arch_dict)
    hero['hero_archetype_list'].append(current_archetype)
    if len(hero['hero_archetype_list']) == 2:
        hero = assign_base_points(hero, hero['hero_archetype_list'][1])
    else:
        hero = assign_max_points(hero, hero['hero_archetype_list'][2])
    hero['loops'] -= 1

    temp_dump(arch_dict, timestamp, 'arch_dict')
    temp_dump(new_arch_dict, timestamp, 'new_arch_dict')
    temp_dump(hero, timestamp, 'hero')

    title = "not sure what's next"

    title2 = "here we go again"
    loops = hero['loops']
    if hero['loops'] == 0:
        return render_template('not_sure.html', the_title=title)
    if hero['loops'] > 0:
        return render_template('alt_power_arch_picker.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title2, loops=loops, new_arch_dict=new_arch_dict)

app.run(debug=True)
