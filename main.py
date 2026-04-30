import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")

        self.trainings = []
        self.filename = "trainings.json"

        # --- Форма ввода ---
        self.form_frame = ttk.LabelFrame(root, text="Добавить тренировку")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.form_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(self.form_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Entry(self.form_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Длительность (минуты):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self.form_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(self.form_frame, text="Добавить тренировку", command=self.add_training)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # --- Таблица тренировок ---
        self.tree_frame = ttk.LabelFrame(root, text="Мои тренировки")
        self.tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.tree_frame, columns=("Date", "Type", "Duration"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип тренировки")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Фильтрация ---
        self.filter_frame = ttk.LabelFrame(root, text="Фильтр")
        self.filter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.filter_frame, text="По типу:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_type_entry = ttk.Entry(self.filter_frame)
        self.filter_type_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filter_type_entry.bind("<KeyRelease>", lambda event: self.apply_filters())

        ttk.Label(self.filter_frame, text="По дате (ДД.ММ.ГГГГ):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.filter_date_entry = ttk.Entry(self.filter_frame)
        self.filter_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.filter_date_entry.bind("<KeyRelease>", lambda event: self.apply_filters())

        self.load_trainings()
        self.update_treeview()

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def is_valid_duration(self, duration_str):
        try:
            duration = int(duration_str)
            return duration > 0
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not date or not training_type or not duration:
            messagebox.showwarning("Внимание", "Все поля должны быть заполнены.")
            return

        if not self.is_valid_date(date):
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД.ММ.ГГГГ.")
            return

        if not self.is_valid_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        self.trainings.append({"date": date, "type": training_type, "duration": int(duration)})
        self.update_treeview()
        self.save_trainings()
        self.clear_entries()

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in self.trainings:
            self.tree.insert("", tk.END, values=(training["date"], training["type"], training["duration"]))

    def apply_filters(self):
        filter_type = self.filter_type_entry.get().lower()
        filter_date = self.filter_date_entry.get().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for training in self.trainings:
            match_type = filter_type in training["type"].lower()
            match_date = filter_date in training["date"].lower()

            if match_type and match_date:
                self.tree.insert("", tk.END, values=(training["date"], training["type"], training["duration"]))

    def save_trainings(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_trainings(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", f"Ошибка чтения файла {self.filename}. Он может быть поврежден.")
            self.trainings = []

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
