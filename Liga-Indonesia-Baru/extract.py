# extract.py
import time, os, re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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

    url = "https://ligaindonesiabaru.com/clubs/index/BRI_LIGA_1_2024-25"
    driver.get(url)
    time.sleep(2)

    klub_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/section/div/div/div/div/a')
    links = [e.get_attribute('href') for e in klub_elements]
    driver.quit()

    df = pd.DataFrame(links, columns=['Link Klub'])
    df.to_csv('Link_Klub.csv', index=False, encoding='utf-8-sig')
    print(f"[✔] {len(links)} klub berhasil diambil.")
    return links

def extract_link_pemain():
    print(f"\nProses Scraping Link Pemain untuk Setiap Klub")
    links = pd.read_csv("Link_Klub.csv")['Link Klub'].tolist()

    for link in links[:2]:
        driver = setup_driver()
        driver.maximize_window()
        driver.get(link)
        time.sleep(3)

        nama_klub = re.search(r'(?<=/single/BRI_LIGA_1_2024-25/)([A-Za-z0-9_]+)', link).group(1)
        print(f"[▶] Klub: {nama_klub}")

        try:
            tab = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div/div/div[1]/ul/li[2]/a')
            tab.click()
            time.sleep(3)
        except:
            print(f"Gagal klik tab pemain: {link}")
            driver.quit()
            continue

        links_pemain = []
        i = 1
        while True:
            try:
                xpath = f"/html/body/div[2]/section/div/div/div/div[2]/div/div[2]/div/div[{i}]/div/a"
                elem = driver.find_element(By.XPATH, xpath)
                links_pemain.append(elem.get_attribute('href'))
                i += 1
            except:
                break

        df = pd.DataFrame(links_pemain, columns=['Link Pemain'])
        os.makedirs("Link Pemain", exist_ok=True)
        df.to_csv(f"Link Pemain/{nama_klub}.csv", index=False, encoding='utf-8-sig')
        print(f"[✔] Disimpan: Link Pemain/{nama_klub}.csv")
        print(f"[✔] {len(links_pemain)} pemain dari {nama_klub} disimpan.\n")
        driver.quit()

def extract_data_pemain():
    print("Proses Scraping Data Pemain")
    folder_path = "Link Pemain"
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    os.makedirs("Data Pemain", exist_ok=True)

    for file in csv_files[:2]:
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)
        link_pemain = data['Link Pemain'].tolist()

        nama_klub = file.replace(".csv", "")
        print(f"[▶] Klub: {nama_klub.title()}")
        data_pemain = []

        for link in link_pemain[:2]:
            driver = setup_driver()
            driver.maximize_window()
            driver.get(link)
            time.sleep(2)

            def get_xpath(xpath):
                try:
                    return driver.find_element(By.XPATH, xpath).text.strip()
                except:
                    return None

            pemain = {
                'Nama Punggung': get_xpath('/html/body/div[2]/div/div/div/div[2]/h1[2]'),
                'Nomor Punggung': get_xpath('/html/body/div[2]/div/div/div/div[2]/h1[1]'),
                'Nama Lengkap': get_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div/table/tbody/tr[2]/td'),
                'Klub': get_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div/table/tbody/tr[3]/td[2]'),
                'Posisi': get_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div/table/tbody/tr[4]/td[2]'),
                'Usia': get_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div/table/tbody/tr[5]/td[2]'),
                'Negara': get_xpath('/html/body/div[2]/section/div/div/div/div[1]/div/div/table/tbody/tr[6]/td[2]'),
                'Penampilan': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[1]/ul/li[1]/h3'),
                'Penyelamatan': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[1]/ul/li[3]/h3'),
                'Gol': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div/ul/li[1]/p/span'),
                'Tembakan': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div/ul/li[2]/p/span'),
                'Tembakan Tepat Sasaran': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div/ul/li[3]/p/span'),
                'Assist': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/ul/li[1]/p/span'),
                'Umpan Sukses': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/ul/li[2]/p/span'),
                'Tekel': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[3]/div/ul/li[1]/p/span'),
                'Intersepsi': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[3]/div/ul/li[2]/p/span'),
                'Sapuan': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[3]/div/ul/li[3]/p/span'),
                'Kartu Kuning': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[4]/div/ul/li[1]/p/span'),
                'Kartu Merah': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[4]/div/ul/li[2]/p/span'),
                'Pelanggaran': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[4]/div/ul/li[3]/p/span'),
                'Offside': get_xpath('/html/body/div[2]/section/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[4]/div/ul/li[4]/p/span')
            }
            print(f"[✔] {pemain['Nama Punggung']}")
            data_pemain.append(pemain)
            driver.quit()

        nama_klub = file.replace(".csv", "")
        df = pd.DataFrame(data_pemain)
        df.to_csv(f"Data Pemain/{nama_klub}-PEMAIN.csv", index=False)
        print(f"[✔] Data pemain {nama_klub} berhasil diambil.\n")
