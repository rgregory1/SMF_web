from flask import Flask, render_template, request, redirect, escape, jsonify, Response
import json
import os
import datetime
from functions import *
import shutil
import copy
from sheet import *

app = Flask(__name__)



@app.route('/')
def entry_page():
    # os.rmdir('temp/180220')
    # shutil.rmtree('temp/180220', ignore_errors=False, onerror=None)

    basedir = os.path.abspath(os.path.dirname(__file__))
    temp_timestamp = str(datetime.datetime.now())
    timestamp = simplify_timestamp(temp_timestamp)
    # timestamp = '180220'
    try:
        os.makedirs(os.path.join(basedir,'static','temp', timestamp))
    except:
        pass

    # grab hero dict
    with open(os.path.join(basedir, 'static', 'data', 'hero_start.json')) as f:
        hero = json.load(f)


    with open(os.path.join(basedir, 'static', 'data', 'archetype_data.json')) as f:
        arch_dict = json.load(f)
    with open(os.path.join(basedir, 'static', 'data', 'major_power_data.json')) as f:
        major_power_data = json.load(f)
    with open(os.path.join(basedir, 'static', 'data', 'minor_power_data.json')) as f:
        minor_power_data = json.load(f)


    temp_dump(hero, timestamp, 'hero', basedir)
    temp_dump(arch_dict, timestamp, 'arch_dict', basedir)
    temp_dump(major_power_data, timestamp, 'major_power_data', basedir)
    temp_dump(minor_power_data, timestamp, 'minor_power_data', basedir)

    # first page, get hero name
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
    return render_template('archetype_picker.html', the_title='Choose an Archetype', arch_dict=arch_dict, heroname=heroname, timestamp=timestamp)



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

    title2 = 'Additinal Archetype Choices'
    loops = hero['loops']
    if hero['hero_archetype_list'][0]['power_type'] == 'Super' or hero['hero_archetype_list'][0]['power_type'] == 'Powerhouse':
        return render_template('alt_power_arch_picker.html', the_archetype_choice=archetype_choice, timestamp=timestamp, the_title=title2, loops=loops, new_arch_dict=new_arch_dict)

    #if hero['hero_archetype_list'][0]['power_type'] == 'Standard' or hero['hero_archetype_list'][0]['power_type'] == 'Henchmen':
    else:
        title = 'Archetype Results:'
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

    # temp_dump(arch_dict, timestamp, 'arch_dict')
    temp_dump(new_arch_dict, timestamp, 'new_arch_dict')
    temp_dump(hero, timestamp, 'hero')

    title = "Additinal Archetype Choices"

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

    # stop renewing mutable archethype list!!!!!!! ------------------------------------------------------------
    if hero['hero_type'] != 'Powerhouse':
        mutable_archetype_list = copy.deepcopy(hero['hero_archetype_list'])
    else:
        if hero['power_house_loop'] == 1:
            mutable_archetype_list = grab_from_temp(timestamp, 'mutable_archetype_list')
        else:
            mutable_archetype_list = copy.deepcopy(hero['hero_archetype_list'])


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
        current_major_power = 'none'
        if hero['hero_type'] == 'Powerhouse':
            hero['power_house_loop'] = 1
            temp_dump(hero, timestamp, 'hero')
        temp_dump(current_major_power, timestamp, 'current_major_power')
        title = 'No Major Power'
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
        if hero['hero_type'] == 'Powerhouse':
            hero['power_house_loop'] = 1


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

            message = "Your Major Power is Sorcery, which allows you one major power in your Grimoire"
            loop_type = "Grimoire"
            title = "Sorcery Major Power Grimoire"

            return render_template('major_power_picker_sorcery.html', current_major_power_choices=sorcery_maj_power_dict, timestamp=timestamp, message=message, loop_type=loop_type, the_title=title)
        else:
            title = 'Major Power'
            return render_template('minor_power_begin.html', timestamp=timestamp, the_current_arch=arch, the_title=title, current_major_power=current_major_power)
    else:
        current_major_power_choices = make_dict_from_list(arch['maj-p'], major_power_data)
        temp_dump(current_major_power_choices, timestamp, 'current_major_power_choices')   # just for testing
        if hero['hero_type'] == 'Powerhouse':
            hero['power_house_loop'] = 1
            temp_dump(hero, timestamp, 'hero')
        loop_type = 'regular'
        title = "Major Power"
        return render_template('major_power_picker.html', current_major_power_choices=current_major_power_choices, timestamp=timestamp, loop_type=loop_type, the_title=title)

@app.route('/major_power_checker', methods=['POST'])
def major_power_checker():
    """receives majaor power choice (of two) and applies changes to stats, then sends info to minor power begin"""

    # grab data from forms and temp files
    timestamp = request.form['timestamp']
    loop_type = request.form['loop_type']
    current_major_power_name = request.form['current_major_power_name']
    major_power_data = grab_from_temp(timestamp, 'major_power_data')
    # sorcery_maj_power_dict = grab_from_temp(timestamp, 'sorcery_maj_power_dict')
    hero = grab_from_temp(timestamp, 'hero')
    arch = grab_from_temp(timestamp, 'current_arch')



    #assign dict of powerchoice to variable
    current_major_power = assign_power_from_dict(current_major_power_name, major_power_data)
    # adjust stats based on major power choosen
    hero = hero_stat_adjust(hero,current_major_power['stat_changes'])

    # assign major power choice to the hero dict
    hero['hero_major_power_list'].append(current_major_power)

    # Add notes from Major Power
    hero['hero_notes'].extend(current_major_power['notes'])

    temp_dump(current_major_power, timestamp, 'current_major_power')
    temp_dump(hero, timestamp, 'hero')

    if current_major_power['power_name'] == 'Archery':

        with open('data/minor_power_data.json') as f:
            temp_power_dict = json.load(f)

        # create list of trick arrows and add 'Trick Arrow' to the power names
        archery_sorcery_power_dict = make_dict_from_list(current_major_power['additional_minor_powers'], temp_power_dict)
        for power in archery_sorcery_power_dict:
            archery_sorcery_power_dict[power]['power_name'] = 'Trick Arrow - ' + archery_sorcery_power_dict[power]['power_name']
            for note in range(len(archery_sorcery_power_dict[power]['notes'])):
                archery_sorcery_power_dict[power]['notes'][note] = 'Trick Arrow - ' + archery_sorcery_power_dict[power]['notes'][note]

        # save list of tric arrows for loop later
        temp_dump(archery_sorcery_power_dict, timestamp, 'archery_sorcery_power_dict')

        message = "Your Major Power is Archery, which allows you three 'Trick Arrow' powers in your quiver"
        title = "Trick Arrows"
        loop_type = current_major_power['additional_power_prefix']

        hero['archery_sorcery_loops'] = current_major_power['add_minor_powers_number']
        temp_dump(hero, timestamp, 'hero')
        archery_sorcery_loops = hero['archery_sorcery_loops']
        return render_template('archery_sorcery_power_picker.html', current_minor_power_dict=archery_sorcery_power_dict, timestamp=timestamp, message=message, loop_type=loop_type, the_title=loop_type, archery_sorcery_loops=archery_sorcery_loops)
    else:
        title = 'Major Power'
        return render_template('minor_power_begin.html', timestamp=timestamp, the_current_arch=arch, the_title=title, current_major_power=current_major_power)

@app.route('/major_power_checker_sorcery', methods=['POST'])
def major_power_checker_sorcery():
    """receives majaor power choice (of two) and applies changes to stats, then sends info to minor power begin"""

    # grab data from forms and temp files
    timestamp = request.form['timestamp']
    loop_type = request.form['loop_type']
    current_major_power_name = request.form['current_major_power_name']
    major_power_data = grab_from_temp(timestamp, 'major_power_data')
    sorcery_maj_power_dict = grab_from_temp(timestamp, 'sorcery_maj_power_dict')
    hero = grab_from_temp(timestamp, 'hero')
    arch = grab_from_temp(timestamp, 'current_arch')
    current_major_power = grab_from_temp(timestamp, 'current_major_power')

    grimoire_current_major_power = assign_power_from_dict(current_major_power_name, sorcery_maj_power_dict)


    # assign major power choice to the hero dict
    hero['hero_major_power_list'].append(grimoire_current_major_power)

    # Add notes from Major Power
    hero['hero_notes'].extend(grimoire_current_major_power['notes'])

    # temp_dump(current_major_power, timestamp, 'current_major_power')
    temp_dump(hero, timestamp, 'hero')



    with open('data/minor_power_data.json') as f:
        archery_sorcery_power_dict = json.load(f)
    del archery_sorcery_power_dict['Magic_Artifact']
    del archery_sorcery_power_dict['Shield']
    del archery_sorcery_power_dict['Immortal']
    del archery_sorcery_power_dict['Legion']

    for power in archery_sorcery_power_dict.copy():
        if archery_sorcery_power_dict[power]['power_type'] == 'boost':
            del archery_sorcery_power_dict[power]

    for power in archery_sorcery_power_dict:
        archery_sorcery_power_dict[power]['power_name'] = 'Grimoire - ' + archery_sorcery_power_dict[power]['power_name']
        for note in range(len(archery_sorcery_power_dict[power]['notes'])):
            archery_sorcery_power_dict[power]['notes'][note] = 'Grimoire - ' + archery_sorcery_power_dict[power]['notes'][note]




    loop_type = current_major_power['additional_power_prefix']

    hero['archery_sorcery_loops'] = current_major_power['add_minor_powers_number']
    temp_dump(hero, timestamp, 'hero')
    temp_dump(archery_sorcery_power_dict, timestamp, 'archery_sorcery_power_dict')
    # trial to see if it works
    message = "Your Major Power is Sorcery, which allows you four spell powers in your Grimoire"
    archery_sorcery_loops = hero['archery_sorcery_loops']
    return render_template('archery_sorcery_power_picker.html', current_minor_power_dict=archery_sorcery_power_dict, timestamp=timestamp, message=message, loop_type=loop_type, archery_sorcery_loops=archery_sorcery_loops, the_title=loop_type)



@app.route('/archery_sorcery_power_loop', methods=['POST'])
def archery_sorcery_power_loop():
    timestamp = request.form['timestamp']
    loop_type = request.form['loop_type']
    current_minor_power_name = request.form['current_minor_power']

    archery_sorcery_power_dict = grab_from_temp(timestamp, 'archery_sorcery_power_dict')
    hero = grab_from_temp(timestamp, 'hero')
    current_arch = grab_from_temp(timestamp, 'current_arch')




    # current_minor_power = assign_power_from_dict(current_minor_power_name, archery_sorcery_power_dict)
    current_minor_power, archery_sorcery_power_dict = pop_dict_from_dicts(current_minor_power_name, archery_sorcery_power_dict)

    # Add notes from Major Power
    hero['hero_notes'].extend(current_minor_power['notes'])
    # add to list of minor powers
    hero['hero_minor_power_list'].append(current_minor_power)
    hero['archery_sorcery_loops'] -= 1

    archery_sorcery_loops = hero['archery_sorcery_loops']
    # temp_dump(archery_sorcery_loops, timestamp, 'archery_sorcery_loops')  # just checking to make sure they are saving

    temp_dump(archery_sorcery_power_dict, timestamp, 'archery_sorcery_power_dict')
    temp_dump(hero, timestamp, 'hero')
    if hero['archery_sorcery_loops'] == 0:
        current_arch = grab_from_temp(timestamp, 'current_arch')
        current_major_power = grab_from_temp(timestamp, 'current_major_power')
        return render_template('/minor_power_begin.html', timestamp=timestamp, the_current_arch=current_arch, current_major_power=current_major_power)
    else:
        return render_template('archery_sorcery_power_picker.html', current_minor_power_dict=archery_sorcery_power_dict, timestamp=timestamp, loop_type=loop_type, archery_sorcery_loops=archery_sorcery_loops, the_title=loop_type)

@app.route('/minor_power_launch', methods=['POST'])
def minor_power_launch():
    timestamp = request.form['timestamp']
    # if 'current_minor_power' in request.files:
    #     current_minor_power_name = request.form['current_minor_power']

    arch = grab_from_temp(timestamp, 'current_arch')
    hero = grab_from_temp(timestamp, 'hero')
    min_power_dict = grab_from_temp(timestamp, 'minor_power_data')
    current_major_power = grab_from_temp(timestamp, 'current_major_power')

    # super archetpe check
    if hero['hero_type'] == 'Super':
        # on first pass if it's a super, send them to the super chooser
        if 'super_archetype_bonus' not in hero:
            title = "Super Choice"
            return render_template('super_choice.html', timestamp=timestamp, the_title=title)
        #if they have been to the chooser already, make adjustments and move on
        if hero['super_archetype_bonus'] == 'Yes':
            current_minor_power_name = request.form['current_minor_power']
            with open('data/minor_power_data.json') as f:
                super_minor_power_dict = json.load(f)
            current_minor_power = assign_power_from_dict(current_minor_power_name, super_minor_power_dict)

            hero = hero_stat_adjust(hero,current_minor_power['stat_changes'])
            # Add notes from Major Power
            hero['hero_notes'].extend(current_minor_power['notes'])
            # add to list of minor powers
            hero['hero_minor_power_list'].insert(0, current_minor_power)

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
    hero['minor_power_loops'] = arch['min_p_num']
    hero['boost_loops'] = 1
    if hero['hero_type'] == 'Super':
        hero['boost_loops'] = 2
        if hero['super_archetype_bonus'] == 'No':
            hero['minor_power_loops'] = hero['minor_power_loops'] + 2


    temp_dump(hero, timestamp, 'hero')
    temp_dump(current_minor_power_dict, timestamp, 'current_minor_power_dict')
    loop_type = 'standard'
    minor_power_loops=hero['minor_power_loops']
    title = 'Minor Powers'
    return render_template('minor_power_picker.html', timestamp=timestamp,current_minor_power_dict=current_minor_power_dict, the_title=title, minor_power_loops=minor_power_loops)

@app.route('/super_choice_results', methods=['POST'])
def super_choice_results():
    timestamp = request.form['timestamp']
    answer = request.form['answer']

    hero = grab_from_temp(timestamp, 'hero')

    if answer == 'No':
        hero['super_archetype_bonus'] = 'No'
        temp_dump(hero, timestamp, 'hero')
        the_title = 'Begin Minor Powers'

        return render_template('/super_on_to_minor_powers.html', timestamp=timestamp, the_title=the_title)
    if answer == 'Yes':
        hero['super_archetype_bonus'] = 'Yes'
        with open('data/minor_power_data.json') as f:
            super_min_power_dict = json.load(f)
        # Remove imortal and legion from dict
        del super_min_power_dict['Immortal']
        del super_min_power_dict['Legion']




        temp_dump(hero, timestamp, 'hero')
        title = "Additional Super Power"
        return render_template('super_power_picker.html', timestamp=timestamp,current_minor_power_dict=super_min_power_dict, the_title=title)


@app.route('/minor_power_loop', methods=['POST'])
def minor_power_loop():
    timestamp = request.form['timestamp']

    current_minor_power_name = request.form['current_minor_power']

    current_minor_power_dict = grab_from_temp(timestamp, 'current_minor_power_dict')
    hero = grab_from_temp(timestamp, 'hero')
    current_arch = grab_from_temp(timestamp, 'current_arch')





    # current_minor_power = assign_power_from_dict(current_minor_power_name, archery_sorcery_power_dict)
    current_minor_power, current_minor_power_dict = pop_dict_from_dicts(current_minor_power_name, current_minor_power_dict)

    # Add notes from minor Power
    hero['hero_notes'].extend(current_minor_power['notes'])
    # add to list of minor powers
    hero['hero_minor_power_list'].append(current_minor_power)
    hero = hero_stat_adjust(hero,current_minor_power['stat_changes'])
    hero['minor_power_loops'] -= 1

    if current_minor_power['power_type'] == 'boost':
        hero['boost_loops'] -= 1
        if hero['boost_loops'] == 0:
            for power in current_minor_power_dict.copy():
                if current_minor_power_dict[power]['power_type'] == 'boost':
                    del current_minor_power_dict[power]

    if hero['minor_power_loops'] <= 1:
        if 'Immortal' in current_minor_power_dict:
            del current_minor_power_dict['Immortal']

    if current_minor_power['power_name'] == 'Immortal':
        hero['minor_power_loops'] -= 1






    minor_power_loops = hero['minor_power_loops']
    temp_dump(current_minor_power_dict, timestamp, 'current_minor_power_dict')
    temp_dump(hero, timestamp, 'hero')
    if hero['minor_power_loops'] == 0:
        mutable_archetype_list = grab_from_temp(timestamp, 'mutable_archetype_list')
        if len(mutable_archetype_list) == 1:
            # current_arch = grab_from_temp(timestamp, 'current_arch')
            # current_major_power = grab_from_temp(timestamp, 'current_major_power')
            title = 'Second Archetype Choices'
            return render_template('powerhouse_second_arch.html', the_title=title, timestamp=timestamp)
        else:
            title = 'Backgrounds'
            backgrounds = ['Alien/Dimensional', 'Arcane', 'Art', 'Athletics', 'Blue Collar', 'Business', 'Criminal', 'Espionage', 'Exploration', 'High Society', 'Journalist', 'Medicine', 'Military', 'Monarch', 'Performance', 'Public Safety', 'Science', 'Social Science']

            return render_template('background_picker.html', the_title=title, timestamp=timestamp, backgrounds=backgrounds)
    else:
        return render_template('minor_power_picker.html', current_minor_power_dict=current_minor_power_dict, timestamp=timestamp, minor_power_loops=minor_power_loops)

@app.route('/begin_roundup', methods=['POST'])
def begin_roundup():
    timestamp = request.form['timestamp']
    background_choices = request.form.getlist('background_choice')

    hero = grab_from_temp(timestamp, 'hero')


    #temp_dump(form_info, timestamp, 'form_info') #test to see how to grab data
    for background in background_choices:
        hero['hero_backgrounds'].append(background)

    if hero['hero_archetype_list'][0]['archetype'] == 'Henchmen':
        hero = henchman_stat_redux(hero)
    heroname = hero['hero_name']
    temp_dump(hero, timestamp, 'hero')
    return render_template('print_character.html', timestamp=timestamp, heroname=heroname)

@app.route('/show_sheet', methods=['POST'])
def show_sheet():
    timestamp = request.form['timestamp']

    hero = grab_from_temp(timestamp, 'hero')
    sheet_timestamp = print_hero(hero)
    suffix = '.png'
    sheet_location = os.path.join('static', 'hero_files', hero['hero_name'] + '_' + sheet_timestamp + suffix)
    return render_template('show_sheet.html', sheet_location=sheet_location)
    # return '<a href="/static/text.png">Your character</a>'

if __name__ == '__main__':
    app.run()
    # app.run(debug=True, host='0.0.0.0')
