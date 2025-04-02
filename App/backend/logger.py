import logging
import os
import json
from datetime import datetime
import traceback

class PredictionLogger:
    def __init__(self, log_dir='logs'):
        """
        Inicializace loggeru pro predikční API.
        
        Args:
            log_dir (str): Adresář, kam se budou ukládat logy
        """
        # Vytvoření adresáře pro logy, pokud neexistuje
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Nastavení hlavního loggeru
        self.logger = logging.getLogger('prediction_api')
        self.logger.setLevel(logging.INFO)
        
        # Vytvoření formátovače pro konzoli
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Handler pro výpis do konzole
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Přidání handleru do loggeru
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

        # Nastavení loggeru pro API požadavky
        self._setup_api_logger()
        
        # Nastavení loggeru pro chyby
        self._setup_error_logger()

    def _setup_api_logger(self):
        """Vytvoření loggeru pro API požadavky"""
        self.api_logger = logging.getLogger('prediction_api.requests')
        self.api_logger.setLevel(logging.INFO)
        
        # Vytvoření souboru pro dnešní datum
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.log_dir, f'api_requests_{today}.log')
        
        # Nastavení formátovače
        file_formatter = logging.Formatter('%(asctime)s - %(message)s')
        
        # Handler pro zápis do souboru
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Odstranění předchozích handlerů, pokud existují
        if self.api_logger.handlers:
            self.api_logger.handlers.clear()
            
        # Přidání handleru
        self.api_logger.addHandler(file_handler)

    def _setup_error_logger(self):
        """Vytvoření loggeru pro chyby"""
        self.error_logger = logging.getLogger('prediction_api.errors')
        self.error_logger.setLevel(logging.ERROR)
        
        # Vytvoření souboru pro chyby
        error_log_file = os.path.join(self.log_dir, 'errors.log')
        
        # Nastavení formátovače
        error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Handler pro zápis do souboru
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(error_formatter)
        
        # Odstranění předchozích handlerů, pokud existují
        if self.error_logger.handlers:
            self.error_logger.handlers.clear()
            
        # Přidání handleru
        self.error_logger.addHandler(error_handler)

    def log_request(self, request_data, client_ip=None):
        """
        Logování požadavku na API.
        
        Args:
            request_data (dict): Data požadavku
            client_ip (str): IP adresa klienta
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'client_ip': client_ip,
            'request_data': request_data
        }
        self.api_logger.info(json.dumps(log_entry, ensure_ascii=False))
        self.logger.info(f"Přijat požadavek na predikci z IP: {client_ip}")

    def log_response(self, response_data, client_ip=None, processing_time=None):
        """
        Logování odpovědi API.
        
        Args:
            response_data (dict): Data odpovědi
            client_ip (str): IP adresa klienta
            processing_time (float): Doba zpracování v sekundách
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'client_ip': client_ip,
            'processing_time_ms': round(processing_time * 1000, 2) if processing_time else None,
            'response_data': response_data
        }
        self.api_logger.info(json.dumps(log_entry, ensure_ascii=False))
        
        predicted_price = response_data.get('predicted_price', 'N/A')
        self.logger.info(f"Odeslána predikce: {predicted_price} Kč, IP: {client_ip}, Čas: {processing_time:.4f}s")

    def log_error(self, error_message, client_ip=None, request_data=None):
        """
        Logování chyby při zpracování požadavku.
        
        Args:
            error_message (str): Zpráva o chybě
            client_ip (str): IP adresa klienta
            request_data (dict): Data požadavku
        """
        error_trace = traceback.format_exc()
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'client_ip': client_ip,
            'error_message': str(error_message),
            'request_data': request_data,
            'traceback': error_trace
        }
        self.error_logger.error(json.dumps(log_entry, ensure_ascii=False))
        self.logger.error(f"Chyba při zpracování požadavku: {error_message}, IP: {client_ip}")

    def log_model_load(self, model_path, success):
        """
        Logování informace o načtení modelu.
        
        Args:
            model_path (str): Cesta k modelu
            success (bool): Úspěch načtení
        """
        if success:
            self.logger.info(f"Model úspěšně načten z: {model_path}")
        else:
            self.logger.error(f"Nepodařilo se načíst model z: {model_path}")