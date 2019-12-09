from flask import Flask, request
from flask_cors import CORS
import sqlite3
import json

# Run server
app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/createPlayer/')
def createPlayer():
    try:
        with sqlite3.connect('wcis.db') as conn:

            player = request.args.get('player')
            db_cursor = conn.cursor()
            db_cursor.execute("INSERT INTO player(player_name) VALUES ('" + player + "')")
            return "OK"
    except Exception as e:
        return "Name already exists, try another name!"
            
@app.route('/signIn', methods=["GET"])
def signIn():
    try:
        with sqlite3.connect('wcis.db') as conn:
            player = request.args.get('player')
            db_cursor = conn.cursor()
            db_cursor.execute("SELECT player_id FROM player WHERE player_name LIKE '" + player + "'")
            res = db_cursor.fetchone()
            return json.dumps(res[0])
    except Exception as e:
        return "Uh oh"
            
@app.route('/createCharacter/')
def createCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            # Parameters
            playerID = request.args.get('playerID')
            charName = request.args.get('charName')
            lvl = request.args.get('lvl')
            className = request.args.get('className')
            race = request.args.get('race')
            
            insert_query = "INSERT INTO character (character_name, player_id, total_level, class_name, race_name) VALUES ('" + charName + "', " + playerID + ", " + lvl + ", '" + className + "', '" + race + "')"

            db_cursor = conn.cursor()
            db_cursor.execute(insert_query)

            return "OK"
    except Exception as e:
        return "Could not create character"

@app.route('/getCharacters/')
def getCharacters():
    try:
        with sqlite3.connect('wcis.db') as conn:
            playerID = request.args.get('playerID')

            select_query = "SELECT * FROM character WHERE player_id = " + playerID 

            db_cursor = conn.cursor()

            db_cursor.execute(select_query)

            res = db_cursor.fetchall()

            return json.dumps(res)
    except Exception as e:
        return "Fail"

@app.route('/deleteCharacter/', methods=['DELETE'])
def deleteCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            characterID = request.form['characterID']
            delete_query = "DELETE FROM character WHERE character_id = " + characterID
            db_cursor = conn.cursor()
            db_cursor.execute(delete_query)
            return "OK"
    except Exception as e:
        return "Could not delete"

@app.route('/getAvailableSpells')
def getAvailableSpells():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.args.get('charID')
            charClass = request.args.get('charClass')


            select_query = "SELECT * FROM spell WHERE class LIKE '%" + charClass + "%' AND spellbook_id NOT IN (SELECT spellbook_id FROM learnedspell WHERE character_id = " + charID + ")"

            db_cursor = conn.cursor()

            db_cursor.execute(select_query)

            res = db_cursor.fetchall()

            return json.dumps(res)
    except Exception as e:
        return e

@app.route('/addSpellToCharacter')
def addSpellToCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.args.get('charID')
            spellID = request.args.get('spellID')
            insert_query = "INSERT INTO learnedspell VALUES (" + charID + ", " + spellID + ")"
            db_cursor = conn.cursor()
            db_cursor.execute(insert_query)
            return "OK"
    except Exception as e:
        return "FAIL"

@app.route('/viewLearnedSpells')
def viewLearnedSpells():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.args.get('charID')

            select_query = "SELECT * FROM learnedspell NATURAL JOIN spell WHERE character_id = " + charID

            db_cursor = conn.cursor()

            db_cursor.execute(select_query)

            res = db_cursor.fetchall()

            return json.dumps(res)

    except Exception as e:
        return "Could not find spells"

@app.route('/removeSpellFromCharacter', methods=['DELETE'])
def removeSpellFromCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.args.get('charID')
            spellID = request.args.get('spellID')
            delete_query = "DELETE FROM learnedspell WHERE character_id=" + charID + " AND spellbook_id=" + spellID
            db_cursor = conn.cursor()
            db_cursor.execute(delete_query)
            return "OK"
    except Exception as e:
        return e

@app.route('/createHomebrewSpell', methods=['POST'])
def createHomebrewSpell():
    try:
        with sqlite3.connect('wcis.db') as conn:
            name = request.form['name']
            description = request.form['description']
            level = request.form['level']
            school = request.form['school']
            spellrange = request.form['range']
            cast_time = request.form['casttime']
            duration = request.form['duration']
            cont_tag = request.form['cont_tag']
            higher_level = request.form['higherlvl']
            ritual_tag = request.form['ritual']
            components = request.form['components']
            material = request.form['material']
            domains = request.form['domains']
            circles = request.form['circles']
            archetype = request.form['archetype']
            className = request.form['class']

            db_cursor = conn.cursor()
            
            insert_query1 = "INSERT INTO spell(name, description, level, school, range, cast_time, duration, cont_tag, higher_level, ritual_tag, components, material, domains, circles, archetype, class) VALUES('" + name + "', '" + description + "', " + level + ", '" + school + "', '" + spellrange + "', '" + cast_time + "', '" + duration + "', " + cont_tag + ", " + higher_level + ", " + ritual_tag + ", '" + components + "', '" + material + "', '" + domains + "', '" + circles + "', '" + archetype + "', '" + className + "')"

            db_cursor.execute(insert_query1)

            insert_query2 = "INSERT INTO book VALUES('5e', '" + name + "', 'H')"
            db_cursor.execute(insert_query2)

            return "OK"
    except Exception as e:
        return "FAILURE"


if __name__ == '__main__':
    app.run(port=5000)
