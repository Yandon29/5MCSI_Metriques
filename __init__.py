from flask import Flask, jsonify, render_template
import json
from urllib.request import urlopen
import requests
from datetime import datetime

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')  # comm2222

# Route pour la page de contact
@app.route("/contact/")
def contact():
    return render_template('contact.html')

# Route pour la météo de Tawarano (données brutes en JSON)
@app.route('/tawarano/')
def meteo_tawarano():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt_txt')  # Utilisation de la date lisible
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'Température (°C)': temp_day_value})
    
    return jsonify(results=results)

# Route pour afficher le graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Route pour afficher l'histogramme des températures
@app.route('/histogramme/')
def histogramme():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

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
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour récupérer et afficher les commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub pour extraire les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Requête à l'API pour obtenir les commits
    response = requests.get(url)
    commits_data = response.json()
    
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
    
    # Appeler le template HTML pour afficher le graphique
    return render_template('commits.html', data=json.dumps(commits_by_minute))

if __name__ == '__main__':
    app.run(debug=True)
