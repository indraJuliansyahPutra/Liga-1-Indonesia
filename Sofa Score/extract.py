# extract.py
import os, re, time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = 'E:/Liga 1 Fix/chromedriver-win64/chromedriver.exe'

def setup_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--mute-audio')
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

def extract_link_klub():
    print(f"Proses Scraping Link Klub")
    driver = setup_driver()
    driver.maximize_window()

    url = "https://www.sofascore.com/id/turnamen/sepak-bola/indonesia/liga-1/1015#id:65049"
    driver.get(url)
    time.sleep(3)

    elements = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div/div[3]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/a')
    links = [e.get_attribute("href") for e in elements]
    driver.quit()

    os.makedirs("Link Pemain", exist_ok=True)
    pd.DataFrame(links, columns=["Link Klub"]).to_csv("Link_Klub.csv", index=False, encoding="utf-8-sig")
    print(f"[✔] {len(links)} klub berhasil diambil.")
    return links

def extract_link_pemain(links_klub):
    print(f"\nProses Scraping Link Pemain untuk Setiap Klub")
    for link in links_klub[:2]:
        try:
            driver = setup_driver()
            driver.maximize_window()
            driver.get(link)
            time.sleep(3)

            match = re.search(r'/tim/sepak-bola/([^/]+)/', link)
            if match:
                nama_klub = match.group(1).replace('-', ' ')  # Ganti dash dengan underscore kalau mau
            else:
                nama_klub = "tim_tidak_dikenal"
            print(f"[▶] Klub: {nama_klub}")

            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(2)

            link_pemain_elements = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div[5]/div/div[3]/div/div[2]/div/a')
            link_pemain = [element.get_attribute('href') for element in link_pemain_elements]

            # Simpan ke DataFrame
            df_links = pd.DataFrame(link_pemain, columns=["Link Pemain"])
            df_links.to_csv(f'Link Pemain/{nama_klub}.csv', index=False)
            print(f"[✔] Disimpan: Link Pemain/{nama_klub}.csv")
            print(f"[✔] {len(link_pemain)} pemain dari {nama_klub} disimpan.\n")

        except Exception as e:
            print(f"[❌] Gagal untuk {link} — {e}")
        finally:
            driver.quit()

def extract_data_pemain():
    print("Proses Scraping Data Pemain")
    xpath_default = {
        "Nama": '/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/h2',
        "Att": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/span',
        "Tec": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/span',
        "Tac": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[3]/div/div/span',
        "Def": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[4]/div/div/span',
        "Cre": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[5]/div/div/span',
        "Total Bermain": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]/div/div/div/div/div[1]/span[2]',
        "Starting Eleven": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]/div/div/div/div/div[2]/span[2]',
        "Total Menit": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]/div/div/div/div/div[4]/span[2]'
    }

    xpath_alternative = {
        "Nama": '/html/body/div[1]/main/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/h2',
        "Total Bermain": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div/div[1]/span[2]',
        "Starting Eleven": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div/div[2]/span[2]',
        "Total Menit": '/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div/div[4]/span[2]'
    }

    os.makedirs("Data Pemain", exist_ok=True)
    folder_path = "Link Pemain"
    for file in os.listdir(folder_path):
        if not file.endswith(".csv"): continue

        data = pd.read_csv(os.path.join(folder_path, file))
        links = data["Link Pemain"].tolist()
        nama_klub = file.replace(".csv", "")
        print(f"[▶] Klub: {nama_klub.title()}")
        hasil = []

        driver = setup_driver()
        driver.maximize_window()

        for link in links[:2]:
            driver.get(link)
            time.sleep(2)
            pemain = {"Link Pemain": link}

            try:
                driver.find_element(By.XPATH, xpath_default["Att"])  # test ATT exists
                for k, x in xpath_default.items():
                    try: pemain[k] = driver.find_element(By.XPATH, x).text
                    except: pemain[k] = None
            except:
                for k, x in xpath_alternative.items():
                    try: pemain[k] = driver.find_element(By.XPATH, x).text
                    except: pemain[k] = None
                for stat in ["Att", "Tec", "Tac", "Def", "Cre"]:
                    pemain[stat] = None
            print(f"[✔] {pemain['Nama']}")
            hasil.append(pemain)
        driver.quit()
        pd.DataFrame(hasil).to_csv(f"Data Pemain/{nama_klub}-PEMAIN.csv", index=False)
        print(f"[✔] Data pemain {nama_klub.title()} berhasil diambil.\n")
