from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Configuração do Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrir a página
url = "https://www.baseball-almanac.com/hitting/hihr5.shtml"
driver.get(url)
time.sleep(3)
html = driver.page_source
driver.quit()

# Parse com BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

# Lista para armazenar dados
data = []

# Percorrer as linhas da tabela (ignorando cabeçalho externo)
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if len(cols) != 8:
        continue  # Linha malformada

    # Extrair texto das colunas
    values = [col.get_text(strip=True) for col in cols]

    # Ignorar linhas de cabeçalho interno repetido
    if any("Year" in val for val in values):
        continue

    # Ignorar linhas com apenas traços ou vazias
    if all(val == "-" or val == "" for val in values):
        continue

    # American League
    year_al, player_al, hr_al, team_al = values[0:4]
    if player_al != "-" and hr_al != "-":
        data.append({
            "Year": year_al,
            "Player": player_al,
            "HR": hr_al,
            "Team": team_al,
            "League": "AL"
        })

    # National League
    year_nl, player_nl, hr_nl, team_nl = values[4:8]
    if player_nl != "-" and hr_nl != "-":
        data.append({
            "Year": year_nl,
            "Player": player_nl,
            "HR": hr_nl,
            "Team": team_nl,
            "League": "NL"
        })

# Criar DataFrame
df = pd.DataFrame(data)

# Convertendo para tipos numéricos
df["HR"] = pd.to_numeric(df["HR"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Salvar CSV
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/hr_leaders_by_team.csv", index=False)

print(f"✅ CSV gerado com sucesso com {len(df)} linhas válidas.")
