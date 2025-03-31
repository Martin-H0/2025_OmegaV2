import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Načtení dat
df = pd.read_csv('houses_martin_lokace_v9.csv', sep=',')
df.dropna(inplace=True)

# "lat", "lon", "new", "parking_lots", "garage", "area", "room_number", 
#                   "kitchen_number", "bonus", "kraj_kod", "je_velke_mesto", "vzdalenost_centrum_km", "kod_velkeho_mesta"
# Definice proměnných
input_features = ["lat", "lon", "new","area", "room_number", "kitchen_number", "kraj_kod", "je_velke_mesto", "vzdalenost_centrum_km", "kod_velkeho_mesta"]
target_feature = "price"

# 1) Pairplot se všemi daty
sns.pairplot(df[input_features + [target_feature]], kind="scatter")
plt.suptitle("Scatter Plot of House Attributes and Prices (všechny záznamy)", y=1.01)
plt.show()

# Rozdělení datasetu na dvě části
df_bez_velkomest = df[df["kod_velkeho_mesta"] != 1.0]  # Bez velkých měst
df_jen_velkomesta = df[df["kod_velkeho_mesta"] == 1.0]  # Jen velká města (Praha)
# df_1Praha = df[df["kraj_kod"] == 1] 
# df_2Moravskoslezsko = df[df["kraj_kod"] == 2]
# df_3Severozápad = df[df["kraj_kod"] == 3] 
# df_4Jihozápad = df[df["kraj_kod"] == 4] 
# df_5Severovýchod = df[df["kraj_kod"] == 5] 
# df_6Střední_Morava = df[df["kraj_kod"] == 6] 
# df_7Jihovýchod = df[df["kraj_kod"] == 7] 

# # 2) Scatter ploty BEZ velkých měst (kod_velkeho_mesta != 1.0)
# for feature in input_features:
#     plt.figure(figsize=(8, 6))
#     plt.scatter(df_bez_velkomest[feature], df_bez_velkomest[target_feature], alpha=0.5, color='blue')
#     plt.title(f"{feature} vs {target_feature} (bez Prahy)")
#     plt.xlabel(feature)
#     plt.ylabel(target_feature)
#     plt.show()

# # 3) Scatter ploty POUZE PRO velká města (kod_velkeho_mesta == 1.0)
# for feature in input_features:
#     plt.figure(figsize=(8, 6))
#     plt.scatter(df_jen_velkomesta[feature], df_jen_velkomesta[target_feature], alpha=0.5, color='red')
#     plt.title(f"{feature} vs {target_feature} (Praha a oklolí)")
#     plt.xlabel(feature)
#     plt.ylabel(target_feature)
#     plt.show()

# # 4) Scatter ploty pro všechny záznamy, ale s odlišením Prahy jinou barvou
# for feature in input_features:
#     plt.figure(figsize=(8, 6))
#     plt.scatter(df_bez_velkomest[feature], df_bez_velkomest[target_feature], alpha=0.1, color='blue', label="Ostatní města")
#     plt.scatter(df_jen_velkomesta[feature], df_jen_velkomesta[target_feature], alpha=0.1, color='red', label="Praha")
#     plt.title(f"{feature} vs {target_feature} (Praha vs ostatní)")
#     plt.xlabel(feature)
#     plt.ylabel(target_feature)
#     plt.legend()
#     plt.show()



# # 4) Scatter ploty pro všechny záznamy, ale s odlišením Prahy jinou barvou
# for feature in input_features:
#     plt.figure(figsize=(8, 6))
#     plt.scatter(df_1Praha[feature], df_1Praha[target_feature], alpha=0.1, color='red', label="Praha")
#     plt.scatter(df_2Moravskoslezsko[feature], df_2Moravskoslezsko[target_feature], alpha=0.1, color='red', label="Moravskoslezsko")
#     plt.scatter(df_3Severozápad[feature], df_3Severozápad[target_feature], alpha=0.1, color='red', label="Severozápad")
#     plt.scatter(df_4Jihozápad[feature], df_4Jihozápad[target_feature], alpha=0.1, color='red', label="Jihozápad")
#     plt.scatter(df_5Severovýchod[feature], df_5Severovýchod[target_feature], alpha=0.1, color='red', label="Severovýchod")
#     plt.scatter(df_6Střední_Morava[feature], df_6Střední_Morava[target_feature], alpha=0.1, color='red', label="Střední_Morava")
#     plt.scatter(df_7Jihovýchod[feature], df_7Jihovýchod[target_feature], alpha=0.1, color='red', label="Jihovýcho")

#     plt.title(f"{feature} vs {target_feature} (Praha vs ostatní)")
#     plt.xlabel(feature)
#     plt.ylabel(target_feature)
#     plt.legend()
#     plt.show()




kraje = {
    "Praha": df[df["kraj_kod"] == 1],
    "Moravskoslezsko": df[df["kraj_kod"] == 2],
    "Severozápad": df[df["kraj_kod"] == 3],
    "Jihozápad": df[df["kraj_kod"] == 4],
    "Severovýchod": df[df["kraj_kod"] == 5],
    "Střední Morava": df[df["kraj_kod"] == 6],
    "Jihovýchod": df[df["kraj_kod"] == 7]
}

# Definování barev pro každý kraj
kraj_colors = {
    "Praha": "red",
    "Moravskoslezsko": "blue",
    "Severozápad": "green",
    "Jihozápad": "purple",
    "Severovýchod": "orange",
    "Střední Morava": "cyan",
    "Jihovýchod": "brown"
}



# Scatter ploty pro každý kraj
for feature in input_features:
    plt.figure(figsize=(8, 6))

    # Pro každý kraj vykreslí scatter plot s unikátní barvou
    for kraj, df_kraj in kraje.items():
        plt.scatter(df_kraj[feature], df_kraj[target_feature], 
                    alpha=0.3, color=kraj_colors[kraj], label=kraj)

    plt.title(f"{feature} vs {target_feature} (Rozděleno podle krajů)")
    plt.xlabel(feature)
    plt.ylabel(target_feature)
    plt.legend()
    plt.show()