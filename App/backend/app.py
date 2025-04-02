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

# Import loggeru
from App.backend.logger import PredictionLogger

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Inicializace loggeru
logger = PredictionLogger(log_dir=os.path.join(os.path.dirname(__file__), '../../logs'))

# Načtení natrénovaného modelu
def load_model():
    try:
        with open(config.MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
            logger.log_model_load(config.MODEL_PATH, True)
            return model
    except FileNotFoundError:
        logger.log_model_load(config.MODEL_PATH, False)
        return None
    except Exception as e:
        logger.log_error(f"Chyba při načítání modelu: {str(e)}")
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
        logger.log_error(f"Chyba při zjišťování kraje: {e}")
        return 0, "Neznámý"

# Základní routy
@app.route('/')
def index():
    client_ip = request.remote_addr
    logger.logger.info(f"Přístup na hlavní stránku z IP: {client_ip}")
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    client_ip = request.remote_addr
    logger.logger.debug(f"Požadavek na statický soubor: {filename}, IP: {client_ip}")
    return send_from_directory(app.static_folder, filename)

@app.route('/predict', methods=['POST'])
def predict():
    client_ip = request.remote_addr
    start_time = time.time()
    
    try:
        # Získání dat z požadavku
        data = request.json
        
        # Logování požadavku
        logger.log_request(data, client_ip)
        
        # Kontrola, zda je model načten
        if model is None:
            error_msg = 'Model není načten. Zkontrolujte konfiguraci.'
            logger.log_error(error_msg, client_ip, data)
            return jsonify({'error': error_msg}), 500

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

        # Výpočet délky zpracování
        processing_time = time.time() - start_time
        
        # Logování odpovědi
        logger.log_response(response, client_ip, processing_time)

        return jsonify(response)

    except Exception as e:
        # Logování chyby
        error_msg = str(e)
        logger.log_error(error_msg, client_ip, request.json if hasattr(request, 'json') else None)
        return jsonify({'error': error_msg}), 500

@app.route('/reload_model', methods=['GET'])
def reload_model():
    """Endpoint pro ruční znovunačtení modelu."""
    client_ip = request.remote_addr
    logger.logger.info(f"Požadavek na znovunačtení modelu z IP: {client_ip}")
    
    global model
    model = load_model()
    if model:
        response = {'status': 'success', 'message': f'Model úspěšně znovu načten z {config.MODEL_PATH}'}
        logger.logger.info(f"Model úspěšně znovu načten z {config.MODEL_PATH}")
        return jsonify(response)
    else:
        response = {'status': 'error', 'message': 'Nepodařilo se znovu načíst model'}
        logger.logger.error("Nepodařilo se znovu načíst model")
        return jsonify(response), 500

# Pomocný endpoint pro kontrolu loggeru
@app.route('/check_logs', methods=['GET'])
def check_logs():
    """Endpoint pro kontrolu, zda logování funguje."""
    if not request.remote_addr.startswith('127.0.0.1'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        log_files = os.listdir(os.path.join(os.path.dirname(__file__), '../../logs'))
        return jsonify({
            'status': 'success',
            'log_files': log_files,
            'message': 'Logování je nastaveno správně.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Chyba při kontrole logů: {str(e)}'
        }), 500

# Pro přímé spuštění
if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)





# from flask import Flask, request, jsonify, render_template, send_from_directory
# import pickle
# import pandas as pd
# import requests
# import time
# from math import radians, sin, cos, sqrt, atan2
# import os
# import sys

# # Přidání cesty pro import konfiguračního souboru
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# import config

# app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# # Načtení natrénovaného modelu
# def load_model():
#     try:
#         with open(config.MODEL_PATH, 'rb') as file:
#             model = pickle.load(file)
#             print(f"Model načten z: {config.MODEL_PATH}")
#             return model
#     except FileNotFoundError:
#         print(f"CHYBA: Model {config.MODEL_PATH} nebyl nalezen!")
#         return None
#     except Exception as e:
#         print(f"CHYBA při načítání modelu: {str(e)}")
#         return None

# # Načtení modelu při startu aplikace
# model = load_model()

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
#         url = f"{config.OSM_API_URL}?lat={lat}&lon={lon}&format=json&accept-language=cs"
#         headers = {'User-Agent': config.OSM_USER_AGENT}
#         response = requests.get(url, headers=headers)
#         data = response.json()

#         # Zkontrolujeme různé možnosti, kde může být informace o kraji
#         kraj_nazev = data.get('address', {}).get('state', None)
#         if not kraj_nazev:
#             kraj_nazev = data.get('address', {}).get('county', 'Neznámý')

#         kraj_kod = config.KRAJE_KODY.get(kraj_nazev, 0)
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
#         # Kontrola, zda je model načten
#         if model is None:
#             return jsonify({'error': 'Model není načten. Zkontrolujte konfiguraci.'}), 500

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

#         for mesto, info in config.VELKA_MESTA.items():
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
#             'lat': [lat],
#             'lon': [lon],
#             'new': [new],
#             'area': [area],
#             'kraj_kod': [kraj_kod],
#             'je_velke_mesto': [je_velke_mesto],
#             'vzdalenost_centrum_km': [vzdalenost_centrum_km],
#             'kod_velkeho_mesta': [kod_velkeho_mesta],
#             'room_number': [room_number],
#             'kitchen_number': [kitchen_number]
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

# @app.route('/reload_model', methods=['GET'])
# def reload_model():
#     """Endpoint pro ruční znovunačtení modelu."""
#     global model
#     model = load_model()
#     if model:
#         return jsonify({'status': 'success', 'message': f'Model úspěšně znovu načten z {config.MODEL_PATH}'})
#     else:
#         return jsonify({'status': 'error', 'message': 'Nepodařilo se znovu načíst model'}), 500

# # Pro přímé spuštění
# if __name__ == '__main__':
#     app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)



