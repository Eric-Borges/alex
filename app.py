from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# Chave da API e localização
API_KEY = "CZFXPKVF2VRY5B2KQ9Y7JFVYK"
LOCATION = "Porto Alegre, RS"

# Modelo de regressão
def calcular_pao(mes, dia_semana, temperatura, umidade, uv):
    return 108.491 + (0.912 * mes) - (0.669 * dia_semana) - (1.372 * temperatura) + (0.127 * umidade) - (0.444 * uv) + 10.191

# Função para obter os dados da API Visual Crossing
def obter_previsao():
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}?unitGroup=metric&key={API_KEY}&include=days"
    resposta = requests.get(url)
    dados = resposta.json()

    previsoes = []
    for i in range(3):  # Pega a previsão para os próximos 3 dias
        dia = dados["days"][i]
        data = datetime.strptime(dia["datetime"], "%Y-%m-%d")
        mes = data.month
        dia_semana = data.weekday()  # 0 = segunda, 6 = domingo
        temperatura = dia["temp"]
        umidade = dia["humidity"]
        uv = dia["uvindex"]

        producao_pao = calcular_pao(mes, dia_semana, temperatura, umidade, uv)
        previsoes.append({"data": dia["datetime"], "pao": round(producao_pao, 2)})

    return previsoes

@app.route("/")
def home():
    previsoes = obter_previsao()
    return render_template("index.html", previsoes=previsoes)

if __name__ == "__main__":
    app.run(debug=True)
