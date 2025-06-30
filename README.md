# 🏆 Liga 1 Indonesia – ETL Football Dashboard

Welcome! This project collects player and team statistics from Liga 1 Indonesia websites and turns them into clean, easy-to-analyze CSV files using Python and Selenium.
ETL stands for:

- **Extract** – Take the data from the website
- **Transform** – Clean and prepare the data
- **Load** – Save the final data to a file (CSV or Excel)

---

## 📁 Project Structure

Here's how the folders and files are organized:
liga-indonesia-baru/
├── extract.py
├── transform.py
├── load.py
├── main.py
├── Link_Klub.csv
├── Semua_Pemain.csv
├── /Data Pemain/
├── /Data Bersih/
└── /Link Pemain/

sofa score/
├── extract.py
├── transform.py
├── load.py
├── main.py
├── Link_Klub.csv
├── Semua_Pemain.csv
├── /Data Pemain/
├── /Data Bersih/
└── /Link Pemain/

transfermarkt/
├── extract.py
├── transform.py
├── load.py
├── main.py
├── Link_Klub.csv
├── Semua_Pemain.csv
├── /Data Pemain/
└── /Data Bersih/

logs/
├── 28 April 2025.md
├── 29 April 2025.md
├── 01 Mei 2025.md
├── 06-07 Mei 2025.md
├── 23 Juni 2025.md
└── 30 Juni 2025.md

## 🚀 How It Works

1. **Extract (extract.py)**

   - Open the Liga Indonesia Baru website
   - Get all club links
   - Visit each club page and get all player links
   - Visit each player page and get the data (goals, assists, cards, etc.)

2. **Transform (transform.py)**

   - Clean the data
   - Fix missing values
   - Split data like “successful passes” into numbers
   - Calculate accuracy percentages (like passing and shooting)

3. **Load (load.py)**

   - Save the cleaned data into the `Data Bersih/` folder as CSV or Excel

4. **main.py**
   - Just run this file to do all the steps automatically.

---

## ✅ How to Use

> Make sure you have **Google Chrome** and the **ChromeDriver** installed. Place your `chromedriver.exe` inside the `chromedriver-win64` folder.

1. Open your terminal and activate the virtual environment:

   ```bash
   .\venv\Scripts\activate

   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the pipeline:

   ```bash
   python main.py
   ```

That’s it! The data will be saved in the `Data Bersih` folder.

---

## 📮 Contact

If you have questions or ideas, feel free to contact me!

- GitHub: [@indraJuliansyahPutra](https://github.com/indraJuliansyahPutra)
- Website: [indranalytics.netlify.app](https://indranalytics.netlify.app/)
- Medium: [@mrindrajuliansyahputra10](https://medium.com/@mrindrajuliansyahputra10)

Thanks for visiting this repo! 👋

## Progress and Change Log

- [Progress Log 28 April 2025](logs/28%20April%202025.md)
- [Progress Log 29 April 2025](logs/29%20April%202025.md)
- [Progress Log 01 Mei 2025](logs/01%20Mei%202025.md)
- [Progress Log 06 Mei 2025](logs/06%20Mei%202025.md)
- [Progress Log 23 Juni 2025](logs/23%20Juni%202025.md)
- [Progress Log 30 Juni 2025](logs/30%20Juni%202025.md)
