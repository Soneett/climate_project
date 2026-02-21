// Каждый элемент левого столбца имеет массив доступных элементов правого столбца
export const SUBJECT_INDICATORS = [
  { 
    id: "temperature", 
    label: "Температура", 
    availableObjects: ["demography", "healthcare", "livingStandard"]
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
  { id: "economy", label: "Экономика", availableSubjects: ["precipitation", "disasters"] },
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
      title: "Заболеваемость",
      chartType: "combinedPlotB",
      combinedPlotBData: {
        title: "Заболеваемость",
        causes: ['Вирус A', 'Вирус B', 'Инфекция C', 'Другие'],
        years: [2020, 2021, 2022, 2023, 2024],
        data: [
          { year: 2020, cause: 'Вирус A', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 1550 },
          { year: 2020, cause: 'Вирус B', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 1020 },
          { year: 2020, cause: 'Инфекция C', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 540 },
          { year: 2020, cause: 'Другие', annual: 5.25, summer: 12.5, winter: -1.0, tmax: 15.7, tmin: -3.8, cases: 280 },
          { year: 2021, cause: 'Вирус A', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 1480 },
          { year: 2021, cause: 'Вирус B', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 1080 },
          { year: 2021, cause: 'Инфекция C', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 570 },
          { year: 2021, cause: 'Другие', annual: 5.4, summer: 12.7, winter: -0.9, tmax: 15.9, tmin: -3.7, cases: 310 },
          { year: 2022, cause: 'Вирус A', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 1520 },
          { year: 2022, cause: 'Вирус B', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 1150 },
          { year: 2022, cause: 'Инфекция C', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 600 },
          { year: 2022, cause: 'Другие', annual: 5.55, summer: 12.9, winter: -0.8, tmax: 16.1, tmin: -3.6, cases: 340 },
          { year: 2023, cause: 'Вирус A', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 1600 },
          { year: 2023, cause: 'Вирус B', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 1200 },
          { year: 2023, cause: 'Инфекция C', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 630 },
          { year: 2023, cause: 'Другие', annual: 5.7, summer: 13.1, winter: -0.7, tmax: 16.3, tmin: -3.5, cases: 370 },
          { year: 2024, cause: 'Вирус A', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 1680 },
          { year: 2024, cause: 'Вирус B', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 1250 },
          { year: 2024, cause: 'Инфекция C', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 660 },
          { year: 2024, cause: 'Другие', annual: 5.85, summer: 13.3, winter: -0.6, tmax: 16.5, tmin: -3.4, cases: 400 }
        ]
      }
    }
  ],
  "temperature-livingStandard": [
    {
      id: "rel-temp-living-1",
      title: "Взаимосвязь температуры и уровня жизни",
      chartType: "combinedPlotA",
      combinedPlotAData: {
        title: "Взаимосвязь температуры и состава доходов",
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
  "precipitation-healthcare": [],
  "precipitation-economy": [],
  "precipitation-infrastructure": [],
  "wind-healthcare": [],
  "disasters-demography": [],
  "disasters-healthcare": [],
  "disasters-livingStandard": [],
  "disasters-economy": [],
  "disasters-infrastructure": [],
  "ecology-demography": [],
  "ecology-healthcare": [],
  "ecology-livingStandard": [],
};
