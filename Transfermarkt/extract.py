# extract.py
import time, os, re
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

def get_xpath(driver, xpath):
    try: return driver.find_element(By.XPATH, xpath).text.strip()
    except: return None

def extract_link_klub():
    print(f"Proses Scraping Link Klub")
    driver = setup_driver()
    driver.maximize_window()

    url = "https://www.transfermarkt.co.id/liga-1-indonesia/startseite/wettbewerb/IN1L"
    driver.get(url)
    time.sleep(2)

    elements = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[1]/div[1]/div[2]/div[2]/div/table/tbody/tr/td[2]/a')
    links = [el.get_attribute('href') for el in elements if "verein" in el.get_attribute("href")]
    klub_links = [link.replace("/startseite/", "/kader/") + "/plus/1" for link in set(links)]

    driver.quit()
    pd.DataFrame(klub_links, columns=["Link Klub"]).to_csv("Link_Klub.csv", index=False)
    print(f"[✔] {len(klub_links)} klub berhasil diambil.")
    return klub_links

def extract_data_pemain(link_klub):
    print("\nProses Scraping Data Pemain")
    os.makedirs("Data Pemain", exist_ok=True)

    for link in link_klub[:2]:
        driver = setup_driver(headless=False)
        driver.maximize_window()
        driver.get(link)
        time.sleep(5)
        
        pattern = r"transfermarkt\.co\.id/([^/]+)/kader"
        match = re.search(pattern, link)

        if match:
            klub_raw = match.group(1)
            nama_klub = klub_raw.replace('-', ' ').title()
        else:
            nama_klub = "tim_tidak_dikenal"
        print(f"[▶] Klub: {nama_klub}")

        data_pemain = []
        for i in range(1, 3):
            try:
                nama_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[2]/table/tbody/tr[1]/td[2]/a'
                nama = driver.find_element(By.XPATH, nama_xpath).text.strip()
            except:
                continue

            klub_xpath = f'/html/body/div/main/header/div[1]/h1'
            posisi_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[2]/table/tbody/tr[2]/td'
            tinggi_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[5]'
            lahir_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[3]'
            kaki_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[6]'
            value_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[10]/a'
            nomor_xpath = f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[1]/div'
            link_xpath = nama_xpath

            data = {
                "Nama": nama,
                "Klub": get_xpath(driver, klub_xpath),
                "Posisi": get_xpath(driver, posisi_xpath),
                "Tinggi": get_xpath(driver, tinggi_xpath),
                "Tanggal Lahir": get_xpath(driver, lahir_xpath),
                "Kaki Dominan": get_xpath(driver, kaki_xpath),
                "Nilai Pasar": get_xpath(driver, value_xpath),
                "Nomor Punggung": get_xpath(driver, nomor_xpath),
                "Link": driver.find_element(By.XPATH, link_xpath).get_attribute('href')
            }
            data_pemain.append(data)
            print(f"[✔] {nama}")

        nama_klub = get_xpath(driver, klub_xpath)
        driver.quit()

        df = pd.DataFrame(data_pemain)
        df.to_csv(f"Data Pemain/{nama_klub}.csv", index=False, encoding='utf-8-sig')
        print(f"[✔] Data pemain {nama_klub.title()} berhasil diambil.\n")

if __name__ == "__main__":
    klub_links = extract_link_klub()
    extract_data_pemain(klub_links)
