from flask import Flask, render_template, jsonify, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# set up Google Sheets API credentials
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('strat-sheet').sheet1

@app.route('/igl')
def igl():
    return render_template('igl.html')

@app.route('/', methods=['GET', 'POST'])
def strategy():
    if request.method == 'POST':
        row = request.form['row']
        column = request.form['column']
        value = request.form['value']
        sheet.update_cell(int(row), int(column), value)
        return 'success'
    else:
        # get data from Google Sheets
        data = sheet.get_all_values()
        # format data for display
        players = []
        player_data = []

        x = 0

        for row in data:
            if row[0] == "TRUE":
                player_data=(data[x:x+5])
            x+=1

        for y in player_data:
            player = {}
            player['name'] = y[2]
            player['gun1'] = y[3]
            player['gun2'] = y[4]
            player['nade'] = y[5]
            player['flash'] = y[6]
            player['smoke'] = y[7]
            player['molly'] = y[8]
            player['description'] = y[9]
            print(player)
            players.append(player)
        return render_template('strategy.html', players=players)

@app.route('/get_data')
def get_data():
    #players = []
    player_data = []
    data = sheet.get_all_values() # get the list of players from the first row
    
    x = 0

    for row in data:
        if row[0] == "TRUE":
            player_data=(data[x:x+5])
        x+=1

    print(player_data)
    
    return jsonify(players=player_data) # return players as a JSON object

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)