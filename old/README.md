# Анализ социально-климатического профиля регионов РФ

Проект по сбору, хранению и визуализации данных.

Структура проекта

| Папка / файл                         | Назначение                               |
| ------------------------------------ | ---------------------------------------- |
| `frontend/`                          | Мок-данные и описание для фронтенда      |
| `frontend/mock/`                     | JSON-файлы, имитирующие API-ответы       |
| `frontend/indicators_description.md` | Описание всех показателей для интерфейса |
|                                      |                                          |
| `backend/`                           | Стартовая структура FastAPI-приложения   |
| `backend/main.py`                    | Пример маршрута `/indicators`            |
| `backend/models/`                    | SQLAlchemy и Pydantic модели             |
| `backend/requirements.txt`           | Зависимости                              |
| `backend/docker-compose.yml`         | Docker-сборка с PostgreSQL               |
| `.env.example`                       | Переменные окружения                     |
|                                      |                                          |
| `data/`                              | Шаблоны и подготовленные данные          |
| `data/indicator_values_template.csv` | CSV-шаблон для загрузки значений         |
| `data/sources_list.md`               | Список всех источников данных            |
|                                      |                                          |
| `docs/`                              | Документация и схемы                     |
| `docs/api_spec.md`                   | Примеры API-запросов                     |
| `docs/figma_mockup.png`              | UI-макет интерфейса                      |
|                                      |                                          |
| `.gitignore`                         | Исключения из коммитов                   |
| `README.md`                          | Описание проекта, цели и структура       |
