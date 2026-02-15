# 📊 Student Analytics Telegram Bot

Telegram-бот для ведения базы учеников и анализа их успеваемости.  
Проект создан в учебных и портфолио-целях с использованием **Python, aiogram, pandas и SQLite**.

---

## 🚀 Возможности бота

Бот поддерживает следующие команды:

/start → главное меню

/stats → общая статистика по всем группам

/top <n> → топ n учеников по среднему баллу

/status <status> → ученики с выбранным статусом (good / bad / excellent)

/export → отправить CSV файл с данными

/add_student <name age grade math physics english> → добавить ученика

/delete_student <name> → удалить ученика

---

## 🧠 Логика проекта

- 📦 **SQLite** — хранение данных
- 📊 **pandas** — аналитика и агрегации
- 🤖 **aiogram 3** — Telegram-бот
- ⚡ Асинхронная работа с БД (`aiosqlite`)
- 📈 Автоматическое определение статуса ученика:
  - `excellent` — средний балл ≥ 85
  - `good` — ≥ 75
  - `bad` — ниже 75

---

## 🗂 Структура проекта
```
student-analytics-bot/
│
├── bot.py                 # Основной файл бота и обработчики команд
├── db.py                  # Модуль работы с базой данных
├── analytics.py           # Функции аналитики с pandas
├── config.py              # Конфигурация и настройки
├── requirements.txt       # Зависимости проекта
├── .env                   # Переменные окружения (токен)
├── data.db                # SQLite база данных (создается автоматически)
└── README.md              # Документация проекта
```

---

## ⚙️ Установка и запуск

## 1️⃣ Клонировать репозиторий
```bash
https://github.com/AldyShap/StudentAnBot.git
cd your/project/path
```

## 2️⃣ Создать виртуальное окружение
```
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows
```

## 3️⃣ Установить зависимости
```
pip install -r requirements.txt
```

## 4️⃣ Запустить бота
```bash
python bot.py
```

## 🧪 Используемые технологии
Python 3.10+

aiogram 3
pandas
aiosqlite
SQLite
python-dotenv

## 🎯 Цель проекта
Проект создан для:
- практики асинхронного Python
- работы с базами данных
- аналитики данных
- структурирования кода
- портфолио

### 📌 Автор
👤 Алдияр
Начинающий backend / Python developer
Интересы: Python, аналитика данных, боты, backend


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
