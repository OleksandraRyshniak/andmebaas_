import sqlite3
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
global entries



create_table="""
 CREATE TABLE IF NOT EXISTS movies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  director TEXT,
  release_year INTEGER,
  genre TEXT,
  duration INTEGER,
  rating REAL,
  language TEXT,
  country TEXT,
  description TEXT
);
"""

insert_into ="""
INSERT INTO movies (title, director, release_year, genre, duration, rating, language, country, description) VALUES
('The From In With.', 'Francis Ford Coppola', 1994, 'Drama', 142, 9.3, 'English', 'USA', 'The In With By On. A In From By The At. On A With By By On To A.'),
('The By On To.', 'Christopher Nolan', 2010, 'Sci-Fi', 148, 8.8, 'English', 'UK', 'The A The On The In. By To A At On The. From The In With At In To A.'),
('In The With On.', 'Quentin Tarantino', 1972, 'Crime', 175, 9.2, 'English', 'USA', 'On From The By At The A. In From By With To On. A The By In With At On To A.'),
('The A To From.', 'Steven Spielberg', 1994, 'Adventure', 154, 8.9, 'English', 'France', 'With By In The A On. The With To A At The From. On A From With At By The.'),
('On The From With.', 'Martin Scorsese', 2008, 'Action', 152, 9.0, 'English', 'Germany', 'The A By On In The. At With To A From On The. With On By The A In To From.'),
('From The By With.', 'Christopher Nolan', 1960, 'Drama', 134, 8.5, 'English', 'UK', 'The A On From The At. With To By In A The On. At The In From With By To A.'),
('The By On A.', 'Francis Ford Coppola', 1999, 'Thriller', 112, 7.8, 'English', 'USA', 'A The On By In The At. From With A On By To The. In The By With At A From.'),
('On A The From.', 'Quentin Tarantino', 2015, 'Comedy', 126, 7.9, 'English', 'Italy', 'By With A On In The From. The By At A With On To. At In The By From With A.'),
('By The On From.', 'Steven Spielberg', 1975, 'Action', 143, 8.7, 'English', 'France', 'A With On The By From In. The A At On With To From. By In The A From With At On.'),
('From With The By.', 'Martin Scorsese', 1980, 'Crime', 163, 9.1, 'English', 'Germany', 'On The A By In The From. With By On A The In From. To The In At By With On A.');
"""
def create_table():
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        print("Ühendus loodud")
        cursor.execute(create_table)
        print("Tabel loodud")
    except sqlite3.Error as error:
        print("Tekkis viga andmebaasiga ühendamisel:", error)
    finally:
        if conn:
            conn.close()

def täida_tabel():
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        print("Ühendus loodud")
        cursor.execute(insert_into)
        print("Tabel täidetud")
        conn.commit()
    except sqlite3.Error as error:
        print("Tekkis viga andmebaasiga ühendamisel:", error)
    finally:
        if conn:
            conn.close()

def loe_tabel(tabel:str):
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        print("Ühendus loodud")
        cursor.execute("SELECT * FROM movies")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except sqlite3.Error as error:
        print("Tekkis viga andmebaasiga ühendamisel või päringu teostamisel:", error)
    finally:
        if conn:
            conn.close()
            print("Ühendus suleti")

def lisa_andmed():
    global entries
    root = tk.Tk()
    root.title("Filmi andmete sisestamine")

    labels = ["Pealkiri", "Režissöör", "Aasta", "Žanr", "Kestus", "Reiting", "Keel", "Riik", "Kirjeldus"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(root, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry
    
    submit_button = tk.Button(root, text="Sisesta andmed", command=insert_data)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)
    root.mainloop()

def validate_data():
    global entries
    title = entries["Pealkiri"].get()
    release_year = entries["Aasta"].get()
    rating = entries["Reiting"].get()

    if not title:
        messagebox.showerror("Viga", "Pealkiri on kohustuslik!")
        return False
    if not release_year.isdigit():
        messagebox.showerror("Viga", "Aasta peab olema arv!")
        return False
    if rating and (not rating.replace('.', '', 1).isdigit() or not (0 <= float(rating) <= 10)):
        messagebox.showerror("Viga", "Reiting peab olema vahemikus 0 kuni 10!")
        return False

    return True

def insert_data():
    global entries
    if validate_data():
        connection = sqlite3.connect("movies.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO movies (title, director, release_year, genre, duration, rating, language, country, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entries["Pealkiri"].get(),
            entries["Režissöör"].get(),
            entries["Aasta"].get(),
            entries["Žanr"].get(),
            entries["Kestus"].get(),
            entries["Reiting"].get(),
            entries["Keel"].get(),
            entries["Riik"].get(),
            entries["Kirjeldus"].get()
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo("Edu", "Andmed sisestati edukalt!")
        clear_entries()

def clear_entries():
    global entries
    for entry in entries.values():
        entry.delete(0, tk.END)
    load_data_from_db(tree, search_query="")  


def load_data_from_db(tree, search_query=""):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT id, title, director, release_year, genre, duration, rating, language, country, description FROM movies WHERE title LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, title, director, release_year, genre, duration, rating, language, country, description FROM movies")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0]) 
    conn.close()

def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

def update_record(record_id, entries, window):
    title = entries["Pealkiri"].get()
    director = entries["Režissöör"].get()
    release_year = entries["Aasta"].get()
    genre = entries["Žanr"].get()
    duration = entries["Kestus"].get()
    rating = entries["Reiting"].get()
    language = entries["Keel"].get()
    country = entries["Riik"].get()
    description = entries["Kirjeldus"].get()
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE movies
        SET title=?, director=?, release_year=?, genre=?, duration=?, rating=?, language=?, country=?, description=?
        WHERE id=?
    """, (title, director, release_year, genre, duration, rating, language, country, description, record_id))
    conn.commit()
    conn.close()
    load_data_from_db(tree)
    window.destroy()

    messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")

def on_update():
    selected_item = tree.selection()  
    if selected_item:
        record_id = selected_item[0] 
        open_update_window(record_id)
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")

def open_update_window(record_id):
    update_window = tk.Toplevel(root)
    update_window.title("Muuda filmi andmeid")

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, director, release_year, genre, duration, rating, language, country, description FROM movies WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    labels = ["Pealkiri", "Režissöör", "Aasta", "Žanr", "Kestus", "Reiting", "Keel", "Riik", "Kirjeldus"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(update_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry

    save_button = tk.Button(update_window, text="Salvesta", command=lambda: update_record(record_id, entries, update_window))
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

def on_delete():
    selected_item = tree.selection()  
    if selected_item:
        record_id = selected_item[0]  
        confirm = messagebox.askyesno("Kinnita kustutamine", "Kas oled kindel, et soovid selle rea kustutada?")
        if confirm:
            try:           
                conn = sqlite3.connect('movies.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM movies WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                load_data_from_db(tree)
                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
            except sqlite3.Error as e:
                messagebox.showerror("Viga", f"Andmebaasi viga: {e}")
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")

root = tk.Tk()
root.title("Filmid")

frame = tk.Frame(root)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Otsi filmi pealkirja järgi:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Otsi", command=on_search)
search_button.pack(side=tk.LEFT)

lisa_button = tk.Button(search_frame, text="Lisa andmeid", command=lisa_andmed)
lisa_button.pack(side=tk.LEFT, padx=10)
update_button = tk.Button(search_frame, text="Uuenda", command=on_update)
update_button.pack(side=tk.LEFT, padx=10)
delete_button = tk.Button(search_frame, text="Kustuta", command=on_delete)
delete_button.pack(side=tk.LEFT, padx=10)

frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("title", "director", "year", "genre", "duration", "rating", "language", "country", "description"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=tree.yview)

tree.heading("title", text="Pealkiri")
tree.heading("director", text="Režissöör")
tree.heading("year", text="Aasta")
tree.heading("genre", text="Žanr")
tree.heading("duration", text="Kestus")
tree.heading("rating", text="Reiting")
tree.heading("language", text="Keel")
tree.heading("country", text="Riik")
tree.heading("description", text="Kirjeldus")
tree.column("title", width=150)
tree.column("director", width=100)
tree.column("year", width=60)
tree.column("genre", width=100)
tree.column("duration", width=60)
tree.column("rating", width=60)
tree.column("language", width=80)
tree.column("country", width=80)
tree.column("description", width=200)
load_data_from_db(tree)


root.mainloop()

