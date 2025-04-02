
MODEL_PATH = "models/best_random_forest_model_RMSE_3377.6362.pkl"

# Nastavení Flask aplikace
DEBUG = True
HOST = "127.0.0.1"          # ip addresa hostu
PORT = 5000                 # port na kter0m pob269 veb


# Nastavení logování
LOG_DIR = 'logs'                                  # Adresář pro ukládání logů
LOG_LEVEL = 'INFO'                                # Úroveň logování (DEBUG, INFO, WARNING, ERROR, CRITICAL)
API_LOG_FORMAT = '%(asctime)s - %(message)s'      # Formát záznamu pro API logy
ERROR_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'  # Formát záznamu pro chybové logy


# Nastavení OpenStreetMap API
OSM_API_URL = "https://nominatim.openstreetmap.org/reverse"
OSM_USER_AGENT = "HousePricePredictor/1.0"

# Slovník velkých měst/spádových oblastí
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

# Mapování distriktů/krajů
KRAJE_KODY = {
    'Praha': 1,
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
    'Jihovýchod': 8,
}