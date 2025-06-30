# transform.py
import pandas as pd
import numpy as np
import os

def transform_data():
    folder_path = "Data Pemain"
    output_folder = "Data Bersih"
    os.makedirs(output_folder, exist_ok=True)
    print(f"\nProses Bersih-bersih (transform)")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    for file in csv_files:
        path = os.path.join(folder_path, file)
        data = pd.read_csv(path)

        kolom_diisi_nol = ['Penyelamatan', 'Gol', 'Tembakan',
                           'Tembakan Tepat Sasaran', 'Assist', 'Tekel',
                           'Intersepsi', 'Sapuan', 'Kartu Kuning',
                           'Kartu Merah', 'Pelanggaran', 'Offside']

        mask = data['Penampilan'].astype(str) == "0"
        data.loc[mask, kolom_diisi_nol] = 0
        data.loc[mask, "Umpan Sukses"] = "0/0"

        data[['Umpan Biasa', 'Umpan Total']] = data['Umpan Sukses'].str.split('/', expand=True)
        data['Umpan Sukses'] = data['Umpan Biasa'].astype(float)
        data['Umpan Total'] = data['Umpan Total'].astype(float)

        data['Akurasi Passing'] = np.where(
            data['Umpan Total'] == 0, 0, data['Umpan Sukses'] / data['Umpan Total']
        )
        data['Akurasi Tembakan'] = np.where(
            data['Tembakan'].astype(float) == 0, 0,
            data['Tembakan Tepat Sasaran'].astype(float) / data['Tembakan'].astype(float)
        )

        nama_file = file.replace("-PEMAIN.csv", ".csv")

        data.to_csv(os.path.join(output_folder, nama_file), index=False)
        print(f"[✔] Data bersih: {nama_file}")
