from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import pandas as pd
import requests
import time
from math import radians, sin, cos, sqrt, atan2
import os
import sys

# Přidání cesty pro import konfiguračního souboru
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Načtení natrénovaného modelu
def load_model():
    try:
        with open(config.MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
            print(f"Model načten z: {config.MODEL_PATH}")
            return model
    except FileNotFoundError:
        print(f"CHYBA: Model {config.MODEL_PATH} nebyl nalezen!")
        return None
    except Exception as e:
        print(f"CHYBA při načítání modelu: {str(e)}")
        return None

# Načtení modelu při startu aplikace
model = load_model()

# Funkce pro výpočet vzdálenosti mezi dvěma body (Haversine formula)
def vypocet_vzdalenosti(lat1, lon1, lat2, lon2):
    R = 6371.0  # Poloměr Země v km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# API pro získání kraje
def zjisti_kraj(lat, lon):
    try:
        url = f"{config.OSM_API_URL}?lat={lat}&lon={lon}&format=json&accept-language=cs"
        headers = {'User-Agent': config.OSM_USER_AGENT}
        response = requests.get(url, headers=headers)
        data = response.json()

        # Zkontrolujeme různé možnosti, kde může být informace o kraji
        kraj_nazev = data.get('address', {}).get('state', None)
        if not kraj_nazev:
            kraj_nazev = data.get('address', {}).get('county', 'Neznámý')

        kraj_kod = config.KRAJE_KODY.get(kraj_nazev, 0)
        return kraj_kod, kraj_nazev
    except Exception as e:
        print(f"Chyba při zjišťování kraje: {e}")
        return 0, "Neznámý"

# Základní routy
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Kontrola, zda je model načten
        if model is None:
            return jsonify({'error': 'Model není načten. Zkontrolujte konfiguraci.'}), 500

        data = request.json

        # Zpracování základních parametrů od uživatele
        new = int(data.get('new', 0))
        area = float(data.get('area', 0))
        room_number = int(data.get('room_number', 0))
        kitchen_number = int(data.get('kitchen_number', 0))

        # Získání souřadnic
        lat = float(data.get('lat', 0))
        lon = float(data.get('lon', 0))

        # Zjištění kraje
        kraj_kod, nazev_kraje = zjisti_kraj(lat, lon)

        # Výpočet vzdálenosti k velkým městům
        min_vzdalenost = float('inf')
        nejblizsi_mesto = ""
        nejblizsi_kod = 0

        for mesto, info in config.VELKA_MESTA.items():
            vzdalenost = vypocet_vzdalenosti(lat, lon, info['lat'], info['lon'])
            if vzdalenost < min_vzdalenost:
                min_vzdalenost = vzdalenost
                nejblizsi_mesto = mesto
                nejblizsi_kod = info['kod']

        je_velke_mesto = 1 if min_vzdalenost <= 5 else 0
        vzdalenost_centrum_km = round(min_vzdalenost, 2)
        kod_velkeho_mesta = nejblizsi_kod

        # Vytvoření DataFrame pro predikci
        input_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lon],
            'new': [new],
            'area': [area],
            'kraj_kod': [kraj_kod],
            'je_velke_mesto': [je_velke_mesto],
            'vzdalenost_centrum_km': [vzdalenost_centrum_km],
            'kod_velkeho_mesta': [kod_velkeho_mesta],
            'room_number': [room_number],
            'kitchen_number': [kitchen_number]
        })

        # Predikce ceny
        predicted_price = model.predict(input_data)[0]

        # Příprava odpovědi
        response = {
            'predicted_price': round(predicted_price, 2),
            'kraj_kod': kraj_kod,
            'nazev_kraje': nazev_kraje,
            'je_velke_mesto': je_velke_mesto,
            'vzdalenost_centrum_km': vzdalenost_centrum_km,
            'kod_velkeho_mesta': kod_velkeho_mesta,
            'nazev_velkeho_mesta': nejblizsi_mesto
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reload_model', methods=['GET'])
def reload_model():
    """Endpoint pro ruční znovunačtení modelu."""
    global model
    model = load_model()
    if model:
        return jsonify({'status': 'success', 'message': f'Model úspěšně znovu načten z {config.MODEL_PATH}'})
    else:
        return jsonify({'status': 'error', 'message': 'Nepodařilo se znovu načíst model'}), 500

# Pro přímé spuštění
if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)







# from flask import Flask, request, jsonify, render_template
# import pickle
# import pandas as pd
# import requests
# import time
# from math import radians, sin, cos, sqrt, atan2
# import os

# app = Flask(__name__)

# # Načtení natrénovaného modelu
# model_path = "best_random_forest_model_RMSE_3377.6362.pkl"
# try:
#     with open(model_path, 'rb') as file:
#         model = pickle.load(file)
# except FileNotFoundError:
#     print(f"Model {model_path} nebyl nalezen!")

# # Slovník velkých měst
# velka_mesta = {
#     "Praha": {"kod": 1, "lat": 50.0755, "lon": 14.4378},
#     "Brno": {"kod": 2, "lat": 49.1951, "lon": 16.6068},
#     "Ostrava": {"kod": 3, "lat": 49.8209, "lon": 18.2625},
#     "Plzeň": {"kod": 4, "lat": 49.7384, "lon": 13.3736},
#     "Liberec": {"kod": 5, "lat": 50.7663, "lon": 15.0543},
#     "Olomouc": {"kod": 6, "lat": 49.5937, "lon": 17.2508},
#     "České Budějovice": {"kod": 7, "lat": 48.9764, "lon": 14.5065},
#     "Hradec Králové": {"kod": 8, "lat": 50.2091, "lon": 15.8323},
#     "Ústí nad Labem": {"kod": 9, "lat": 50.6608, "lon": 14.0313},
#     "Pardubice": {"kod": 10, "lat": 50.0343, "lon": 15.7812}
# }

# # Mapování krajů
# kraje_kody = {
#     'Praha': 1,
#     'Moravskoslezský kraj': 2,  # Upraveno pro formát z OpenStreetMap
#     'Moravskoslezsko': 2,
#     'Ústecký kraj': 3,          # Přidáno pro formát z OpenStreetMap
#     'Karlovarský kraj': 3,      # Přidáno pro formát z OpenStreetMap
#     'Severozápad': 3,
#     'Plzeňský kraj': 4,         # Přidáno pro formát z OpenStreetMap
#     'Jihočeský kraj': 4,        # Přidáno pro formát z OpenStreetMap
#     'Jihozápad': 4,
#     'Liberecký kraj': 5,        # Přidáno pro formát z OpenStreetMap
#     'Královéhradecký kraj': 5,  # Přidáno pro formát z OpenStreetMap
#     'Pardubický kraj': 5,       # Přidáno pro formát z OpenStreetMap
#     'Severovýchod': 5,
#     'Olomoucký kraj': 6,        # Přidáno pro formát z OpenStreetMap
#     'Zlínský kraj': 6,          # Přidáno pro formát z OpenStreetMap
#     'Střední Morava': 6,
#     'Středočeský kraj': 7,      # Přidáno pro formát z OpenStreetMap
#     'Střední Čechy': 7,
#     'Jihomoravský kraj': 8,     # Přidáno pro formát z OpenStreetMap
#     'Kraj Vysočina': 8,         # Přidáno pro formát z OpenStreetMap
#     'Jihovýchod': 8,
# }

# # Funkce pro výpočet vzdálenosti mezi dvěma body (Haversine formula)
# def vypocet_vzdalenosti(lat1, lon1, lat2, lon2):
#     R = 6371.0  # Poloměr Země v km
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     return R * c

# # API pro získání kraje
# def zjisti_kraj(lat, lon):
#     try:
#         url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=cs"
#         headers = {'User-Agent': 'HousePricePredictor/1.0'}
#         response = requests.get(url, headers=headers)
#         data = response.json()

#         # Zkontrolujeme různé možnosti, kde může být informace o kraji
#         kraj_nazev = data.get('address', {}).get('state', None)
#         if not kraj_nazev:
#             kraj_nazev = data.get('address', {}).get('county', 'Neznámý')

#         kraj_kod = kraje_kody.get(kraj_nazev, 0)
#         return kraj_kod, kraj_nazev
#     except Exception as e:
#         print(f"Chyba při zjišťování kraje: {e}")
#         return 0, "Neznámý"

# # Základní routy
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json

#         # Zpracování základních parametrů od uživatele
#         new = int(data.get('new', 0))
#         area = float(data.get('area', 0))
#         room_number = int(data.get('room_number', 0))
#         kitchen_number = int(data.get('kitchen_number', 0))

#         # Získání souřadnic
#         lat = float(data.get('lat', 0))
#         lon = float(data.get('lon', 0))

#         # Zjištění kraje
#         kraj_kod, nazev_kraje = zjisti_kraj(lat, lon)

#         # Výpočet vzdálenosti k velkým městům
#         min_vzdalenost = float('inf')
#         nejblizsi_mesto = ""
#         nejblizsi_kod = 0

#         for mesto, info in velka_mesta.items():
#             vzdalenost = vypocet_vzdalenosti(lat, lon, info['lat'], info['lon'])
#             if vzdalenost < min_vzdalenost:
#                 min_vzdalenost = vzdalenost
#                 nejblizsi_mesto = mesto
#                 nejblizsi_kod = info['kod']

#         je_velke_mesto = 1 if min_vzdalenost <= 5 else 0
#         vzdalenost_centrum_km = round(min_vzdalenost, 2)
#         kod_velkeho_mesta = nejblizsi_kod

#         # Vytvoření DataFrame pro predikci
#         input_data = pd.DataFrame({
#             'new': [new],
#             'area': [area],
#             'room_number': [room_number],
#             'kitchen_number': [kitchen_number],
#             'kraj_kod': [kraj_kod],
#             'je_velke_mesto': [je_velke_mesto],
#             'vzdalenost_centrum_km': [vzdalenost_centrum_km],
#             'kod_velkeho_mesta': [kod_velkeho_mesta]
#         })

#         # Predikce ceny
#         predicted_price = model.predict(input_data)[0]

#         # Příprava odpovědi
#         response = {
#             'predicted_price': round(predicted_price, 2),
#             'kraj_kod': kraj_kod,
#             'nazev_kraje': nazev_kraje,
#             'je_velke_mesto': je_velke_mesto,
#             'vzdalenost_centrum_km': vzdalenost_centrum_km,
#             'kod_velkeho_mesta': kod_velkeho_mesta,
#             'nazev_velkeho_mesta': nejblizsi_mesto
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)





