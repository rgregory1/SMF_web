from flask import Flask, render_template, request, redirect, escape
import json

app = Flask(__name__)

# load information into dictionaries ---------------------------------------------------------------
with open('data/archetype_data.json') as f:
    arch_dict = json.load(f)



@app.route('/')
def entry_page():
    return render_template('home.html', the_title='SMF Character Creator')

@app.route('/archetype_picker', methods=['POST'])
def archetype_page():
    with open('data/hero_start.json') as f:
        hero = json.load(f)
    heroname = request.form['heroname']
    hero['hero_name'] = heroname
    with open('data/temp.json', 'w') as f:
      json.dump(hero, f, indent=2)
    return render_template('archetype_picker.html', the_title='Archetype Picker Page', arch_dict=arch_dict, heroname=heroname)


@app.route('/setup_arch', methods=['POST'])
def setup_current_arch() -> 'html':
    archetype_choice = request.form['current_arch']
    title = 'Here are your results:'
    return render_template('results.html',
                           the_archetype_choice=archetype_choice)

# hi
app.run(debug=True)
