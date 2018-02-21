from flask import Flask, render_template, request, redirect, escape, jsonify, Response
import json
import os
import datetime
from functions import *


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
    with open('data/major_power_data.json') as f:
        major_power_data = json.load(f)


    temp_dump(hero, timestamp, 'hero')
    temp_dump(arch_dict, timestamp, 'arch_dict')
    temp_dump(major_power_data, timestamp, 'major_power_data')

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
    # this totally works, just seeing about a different path below
    # if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
    #     return render_template('results.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title)
    if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
        return render_template('arch_results.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title)
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

@app.route('/begin_major_power', methods=['POST'])
def begin_major_power():
    timestamp = request.form['timestamp']
    hero = grab_from_temp(timestamp, 'hero')
    major_power_data = grab_from_temp(timestamp, 'major_power_data')
    mutable_archetype_list = hero['hero_archetype_list']

    # drop powerhouse and super from list
    if len(mutable_archetype_list) == 2:
        del mutable_archetype_list[0]
    # second if equals powerhouse
    if len(mutable_archetype_list) == 3:
        del mutable_archetype_list[0]

    arch = mutable_archetype_list[0]

    if len(arch['maj-p']) == 0:
        # del mutable_archetype_list[0]
        return render_template('begin_minor_power.html', timestamp=timestamp)
    elif len(arch['maj-p']) == 1:
        current_major_power_name = arch['maj-p'][0]
        for majorpower in major_power_data:
            if current_major_power_name == major_power_data[majorpower]['power_name']:
                current_major_power = major_power_data[majorpower].copy()
                break
        temp_dump(current_major_power, timestamp, 'current_major_power')   # just for testing
        # assign major power choice to the hero dict
        hero['hero_major_power_list'].append(current_major_power)

        # adjust stats based on major power choosen
        hero = hero_stat_adjust(hero,current_major_power['stat_changes'])
        # Add notes from Major Power
        hero['hero_notes'].extend(current_major_power['notes'])
        temp_dump(hero, timestamp, 'hero')
        return 'Finished up a major power'
        # return render_template('begin_minor_power.html', timestamp=timestamp, the_current_major_power_name=current_major_power_name)
    else:
        return render_template('major_power_chooser.html')

@app.route('/begin_minor_power', methods=['POST'])
def begin_minor_power():
    return 'begin minor power'

app.run(debug=True)
