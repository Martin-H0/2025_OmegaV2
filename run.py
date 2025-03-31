# spouštěcí soubor pro applikaci

from App.backend.app import app
import config

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)