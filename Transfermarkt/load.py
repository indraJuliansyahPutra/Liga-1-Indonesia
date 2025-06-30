# load.py
import pandas as pd
import os

def gabungkan_data():
    folder = "Data Bersih"
    semua_data = []

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            df["Asal Klub"] = file.replace(".csv", "")
            semua_data.append(df)

    df_all = pd.concat(semua_data, ignore_index=True)
    df_all.to_csv("Semua_Pemain.csv", index=False)
    print(f"\n[✔] Semua data pemain berhasil digabung ke 'Semua_Pemain.csv'")
