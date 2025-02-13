import sqlite3

def connect_database(db_name: str):
    conn = sqlite3.connect(db_name + '.db')
    return conn
import sqlite3

def draw_table_from_sqlite(cursor, query, title="Table"):
    """SQLite dan qaytgan natijani string jadval sifatida chizadi."""
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]  # Ustun nomlarini olish

    if not rows:
        return f"{title}\n" + "-" * (len(title) + 2) + "\nNo data available."

    # Ustun kengliklarini hisoblash
    col_widths = [max(len(str(header)), max((len(str(row[i])) for row in rows), default=0)) for i, header in enumerate(headers)]

    # Jadvalning sarlavhasi
    title_line = f" {title} "
    table_width = sum(col_widths) + len(col_widths) * 3 + 1
    header_line = "| " + " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers)) + " |"
    separator = "+" + "+".join("-" * (col_widths[i] + 2) for i in range(len(headers))) + "+"

    # Ma'lumotlar qismi
    row_lines = "\n".join("| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))) + " |" for row in rows)

    # Yakuniy jadval
    table_str = f"{title_line.center(table_width, '-')}\n{separator}\n{header_line}\n{separator}\n{row_lines}\n{separator}"
    return table_str

conn = sqlite3.connect('problems.db')
cursor = conn.cursor()
PROBLEMS_IDS = cursor.execute("SELECT problem_id FROM Problems;")
PROBLEMS_IDS = [problem_id[0] for problem_id in PROBLEMS_IDS]
conn.close()

if __name__ == '__main__':
    pass
 