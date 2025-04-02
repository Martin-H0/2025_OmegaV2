
# Dokumentace projektu BytMetric.cz

---

## 1. Základní informace o projektu

### Název projektu:
**BytMetric.cz** – Inteligentní odhad cen pronájmů v České republice

### Autor:
- Martin Hornch

### Kontaktní údaje:
- Email: info@bytmetric.cz

### Datum vypracování:
- 02.04.2025

### Název školy:
- Střední průmyslová škola elektrotechnická Ječná 30

### Typ projektu:
- školní

---

## 2. Specifikace požadavků uživatele

### Požadavky na aplikaci:
1. **Odhad ceny pronájmu nemovitostí**:
   - Uživatel zadá parametry nemovitosti (plocha, počet pokojů, počet kuchyní, novostavba).
   - Uživatel označí lokaci nemovitosti na interaktivní mapě.
   - Aplikace vypočítá odhad ceny pronájmu pomocí trénovaného modelu Random Forest.

2. **Responzivní design**:
   - Aplikace musí být plně responzivní a přizpůsobitelná různým velikostem obrazovek.

3. **Navigace**:
   - Uživatel se může pohybovat mezi stránkami pomocí fixního headeru.

4. **404 stránka**:
   - Pokud uživatel navštíví neexistující URL, zobrazí se stránka s chybou 404.

5. **Favicon**:
   - Aplikace obsahuje favicon pro běžné prohlížeče i Android zařízení.

---

## 3. Architektura aplikace

### Popis architektury:
Aplikace je rozdělena na **backend** a **frontend** části:

#### Backend:
- **Flask**: Webový framework pro obsluhu HTTP požadavků.
- **Random Forest model**: Trénovaný model pro odhad ceny pronájmu.
- **Logger**: Modul pro logování chyb a událostí.

#### Frontend:
- **HTML**: Šablony pro jednotlivé stránky.
- **CSS**: Stylování aplikace.
- **JavaScript**: Interaktivní funkce (např. práce s mapou).
- **Bootstrap**: Framework pro responzivní design.
```
omega_project/
├── app/
│   ├── backend/
│   │   ├── app.py
│   │   ├── logger.py
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── main.js
│   │   │   ├── media/
│   │   │   │   └── logo/
│   │   │   │       └── logo_BytMetric_v5_AdobeExpress.png
│   │   │   └── favicon.ico
│   │   │
│   │   └── templates/
│   │       ├── header.html
│   │       ├── footer.html
│   │       ├── index.html 
│   │       ├── estimate.html
│   │       └── about.html
│   └── models/
│       └── best_random_forest_model_RMSE_3377.6362.pkl
├── config.py
├── run.py
├── install.py
├── requirements.txt  
└── app.log
```


---

### UML diagramy

#### Use Case diagram:
```mermaid
graph TD
    Uživatel --> Zadání parametrů nemovitosti
    Uživatel --> Označení lokace na mapě
    Uživatel --> Zobrazení odhadu ceny
    Uživatel --> Navigace mezi stránkami
    Uživatel --> Zobrazení 404 stránky
```

#### Use Case diagram:

---
## 4. Použití aplikace

### Popis chodu aplikace:
1. **Zadání parametrů nemovitosti**:
   - Uživatel vyplní formulář s parametry nemovitosti (plocha, počet pokojů, počet kuchyní, novostavba).
2. **Označení lokace na mapě**:
   - Uživatel klikne na mapu, aby označil lokaci nemovitosti.
3. **Výpočet odhadu ceny**:
   - Backend zpracuje data a použije model Random Forest k výpočtu odhadu ceny.
4. **Zobrazení výsledků**:
   - Uživatel vidí odhad ceny pronájmu a další informace o lokalitě.

---
## 5. Databáze

Aplikace **nepoužívá databázi**. Veškeré výpočty probíhají na základě dat zadaných uživatelem a trénovaného modelu Random Forest.

---
## 6. Konfigurace aplikace

### Konfigurační soubor:
**config.py** obsahuje:
- **Nastavení aplikace**:
  - `DEBUG`, `HOST`, `PORT`
- **Cesty k souborům**:
  - Model: `app/models/best_random_forest_model_RMSE_3377.6362.pkl`
  - Logy: `app.log`
- **API nastavení**:
  - URL pro OpenStreetMap: `https://nominatim.openstreetmap.org/reverse`
- **Mapování krajů a distriktů**:
  - Slovníky pro mapování názvů krajů na kódy.
---
## 7. Instalace a spuštění aplikace

### Instalace:
1. spuste install.py.
   ```bash
   python install.py
   ```
### Spuštění
1. Spusťte aplikaci příkazem.
   ```bash
   python run.py
   ```
2. Otevřete prohlížeč a přejděte na adresu:
      ```bash
   (http://127.0.0.1:5000/)
   ```

---
## 8. Chybové stavy

### Možné chyby:
1. **Model není načten**:
   - Chyba: `Model není načten. Zkontrolujte konfiguraci.`
   - Řešení: Ujistěte se, že soubor modelu existuje na správné cestě.

2. **Chyba při zjišťování kraje**:
   - Chyba: `Error detecting region: ...`
   - Řešení: Zkontrolujte dostupnost OpenStreetMap API.

3. **404 stránka**:
   - Chyba: `Stránka nenalezena.`
   - Řešení: Uživatel je přesměrován na 404 stránku.
---
## 9. Použité knihovny

### Knihovny třetích stran:
1. **Flask**: Webový framework.
2. **Pandas**: Práce s daty.
3. **Scikit-learn**: Strojové učení (Random Forest).
4. **Requests**: HTTP požadavky.
5. **Leaflet.js**: Interaktivní mapy.
6. **Bootstrap**: Responzivní design.
---
## 10. Závěrečné shrnutí

Projekt **BytMetric.cz** je webová aplikace pro odhad cen pronájmů nemovitostí v České republice. Aplikace využívá umělou inteligenci (Random Forest) k výpočtu odhadu ceny na základě parametrů nemovitosti a její lokace. Projekt je plně responzivní, obsahuje navigaci, 404 stránku a podporu pro favicon.

### Klíčové vlastnosti:
- Odhad ceny pronájmu.
- Responzivní design.
- Interaktivní mapa.
- Podpora pro Android favicon.

Projekt je připraven k dalšímu rozšíření, například přidání databáze nebo dalších funkcí.

