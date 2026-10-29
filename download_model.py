import os
from sentence_transformers import SentenceTransformer

# Указываем имя модели на Hugging Face
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Путь для сохранения (поднимаемся на уровень выше в общую папку Models)
save_path = os.path.join("..", "..", "Models", "paraphrase-multilingual-MiniLM-L12-v2")

print("Начало скачивания модели...")
model = SentenceTransformer(model_name)

print(f"Сохранение модели в: {save_path}")
model.save(save_path)
print("Модель успешно сохранена локально!")