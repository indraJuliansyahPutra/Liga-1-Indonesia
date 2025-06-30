# main.py
from extract import extract_link_klub, extract_link_pemain, extract_data_pemain
from transform import transform_data
from load import gabung_data

if __name__ == "__main__":
    klub = extract_link_klub()
    extract_link_pemain(klub)
    extract_data_pemain()
    transform_data()
    gabung_data()
