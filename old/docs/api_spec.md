# API Спецификация

## GET /indicators

**Описание:** Получить список всех показателей

**Пример ответа:**
```json
[
  {
    "id": 1,
    "name": "Население",
    "type": "social",
    "unit": "чел"
  }
]
```

---

## GET /indicator-values

**Описание:** Получить значения по региону, году и/или показателю

**Параметры запроса:**
- `region` (string)
- `year` (int)
- `indicator` (string)

**Пример запроса:**
`/indicator-values?region=04&year=2020&indicator=Население`

**Пример ответа:**
```json
[
  {
    "region": "Республика Алтай",
    "year": 2020,
    "indicator": "Население",
    "value": 213500,
    "unit": "чел"
  }
]
```
