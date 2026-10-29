import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# 1. Задаем путь к папке, где Qdrant будет локально хранить свои данные
db_path = os.path.join(".", "qdrant_data")
collection_name = "nomenclature"

print(f"Инициализация локальной базы Qdrant по пути: {db_path}...")
# Подключаемся к локальной БД (если папки нет, она создастся автоматически)
client = QdrantClient(path=db_path)

# 2. Создаем коллекцию (аналог таблицы в реляционных БД)
# ВАЖНО: size=384, так как наша модель paraphrase-multilingual выдает векторы именно такой длины
print(f"Создание коллекции '{collection_name}'...")
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384, 
        distance=Distance.COSINE  # Используем косинусное сходство по архитектуре
    ),
)

print(f"Коллекция '{collection_name}' успешно создана и настроена на размерность 384!")
print("База данных готова к приему векторов.")
