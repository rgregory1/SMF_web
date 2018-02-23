from flask import Flask, render_template, request, redirect, escape, jsonify, Response
import json
import os
import datetime
from functions import *


app = Flask(__name__)



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
    with open('data/minor_power_data.json') as f:
        minor_power_data = json.load(f)


    temp_dump(hero, timestamp, 'hero')
    temp_dump(arch_dict, timestamp, 'arch_dict')
    temp_dump(major_power_data, timestamp, 'major_power_data')
    temp_dump(minor_power_data, timestamp, 'minor_power_data')

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
    if hero['hero_archetype_list'][0]['power_type'] == 'Super' or hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
        return render_template('alt_power_arch_picker.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title2, loops=loops, new_arch_dict=new_arch_dict)

    #if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
    else:
        return render_template('arch_results.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title)


@app.route('/archetype_loop', methods=['POST'])
def archetype_loop():
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

    title = "Finished with Archetypes"

    title2 = "Additional Archetype Choice"
    powerhouse_archetype_choice = "Powerhouse"
    loops = hero['loops']
    if hero['loops'] == 0:
        if hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
            hero_archetype_list = hero['hero_archetype_list']
            return render_template('arch_results_powerhouse.html', hero_archetype_list=hero_archetype_list, timestamp=timestamp, the_title=title)
        if hero['hero_archetype_list'][0]['power_type'] == 'Super':
            return render_template('arch_results_super.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title)
        # return render_template('not_sure.html', the_title=title)
    if hero['loops'] > 0:
        return render_template('alt_power_arch_picker.html', the_archetype_choice=powerhouse_archetype_choice, timestamp=timestamp, the_title=title2, loops=loops, new_arch_dict=new_arch_dict)

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
    temp_dump(arch, timestamp, 'current_arch')   # testing if this new location works
    # holy cow, highly exprimental deletion here, I think it can help me with the loop
    del mutable_archetype_list[0]
    temp_dump(mutable_archetype_list, timestamp, 'mutable_archetype_list')

    if len(arch['maj-p']) == 0:

        title = 'You have no Major Power with this Archetype...'
        return render_template('minor_power_begin_no_major.html', timestamp=timestamp, the_current_arch=arch, the_title=title)
    elif len(arch['maj-p']) == 1:
        current_major_power_name = arch['maj-p'][0]
        for majorpower in major_power_data:
            if current_major_power_name == major_power_data[majorpower]['power_name']:
                current_major_power = major_power_data[majorpower].copy()
                break

        # assign major power choice to the hero dict
        hero['hero_major_power_list'].append(current_major_power)

        # adjust stats based on major power choosen
        hero = hero_stat_adjust(hero,current_major_power['stat_changes'])
        # Add notes from Major Power
        hero['hero_notes'].extend(current_major_power['notes'])


        temp_dump(current_major_power, timestamp, 'current_major_power')
        # temp_dump(arch, timestamp, 'current_arch') testing if moving to before loop works
        temp_dump(hero, timestamp, 'hero')
        if current_major_power['power_name'] == 'Sorcery':
            with open('data/major_power_data.json') as f:
                sorcery_maj_power_dict = json.load(f)
            del sorcery_maj_power_dict['Sorcery']
            for power in sorcery_maj_power_dict:
                sorcery_maj_power_dict[power]['power_name'] = 'Grimoire - ' + sorcery_maj_power_dict[power]['power_name']



            temp_dump(sorcery_maj_power_dict, timestamp, 'sorcery_maj_power_dict')

            message = "Sorcerers are allowed one major power in thier Grimoire"



            return render_template('major_power_picker.html', current_major_power_choices=sorcery_maj_power_dict, timestamp=timestamp, message=message)
        else:
            title = 'Now let us work on the minor powers'
            return render_template('minor_power_begin.html', timestamp=timestamp, the_current_arch=arch, the_title=title, current_major_power=current_major_power)
    else:
        current_major_power_choices = make_dict_from_list(arch['maj-p'], major_power_data)
        temp_dump(current_major_power_choices, timestamp, 'current_major_power_choices')   # just for testing
        return render_template('major_power_picker.html', current_major_power_choices=current_major_power_choices, timestamp=timestamp)

@app.route('/major_power_checker', methods=['POST'])
def major_power_checker():
    """receives majaor power choice (of two) and applies changes to stats, then sends info to minor power begin"""

    # grab data from forms and temp files
    timestamp = request.form['timestamp']
    current_major_power_name = request.form['current_major_power_name']
    major_power_data = grab_from_temp(timestamp, 'major_power_data')
    hero = grab_from_temp(timestamp, 'hero')
    arch = grab_from_temp(timestamp, 'current_arch')
    #assign dict of powerchoice to variable
    current_major_power = assign_power_from_dict(current_major_power_name, major_power_data)



    # assign major power choice to the hero dict
    hero['hero_major_power_list'].append(current_major_power)

    # adjust stats based on major power choosen
    hero = hero_stat_adjust(hero,current_major_power['stat_changes'])
    # Add notes from Major Power
    hero['hero_notes'].extend(current_major_power['notes'])


    temp_dump(current_major_power, timestamp, 'current_major_power')
    temp_dump(hero, timestamp, 'hero')
    title = 'Now let us work on the minor powers'


    return render_template('minor_power_begin.html', timestamp=timestamp, the_current_arch=arch, the_title=title, current_major_power=current_major_power)

@app.route('/minor_power_launch', methods=['POST'])
def minor_power_launch():
    timestamp = request.form['timestamp']

    arch = grab_from_temp(timestamp, 'current_arch')
    hero = grab_from_temp(timestamp, 'hero')
    min_power_dict = grab_from_temp(timestamp, 'minor_power_data')
    current_major_power = grab_from_temp(timestamp, 'current_major_power')

    #temp_dump(current_major_power, timestamp, 'current_major_power')   # just for testing
    #temp_dump(arch, timestamp, 'arch')   # just for testing

    # check for archery exception
    if arch['archetype'] == 'Blaster' and current_major_power['power_name'] == 'Archery':
        current_major_power = grab_from_temp(timestamp, 'current_major_power')
        current_minor_power_dict = {}
        for x in min_power_dict:
            for y in arch['archer_minor_p_list']:
                if x == y:
                    current_minor_power_dict[x] = min_power_dict[x].copy()
                elif min_power_dict[x]['power_type'] == 'boost':
                    current_minor_power_dict[x] = min_power_dict[x].copy()

    # create regular minor power dict
    else:
        current_minor_power_dict = {}
        for x in min_power_dict:
            for y in arch['minor_p_list']:
                if x == y:
                    current_minor_power_dict[x] = min_power_dict[x].copy()
                elif min_power_dict[x]['power_type'] == 'boost':
                    current_minor_power_dict[x] = min_power_dict[x].copy()
    if hero['hero_type'] == 'Super' or hero['hero_type'] == 'Powerhouse':
        if 'Immortal' in current_minor_power_dict:
            del current_minor_power_dict['Immortal']



    # remove current minor powers from list for powerhouse archetype second group of minor power Choices
    if hero['hero_minor_power_list'] is not []:
        for x in hero['hero_minor_power_list']:
            for y in current_minor_power_dict.copy():
                if x['power_name'] == y:
                    del current_minor_power_dict[y]
    temp_dump(hero, timestamp, 'hero')
    temp_dump(current_minor_power_dict, timestamp, 'current_minor_power_dict')
    heroname = hero['hero_name']
    return render_template('minor_power_picker.html', timestamp=timestamp,current_minor_power_dict=current_minor_power_dict, heroname=heroname)

@app.route('/minor_power_loop', methods=['POST'])
def minor_power_loop():
    return 'begin minor power loop'

app.run(debug=True, host='0.0.0.0')
#app.run(debug=True)
