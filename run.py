import sys
import os

# Přidání aktuálního adresáře do cesty pro import
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.backend.app import app
import config

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
