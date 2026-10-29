import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# 1. Настраиваем пути к локальной модели и локальной базе данных
MODEL_PATH = os.path.join("..", "..", "Models", "paraphrase-multilingual-MiniLM-L12-v2")
DB_PATH = os.path.join(".", "qdrant_data")

# Инициализируем компоненты (строго офлайн)
model = SentenceTransformer(MODEL_PATH)
client = QdrantClient(path=DB_PATH)

print("🔍 Локальная поисковая система ТОиР готова к работе!")
print("-" * 50)

# 2. Интерактивный цикл поиска в консоли
try:
    while True:
        # Запрашиваем ввод у пользователя
        query = input("\nВведите запрос для поиска (или 'выход' для завершения): ")
        
        if query.lower() == "выход":
            print("Завершение работы системы.")
            break
            
        if not query.strip():
            continue

        # Превращаем пользовательский запрос в поисковый вектор
        query_vector = model.encode(query).tolist()

        # ИСПРАВЛЕНО: Новый корректный синтаксис query_points для qdrant-client
        search_results = client.query_points(
            collection_name="nomenclature",
            query=query_vector,  # Передаем вектор в параметр query
            limit=3
        )

        print(f"\nРезультаты поиска по запросу: '{query}':")
        print("-" * 50)
        
        # Выводим результаты
        for i, hit in enumerate(search_results.points, 1):
            payload = hit.payload
            score = hit.score  # Коэффициент схожести (от 0 до 1)
            
            print(f"{i}. [Совпадение: {score:.2f}]")
            print(f"   ID материала: {payload.get('MaterialID')}")
            print(f"   Артикул:      {payload.get('Article')}")
            print(f"   Наименование: {payload.get('MaterialName')}")
            print(f"   Описание:     {payload.get('SearchDescription')}")
            print("-" * 50)

finally:
    # Закрываем соединение с БД при выходе
    client.close()
