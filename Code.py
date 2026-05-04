import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTrackerApp:
    def __init__(self, root):
        # Настройка главного окна
        self.root = root
        self.root.title("Book Tracker")
        self.books = []  # Список для хранения данных о книгах
        self.load_books()  # Загрузка данных при запуске

        # --- Блок 1: Поля ввода ---
        ttk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = ttk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = ttk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = ttk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Блок 2: Кнопка добавления ---
        ttk.Button(root, text="Добавить книгу", command=self.add_book).grid(
            row=4, columnspan=2, pady=10)

        # --- Блок 3: Фильтры ---
        ttk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, sticky="e")
        self.filter_genre = ttk.Entry(root)
        self.filter_genre.grid(row=5, column=1, padx=5)

        ttk.Label(root, text="Фильтр по страницам (>):").grid(row=6, column=0, padx=5, sticky="e")
        self.filter_pages = ttk.Entry(root)
        self.filter_pages.grid(row=6, column=1)

        ttk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(
            row=7, columnspan=2)

        # --- Блок 4: Таблица для отображения книг ---
        self.tree = ttk.Treeview(columns=("Автор", "Жанр", "Страниц"), show="headings")

        # Настройка заголовков таблицы
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страниц", text="Страниц")

        # Размещение таблицы в интерфейсе (начиная с 8-й строки)
        self.tree.grid(row=8, columnspan=2)

    def add_book(self):
        """Добавляет книгу в список после проверки ввода."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
        self.books.append(book)
        self.save_books()
        self.update_table()

    def update_table(self):
        """Очищает и обновляет таблицу на экране."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in self.books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        """Фильтрует и отображает книги по заданным критериям."""
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get().strip())
        except:
            pages_filter = 0

        filtered_books = [
            book for book in self.books
            if (not genre_filter or genre_filter in book["genre"].lower())
               and (book["pages"] > pages_filter if pages_filter else True)
        ]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def save_books(self):
        """Сохраняет список книг в файл JSON."""
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        """Загружает список книг из файла JSON."""
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                try:
                    self.books = json.load(f)
                except json.JSONDecodeError:
                    self.books = []
                    self.save_books()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
