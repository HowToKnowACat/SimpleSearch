import os
import tkinter as tk
from tkinter import ttk, messagebox
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# ==========================================
# 1. НАСТРОЙКА ПУТЕЙ И КОМПОНЕНТОВ (OFFLINE)
# ==========================================
MODEL_PATH = os.path.join("..", "..", "Models", "paraphrase-multilingual-MiniLM-L12-v2")
DB_PATH = os.path.join(".", "qdrant_data")

# Инициализируем локальные ИИ-компоненты
model = SentenceTransformer(MODEL_PATH)
client = QdrantClient(path=DB_PATH)

# ==========================================
# 2. ЛОГИКА ПОИСКА И АВТО-ОБОСНОВАНИЯ
# ==========================================
def perform_search():
    query_text = entry_query.get().strip()
    if not query_text:
        messagebox.showwarning("Внимание", "Введите текст запроса для поиска!")
        return
    
    # Очищаем таблицу перед новым поиском
    for item in tree.get_children():
        tree.delete(item)
    # Очищаем блок обоснования
    text_reasoning.config(state=tk.NORMAL)
    text_reasoning.delete("1.0", tk.END)
    text_reasoning.config(state=tk.DISABLED)
    
    try:
        # Векторизуем запрос инженера
        query_vector = model.encode(query_text).tolist()
        
        # Запрос к локальному Qdrant (ищем ТОП-5 для наглядности в UI)
        search_results = client.query_points(
            collection_name="nomenclature",
            query=query_vector,
            limit=5
        )
        
        if not search_results.points:
            messagebox.showinfo("Результат", "Ничего не найдено.")
            return
            
        # Заполняем таблицу результатами
        for hit in search_results.points:
            payload = hit.payload
            score_percent = f"{hit.score * 100:.1f}%" # Превращаем score в красивый процент
            
            tree.insert("", tk.END, values=(
                payload.get("MaterialID"),
                payload.get("Article"),
                payload.get("MaterialName"),
                score_percent,
                payload.get("SearchDescription") # Скрытая колонка для логики
            ))
            
    except Exception as e:
        messagebox.showerror("Ошибка ИИ", f"Критическая ошибка при поиске: {e}")

def on_item_select(event):
    """Функция срабатывает при клике на строку в таблице и генерирует обоснование"""
    selected_items = tree.selection()
    if not selected_items:
        return
        
    item = selected_items[0]
    values = tree.item(item, "values")
    
    # Достаем данные из кликнутой строки
    mat_id = values[0]
    art = values[1]
    name = values[2]
    score = values[3]
    description = values[4]
    
    # Генерируем автоматическое инженерное обоснование (Reasoning)
    query_lower = entry_query.get().lower()
    desc_lower = description.lower()
    
    triggers = []
    if "зим" in query_lower and ("-30" in desc_lower or "-35" in desc_lower or "-45" in desc_lower or "true" in desc_lower):
        triggers.append("• Соответствие климатическому режиму: позиция содержит зимние присадки или расширенный отрицательный температурный диапазон.")
    if "кат" in query_lower or "caterpillar" in query_lower:
        if "cat" in desc_lower or "caterpillar" in desc_lower:
            triggers.append("• Кросс-брендовое соответствие: распознан синоним техники/бренда Caterpillar (CAT).")
    if "масло" in query_lower and "масло" in desc_lower:
        triggers.append("• Соответствие класса МДМ: Объект относится к группе смазочных материалов.")
    if "гидравлик" in query_lower and "hydraulic" in desc_lower:
        triggers.append("• Функциональный узел: Подтверждено назначение для гидравлических систем высокого давления.")
    if "фильтр" in query_lower and "filter" in desc_lower:
        triggers.append("• Класс расходных материалов: Объект идентифицирован как элемент фильтрации системы ТОиР.")

    if not triggers:
        triggers.append("• Высокое семантическое сходство текстового описания и контекста применения в процессах ТОиР.")
        
    reasoning_text = f"МАТЕРИАЛ: {name} (Артикул: {art})\n"
    reasoning_text += f"МАТЕМАТИЧЕСКАЯ РЕЛЕВАНТНОСТЬ: {score} близости в пространстве эмбеддингов.\n\n"
    reasoning_text += "ИНЖЕНЕРНОЕ ОБОСНОВАНИЕ ВЫБОРА:\n"
    reasoning_text += "\n".join(triggers) + "\n\n"
    reasoning_text += f"ПОЛНЫЙ СЛЕД ИЗ БАЗЫ ДАННЫХ МДМ:\n{description}"
    
    # Выводим текст в нижний блок
    text_reasoning.config(state=tk.NORMAL)
    text_reasoning.delete("1.0", tk.END)
    text_reasoning.insert(tk.END, reasoning_text)
    text_reasoning.config(state=tk.DISABLED)

# ==========================================
# 3. ПОСТРОЕНИЕ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА (UI)
# ==========================================
root = tk.Tk()
root.title("Прототип векторного поиска МДМ ТОиР и Склад v1.0")
root.geometry("900x650")
root.minsize(800, 500)

# Верхняя панель поиска
frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill=tk.X)

lbl_query = ttk.Label(frame_top, text="Поисковый запрос инженера (естественный язык):", font=("Segoe UI", 10, "bold"))
lbl_query.pack(anchor=tk.W, pady=(0, 5))

entry_query = ttk.Entry(frame_top, font=("Segoe UI", 11))
entry_query.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry_query.insert(0, "Масло моторное для зимы на бульдозер катерпиллер") # Дефолтный запрос для демонстрации
entry_query.bind("<Return>", lambda event: perform_search()) # Поиск по кнопке Enter

btn_search = ttk.Button(frame_top, text="Искать в Qdrant", command=perform_search)
btn_search.pack(side=tk.RIGHT, ipadx=10)

# Центральная панель — Таблица результатов
frame_mid = ttk.LabelFrame(root, text=" Найдено позиций в локальной базе данных Qdrant ", padding=10)
frame_mid.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("id", "article", "name", "score")
tree = ttk.Treeview(frame_mid, columns=columns, show="headings", selectmode="browse")

tree.heading("id", text="ID")
tree.heading("article", text="Артикул")
tree.heading("name", text="Наименование материала (МДМ)")
tree.heading("score", text="Сходство %")

tree.column("id", width=50, anchor=tk.CENTER)
tree.column("article", width=120, anchor=tk.CENTER)
tree.column("name", width=450, anchor=tk.W)
tree.column("score", width=100, anchor=tk.CENTER)

# Скроллбар для таблицы
scrollbar = ttk.Scrollbar(frame_mid, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Привязываем событие клика по таблице
tree.bind("<<TreeviewSelect>>", on_item_select)

# Ниже панель — Обоснование ИИ
frame_bot = ttk.LabelFrame(root, text=" Инженерное обоснование выбора (ИИ-Логика) ", padding=10)
frame_bot.pack(fill=tk.X, padx=10, pady=10)

text_reasoning = tk.Text(frame_bot, height=10, font=("Consolas", 10), bg="#f8f9fa", fg="#212529", state=tk.DISABLED, wrap=tk.WORD)
text_reasoning.pack(fill=tk.X)

# Запуск UI-цикла
root.mainloop()
