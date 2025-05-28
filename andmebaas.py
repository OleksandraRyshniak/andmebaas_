import sqlite3
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
global entries


# create_table="""
#  CREATE TABLE IF NOT EXISTS movies (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   title TEXT NOT NULL,
#   director TEXT,
#   release_year INTEGER,
#   genre TEXT,
#   duration INTEGER,
#   rating REAL,
#   language TEXT,
#   country TEXT,
#   description TEXT
# );
# """

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
CREATE TABLE IF NOT EXISTS movies (
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

insert_zanrid="""
insert into genres(name)
values("Drama"), ("Sci-Fi"), ("Crime"), ("Adventure"), ("Action"), ("Thriller"), ("Comedy")
"""

insert_into ="""
INSERT INTO movies (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description) VALUES
('The From In With.',1, 1994, 1, 142, 9.3, 1,1, 'The In With By On. A In From By The At. On A With By By On To A.'),
('The By On To.', 2, 2010, 2, 148, 8.8, 1, 2, 'The A The On The In. By To A At On The. From The In With At In To A.'),
('In The With On.', 3, 1972, 3, 175, 9.2, 1, 1, 'On From The By At The A. In From By With To On. A The By In With At On To A.'),
('The A To From.', 4, 1994, 4, 154, 8.9, 1, 3, 'With By In The A On. The With To A At The From. On A From With At By The.'),
('On The From With.', 5, 2008, 5, 152, 9.0, 1, 4, 'The A By On In The. At With To A From On The. With On By The A In To From.'),
('From The By With.', 2, 1960, 1, 134, 8.5, 1, 2, 'The A On From The At. With To By In A The On. At The In From With By To A.'),
('The By On A.', 1, 1999, 6, 112, 7.8, 1, 1, 'A The On By In The At. From With A On By To The. In The By With At A From.'),
('On A The From.', 3, 2015, 7, 126, 7.9, 1, 5, 'By With A On In The From. The By At A With On To. At In The By From With A.'),
('By The On From.', 4, 1975, 5, 143, 8.7, 1, 3, 'A With On The By From In. The A At On With To From. By In The A From With At On.'),
('From With The By.', 5, 1980, 3, 163, 9.1, 1, 4, 'On The A By In The From. With By On A The In From. To The In At By With On A.');
"""

# Функция для создания таблиц
def create_tables():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute(table_keeled)
    cursor.execute(table_riigid)
    cursor.execute(table_zanrid)
    cursor.execute(table_rezissoorid)
    cursor.execute(create_filmid)
    conn.commit()
    conn.close()

create_tables()

# Основное окно
root = tk.Tk()
root.title("Фильмы и справочники")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

tables = {
    "Фильмы": "movies",
    "Режиссёры": "directors",
    "Жанры": "genres",
    "Языки": "languages",
    "Страны": "countries"
}

treeviews = {}

# Загрузка данных таблицы
def load_table_data(tree, table_name):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    if table_name == "movies":
        cursor.execute("SELECT id, title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description FROM movies")
        columns = ["ID", "Название", "Режиссёр ID", "Год", "Жанр ID", "Длительность", "Рейтинг", "Язык ID", "Страна ID", "Описание"]
    else:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    tree["columns"] = columns
    tree["show"] = "headings"
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

for tab_name, table_name in tables.items():
    frame = tk.Frame(notebook)
    notebook.add(frame, text=tab_name)
    tree = ttk.Treeview(frame)
    tree.pack(fill=tk.BOTH, expand=True)
    treeviews[table_name] = tree
    load_table_data(tree, table_name)

# Поиск фильмов
def search_movies():
    query = search_entry.get()
    tree = treeviews["movies"]
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{query}%",))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    tree["columns"] = columns
    tree["show"] = "headings"
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

# Добавление данных
def add_movie():
    window = tk.Toplevel(root)
    window.title("Добавить фильм")
    labels = ["Название", "Режиссёр ID", "Год", "Жанр ID", "Длительность", "Рейтинг", "Язык ID", "Страна ID", "Описание"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0)
        entry = tk.Entry(window)
        entry.grid(row=i, column=1)
        entries[label] = entry
    def save():
        data = [entries[label].get() for label in labels]
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movies (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        load_table_data(treeviews["movies"], "movies")
        window.destroy()
    tk.Button(window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2)

# Удаление фильма
def delete_movie():
    tree = treeviews["movies"]
    selected = tree.selection()
    if selected:
        record = tree.item(selected)["values"]
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id=?", (record[0],))
        conn.commit()
        conn.close()
        load_table_data(tree, "movies")
    else:
        messagebox.showwarning("Ошибка", "Выберите фильм для удаления")

# Обновление фильма
def update_movie():
    tree = treeviews["movies"]
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите фильм для обновления")
        return
    record = tree.item(selected)["values"]
    window = tk.Toplevel(root)
    window.title("Изменить фильм")
    labels = ["Название", "Режиссёр ID", "Год", "Жанр ID", "Длительность", "Рейтинг", "Язык ID", "Страна ID", "Описание"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0)
        entry = tk.Entry(window)
        entry.grid(row=i, column=1)
        entry.insert(0, record[i+1])
        entries[label] = entry
    def save():
        data = [entries[label].get() for label in labels]
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE movies SET title=?, director_id=?, release_year=?, genre_id=?, duration=?, rating=?, language_id=?, country_id=?, description=?
            WHERE id=?
        """, data + [record[0]])
        conn.commit()
        conn.close()
        load_table_data(tree, "movies")
        window.destroy()
    tk.Button(window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2)

# Панель поиска и кнопок
panel = tk.Frame(root)
panel.pack(fill=tk.X)
tk.Label(panel, text="Поиск фильма:").pack(side=tk.LEFT)
search_entry = tk.Entry(panel)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(panel, text="Поиск", command=search_movies).pack(side=tk.LEFT, padx=10)
tk.Button(panel, text="Добавить", command=add_movie).pack(side=tk.LEFT, padx=10)
tk.Button(panel, text="Удалить", command=delete_movie).pack(side=tk.LEFT, padx=10)
tk.Button(panel, text="Изменить", command=update_movie).pack(side=tk.LEFT, padx=10)

root.mainloop()
