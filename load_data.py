import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# 1. Настраиваем пути (используем сырые строки r'...')
DATA_PATH = r"C:\Users\inevs\OneDrive\AI_Workshop\Datasets\excel_data"
MODEL_PATH = os.path.join("..", "..", "Models", "paraphrase-multilingual-MiniLM-L12-v2")
DB_PATH = os.path.join(".", "qdrant_data")

print("Шаг 1: Загрузка локальной модели эмбеддингов...")
model = SentenceTransformer(MODEL_PATH)

print("Шаг 2: Подключение к локальной базе Qdrant...")
client = QdrantClient(path=DB_PATH)

print("Шаг 3: Чтение тестовых данных из Excel...")
# Читаем файл .xlsx. Указываем точное имя файла и имя нужной вкладки (sheet_name)
excel_file = os.path.join(DATA_PATH, "materials.xlsx") 

# pandas автоматически призовет openpyxl, чтобы открыть этот файл
df_materials = pd.read_excel(excel_file, sheet_name="Materials") 

print(f"Успешно прочитано {len(df_materials)} строк номенклатуры из Excel.")

print("Шаг 4: Расчет векторов и загрузка в базу...")
points = []

for idx, row in df_materials.iterrows():
    # Берем текст описания для превращения в вектор
    text_to_vector = str(row["SearchDescription"])
    
    # Строим вектор (размерность 384)
    vector = model.encode(text_to_vector).tolist()
    
    # Формируем полезную нагрузку (payload)
    payload = {
        "MaterialID": int(row["MaterialID"]),
        "MaterialName": str(row["MaterialName"]),
        "Article": str(row["Article"]),
        "SearchDescription": text_to_vector
    }
    
    # Добавляем точку в наш список загрузки
    points.append(
        PointStruct(
            id=int(row["MaterialID"]), 
            vector=vector,
            payload=payload
        )
    )

# Загружаем все точки в созданную ранее коллекцию nomenclature
client.upsert(
    collection_name="nomenclature",
    points=points
)

print("🚀 Все данные из Excel успешно векторизованы и загружены в локальный Qdrant!")
