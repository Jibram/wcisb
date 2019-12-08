from flask import Flask, request
import sqlite3
import json

# Run server
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/createPlayer/', methods=["POST"])
def createPlayer():
    try:
        with sqlite3.connect('wcis.db') as conn:

            player = request.form['player']
            db_cursor = conn.cursor()
            db_cursor.execute("INSERT INTO player(player_name) VALUES ('" + player + "')")
            return "OK"
    except Exception as e:
        return "Name already exists, try another name!"
            

@app.route('/createCharacter/', methods=["POST"])
def createCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            
            player = request.form['player']
            db_cursor = conn.cursor()
            db_cursor.execute("SELECT player_id FROM player WHERE player_name = '" + player + "'")

            # Parameters
            playerID = str(db_cursor.fetchone()[0])
            charName = request.form['charName']
            lvl = request.form['lvl']
            className = request.form['className']
            race = request.form['race']
            
            insert_query = "INSERT INTO character (character_name, player_id, total_level, class_name, race_name) VALUES ('" + charName + "', " + playerID + ", " + lvl + ", '" + className + "', '" + race + "')"

            db_cursor.execute(insert_query)

            return "OK"
    except Exception as e:
        return "Could not create character"

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

@app.route('/viewAvailableSpells')
def viewAvailableSpells():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charClass = request.form['class']

            select_query = "SELECT * FROM spell WHERE class = '" + charClass + "'" 

            db_cursor = conn.cursor()

            db_cursor.execute(select_query)

            res = db_cursor.fetchall()

            return json.dumps(res)
    except Exception as e:
        return e

@app.route('/addSpellToCharacter', methods=['POST'])
def addSpellToCharacter():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.form['charID']
            spellID = request.form['spellID']
            insert_query = "INSERT INTO learnedspell VALUES (" + charID + ", " + spellID + ")"
            db_cursor = conn.cursor()
            db_cursor.execute(insert_query)
            return "OK"
    except Exception as e:
        return e

@app.route('/viewLearnedSpells')
def viewLearnedSpells():
    try:
        with sqlite3.connect('wcis.db') as conn:
            charID = request.form['charID']

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
            charID = request.form['charID']
            spellID = request.form['spellID']
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
