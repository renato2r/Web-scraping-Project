import sqlite3

DB_PATH = "data/mlb_data.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def print_menu():
    print("\n MLB Home Run Leaders - Query Menu")
    print("1. List leaders for a specific year")
    print("2. Filter by American League or National league (AL/NL)")
    print("3. Show players with more than X home runs")
    print("4. Search for a player by name")
    print("5. Exit")

def query_year(conn):
    year = input("Enter the year (e.g., 2001): ")
    try:
        cursor = conn.execute("SELECT Year, Player, HR, Team, League FROM hr_leaders WHERE Year = ?", (year,))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No results found for that year.")
    except Exception as e:
        print("Error:", e)

def query_league(conn):
    league = input("Enter the league (AL or NL): ").upper()
    if league not in ["AL", "NL"]:
        print("Invalid league. Please enter 'AL' or 'NL'.")
        return
    cursor = conn.execute("SELECT Year, Player, HR, Team FROM hr_leaders WHERE League = ?", (league,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print(f"No results found for league '{league}'.")

def query_hr_above(conn):
    try:
        hr = int(input("Show players with more than how many HRs? "))
        cursor = conn.execute("SELECT Year, Player, HR, Team, League FROM hr_leaders WHERE HR > ?", (hr,))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print(f"No players found with more than {hr} HRs.")
    except ValueError:
        print("Invalid number. Please enter an integer.")

def query_player(conn):
    name = input("Enter part of the player's name: ").strip()
    cursor = conn.execute("SELECT Year, Player, HR, Team, League FROM hr_leaders WHERE Player LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print(f"No players found matching '{name}'.")

def main():
    conn = connect_db()
    while True:
        print_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            query_year(conn)
        elif choice == "2":
            query_league(conn)
        elif choice == "3":
            query_hr_above(conn)
        elif choice == "4":
            query_player(conn)
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 5.")
    conn.close()

if __name__ == "__main__":
    main()
