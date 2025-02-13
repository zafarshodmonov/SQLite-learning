import tkinter as tk
from tkinter import ttk
from main import PROBLEMS_IDS, connect_database, draw_table_from_sqlite
import sqlite3

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Masalalar")
        self.width = 900
        self.height = 450
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.resizable(False, False)

        # Masalalar ID larining ro'yxati
        self.problem_ids = PROBLEMS_IDS
        self.current_index = 0

        # Yuqori markaz: ID tanlash
        self.selected_id = tk.IntVar()
        self.selected_id.set(self.problem_ids[self.current_index])  # Default qiymat
        self.combobox = ttk.Combobox(root, values=self.problem_ids, textvariable=self.selected_id, state="readonly")
        self.combobox.pack(pady=10)

        # O'rtada: Matn oynasi
        self.text_box = tk.Text(root, height=16, width=100)
        self.text_box.pack(pady=20)
        self.update_text()

        # Pastki markaz: Tugmalar
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        self.prev_button = tk.Button(button_frame, text="OLDINGI", command=self.prev_problem)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(button_frame, text="KEYINGI", command=self.next_problem)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Combo box o'zgarganda matnni yangilash
        self.combobox.bind("<<ComboboxSelected>>", lambda event: self.update_text())


    def update_text(self):
        """Matn oynasini yangilash"""
        self.text_box.delete("1.0", tk.END)
        text = self.show_problem()
        self.text_box.insert(tk.END, f"Problem Description: {text}")

    def prev_problem(self):
        """OLDINGI tugmasi bosilganda"""
        if self.current_index > 0:
            self.current_index -= 1
            self.selected_id.set(self.problem_ids[self.current_index])
            self.update_text()

    def next_problem(self):
        """KEYINGI tugmasi bosilganda"""
        if self.current_index < len(self.problem_ids) - 1:
            self.current_index += 1
            self.selected_id.set(self.problem_ids[self.current_index])
            self.update_text()

    def show_problem(self):
        """Masalani ko'rsatish"""
        conn = sqlite3.connect('problems.db')
        cursor = conn.cursor()
        problem_ID = self.selected_id.get()
        cursor.execute(f'SELECT problem_description from Problems WHERE problem_id = {problem_ID};')
        problem_description = cursor.fetchall()[0][0]

        #
        cursor.execute(f'SELECT dfp.Database_Name FROM Problem_Database_Details pdd INNER JOIN Database_For_Problems dfp ON pdd.Database_ID = dfp.Database_ID WHERE pdd.Problem_ID = {problem_ID};')
        db = cursor.fetchall()[0][0]
        conn_p = connect_database(f"database_for_problems/{db}")
        cursor_p = conn_p.cursor()

        #
        cursor_p.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor_p.fetchall()

        for table in tables:
            t = draw_table_from_sqlite(cursor_p, f"SELECT * FROM {table[0]}", table[0])
            problem_description += "\n\n" + t
            
            
        #
        
        conn_p.close()
        conn.close()
        #
        return problem_description

# Dastur ishga tushirish
root = tk.Tk()
app = SimpleApp(root)
root.mainloop()
