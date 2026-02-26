# API test: половозрастная структура

Скрипт `population_age_sex_charts.py` строит график-пирамиду на основании API backend.

## Запуск

```bash
python api_test/population_age_sex_charts.py --region-id 1 --api-url http://127.0.0.1:8080
```

Если `--year` не задан, backend берёт последний доступный год из таблицы `population_age_sex`.
