import sqlite3
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
global entries


table_keeled="""
CREATE TABLE IF NOT EXISTS languages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);
"""
insert_keeled="""
insert into languages(name)
values("English")
"""

table_riigid="""
CREATE TABLE IF NOT EXISTS countries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);
"""
insert_riigid="""
insert into countries(name)
values("USA"), ("UK"), ("France"), ("Germany"), ("Italy")
"""

table_zanrid="""
CREATE TABLE IF NOT EXISTS genres (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);
"""
insert_zanrid="""
insert into genres(name)
values("Drama"), ("Sci-Fi"), ("Crime"), ("Adventure"), ("Action"), ("Thriller"), ("Comedy")
"""

table_rezissoorid="""
CREATE TABLE IF NOT EXISTS directors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);
"""
insert_rezissoorid="""
insert into directors(name)
values
("Francis Ford Coppola"),
("Christopher Nolan"), 
("Quentin Tarantino"), 
("Steven Spielberg"),
("Martin Scorsese")
"""

create_filmid="""
CREATE TABLE IF NOT EXISTS Filmid (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  director_id INTEGER,
  release_year INTEGER,
  genre_id INTEGER,
  duration INTEGER,
  rating REAL,
  language_id INTEGER,
  country_id INTEGER,
  description TEXT,
  FOREIGN KEY (director_id) REFERENCES directors(id),
  FOREIGN KEY (genre_id) REFERENCES genres(id),
  FOREIGN KEY (language_id) REFERENCES languages(id),
  FOREIGN KEY (country_id) REFERENCES countries(id)
);
"""

insert_into ="""
INSERT INTO Filmid (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description) VALUES
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



def create_tables():
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute(table_keeled)
    cursor.execute(table_riigid)
    cursor.execute(table_zanrid)
    cursor.execute(table_rezissoorid)
    cursor.execute(create_filmid)
    conn.commit()
    conn.close()

def täida_tabel():
    try:
        conn = sqlite3.connect('filmid.db')
        cursor = conn.cursor()
        print("Ühendus loodud")
        cursor.execute(insert_keeled)
        cursor.execute(insert_rezissoorid)
        cursor.execute(insert_riigid)
        cursor.execute(insert_zanrid)
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
        conn = sqlite3.connect('filmid.db')
        cursor = conn.cursor()
        print("Ühendus loodud")
        cursor.execute("SELECT * FROM filmid")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as error:
        print("Tekkis viga andmebaasiga ühendamisel või päringu teostamisel:", error)
    finally:
        if conn:
            conn.close()
            print("Ühendus suleti")

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
        connection = sqlite3.connect("filmid.db")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Filmid (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description)
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

def load_data_from_db(tree, search_query=""):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT id, title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description FROM filmid WHERE title LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description FROM filmid")
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
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Filmid
        SET title=?, director_id=?, release_year=?, genre_id=?, duration=?, rating=?, language_id=?, country_id=?, description=?
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
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description FROM Filmid WHERE id=?", (record_id,))
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
                conn = sqlite3.connect('filmid.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Filmid WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                load_data_from_db(tree)
                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
            except sqlite3.Error as e:
                messagebox.showerror("Viga", f"Andmebaasi viga: {e}")
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")




def clear_keeled():
    global keel
    global tree1
    for entry in keel.values():
        entry.delete(0, tk.END)
    load_keel(tree1, search_query="") 

def lisa_keeled():
    global keel
    global tree1
    window = tk.Toplevel()
    window.title("Keele lisamine")
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)
    labels = ["Keel"]
    keel = {}
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(input_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        keel[label] = entry

    submit_button = tk.Button(input_frame, text="Sisesta andmed", command= insert_keel)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    table_frame = tk.Frame(window)
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree1 = ttk.Treeview(table_frame, columns=("id", "name"), show="headings")
    tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree1.heading("id", text="ID")
    tree1.heading("name", text="Keel")
    tree1.column("id", width=50)
    tree1.column("name", width=100)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree1.yview)
    tree1.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    load_keel(tree1)

    def on_close():
        keel.clear()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def insert_keel():
    global keel
    global tree1
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    language = keel["Keel"].get()
    if language.strip() == "":
        messagebox.showwarning("Viga", "Palun sisesta keele nimi.")
        return
    cursor.execute("INSERT INTO languages (name) VALUES (?)", (language,))
    conn.commit()
    conn.close()
    load_keel(tree1)

def load_keel(tree1):
    global keel
    for item in tree1.get_children():
        tree1.delete(item) 
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM languages")
    rows = cursor.fetchall()
    for row in rows:
        tree1.insert("", "end", values=row)
    conn.close()


def clear_riigid():
    global riik
    global tree2
    for entry in riik.values():
        entry.delete(0, tk.END)
    load_riik(tree2, search_query="") 

def lisa_riigid():
    global riik
    global tree2
    window = tk.Toplevel()
    window.title("Riigi lisamine")
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)
    labels = ["Riik"]
    riik = {}
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(input_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        riik[label] = entry

    submit_button = tk.Button(input_frame, text="Sisesta andmed", command= insert_riigid)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    table_frame = tk.Frame(window)
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree2 = ttk.Treeview(table_frame, columns=("id", "name"), show="headings")
    tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree2.heading("id", text="ID")
    tree2.heading("name", text="Riik")
    tree2.column("id", width=50)
    tree2.column("name", width=100)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree2.yview)
    tree2.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    load_riik(tree2)
    def on_close():
        riik.clear()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def insert_riigid():
    global riik
    global tree2
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    country = riik["Riik"].get()
    if country.strip() == "":
        messagebox.showwarning("Viga", "Palun sisesta riigi nimi.")
        return
    cursor.execute("INSERT INTO countries (name) VALUES (?)", (country,))
    conn.commit()
    conn.close()
    load_riik(tree2)

def load_riik(tree2):
    global riik
    for item in tree2.get_children():
        tree2.delete(item) 
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM countries")
    rows = cursor.fetchall()
    for row in rows:
        tree2.insert("", "end", values=row)
    conn.close()


def clear_zanrid():
    global zanr
    global tree3
    for entry in zanr.values():
        entry.delete(0, tk.END)
    load_zanr(tree3, search_query="") 

def lisa_zanrid():
    global zanr
    global tree3
    window = tk.Toplevel()
    window.title("Žanri lisamine")
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)
    labels = ["Žanr"]
    zanr = {}
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(input_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        zanr[label] = entry

    submit_button = tk.Button(input_frame, text="Sisesta andmed", command= insert_zanrid)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    table_frame = tk.Frame(window)
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree3 = ttk.Treeview(table_frame, columns=("id", "name"), show="headings")
    tree3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree3.heading("id", text="ID")
    tree3.heading("name", text="Žanr")
    tree3.column("id", width=50)
    tree3.column("name", width=100)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree3.yview)
    tree3.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    load_zanr(tree3)
    def on_close():
        zanr.clear()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def insert_zanrid():
    global zanr
    global tree3
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    genres = zanr["Žanr"].get()
    if genres.strip() == "":
        messagebox.showwarning("Viga", "Palun sisesta žanri nimi.")
        return
    cursor.execute("INSERT INTO genres (name) VALUES (?)", (genres,))
    conn.commit()
    conn.close()
    load_zanr(tree3)

def load_zanr(tree3):
    global zanr
    for item in tree3.get_children():
        tree3.delete(item) 
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM genres")
    rows = cursor.fetchall()
    for row in rows:
        tree3.insert("", "end", values=row)
    conn.close()


def clear_rezissoorid():
    global rezissoor
    global tree4
    for entry in rezissoor.values():
        entry.delete(0, tk.END)
    load_rezissoor(tree4, search_query="") 

def lisa_rezisoorid():
    global rezissoor
    global tree4
    window = tk.Toplevel()
    window.title("Režissööri lisamine")
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)
    labels = ["Režissöör"]
    rezissoor = {}
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(input_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        rezissoor[label] = entry

    submit_button = tk.Button(input_frame, text="Sisesta andmed", command= insert_rezissoorid)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    table_frame = tk.Frame(window)
    table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    tree4 = ttk.Treeview(table_frame, columns=("id", "name"), show="headings")
    tree4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree4.heading("id", text="ID")
    tree4.heading("name", text="Žanr")
    tree4.column("id", width=50)
    tree4.column("name", width=100)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree4.yview)
    tree4.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    load_rezissoor(tree4)
    def on_close():
        rezissoor.clear()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def insert_rezissoorid():
    global rezissoor
    global tree4
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    directors = rezissoor["Režissöör"].get()
    if directors.strip() == "":
        messagebox.showwarning("Viga", "Palun sisesta režissööri nimi.")
        return
    cursor.execute("INSERT INTO directors(name) VALUES (?)", (directors,))
    conn.commit()
    conn.close()
    load_rezissoor(tree4)

def load_rezissoor(tree4):
    global rezissoor
    for item in tree4.get_children():
        tree4.delete(item) 
    conn = sqlite3.connect('filmid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM directors")
    rows = cursor.fetchall()
    for row in rows:
        tree4.insert("", "end", values=row)
    conn.close()


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
lisa_keel_button= tk.Button(search_frame, text="Lisa keel", command=lisa_keeled)
lisa_keel_button.pack(side=tk.LEFT, padx=10)
lisa_riik_button= tk.Button(search_frame, text="Lisa riik", command=lisa_riigid)
lisa_riik_button.pack(side=tk.LEFT, padx=10)
lisa_zanr_button= tk.Button(search_frame, text="Lisa žanr", command=lisa_zanrid)
lisa_zanr_button.pack(side=tk.LEFT, padx=10)
lisa_rezissoor_button= tk.Button(search_frame, text="Lisa režissöör", command=lisa_rezisoorid)
lisa_rezissoor_button.pack(side=tk.LEFT, padx=10)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("title", "director_id", "release_year", "genre_id", "duration", "rating", "language_id", "country_id", "description"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=tree.yview)


tree.heading("title", text="Pealkiri")
tree.heading("director_id", text="Režissöör")
tree.heading("release_year", text="Aasta")
tree.heading("genre_id", text="Žanr")
tree.heading("duration", text="Kestus")
tree.heading("rating", text="Reiting")
tree.heading("language_id", text="Keel")
tree.heading("country_id", text="Riik")
tree.heading("description", text="Kirjeldus")

tree.column("title", width=150)
tree.column("director_id", width=100)
tree.column("release_year", width=60)
tree.column("genre_id", width=100)
tree.column("duration", width=60)
tree.column("rating", width=60)
tree.column("language_id", width=80)
tree.column("country_id", width=80)
tree.column("description", width=200)

load_data_from_db(tree)


root.mainloop()