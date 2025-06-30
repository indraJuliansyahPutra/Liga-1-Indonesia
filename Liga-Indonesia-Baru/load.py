# load.py
import pandas as pd
import os

def gabungkan_data():
    folder = "Data Bersih"
    all_data = []

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            data = pd.read_csv(os.path.join(folder, file))
            all_data.append(data)

    data_all = pd.concat(all_data, ignore_index=True)
    data_all.to_csv("Semua_Pemain.csv", index=False, encoding='utf-8-sig')
    print(f"\n[✔] Semua data pemain berhasil digabung ke 'Semua_Pemain.csv'")
