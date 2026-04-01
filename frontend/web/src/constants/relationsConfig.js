import { DISASTER_ROADS_DATA, INDICATOR_OPTIONS } from '../data/disasterRoadsData';
export { DISASTER_ROADS_DATA };

export const SUBJECT_INDICATORS = [
  {
    id: "temperature",
    label: "Температура",
    availableObjects: ["demography", "healthcare", "livingStandard", "economy"]
  },
  {
    id: "precipitation",
    label: "Осадки",
    availableObjects: ["healthcare", "economy", "infrastructure"]
  },
  {
    id: "wind",
    label: "Ветер",
    availableObjects: ["healthcare"]
  },
  {
    id: "disasters",
    label: "Природные катаклизмы",
    availableObjects: ["demography", "healthcare", "livingStandard", "economy", "infrastructure"]
  },
  {
    id: "ecology",
    label: "Экология",
    availableObjects: ["demography", "healthcare", "livingStandard"]
  },
];

export const OBJECT_INDICATORS = [
  { id: "demography", label: "Демография", availableSubjects: ["temperature", "disasters", "ecology"] },
  { id: "healthcare", label: "Здравоохранение", availableSubjects: ["temperature", "precipitation", "wind", "disasters", "ecology"] },
  { id: "livingStandard", label: "Уровень жизни", availableSubjects: ["temperature", "disasters", "ecology"] },
  { id: "education", label: "Образование", availableSubjects: [] },
  { id: "economy", label: "Экономика", availableSubjects: ["precipitation", "disasters", "temperature"] },
  { id: "infrastructure", label: "Инфраструктура", availableSubjects: ["precipitation", "disasters"] },
];

export const RELATIONS_CONTENT = {
  "temperature-demography": [
    {
      id: "rel-temp-demo-1",
      title: "Взаимосвязь температуры и демографии",
      chartType: "scatterPlot",
      scatterPlotData: {
        title: "Взаимосвязь температуры и демографии",
        categories: ['Рождаемость', 'Смертность', 'Миграция', 'Население'],
        years: [2020, 2021, 2022, 2023, 2024],
        xAxisOptions: [
          { key: 'annual', label: 'Среднегодовая температура (°C)' },
          { key: 'summer', label: 'Средняя температура лета (°C)' },
          { key: 'winter', label: 'Средняя температура зимы (°C)' },
          { key: 'tmax', label: 'Максимальная зарегистрированная температура (°C)' },
          { key: 'tmin', label: 'Минимальная зарегистрированная температура (°C)' }
        ],
        yAxisLabel: 'Количество человек',
        data: [
          { year: 2020, category: 'Рождаемость', annual: 5.0, summer: 12.0, winter: -1.0, tmax: 15.0, tmin: -5.0, value: 1200000 },
          { year: 2020, category: 'Смертность', annual: 5.0, summer: 12.0, winter: -1.0, tmax: 15.0, tmin: -5.0, value: 800000 },
          { year: 2020, category: 'Миграция', annual: 5.0, summer: 12.0, winter: -1.0, tmax: 15.0, tmin: -5.0, value: 250000 },
          { year: 2020, category: 'Население', annual: 5.0, summer: 12.0, winter: -1.0, tmax: 15.0, tmin: -5.0, value: 14000000 },
          { year: 2021, category: 'Рождаемость', annual: 5.2, summer: 12.3, winter: -0.8, tmax: 15.3, tmin: -4.7, value: 1250000 },
          { year: 2021, category: 'Смертность', annual: 5.2, summer: 12.3, winter: -0.8, tmax: 15.3, tmin: -4.7, value: 850000 },
          { year: 2021, category: 'Миграция', annual: 5.2, summer: 12.3, winter: -0.8, tmax: 15.3, tmin: -4.7, value: 300000 },
          { year: 2021, category: 'Население', annual: 5.2, summer: 12.3, winter: -0.8, tmax: 15.3, tmin: -4.7, value: 14100000 },
          { year: 2022, category: 'Рождаемость', annual: 5.4, summer: 12.6, winter: -0.5, tmax: 15.6, tmin: -4.3, value: 1180000 },
          { year: 2022, category: 'Смертность', annual: 5.4, summer: 12.6, winter: -0.5, tmax: 15.6, tmin: -4.3, value: 820000 },
          { year: 2022, category: 'Миграция', annual: 5.4, summer: 12.6, winter: -0.5, tmax: 15.6, tmin: -4.3, value: 280000 },
          { year: 2022, category: 'Население', annual: 5.4, summer: 12.6, winter: -0.5, tmax: 15.6, tmin: -4.3, value: 14050000 },
          { year: 2023, category: 'Рождаемость', annual: 5.6, summer: 12.9, winter: -0.2, tmax: 15.9, tmin: -3.9, value: 1220000 },
          { year: 2023, category: 'Смертность', annual: 5.6, summer: 12.9, winter: -0.2, tmax: 15.9, tmin: -3.9, value: 780000 },
          { year: 2023, category: 'Миграция', annual: 5.6, summer: 12.9, winter: -0.2, tmax: 15.9, tmin: -3.9, value: 320000 },
          { year: 2023, category: 'Население', annual: 5.6, summer: 12.9, winter: -0.2, tmax: 15.9, tmin: -3.9, value: 14200000 },
          { year: 2024, category: 'Рождаемость', annual: 5.8, summer: 13.2, winter: 0.1, tmax: 16.2, tmin: -3.5, value: 1260000 },
          { year: 2024, category: 'Смертность', annual: 5.8, summer: 13.2, winter: 0.1, tmax: 16.2, tmin: -3.5, value: 750000 },
          { year: 2024, category: 'Миграция', annual: 5.8, summer: 13.2, winter: 0.1, tmax: 16.2, tmin: -3.5, value: 350000 },
          { year: 2024, category: 'Население', annual: 5.8, summer: 13.2, winter: 0.1, tmax: 16.2, tmin: -3.5, value: 14350000 }
        ]
      }
    }
  ],
  "temperature-healthcare": [
    {
      id: "rel-temp-health-1",
      title: "Взаимосвязь температуры и заболеваемости",
      chartType: "combinedPlotB",
      combinedPlotBData: {
        title: "Заболеваемость",
        categories: ['Вирус A', 'Вирус B', 'Инфекция C', 'Другие'],
        years: [2020, 2021, 2022, 2023, 2024],
        xAxisOptions: [
          { key: 'annual', label: 'Среднегодовая температура (°C)' },
          { key: 'summer', label: 'Средняя температура лета (°C)' },
          { key: 'winter', label: 'Средняя температура зимы (°C)' },
          { key: 'tmax', label: 'Максимальная зарегистрированная температура (°C)' },
          { key: 'tmin', label: 'Минимальная зарегистрированная температура (°C)' }
        ],
        yAxisLabel: 'Число заболевших',
        data: [
          { year: 2020, category: 'Вирус A', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 1550 },
          { year: 2020, category: 'Вирус B', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 1020 },
          { year: 2020, category: 'Инфекция C', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 540 },
          { year: 2020, category: 'Другие', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 280 },
          { year: 2021, category: 'Вирус A', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 1480 },
          { year: 2021, category: 'Вирус B', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 1080 },
          { year: 2021, category: 'Инфекция C', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 570 },
          { year: 2021, category: 'Другие', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 310 },
          { year: 2022, category: 'Вирус A', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 1520 },
          { year: 2022, category: 'Вирус B', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 1150 },
          { year: 2022, category: 'Инфекция C', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 600 },
          { year: 2022, category: 'Другие', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 340 },
          { year: 2023, category: 'Вирус A', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 1600 },
          { year: 2023, category: 'Вирус B', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 1200 },
          { year: 2023, category: 'Инфекция C', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 630 },
          { year: 2023, category: 'Другие', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 370 },
          { year: 2024, category: 'Вирус A', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 1680 },
          { year: 2024, category: 'Вирус B', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 1250 },
          { year: 2024, category: 'Инфекция C', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 660 },
          { year: 2024, category: 'Другие', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 400 }
        ]
      }
    }
  ],
  "temperature-livingStandard": [
    {
      id: "rel-temp-living-1",
      title: "Взаимосвязь температуры и состава доходов",
      chartType: "combinedPlotA",
      combinedPlotAData: {
        title: "Взаимосвязь температуры и состава доходов",
        yAxis1Series: [
          { key: 'income', name: 'Доходы', color: '#26af55' },
          { key: 'expense', name: 'Расходы', color: '#e54e1b' }
        ],
        yAxis1Label: 'Финансовые показатели (млн)',
        yAxis2Options: [
          { key: 'annual', label: 'Среднегодовая температура' },
          { key: 'summer', label: 'Средняя температура лета' },
          { key: 'winter', label: 'Средняя температура зимы' },
          { key: 'tmax', label: 'Максимальная зарегистрированная температура' },
          { key: 'tmin', label: 'Минимальная зарегистрированная температура' }
        ],
        data: [
          { year: '2020', income: 610, expense: 605, annual: 6.1, summer: 13.4, winter: -0.2, tmax: 16.7, tmin: -4.3 },
          { year: '2021', income: 650, expense: 630, annual: 6.3, summer: 13.7, winter: 0.0, tmax: 17.0, tmin: -3.9 },
          { year: '2022', income: 670, expense: 645, annual: 6.6, summer: 14.0, winter: 0.3, tmax: 17.4, tmin: -3.5 },
          { year: '2023', income: 700, expense: 680, annual: 6.9, summer: 14.4, winter: 0.6, tmax: 17.9, tmin: -3.1 },
          { year: '2024', income: 730, expense: 710, annual: 7.1, summer: 14.8, winter: 0.9, tmax: 18.3, tmin: -2.7 }
        ]
      }
    }
  ],
  "temperature-economy": [
    {
      id: "rel-temp-eco-1",
      title: "Взаимосвязь температуры и индекса стоимости жизни",
      chartType: "combinedPlotA",
      combinedPlotAData: {
        title: "Взаимосвязь температуры и индекса стоимости жизни",
        yAxis1Series: [
          { key: 'cost_of_living', name: 'Индекс стоимости жизни', color: '#26af55' }
        ],
        yAxis1Label: 'Индекс стоимости жизни',
        yAxis2Options: [
          { key: 'annual', label: 'Среднегодовая температура' },
          { key: 'summer', label: 'Средняя температура лета' },
          { key: 'winter', label: 'Средняя температура зимы' },
          { key: 'tmax', label: 'Максимальная зарегистрированная температура' },
          { key: 'tmin', label: 'Минимальная зарегистрированная температура' }
        ],
        data: [
          { year: '2020', cost_of_living: 72.4, annual: 6.1, summer: 13.4, winter: -0.2, tmax: 16.7, tmin: -4.3 },
          { year: '2021', cost_of_living: 74.1, annual: 6.3, summer: 13.7, winter: 0.0, tmax: 17.0, tmin: -3.9 },
          { year: '2022', cost_of_living: 78.6, annual: 6.6, summer: 14.0, winter: 0.3, tmax: 17.4, tmin: -3.5 },
          { year: '2023', cost_of_living: 80.2, annual: 6.9, summer: 14.4, winter: 0.6, tmax: 17.9, tmin: -3.1 },
          { year: '2024', cost_of_living: 82.5, annual: 7.1, summer: 14.8, winter: 0.9, tmax: 18.3, tmin: -2.7 }
        ]
      }
    },
    {
      id: "rel-temp-eco-2",
      title: "Взаимосвязь температуры и уровня бедности",
      chartType: "combinedPlotA",
      combinedPlotAData: {
        title: "Взаимосвязь температуры и уровня бедности",
        yAxis1Series: [
          { key: 'poverty_rate', name: 'Уровень бедности', color: '#e54e1b' }
        ],
        yAxis1Label: 'Уровень бедности (%)',
        yAxis2Options: [
          { key: 'annual', label: 'Среднегодовая температура' },
          { key: 'summer', label: 'Средняя температура лета' },
          { key: 'winter', label: 'Средняя температура зимы' },
          { key: 'tmax', label: 'Максимальная зарегистрированная температура' },
          { key: 'tmin', label: 'Минимальная зарегистрированная температура' }
        ],
        data: [
          { year: '2020', poverty_rate: 12.5, annual: 6.1, summer: 13.4, winter: -0.2, tmax: 16.7, tmin: -4.3 },
          { year: '2021', poverty_rate: 11.8, annual: 6.3, summer: 13.7, winter: 0.0, tmax: 17.0, tmin: -3.9 },
          { year: '2022', poverty_rate: 11.2, annual: 6.6, summer: 14.0, winter: 0.3, tmax: 17.4, tmin: -3.5 },
          { year: '2023', poverty_rate: 10.7, annual: 6.9, summer: 14.4, winter: 0.6, tmax: 17.9, tmin: -3.1 },
          { year: '2024', poverty_rate: 10.1, annual: 7.1, summer: 14.8, winter: 0.9, tmax: 18.3, tmin: -2.7 }
        ]
      }
    }
  ],
  "precipitation-healthcare": [],
  "precipitation-economy": [
    {
      id: "rel-precip-eco-1",
      title: "Взаимосвязь осадков и площади сельскохозяйственных угодий",
      chartType: "scatterPlot",
      scatterPlotData: {
        title: "Взаимосвязь осадков и площади сельскохозяйственных угодий",
        categories: ['Зерновые', 'Овощеводство', 'Пастбища'],
        years: [2020, 2021, 2022, 2023, 2024],
        xAxisOptions: [
          { key: 'annual_precip', label: 'Годовое количество осадков (мм)' },
          { key: 'snow_days', label: 'Количество снежных дней' },
          { key: 'rain_days', label: 'Количество дождливых дней' }
        ],
        yAxisLabel: 'Площадь сельскохозяйственных угодий (тыс. га)',
        data: [
          { year: 2020, category: 'Зерновые', annual_precip: 520, snow_days: 45, rain_days: 90, value: 1200 },
          { year: 2020, category: 'Овощеводство', annual_precip: 520, snow_days: 45, rain_days: 90, value: 380 },
          { year: 2020, category: 'Пастбища', annual_precip: 520, snow_days: 45, rain_days: 90, value: 2100 },
          { year: 2021, category: 'Зерновые', annual_precip: 490, snow_days: 40, rain_days: 85, value: 1150 },
          { year: 2021, category: 'Овощеводство', annual_precip: 490, snow_days: 40, rain_days: 85, value: 360 },
          { year: 2021, category: 'Пастбища', annual_precip: 490, snow_days: 40, rain_days: 85, value: 2050 },
          { year: 2022, category: 'Зерновые', annual_precip: 560, snow_days: 50, rain_days: 95, value: 1280 },
          { year: 2022, category: 'Овощеводство', annual_precip: 560, snow_days: 50, rain_days: 95, value: 410 },
          { year: 2022, category: 'Пастбища', annual_precip: 560, snow_days: 50, rain_days: 95, value: 2200 },
          { year: 2023, category: 'Зерновые', annual_precip: 480, snow_days: 38, rain_days: 80, value: 1100 },
          { year: 2023, category: 'Овощеводство', annual_precip: 480, snow_days: 38, rain_days: 80, value: 340 },
          { year: 2023, category: 'Пастбища', annual_precip: 480, snow_days: 38, rain_days: 80, value: 1980 },
          { year: 2024, category: 'Зерновые', annual_precip: 540, snow_days: 47, rain_days: 92, value: 1240 },
          { year: 2024, category: 'Овощеводство', annual_precip: 540, snow_days: 47, rain_days: 92, value: 395 },
          { year: 2024, category: 'Пастбища', annual_precip: 540, snow_days: 47, rain_days: 92, value: 2150 }
        ]
      }
    },
    {
      id: "rel-precip-eco-2",
      title: "Взаимосвязь осадков и вклада сельского хозяйства в ВРП",
      chartType: "scatterPlot",
      scatterPlotData: {
        title: "Взаимосвязь осадков и вклада сельского хозяйства в ВРП",
        categories: ['Зерновые', 'Овощеводство', 'Пастбища'],
        years: [2020, 2021, 2022, 2023, 2024],
        xAxisOptions: [
          { key: 'annual_precip', label: 'Годовое количество осадков (мм)' },
          { key: 'snow_days', label: 'Количество снежных дней' },
          { key: 'rain_days', label: 'Количество дождливых дней' }
        ],
        yAxisLabel: 'Вклад сельского хозяйства в ВРП (%)',
        data: [
          { year: 2020, category: 'Зерновые', annual_precip: 520, snow_days: 45, rain_days: 90, value: 8.2 },
          { year: 2020, category: 'Овощеводство', annual_precip: 520, snow_days: 45, rain_days: 90, value: 2.5 },
          { year: 2020, category: 'Пастбища', annual_precip: 520, snow_days: 45, rain_days: 90, value: 4.1 },
          { year: 2021, category: 'Зерновые', annual_precip: 490, snow_days: 40, rain_days: 85, value: 7.8 },
          { year: 2021, category: 'Овощеводство', annual_precip: 490, snow_days: 40, rain_days: 85, value: 2.3 },
          { year: 2021, category: 'Пастбища', annual_precip: 490, snow_days: 40, rain_days: 85, value: 3.9 },
          { year: 2022, category: 'Зерновые', annual_precip: 560, snow_days: 50, rain_days: 95, value: 9.0 },
          { year: 2022, category: 'Овощеводство', annual_precip: 560, snow_days: 50, rain_days: 95, value: 2.8 },
          { year: 2022, category: 'Пастбища', annual_precip: 560, snow_days: 50, rain_days: 95, value: 4.5 },
          { year: 2023, category: 'Зерновые', annual_precip: 480, snow_days: 38, rain_days: 80, value: 7.5 },
          { year: 2023, category: 'Овощеводство', annual_precip: 480, snow_days: 38, rain_days: 80, value: 2.2 },
          { year: 2023, category: 'Пастбища', annual_precip: 480, snow_days: 38, rain_days: 80, value: 3.7 },
          { year: 2024, category: 'Зерновые', annual_precip: 540, snow_days: 47, rain_days: 92, value: 8.6 },
          { year: 2024, category: 'Овощеводство', annual_precip: 540, snow_days: 47, rain_days: 92, value: 2.6 },
          { year: 2024, category: 'Пастбища', annual_precip: 540, snow_days: 47, rain_days: 92, value: 4.3 }
        ]
      }
    }
  ],
  "precipitation-infrastructure": [],
  "wind-healthcare": [
    {
      id: "rel-wind-health-1",
      title: "Взаимосвязь ветра и заболеваемости",
      chartType: "combinedPlotB",
      combinedPlotBData: {
        title: "Взаимосвязь ветра и заболеваемости",
        categories: ['Респираторные', 'Аллергические', 'Сердечно-сосудистые', 'Другие'],
        years: [2020, 2021, 2022, 2023, 2024],
        xAxisOptions: [
          { key: 'avg_wind', label: 'Средняя скорость ветра (м/с)' },
          { key: 'max_wind', label: 'Максимальная скорость ветра (м/с)' }
        ],
        yAxisLabel: 'Число заболевших',
        data: [
          { year: 2020, category: 'Респираторные', avg_wind: 4.2, max_wind: 12.5, cases: 3200 },
          { year: 2020, category: 'Аллергические', avg_wind: 4.2, max_wind: 12.5, cases: 1800 },
          { year: 2020, category: 'Сердечно-сосудистые', avg_wind: 4.2, max_wind: 12.5, cases: 950 },
          { year: 2020, category: 'Другие', avg_wind: 4.2, max_wind: 12.5, cases: 420 },
          { year: 2021, category: 'Респираторные', avg_wind: 3.8, max_wind: 11.0, cases: 2900 },
          { year: 2021, category: 'Аллергические', avg_wind: 3.8, max_wind: 11.0, cases: 1650 },
          { year: 2021, category: 'Сердечно-сосудистые', avg_wind: 3.8, max_wind: 11.0, cases: 880 },
          { year: 2021, category: 'Другие', avg_wind: 3.8, max_wind: 11.0, cases: 390 },
          { year: 2022, category: 'Респираторные', avg_wind: 4.8, max_wind: 14.0, cases: 3500 },
          { year: 2022, category: 'Аллергические', avg_wind: 4.8, max_wind: 14.0, cases: 2100 },
          { year: 2022, category: 'Сердечно-сосудистые', avg_wind: 4.8, max_wind: 14.0, cases: 1050 },
          { year: 2022, category: 'Другие', avg_wind: 4.8, max_wind: 14.0, cases: 480 },
          { year: 2023, category: 'Респираторные', avg_wind: 4.0, max_wind: 11.8, cases: 3100 },
          { year: 2023, category: 'Аллергические', avg_wind: 4.0, max_wind: 11.8, cases: 1750 },
          { year: 2023, category: 'Сердечно-сосудистые', avg_wind: 4.0, max_wind: 11.8, cases: 910 },
          { year: 2023, category: 'Другие', avg_wind: 4.0, max_wind: 11.8, cases: 440 },
          { year: 2024, category: 'Респираторные', avg_wind: 4.5, max_wind: 13.2, cases: 3350 },
          { year: 2024, category: 'Аллергические', avg_wind: 4.5, max_wind: 13.2, cases: 1950 },
          { year: 2024, category: 'Сердечно-сосудистые', avg_wind: 4.5, max_wind: 13.2, cases: 1000 },
          { year: 2024, category: 'Другие', avg_wind: 4.5, max_wind: 13.2, cases: 460 }
        ]
      }
    }
  ],
  "disasters-demography": [],
  "disasters-healthcare": [],
  "disasters-livingStandard": [],
  "disasters-economy": [
    {
      id: "rel-dis-eco-1",
      title: "Взаимосвязь экономического ущерба и ВРП",
      chartType: "combinedPlotC",
      combinedPlotCData: {
        title: "Доля ущерба от катаклизмов в ВРП",
        yAxisLabel: "Доля ущерба от катаклизмов в ВРП (%)",
        legendLabel: "Доля ущерба в ВРП",
        data: [
          { year: '2020', gdp: 1500, damage: 30 },
          { year: '2021', gdp: 1580, damage: 45 },
          { year: '2022', gdp: 1640, damage: 25 },
          { year: '2023', gdp: 1700, damage: 60 },
          { year: '2024', gdp: 1780, damage: 40 }
        ]
      }
    }
  ],
  "disasters-infrastructure": [
    {
      id: "disaster-roads-map",
      title: "Взаимосвязь природных катаклизмов и автодорог",
      chartType: "colorMarkerMap",
      colorMarkerMapData: {
        geojsonPath: "/altai.geojson",
        indicatorOptions: INDICATOR_OPTIONS,
        dataByYear: DISASTER_ROADS_DATA,
        regionTitle: 'Республика Алтай',
      },
    },
  ],
  "ecology-demography": [
    {
      id: "eco-demo-linedot",
      title: "Взаимосвязь индекса качества воздуха/воды и демографии",
      chartType: "lineDotChart",
      lineDotChartData: {
        years: ['2020', '2021', '2022', '2023', '2024'],
        primaryCategories: ['Рождаемость', 'Смертность', 'Миграция', 'Численность населения'],
        secondaryOptions: [
          { key: 'airQuality', label: 'Индекс качества воздуха' },
          { key: 'waterQuality', label: 'Индекс качества воды' }
        ],
        yAxisLabel: 'Число людей (тыс.)',
        data: [
          { year: '2020', category: 'Рождаемость', value: 12500, airQuality: 65, waterQuality: 72 },
          { year: '2021', category: 'Рождаемость', value: 12300, airQuality: 68, waterQuality: 74 },
          { year: '2022', category: 'Рождаемость', value: 12100, airQuality: 71, waterQuality: 76 },
          { year: '2023', category: 'Рождаемость', value: 11900, airQuality: 73, waterQuality: 78 },
          { year: '2024', category: 'Рождаемость', value: 11800, airQuality: 75, waterQuality: 80 },
          { year: '2020', category: 'Смертность', value: 14200, airQuality: 65, waterQuality: 72 },
          { year: '2021', category: 'Смертность', value: 15100, airQuality: 68, waterQuality: 74 },
          { year: '2022', category: 'Смертность', value: 14800, airQuality: 71, waterQuality: 76 },
          { year: '2023', category: 'Смертность', value: 14500, airQuality: 73, waterQuality: 78 },
          { year: '2024', category: 'Смертность', value: 14100, airQuality: 75, waterQuality: 80 },
          { year: '2020', category: 'Миграция', value: -3200, airQuality: 65, waterQuality: 72 },
          { year: '2021', category: 'Миграция', value: -2800, airQuality: 68, waterQuality: 74 },
          { year: '2022', category: 'Миграция', value: -2100, airQuality: 71, waterQuality: 76 },
          { year: '2023', category: 'Миграция', value: -1500, airQuality: 73, waterQuality: 78 },
          { year: '2024', category: 'Миграция', value: -800, airQuality: 75, waterQuality: 80 },
          { year: '2020', category: 'Численность населения', value: 1420000, airQuality: 65, waterQuality: 72 },
          { year: '2021', category: 'Численность населения', value: 1415000, airQuality: 68, waterQuality: 74 },
          { year: '2022', category: 'Численность населения', value: 1412000, airQuality: 71, waterQuality: 76 },
          { year: '2023', category: 'Численность населения', value: 1410000, airQuality: 73, waterQuality: 78 },
          { year: '2024', category: 'Численность населения', value: 1409000, airQuality: 75, waterQuality: 80 }
        ]
      }
    }
  ],
  "ecology-healthcare": [],
  "ecology-livingStandard": [],
};
