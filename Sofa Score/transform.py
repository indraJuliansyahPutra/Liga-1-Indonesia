# transform.py
import os
import pandas as pd

def transform_data():
    input_folder = "Data Pemain"
    output_folder = "Data Bersih"
    os.makedirs(output_folder, exist_ok=True)
    print(f"\nProses Bersih-bersih (transform)")

    for file in os.listdir(input_folder):
        if not file.endswith(".csv"):
            continue

        path = os.path.join(input_folder, file)
        df = pd.read_csv(path)
        df["Nama"] = df["Nama"].str.upper()

        kolom = ['Nama', 'Att', 'Tac', 'Tec', 'Def', 'Cre', 'Total Bermain', 'Starting Eleven', 'Total Menit', 'Link Pemain']
        for k in kolom:
            if k not in df.columns:
                df[k] = None

        df = df[kolom]
        nama_file = file.replace("-PEMAIN.csv", ".csv")
        df.to_csv(os.path.join(output_folder, nama_file), index=False)
        print(f"[✔] Data bersih: {nama_file}")
