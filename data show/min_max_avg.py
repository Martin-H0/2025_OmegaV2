import pandas as pd

def analyze_csv(file_path):
    # Načtení CSV souboru
    df = pd.read_csv(file_path)
    
    # Výběr pouze číselných sloupců
    numeric_cols = df.select_dtypes(include=['number'])
    
    # Výpočet statistik
    stats = numeric_cols.agg(['min', 'max', 'mean']).T
    stats.columns = ['Minimum', 'Maximum', 'Průměr']
    
    return stats

if __name__ == "__main__":
    file_path = "houses_martin_lokace_v10.csv"  # Změň na správnou cestu k souboru
    stats = analyze_csv(file_path)
    print(stats)
