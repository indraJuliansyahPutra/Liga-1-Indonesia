# main.py
from extract import extract_link_klub, extract_data_pemain
from transform import transform_data
from load import gabungkan_data

if __name__ == "__main__":
    klub = extract_link_klub()
    extract_data_pemain(klub)
    transform_data()
    gabungkan_data()
