# Прототип семантического поиска инженерных данных (МДМ, ТОиР, Склад) 🏭
# Semantic Search Prototype for Engineering MDM, MRO, and Warehouse Data 🛠️

[Русское описание](#русский) | [English Description](#english)

---

## <a name="русский"></a> 🇷🇺 Русский

Данный репозиторий содержит исходный код работающего MVP-прототипа интеллектуальной надстройки над мастер-данными (МДМ) промышленного предприятия. Система позволяет выполнять семантический поиск по складской номенклатуре и запчастям ТОиР, используя **естественный язык**. 

В отличие от классического поиска по подстроке в реляционных БД (SQL) или Excel, этот прототип понимает инженерный контекст, опечатки, транслит и кросс-брендовые синонимы (например, связывает текстовый запрос `Катерпиллар` с артикулами `CAT`).

### 📐 Архитектура и ИИ-стек решения
Проект построен в рамках контура **«Мастерская ИИ»** и спроектирован для полностью **автономной (offline) работы** на компьютерах без мощных видеокарт (расчеты выполняются на CPU):

* **Уровень данных:** `MS Excel` (`.xlsx`) — источник нормативно-справочной информации (150 тестовых позиций: масла, фильтры, смазки, антифризы).
* **Модель эмбеддингов (ИИ):** `paraphrase-multilingual-MiniLM-L12-v2` от *Sentence Transformers* (размерность векторов — 384). Превращает текст в математические слепки смыслов.
* **Векторная база данных:** `Qdrant Local` — локальное хранилище векторов. Сравнение векторов запроса и номенклатуры происходит на основе **косинусного сходства (Cosine Similarity)**.
* **Интерфейс (UI):** Десктопное приложение на встроенной библиотеке `Tkinter` с блоком генерации автоматического инженерного обоснования выбора.

### 📂 Структура проекта
```text
SimpleSearch/
│
├── qdrant_data/          # Локальные файлы векторной базы данных Qdrant
├── init_db.py            # Скрипт инициализации БД и создания коллекции
├── load_data.py          # Скрипт парсинга Excel, векторизации и загрузки в Qdrant
├── search_gui.py         # Графический интерфейс приложения (Tkinter)
├── .gitignore            # Файл исключений (скрывает тяжелые модели и локальную БД)
└── README.md             # Документация проекта
```

### 🚀 Инструкция по локальному запуску

**1. Подготовка окружения и установка библиотек:**
Убедитесь, что у вас установлен Python 3.12+. Разверните виртуальное окружение и выполните команду в терминале:
```bash
pip install sentence-transformers pandas openpyxl qdrant-client
```

**2. Развертывание базы данных:**
Запустите скрипт для инициализации пустой локальной коллекции в Qdrant:
```bash
python init_db.py
```

**3. Загрузка и векторизация данных из Excel:**
Убедитесь, что ваш датасет номенклатуры сохранен в формате `.xlsx`. Обновите путь к файлу в коде и запустите заливку:
```bash
python load_data.py
```

**4. Запуск графического поисковика:**
Запустите финальное приложение. Введите поисковый запрос (например: *«Масло моторное для зимы на бульдозер катерпиллер»*) и нажмите «Искать»:
```bash
python search_gui.py
```

---

## <a name="english"></a> 🇬🇧 English

This repository contains the source code for a functional MVP prototype of an AI-powered add-on for industrial Master Data Management (MDM) systems. The system enables **natural language semantic search** across warehouse inventory, spare parts, and MRO (Maintenance, Repair, and Operations) nomenclature.

Unlike traditional keyword or substring matching used in relational databases (SQL) or Excel, this prototype understands engineering context, typos, transliteration, and cross-brand synonyms (e.g., matching a natural language query `Катерпиллар` or `Caterpillar` with parts labeled as `CAT`).

### 📐 Architecture & AI Stack
The project was developed as part of the **"AI Workshop"** framework and is specifically engineered for completely **offline operation** on standard computers without discrete GPUs (all inference runs efficiently on the CPU):

* **Data Layer:** `MS Excel` (`.xlsx`) — acts as the golden master data source (150 sample rows including industrial oils, filters, greases, and coolants).
* **Embedding Model (AI):** `paraphrase-multilingual-MiniLM-L12-v2` by *Sentence Transformers* (vector dimension: 384). It converts raw engineering texts into semantic vector spaces.
* **Vector Database:** `Qdrant Local` — embedded vector storage. Vector retrieval is processed using **Cosine Similarity** constraints.
* **User Interface (UI):** A lightweight desktop interface built with native `Tkinter`, featuring an automatic engineering reasoning and justification component.

### 📂 Repository Structure
```text
SimpleSearch/
│
├── qdrant_data/          # Local Qdrant vector database storage files
├── init_db.py            # DB initialization and collection schema setup script
├── load_data.py          # Excel parser, embedding generator, and Qdrant upsert script
├── search_gui.py         # GUI desktop application interface (Tkinter)
├── .gitignore            # Git exclusion schema (masks local database and models)
└── README.md             # Project documentation
```

### 🚀 Local Quickstart Guide

**1. Environment Setup & Requirements:**
Ensure Python 3.12+ is installed. Activate your virtual environment and run:
```bash
pip install sentence-transformers pandas openpyxl qdrant-client
```

**2. Database Initialization:**
Run the core script to spin up the local embedded Qdrant storage and initialize schemas:
```bash
python init_db.py
```

**3. Vectorizing & Uploading Master Data:**
Verify your dataset is properly formatted in an `.xlsx` file. Update the directory paths inside the script and execute the data ingestion workflow:
```bash
python load_data.py
```

**4. Running the Semantic Search Application:**
Launch the desktop UI client. Enter any natural language query and test the vector semantic retrieval:
```bash
python search_gui.py
```
