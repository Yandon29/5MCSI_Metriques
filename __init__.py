from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # test2

@app.route("/contact/")
def mongraphique3():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def histogramme():
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération des données météo', 'message': str(e)}), 502

    # Extraction des données pour l'histogramme
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt_txt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append([dt_value, temp_day_value])  # Format compatible avec Google Charts

    # Appel du template HTML pour afficher le graphique
    return render_template('histogramme.html', data=json.dumps(results))

# Route pour extraire les minutes d'une information formatée comme "2024-02-11T11:57:27Z"
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except Exception as e:
        return jsonify({'error': 'Erreur lors de l\'extraction des minutes', 'message': str(e)}), 400

# Route pour récupérer et afficher les commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub pour extraire les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Requête à l'API GitHub
    try:
        response = requests.get(url)
        response.raise_for_status()  # Génère une exception si la réponse a un code d'erreur
    except requests.exceptions.HTTPError as errh:
        return jsonify({"error": "Http Error", "message": str(errh)})
    except requests.exceptions.ConnectionError as errc:
        return jsonify({"error": "Error Connecting", "message": str(errc)})
    except requests.exceptions.Timeout as errt:
        return jsonify({"error": "Timeout Error", "message": str(errt)})
    except requests.exceptions.RequestException as err:
        return jsonify({"error": "Oops: Something Else", "message": str(err)})
    
    # Récupération des données JSON
    try:
        commits_data = response.json()
    except Exception as e:
        return jsonify({"error": "Erreur lors de l'analyse des données", "message": str(e)}), 500

    # Liste pour stocker les minutes des commits
    minutes_list = []
    
    # Parcourir les commits et extraire les minutes de chaque commit
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        minutes_list.append(minutes)
    
    # Préparer les données sous forme de tableau pour Google Charts
    commits_by_minute = []
    for minute in range(60):
        commits_by_minute.append([str(minute), minutes_list.count(minute)])
    
    # Appel du template HTML pour afficher le graphique
    return render_template('commits.html', data=json.dumps(commits_by_minute))

if __name__ == "__main__":
    app.run(debug=True)
