# 🎬 MyAnimeList Advanced Data Pipeline: Scraping, Cleaning & EDA

Professional Python-based data pipeline designed to scrape over 10,000 anime records from MyAnimeList (MAL), perform robust data cleaning, handle structural anomalies, and execute Exploratory Data Analysis (EDA).

---

## 📌 Обзор Проекта

Этот проект представляет собой законченный сквозной (End-to-End) сценарий из области **Data Science**. Он решает задачу создания собственного датасета "с нуля" (через веб-скрапинг) и доведения его до аналитических инсайтов с построением статистических визуализаций.

**Процесс разделен на 3 основных этапа:**
1. **Парсинг данных (Web Scraping):** Автоматический сбор 10,000 записей аниме с MyAnimeList с обходом пагинации.
2. **Очистка данных и Feature Engineering:** Преобразование типов данных, обработка пропусков ($NaN$/$NaT$), фильтрация статистических выбросов по методу IQR и создание новых признаков.
3. **Разведочный анализ данных (EDA):** Анализ распределения оценок, эпизодов, корреляционный анализ признаков и генерация графиков.

---

## 🏗️ Архитектура Данных (Схема Pipeline)

Ниже представлена логическая структура движения и обработки данных в проекте:

[ MyAnimeList Website ]
│ (requests + BeautifulSoup, с задержкой time.sleep)
▼
[ Raw Data: Anime_top_10000.csv ] (10,000 строк, сырые типы, строки вместо дат)
│
▼ [ Этап очистки данных (Data Cleaning) ]
├─ Перевод столбцов Score, Episodes, Members в численные типы
├─ Парсинг Start_Date и End_Date в Datetime форматы
├─ Обработка текстовых полей: удаление HTML-тегов, приведение к нижнему регистру
├─ Фильтрация выбросов по популярности (Members) через Interquartile Range (IQR)
└─ Feature Engineering: генерация 'Duration_months' и 'Score_group'
│
▼
[ Cleaned Data: Anime_top_10000_clean.csv ]
│
▼ [ Этап визуализации и анализа (EDA) ]
└─ Построение графиков распределения, корреляционной матрицы (Seaborn/Matplotlib)


---

## 📊 Структура Исходного и Очищенного Датасета

После этапа очистки и конструирования признаков датасет содержит следующие поля:

| Название признака | Тип данных | Описание |
| :--- | :--- | :--- |
| `Title` | `object` (string) | Очищенное название аниме (в нижнем регистре, без HTML-мусора) |
| `Score` | `float64` | Пользовательский рейтинг на MAL (пропуски заполнены средним значением) |
| `Type` | `object` (string) | Формат выпуска (TV, Movie, OVA, ONA, Special, TV Special) |
| `Episodes` | `float64` | Количество эпизодов (нечисловые значения заменены медианным стандартом — 12) |
| `Start_Date` | `datetime64[ns]` | Дата начала трансляции |
| `End_Date` | `datetime64[ns]` | Дата окончания трансляции (для онгоингов заменена на текущую дату) |
| `Members` | `float64` | Количество пользователей, добавивших аниме в список (без выбросов IQR) |
| `Duration_months` | `float64` | **[New]** Длительность трансляции аниме в месяцах |
| `Score_group` | `category` | **[New]** Категориальный рейтинг (`Low`, `Medium`, `High`, `Top`) |

---

## ⚡ Инструкция по Развертыванию и Запуску

### 1. Клонирование репозитория
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
2. Установка зависимостей
Рекомендуется использовать виртуальное окружение (venv):

Bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate     # Для Windows

pip install -r requirements.txt
Примечание: Если файла requirements.txt еще нет, установите библиотеки вручную:

Bash
pip install pandas numpy requests beautifulsoup4 lxml matplotlib seaborn
3. Запуск пайплайна
Запустите основной скрипт для сбора, очистки и анализа данных:

Bash
python main.py
