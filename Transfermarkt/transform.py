# transform.py
import pandas as pd
import os

def ke_miliar(nilai):
    if pd.isna(nilai) or not isinstance(nilai, str):
        return 0.0
    nilai = nilai.replace('Rp', '').replace('.', '')
    if 'Mlyr' in nilai:
        return float(nilai.replace('Mlyr', '').replace(',', '.'))
    elif 'Jt' in nilai:
        return float(nilai.replace('Jt', '').replace(',', '.')) / 1000
    return 0.0

def transform_data():
    os.makedirs("Data Bersih", exist_ok=True)
    folder_path = "Data Pemain"
    print(f"\nProses Bersih-bersih (transform)")

    for file in os.listdir(folder_path):
        if not file.endswith(".csv"):
            continue

        df = pd.read_csv(os.path.join(folder_path, file))
        nama_file = file.replace(".csv", "")

        df['Nama'] = df['Nama'].str.upper()
        df['Klub'] = df['Klub'].str.upper()
        df['Posisi'] = df['Posisi'].str.upper()
        df['Tinggi'] = df['Tinggi'].str.replace("m", "").str.replace(".", ",", regex=False)
        df["Usia"] = df["Tanggal Lahir"].str.extract(r"\((\d+)\)").astype(float)
        df["Tanggal Lahir"] = df["Tanggal Lahir"].str.replace(r"\s*\(\d+\)", "", regex=True)
        df['Kaki Dominan'] = df['Kaki Dominan'].str.upper()
        df['Nomor Punggung'] = df['Nomor Punggung'].replace("-", "0")
        df['Nilai Pasar'] = df['Nilai Pasar'].apply(ke_miliar).round(2)

        df = df.sort_values(by="Nama")
        df.to_csv(f'Data Bersih/{nama_file}.csv', index=False)
        df.to_excel(f'Data Bersih/{nama_file}.xlsx', index=False)
        print(f"[✔] Data Bersih: {nama_file}")
