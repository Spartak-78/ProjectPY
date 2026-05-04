import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Поля ввода ---
        ttk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = ttk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = ttk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        ttk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Фильтры ---
        ttk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_genre = ttk.Entry(root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(root, text="Фильтр по страницам (>):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_pages = ttk.Entry(root, width=30)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, columnspan=2, pady=10)

        # --- Таблица книг ---
        self.tree = ttk.Treeview(root, columns=("Автор", "Жанр", "Страниц"), show="headings")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страниц", text="Страниц")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Загрузка данных в таблицу
        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.save_books()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in self.books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get().strip())
        except:
            pages_filter = 0

        filtered_books = [
            book for book in self.books
            if (not genre_filter or genre_filter in book["genre"].lower())
            and (pages_filter == 0 or book["pages"] > pages_filter)
        ]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                try:
                    self.books = json.load(f)
                except:
                    self.books = []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()