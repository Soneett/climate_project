CONTENT_BLOCKS = {
    "regional": [
        {
            "id": "regional-1",
            "title": "Карта региона",
            "chartType": "line",
            "indicators": ["Рождаемость", "Смертность"],
            "chartData": {
                "labels": ["2019", "2020", "2021", "2022", "2023", "2024"],
                "datasets": [
                    {"name": "Рождаемость", "data": [120, 132, 101, 134, 90, 230]},
                    {"name": "Смертность", "data": [220, 182, 191, 234, 290, 330]},
                ],
            },
        }
    ],
    "s1": [
        {
            "id": "s1-1",
            "title": "Динамика рождаемости и смертности",
            "chartType": "line",
            "indicators": ["Рождаемость", "Смертность"],
            "chartData": {
                "labels": ["2019", "2020", "2021", "2022", "2023", "2024"],
                "datasets": [
                    {"name": "Рождаемость", "data": [10.1, 9.8, 9.6, 9.0, 8.7, 8.5]},
                    {"name": "Смертность", "data": [12.5, 14.5, 16.7, 13.2, 12.1, 11.8]},
                ],
            },
        }
    ],
}

SUBJECT_INDICATORS = []
OBJECT_INDICATORS = []
RELATIONS_CONTENT = {}