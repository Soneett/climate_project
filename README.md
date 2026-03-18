# Climate Project

Проект состоит из backend (FastAPI + PostgreSQL) и frontend (React + Vite) для визуализации региональных показателей и демографии.

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
