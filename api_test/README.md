# API tests: интерактивные графики на локальном сайте

В `api_test` добавлен локальный mini-site, где графики отображаются в браузере интерактивно (как на фронтенде: ECharts, legend toggle, tooltip, zoom/resize поведения ECharts).

## Запуск сайта

```bash
python api_test/charts_site.py --host 127.0.0.1 --port 8090
```

После запуска откройте:
- `http://127.0.0.1:8090/site/index.html`

## Что отображается

1. **Population age/sex** (аналог `BarChartB` во фронтенде)
   - Данные из backend: `GET /analytics/population_pyramid`
   - Параметры: `region_id`, `year`
   - Интерактивность: легенда (вкл/выкл серий), tooltip, адаптация на resize.

2. **Indicator values / chart_data** (аналог `LineChart` во фронтенде)
   - Данные из backend: `GET /analytics/chart_data`
   - Параметры: `region_id`, `indicator_ids`
   - Интерактивность: легенда (вкл/выкл серий), tooltip, адаптация на resize.

## Важно

- Фронтенд проекта **не изменяется**.
- Все сделано только в `api_test`.
- Скриншоты не требуются: графики смотрятся напрямую в браузере на локальном сайте.
