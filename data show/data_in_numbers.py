import pandas as pd

# Načtení CSV souboru
file_path = 'houses_martin_lokace_v8.csv'  # Změňte na cestu k vašemu souboru
data = pd.read_csv(file_path)

# Seznam číselných sloupců
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

# Výpočet min, max a průměr pro každý číselný sloupec
stats = {}
for col in numeric_columns:
    stats[col] = {
        'min': data[col].min(),
        'max': data[col].max(),
        'mean': data[col].mean()
    }

# Výpis statistik pro číselné sloupce
print("Statistiky pro číselné sloupce:")
for col, values in stats.items():
    print(f"{col} - Min: {values['min']}, Max: {values['max']}, Mean: {values['mean']}")

# Počet záznamů podle 'nazev_velkeho_mesta' (velké město)
city_counts = data['nazev_velkeho_mesta'].value_counts()
print("\nPočet záznamů podle velkého města:")
print(city_counts)

# Počet záznamů podle 'kraj_kod' (kraj)
region_counts = data['kraj_kod'].value_counts()
print("\nPočet záznamů podle kraje (kraj_kod):")
print(region_counts)

# Počet záznamů podle 'nazev_kraje' (název kraje)
region_name_counts = data['nazev_kraje'].value_counts()
print("\nPočet záznamů podle názvu kraje:")
print(region_name_counts)

# Počet záznamů podle kombinace 'kraj_kod' a 'nazev_velkeho_mesta'
region_city_counts = data.groupby(['kraj_kod', 'nazev_velkeho_mesta']).size()
print("\nPočet záznamů podle kombinace kraje a města:")
print(region_city_counts)

# Další smysluplné kombinace
# Počet záznamů podle 'parking_lots' (počet parkovacích míst)
parking_counts = data['parking_lots'].value_counts()
print("\nPočet záznamů podle počtu parkovacích míst:")
print(parking_counts)

# Počet záznamů podle 'garage' (garáž)
garage_counts = data['garage'].value_counts()
print("\nPočet záznamů podle garáže:")
print(garage_counts)
