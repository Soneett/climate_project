# API tests: отрисовка графиков в браузере

В этой папке находятся тестовые скрипты для проверки данных backend и отрисовки в браузере через ECharts (аналогично фронтенд-графикам, но без изменений фронтенда).

## 1) Population age/sex (демографическая пирамида)

Скрипт получает данные из `/analytics/population_pyramid`, строит ECharts-график и сохраняет 2 скриншота:
- полный график;
- график после интерактивной фильтрации (скрытие серии через legendUnSelect).

```bash
python api_test/web_echarts_population_test.py \
  --api-url http://127.0.0.1:8080 \
  --region-id 1
```

Артефакты по умолчанию:
- `api_test/artifacts/population_echarts_all.png`
- `api_test/artifacts/population_echarts_filtered.png`

## 2) Indicator values (chart_data)

Скрипт получает данные из `/analytics/chart_data` для выбранных индикаторов и региона, строит line chart и сохраняет:
- полный график;
- график после интерактивной фильтрации (отключение одной серии через legendUnSelect).

```bash
python api_test/web_echarts_indicator_values_test.py \
  --api-url http://127.0.0.1:8080 \
  --region-id 1 \
  --indicator-ids 1 2 3
```

Артефакты по умолчанию:
- `api_test/artifacts/indicator_values_line_all.png`
- `api_test/artifacts/indicator_values_line_filtered.png`

## Примечания

- Скрипты используют `playwright` + `chromium` для рендера графиков и скриншотов.
- Фронтенд-код не модифицируется: тесты находятся только в `api_test`.
