from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm222

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Route pour afficher les données météo en format JSON
@app.route('/meteo/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt_txt')  # Utilisation de la date lisible
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'Température (°C)': temp_day_value})
    
    return jsonify(results=results)

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
  
if __name__ == "__main__":
  app.run(debug=True)
