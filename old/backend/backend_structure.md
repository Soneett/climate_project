Описание назначения папок и файлов backend-части.

## Корень backend
- `app.py` - точка входа FastAPI, конфигурация middleware, health/info endpoints, подключение роутеров.
- `database.py` - создание SQLAlchemy engine/session и dependency `get_db`.
- `config.py` - чтение переменных окружения и сборка `DATABASE_URL`.
- `requirements.txt` - python-зависимости backend.
- `Dockerfile` - сборка Docker-образа сервиса.
- `docker-compose.yaml` - запуск postgres + backend локально в контейнерах.
- `OpenAPI.yaml` - описание API-приложения.
- `__init__.py` - маркер python-пакета.

## `routers/` — HTTP API (FastAPI APIRouter)
- `routers/__init__.py` — централизованный экспорт всех роутеров.
- `routers/regions.py` — CRUD API для регионов.
- `routers/units.py` — CRUD API для единиц измерения.
- `routers/indicator_subtypes.py` — CRUD API для подтипов показателей.
- `routers/indicators.py` — CRUD API для справочника показателей.
- `routers/data_sources.py` — CRUD API для источников данных.
- `routers/indicator_values.py` — CRUD API для значений показателей (region/year/value).
- `routers/population_age_sex.py` — CRUD API для половозрастной структуры населения.
- `routers/regional_programs.py` — CRUD API для программ.
- `routers/program_regions.py` — CRUD API для связки программ и регионов.
- `routers/events.py` — CRUD API для событий/ЧС.
- `routers/analytics.py` — агрегирующий endpoint для графиков фронтенда (`/analytics/chart_data`).

## `models/` — Pydantic-модели API
- `models/__init__.py` — экспорт всех pydantic-моделей.
- `models/base.py` — базовые модели репозитория (`RepoBaseModel`, `RepoBaseIdModel`).
- `models/filter.py` — модели фильтрации/пагинации и enum операций фильтра.
- `models/regions.py` — модели create/read/update для регионов.
- `models/units.py` — модели create/read/update для единиц измерения.
- `models/indicator_subtypes.py` — модели create/read/update для подтипов индикаторов.
- `models/indicators.py` — модели create/read/update для индикаторов.
- `models/data_sources.py` — модели create/read/update для источников данных.
- `models/indicator_values.py` — модели create/read/update для значений показателей.
- `models/population_age_sex.py` — модели create/read/update по демографии возраст/пол.
- `models/regional_programs.py` — модели create/read/update для программ.
- `models/program_regions.py` — модели create/read/update связки программа↔регион.
- `models/events.py` — модели create/read/update событий.
- `models/analytics.py` — response-модели для данных графиков (series/points).

## `tables/` — SQLAlchemy ORM таблицы
- `tables/__init__.py` — экспорт ORM-таблиц.
- `tables/base.py` — общая ORM-база: `id`, `is_deleted`, утилиты сериализации.
- `tables/camel_snake.py` — helper преобразования CamelCase → snake_case для table names.
- `tables/regions.py` — ORM-таблица регионов.
- `tables/units.py` — ORM-таблица единиц измерения.
- `tables/indicator_subtypes.py` - ORM-таблица подтипов индикаторов.
- `tables/indicators.py` - ORM-таблица справочника индикаторов.
- `tables/data_sources.py` - ORM-таблица источников данных.
- `tables/indicator_values.py` - ORM-таблица факт-значений показателей.
- `tables/population_age_sex.py` - ORM-таблица половозрастных данных населения.
- `tables/regional_programs.py` - ORM-таблица региональных программ.
- `tables/program_regions.py` - ORM-таблица many-to-many программ и регионов.
- `tables/events.py` - ORM-таблица климатических/ЧС событий.

## `repo/` — generic repository слой
- `repo/__init__.py` - экспорт репозиториев.
- `repo/base.py` - базовая логика конвертации из ORM в pydantic-модели.
- `repo/read.py` - чтение, фильтрация, пагинация, подсчёт.
- `repo/create.py` - создание одной и нескольких записей.
- `repo/update.py` - обновление записей.
- `repo/delete.py` - soft-delete записей.
- `repo/crud.py` - агрегированный CRUD-репозиторий (композиция create/read/update/delete).

## `scripts/` — утилиты загрузки данных
- `scripts/fill_db.py` — orchestration-скрипт первичного наполнения БД.
- `scripts/loaders/__init__.py` — экспорт loader-функций.
- `scripts/loaders/load_regions.py` — загрузка регионов в БД.
- `scripts/loaders/load_units.py` — загрузка единиц измерения.
- `scripts/loaders/load_indicator_subtypes.py` — загрузка подтипов индикаторов.
- `scripts/loaders/load_indicators.py` — загрузка индикаторов.
- `scripts/loaders/load_data_sources.py` — загрузка источников данных.
- `scripts/loaders/load_population.py` — загрузка population age/sex данных.
- `scripts/loaders/load_indicator_values.py` — загрузка факт-значений индикаторов.

## `parsers/` — парсинг исходных JSON
- `parsers/__init__.py` — экспорт parser-функций.
- `parsers/regions.py` — парсинг файла регионов.
- `parsers/units.py` — парсинг справочника единиц измерения.
- `parsers/indicator_subtypes.py` — парсинг подтипов индикаторов.
- `parsers/indicators.py` — парсинг справочника индикаторов.
- `parsers/data_sources.py` — парсинг источников данных.
- `parsers/population_age_sex.py` — парсинг демографических данных.
- `parsers/indicator_values.py` — парсинг значений индикаторов.

## `data/` — исходные данные для заполнения БД
- `data/regions.json` — справочник регионов.
- `data/units.json` — справочник единиц измерения.
- `data/indicator_subtypes.json` — справочник подтипов индикаторов.
- `data/indicators.json` — справочник всех индикаторов и метаданных.
- `data/data_sources.json` — справочник источников.
- `data/population/` — демографические JSON (возраст/пол).
  - `separated_by_age.json` — агрегаты по возрасту.
  - `separated_by_sex.json` — агрегаты по полу.
  - `separated_age_sex.json` — комбинированные данные возраст+пол.
- `data/indicator_values/` — набор JSON по тематическим блокам показателей.
  - `birth_abs.json` — рождаемость (абсолют).
  - `deaths.json` — смертность.
  - `death_causes.json` — причины смертности.
  - `migration.json` — миграция.
  - `natural_abs.json` — естественный прирост/убыль.
  - `poverty_level.json` — уровень бедности.
  - `consumption_expenditure.json` — потребление/расходы.
  - `structure_of_income.json` — структура доходов.
  - `healthcare_indicators.json` — показатели здравоохранения.
  - `morbidity.json` — заболеваемость.
  - `vrp.json` — валовой региональный продукт.
  - `IVBO.json` — блок показателей IVBO.
  - `kmn_population.json` — данные по численности КМН.
  - `road_press_release.json` — дорожная/пресс статистика (источник проекта).
