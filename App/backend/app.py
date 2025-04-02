from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import pandas as pd
import requests
import time
from math import radians, sin, cos, sqrt, atan2
import os
import sys

#efef
# Add path for config file import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config
from app.backend.logger import Logger

# Initialize logger
logger = Logger("omega_app")

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Load trained model
def load_model():
    try:
        with open(config.MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
            logger.info(f"Model loaded from: {config.MODEL_PATH}")
            return model
    except FileNotFoundError:
        logger.error(f"ERROR: Model {config.MODEL_PATH} not found!")
        return None
    except Exception as e:
        logger.error(f"ERROR loading model: {str(e)}")
        return None

# Load model at application startup
model = load_model()

# Function to calculate distance between two points (Haversine formula)
def vypocet_vzdalenosti(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# API to get region information
def zjisti_kraj(lat, lon):
    try:
        url = f"{config.OSM_API_URL}?lat={lat}&lon={lon}&format=json&accept-language=cs"
        headers = {'User-Agent': config.OSM_USER_AGENT}
        logger.info(f"OSM API request: {url}")
        response = requests.get(url, headers=headers)
        data = response.json()

        # Check different possibilities where region information might be stored
        kraj_nazev = data.get('address', {}).get('state', None)
        if not kraj_nazev:
            kraj_nazev = data.get('address', {}).get('county', 'Unknown')

        logger.info(f"Region detected: {kraj_nazev}")
        
        # Map the region to district code using the updated mapping
        kraj_kod = 0
        for region, code in config.EXTENDED_REGION_MAPPING.items():
            if region.lower() in kraj_nazev.lower() or kraj_nazev.lower() in region.lower():
                kraj_kod = code
                break
                
        if kraj_kod == 0:
            logger.warning(f"Could not map region '{kraj_nazev}' to any district code")
            district_name = "Unknown"
        else:
            # Get district name from the district code
            district_name = config.DISTRICT_NAMES.get(kraj_kod, "Unknown")
            logger.info(f"Mapped to district: {district_name} (code: {kraj_kod})")
            
        return kraj_kod, district_name
    except Exception as e:
        logger.error(f"Error detecting region: {e}")
        return 0, "Unknown"

# Basic routes
@app.route('/')
def index():
    logger.info("Access to home page")
    return render_template('index.html')

@app.route('/estimate')
def estimate():
    logger.info("Access to estimate page")
    return render_template('estimate.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if model is loaded
        if model is None:
            logger.error("Model is not loaded.")
            return jsonify({'error': 'Model is not loaded. Check configuration.'}), 500

        data = request.json
        logger.info(f"Prediction data received: {data}")

        # Process basic parameters from user
        new = int(data.get('new', 0))
        area = float(data.get('area', 0))
        room_number = int(data.get('room_number', 0))
        kitchen_number = int(data.get('kitchen_number', 0))

        # Get coordinates
        lat = float(data.get('lat', 0))
        lon = float(data.get('lon', 0))

        # Get region information
        kraj_kod, nazev_kraje = zjisti_kraj(lat, lon)

        # Calculate distance to major cities
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

        logger.info(f"Nearest city: {nejblizsi_mesto}, distance: {vzdalenost_centrum_km} km")

        # Create DataFrame for prediction
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

        # Predict price
        predicted_price = model.predict(input_data)[0]
        logger.info(f"Predicted price: {predicted_price}")

        # Prepare response
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
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/reload_model', methods=['GET'])
def reload_model():
    """Endpoint for manual model reloading."""
    global model
    logger.info("Reloading model")
    model = load_model()
    if model:
        return jsonify({'status': 'success', 'message': f'Model successfully reloaded from {config.MODEL_PATH}'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to reload model'}), 500





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
# from app.backend.logger import Logger

# # Inicializace loggeru
# logger = Logger("omega_app")

# app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# # Načtení natrénovaného modelu
# def load_model():
#     try:
#         with open(config.MODEL_PATH, 'rb') as file:
#             model = pickle.load(file)
#             logger.info(f"Model načten z: {config.MODEL_PATH}")
#             return model
#     except FileNotFoundError:
#         logger.error(f"CHYBA: Model {config.MODEL_PATH} nebyl nalezen!")
#         return None
#     except Exception as e:
#         logger.error(f"CHYBA při načítání modelu: {str(e)}")
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
#         logger.info(f"Dotaz na OSM API: {url}")
#         response = requests.get(url, headers=headers)
#         data = response.json()

#         # Zkontrolujeme různé možnosti, kde může být informace o kraji
#         kraj_nazev = data.get('address', {}).get('state', None)
#         if not kraj_nazev:
#             kraj_nazev = data.get('address', {}).get('county', 'Neznámý')

#         logger.info(f"Zjištěný kraj: {kraj_nazev}")
#         kraj_kod = config.KRAJE_KODY.get(kraj_nazev, 0)
#         return kraj_kod, kraj_nazev
#     except Exception as e:
#         logger.error(f"Chyba při zjišťování kraje: {e}")
#         return 0, "Neznámý"

# # Základní routy
# @app.route('/')
# def index():
#     logger.info("Přístup na hlavní stránku")
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Kontrola, zda je model načten
#         if model is None:
#             logger.error("Model není načten.")
#             return jsonify({'error': 'Model není načten. Zkontrolujte konfiguraci.'}), 500

#         data = request.json
#         logger.info(f"Přijata predikční data: {data}")

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

#         logger.info(f"Nejbližší město: {nejblizsi_mesto}, vzdálenost: {vzdalenost_centrum_km} km")

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
#         logger.info(f"Predikovaná cena: {predicted_price}")

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
#         logger.error(f"Chyba při predikci: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/reload_model', methods=['GET'])
# def reload_model():
#     """Endpoint pro ruční znovunačtení modelu."""
#     global model
#     logger.info("Probíhá znovunačtení modelu")
#     model = load_model()
#     if model:
#         return jsonify({'status': 'success', 'message': f'Model úspěšně znovu načten z {config.MODEL_PATH}'})
#     else:
#         return jsonify({'status': 'error', 'message': 'Nepodařilo se znovu načíst model'}), 500
