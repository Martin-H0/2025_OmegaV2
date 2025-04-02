import os
import logging

# Basic application settings
DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'app/models/best_random_forest_model_RMSE_3377.6362.pkl')

# API settings
OSM_API_URL = "https://nominatim.openstreetmap.org/reverse"
OSM_USER_AGENT = "OMEGA_AI_Property_Estimator/1.0"

# Logger settings
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(BASE_DIR, 'app.log')

# Dictionary of major cities
VELKA_MESTA = { 
    "Praha": {"kod": 1, "lat": 50.0755, "lon": 14.4378}, 
    "Brno": {"kod": 2, "lat": 49.1951, "lon": 16.6068}, 
    "Ostrava": {"kod": 3, "lat": 49.8209, "lon": 18.2625}, 
    "Plzeň": {"kod": 4, "lat": 49.7384, "lon": 13.3736}, 
    "Liberec": {"kod": 5, "lat": 50.7663, "lon": 15.0543}, 
    "Olomouc": {"kod": 6, "lat": 49.5937, "lon": 17.2508}, 
    "České Budějovice": {"kod": 7, "lat": 48.9764, "lon": 14.5065}, 
    "Hradec Králové": {"kod": 8, "lat": 50.2091, "lon": 15.8323}, 
    "Ústí nad Labem": {"kod": 9, "lat": 50.6608, "lon": 14.0313}, 
    "Pardubice": {"kod": 10, "lat": 50.0343, "lon": 15.7812} 
}

# District names corresponding to district codes
DISTRICT_NAMES = {
    1: 'Praha',
    2: 'Moravskoslezsko',
    3: 'Severozápad',
    4: 'Jihozápad',
    5: 'Severovýchod',
    6: 'Střední Morava',
    7: 'Střední Čechy',
    8: 'Jihovýchod',
}

# District code mapping
KRAJE_KODY = { 
    'Praha': 1, 
    'Moravskoslezsko': 2, 
    'Severozápad': 3, 
    'Jihozápad': 4, 
    'Severovýchod': 5, 
    'Střední Morava': 6, 
    'Střední Čechy': 7, 
    'Jihovýchod': 8, 
}

# Extended mapping to handle different region names returned by OSM API
EXTENDED_REGION_MAPPING = {
    'Praha': 1,
    'Hlavní město Praha': 1,
    'Prague': 1,
    'Moravskoslezský kraj': 2,
    'Moravskoslezsko': 2,
    'Ústecký kraj': 3,
    'Karlovarský kraj': 3,
    'Severozápad': 3,
    'Plzeňský kraj': 4,
    'Jihočeský kraj': 4,
    'Jihozápad': 4,
    'Liberecký kraj': 5,
    'Královéhradecký kraj': 5,
    'Pardubický kraj': 5,
    'Severovýchod': 5,
    'Olomoucký kraj': 6,
    'Zlínský kraj': 6,
    'Střední Morava': 6,
    'Středočeský kraj': 7,
    'Střední Čechy': 7,
    'Jihomoravský kraj': 8,
    'Kraj Vysočina': 8,
    'Vysočina': 8,
    'Jihovýchod': 8,
}
