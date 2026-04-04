# Climate Project

Проект состоит из backend (FastAPI + PostgreSQL) и frontend (React + Vite) для визуализации региональных показателей и демографии.

## Описание ERD-модели

---

## 1. `regions` - регионы

Хранит информацию о регионах России.

* **id** - уникальный номер региона (первичный ключ)
* **name** - название региона (например, «Республика Алтай»)
* **code** - код региона (например, ОКАТО/ОКТМО или внутренний)
* **type** - тип региона («республика», «край», «область» и т.п.)
* **parent\_id** - ссылка на родительский регион (например, муниципалитет относится к региону)

**Связи:**
Используется во всех таблицах, где данные привязаны к конкретному региону.

---

## 2. `units` - единицы измерения

Справочник единиц, чтобы не дублировать и не ошибаться в текстовых записях.

* **id** - уникальный номер единицы
* **code** - сокращение (например, «чел», «%», «°C»)
* **name** - полное название (например, «человек», «процент», «градус Цельсия»)

**Связи:**
Используется в `indicators` для указания единицы измерения показателя.

---

## 3. `indicator_subtypes` - подтипы показателей

Справочник для уточняющей классификации показателей.

* **id** - уникальный номер подтипа
* **name** - название подтипа (например, «Смертность до 1 года», «PM2.5», «PM10»)

**Связи:**
Используется в `indicators` для детализации показателей внутри одной темы.

---

## 4. `indicators` - показатели

Справочник всех показателей, которые собираются и анализируются.

* **id** - уникальный номер показателя
* **name** - название (например, «Смертность», «Рождаемость», «Средняя температура»)
* **unit\_id** - ссылка на единицу измерения (`units.id`)
* **type** - общий тип (например, «демография», «экономика», «экология»)
* **theme** - тематическая группа (например, «рождаемость и смертность»)
* **subtype\_id** - ссылка на подтип (`indicator_subtypes.id`)

**Связи:**
Используется в `indicator_values` для хранения конкретных значений.

---

## 5. `data_sources` - источники данных

Справочник, откуда были получены данные.

* **id** - уникальный номер источника
* **name** - название источника (например, «Росстат»)
* **url** - ссылка на источник (если есть)
* **organization** - организация, предоставившая данные
* **date\_collected** - дата выгрузки/сбора данных

**Связи:**
Используется в `indicator_values` и `population_age_sex`, чтобы было понятно, откуда взялись данные.

---

## 6. `indicator_values` - значения показателей

Хранит числовые значения показателей для разных регионов и лет.

* **id** - уникальный номер записи
* **indicator\_id** - ссылка на показатель (`indicators.id`)
* **region\_id** - ссылка на регион (`regions.id`)
* **year** - год, к которому относится показатель
* **value** - числовое значение (например, 6,5 (%))
* **source\_id** - ссылка на источник данных (`data_sources.id`)

**Связи:**
Привязывает показатель к региону, году и источнику.
Основная таблица фактических данных.

---

## 7. `population_age_sex` - население по возрасту и полу

Хранит демографическую пирамиду: численность населения по полу и возрасту.

* **id** - уникальный номер записи
* **region\_id** - ссылка на регион (`regions.id`)
* **year** - год данных
* **age\_code** - код или диапазон возраста (например, «0-4», «20-24»)
* **sex\_code** - пол: M - мужчины, F - женщины, T - всего
* **value** - численность людей
* **source\_id** - ссылка на источник данных (`data_sources.id`)

**Связи:**
Для каждого региона и года можно хранить полновозрастную структуру населения.

---

## 8. `regional_programs` - региональные программы

Содержит информацию о государственных и региональных программах.

* **id** - уникальный номер программы
* **name** - название программы
* **level** - уровень программы («федеральная», «региональная»)
* **start\_year** - год начала
* **end\_year** - год окончания
* **description** - текстовое описание
* **status** - статус («действует», «завершена»)
* **budget\_total** - общий бюджет программы в рублях

**Связи:**
Через `program_regions` можно связать программу с одним или несколькими регионами.

---

## 9. `program_regions` - связь программ и регионов

Нужна для случаев, когда одна программа затрагивает несколько регионов.

* **id** - уникальный номер записи
* **program\_id** - ссылка на программу (`regional_programs.id`)
* **region\_id** - ссылка на регион (`regions.id`)

**Связи:**
Реализует связь «многие ко многим»:

* один регион может участвовать в нескольких программах;
* одна программа может действовать сразу в нескольких регионах.

---

## 10. `events` - события (катаклизмы, ЧС)

Эта таблица хранит информацию о природных и чрезвычайных происшествиях: пожары, наводнения, засухи, оползни и т.д.

* **id** - уникальный номер события
* **region\_id** - ссылка на регион (`regions.id`), где произошло событие
* **date** - дата происшествия
* **type** - тип события (например, «пожар», «наводнение», «засуха»)
* **severity** - тяжесть последствий (например, от 1 до 10)
* **description** - дополнительное текстовое описание (например, «эвакуация 300 человек»)
* **economic\_loss** - экономический ущерб в рублях

**Связи:**

* Каждое событие обязательно относится к конкретному региону
* Один регион может иметь множество событий в разные годы
* События можно агрегировать и анализировать во времени (например, сколько пожаров произошло в Алтайском крае за 10 лет)

---

## Итоговые связи модели (↔ связь многие-ко-многим)

1. **Регионы и показатели (`regions` ↔ `indicator_values`)**
   Значения показателей всегда привязаны к конкретному региону и году.

2. **Регионы и демография (`regions` → `population_age_sex`)**
   У каждого региона хранится своя возрастно-половая структура по годам.

3. **Регионы и программы (`regions` ↔ `program_regions` ↔ `regional_programs`)**
   Одна программа может охватывать много регионов, и один регион участвует в многих программах.

4. **Показатели и их значения (`indicators` → `indicator_values`)**
   Один показатель имеет множество значений по регионам и годам.

5. **Источники и показатели (`data_sources` → `indicator_values`)**
   Каждое числовое значение знает, из какого источника оно пришло.

6. **Источники и демография (`data_sources` → `population_age_sex`)**
   Для каждой записи по возрасту/полу указан источник данных.

7. **Регионы и события (`regions` → `events`)**
   Каждое событие относится к конкретному региону и дате.

8. **Единицы измерения (`units` → `indicators`)**
   Многие показатели могут ссылаться на одну и ту же единицу (проценты, человек, °C и т.д.).
   Это связь **один `unit` — ко многим `indicators`**.

9. **Подтипы показателей (`indicator_subtypes` → `indicators`)**
   Подтип (например, «Смертность до 1 года») назначается множеству показателей.
   Это связь **один `subtype` — ко многим `indicators`**.

10. **Иерархия регионов (`regions.parent_id` → `regions.id`)**
    Самоссылка: у района родитель — субъект и т.п. Это позволяет строить дерево «субъект → район → МО».

---


## 1. Структура проекта

- `old/backend/` — backend API.
  - `app.py` — точка входа FastAPI.
  - `routers/` — REST endpoints.
  - `services/` — бизнес-логика (подготовка данных для графиков).
  - `repo/` — доступ к PostgreSQL.
  - `tables/` — SQLAlchemy таблицы.
  - `scripts/` — загрузка данных в БД.
- `frontend/web/` — React frontend (графики на ECharts).
- `deploy/nginx.conf` — reverse proxy для production.
- `docker-compose.prod.yml` — production-сборка backend + frontend + db + nginx.

## 2. Требования

Локальная разработка:
- Python 3.12+
- Node.js 20+
- PostgreSQL 15+

Docker запуск:
- Docker Engine 24+
- Docker Compose v2+

## 3. Локальный запуск (без Docker)

### Backend

```bash
cd old/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создайте `.env` в `old/backend`:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=climate_user
DB_PASS=climate_pass
DB_NAME=climate_db
```

Запуск:

```bash
uvicorn app:app --host 0.0.0.0 --port 8081
```

### Frontend

```bash
cd frontend/web
npm install
npm run dev
```

Для работы через backend API можно задать:

```bash
VITE_API_BASE_URL=http://localhost:8081
```

## 4. Запуск через Docker (dev)

Для backend + PostgreSQL:

```bash
cd old/backend
docker compose up --build
```

Backend будет доступен на `http://localhost:8081`.

## 5. Загрузка данных в БД

После старта backend/db выполните:

```bash
cd old/backend
python scripts/fill_db.py
```

Скрипт загружает справочники и значения показателей из `old/backend/data/`.

## 6. Основные API endpoints

Служебные:
- `GET /health`
- `GET /api-info`

Аналитика:
- `GET /analytics/line-chart?region_id=<id>&indicator_ids=1&indicator_ids=2`
  - ответ: `{ labels: [...], datasets: [{ name, data }] }`
- `GET /analytics/pie-chart?region_id=<id>&indicator_ids=1&indicator_ids=2`
  - ответ: `{ timelineLabels: [...], timelineData: [...] }`
- `GET /analytics/population-pyramid?region_id=<id>`
  - ответ: `{ categories: [...], legendItems: [...], timelineLabels: [...], timelineData: [...] }`

Стандартные CRUD endpoints доступны для `regions`, `indicators`, `indicator_values`, `population`, `events`, `programs` и др. через `/docs`.

## 7. Деплой на Linux сервер (Ubuntu)

### 7.1 Установка Docker

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Перелогиньтесь, затем проверьте:

```bash
docker --version
docker compose version
```

### 7.2 Клонирование проекта

```bash
git clone <YOUR_REPOSITORY_URL>
cd climate_project
cp .env.example .env
```

При необходимости отредактируйте `.env`.

### 7.3 Сборка и запуск production

```bash
docker compose -f docker-compose.prod.yml --env-file .env build
docker compose -f docker-compose.prod.yml --env-file .env up -d
```

### 7.4 Первичное заполнение БД

```bash
docker compose -f docker-compose.prod.yml exec backend python scripts/fill_db.py
```

### 7.5 Проверка

- `http://<SERVER_IP>/` — frontend
- `http://<SERVER_IP>/api/health` — backend через nginx reverse proxy
- `http://<SERVER_IP>/api/docs` — Swagger backend

## 8. Nginx reverse proxy (production)

Используется конфигурация `deploy/nginx.conf`:
- `/` проксируется в `frontend` контейнер.
- `/api/*` проксируется в `backend:8081` с удалением префикса `/api`.

Это позволяет держать frontend и API на одном домене без изменения архитектуры приложения.
