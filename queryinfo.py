import sqlite3

conn = sqlite3.connect(r"E:\vscode yap\database finale 3.db")
cursor = conn.cursor()

with open("output.txt", "w") as file:
    def query_table(table_name):
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        file.write(f"Data from {table_name}:\n")
        for row in rows:
            file.write(f"{row},\n")
        file.write("\n\n")

    query_table('vuserpoints')
    query_table('iuserpoints')
    query_table('muserpoints')
    query_table('tuserpoints')
    query_table('rooms')

conn.close()
