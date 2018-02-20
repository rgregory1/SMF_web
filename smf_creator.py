from flask import Flask, render_template, request, redirect, escape, jsonify, Response
import json
import os
import datetime
from functions import simplify_timestamp, arch_dict_adjustment


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
    return render_template('home.html', the_title='SMF Character Creator')

@app.route('/archetype_picker', methods=['POST'])
def archetype_page():
    # temp_timestamp = str(datetime.datetime.now())
    # timestamp = simplify_timestamp(temp_timestamp)
    timestamp = 'temp'
    try:
        os.makedirs(os.path.join('temp', timestamp))
    except:
        pass

    # grab hero dict
    with open('data/hero_start.json') as f:
        hero = json.load(f)
    with open('data/archetype_data.json') as f:
        arch_dict = json.load(f)

    temp_dump(arch_dict, timestamp, 'arch_dict')
    # get hero name from last page/form
    heroname = request.form['heroname']

    #create and assign hero name in dict
    hero['hero_name'] = heroname

    temp_dump(hero, timestamp, 'hero')
    return render_template('archetype_picker.html', the_title='Archetype Picker Page', arch_dict=arch_dict, heroname=heroname, timestamp=timestamp)



@app.route('/setup_arch', methods=['POST'])
def setup_current_arch():


    timestamp = request.form['timestamp']
    archetype_choice = request.form['current_arch']

    # get hero stats from temp folder
    #hero = grab_hero(timestamp)
    hero = grab_from_temp(timestamp, 'hero')
    arch_dict = grab_from_temp(timestamp, 'arch_dict')

    current_archetype, arch_dict = arch_dict_adjustment(archetype_choice, arch_dict)

    temp_dump(arch_dict, timestamp, 'arch_dict')
    hero['hero_archetype_list'].append(current_archetype)
    title = 'Here are your results:'
    return render_template('results.html', the_archetype_choice=archetype_choice, timestamp=timestamp)



app.run(debug=True)
