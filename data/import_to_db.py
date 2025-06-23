import pandas as pd
import sqlite3
import os

# Caminhos
csv_path = "data/clean/hr_leaders_by_team_clean.csv"
db_path = "data/mlb_data.db"

# 📥 Ler CSV limpo
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("❌ CSV não encontrado. Execute a limpeza primeiro.")
    exit()

# 📁 Criar diretório se necessário
os.makedirs("data", exist_ok=True)

# 🔌 Conectar ao SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🧱 Criar tabela com chave primária
cursor.execute("DROP TABLE IF EXISTS hr_leaders")
cursor.execute("""
    CREATE TABLE hr_leaders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Year INTEGER,
        Player TEXT,
        HR INTEGER,
        Team TEXT,
        League TEXT
    )
""")

# 📤 Inserir dados (sem a coluna id)
try:
    df.to_sql("hr_leaders", conn, if_exists="append", index=False)
    print(f"✅ Dados importados com sucesso para: {db_path}")
except Exception as e:
    print("❌ Erro ao importar:", e)

# 🔍 Verificação inicial
result = cursor.execute("SELECT * FROM hr_leaders LIMIT 5").fetchall()
print("\n📌 Primeiras linhas no banco:")
for row in result:
    print(row)

# 🔒 Fechar conexão
conn.commit()
conn.close()
