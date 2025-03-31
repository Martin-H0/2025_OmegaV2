import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('houses_martin_lokace_v9.csv', sep=',') #houses_martin_lokace_v9.csv
df.dropna(inplace=True)
input_features = ["lat","lon","new","parking_lots","garage","area","room_number","kitchen_number","bonus","kraj_kod","je_velke_mesto","vzdalenost_centrum_km","kod_velkeho_mesta"]
target_feature = "price"

sns.pairplot(df[input_features + [target_feature]], kind="scatter")
plt.suptitle("Scatter Plot of House Attributes and Prices", y=1.01)
plt.show()



import matplotlib.pyplot as plt


for feature in input_features:
    plt.figure(figsize=(8, 6))
    plt.scatter(df[feature], df[target_feature], alpha=0.5)
    plt.title(f"{feature} vs {target_feature}")
    plt.xlabel(feature)
    plt.ylabel(target_feature)
    plt.show()