import pandas as pd

# 📥 Carregar os dados crus
df = pd.read_csv("data/raw/hr_leaders_by_team.csv")

print("📊 Antes da limpeza:")
print(df.shape)
print(df.info())
print(df.head())

# 🔍 1. Remover espaços e caracteres estranhos
df["Player"] = df["Player"].str.strip()
df["Team"] = df["Team"].str.strip()

# 🔢 2. Converter colunas para os tipos corretos
df["HR"] = pd.to_numeric(df["HR"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# 🧹 3. Remover registros com valores nulos nas colunas principais
df.dropna(subset=["Player", "Team", "HR", "Year", "League"], inplace=True)

# 📄 4. Remover duplicatas
df.drop_duplicates(inplace=True)

# 🔠 5. Padronizar nomes de times e jogadores (título)
df["Player"] = df["Player"].str.title()
df["Team"] = df["Team"].str.title()

# ✅ 6. Resetar índice
df.reset_index(drop=True, inplace=True)

print("\n✅ Depois da limpeza:")
print(df.shape)
print(df.info())
print(df.head())

# 💾 Salvar versão limpa
df.to_csv("data/clean/hr_leaders_by_team_clean.csv", index=False)
print("\n📁 Arquivo salvo em: data/clean/hr_leaders_by_team_clean.csv")
