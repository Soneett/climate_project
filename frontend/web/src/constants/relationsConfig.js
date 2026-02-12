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
      id: "temp-demo-1", 
      title: "Влияние температуры на рождаемость", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Рождаемость на 1000 чел.', data: [10.1, 9.8, 9.6, 9.0, 8.7, 8.5] },
          { name: 'Средняя температура, °C', data: [5.2, 5.8, 6.1, 5.5, 5.9, 6.2] }
        ]
      }
    },
    { 
      id: "temp-demo-2", 
      title: "Температура и миграция населения", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Миграционный прирост', data: [-3000, -3000, -2400, -1600, -400, 600] },
          { name: 'Средняя температура, °C', data: [5.2, 5.8, 6.1, 5.5, 5.9, 6.2] }
        ]
      }
    },
  ],
  "temperature-healthcare": [
    { 
      id: "temp-health-1", 
      title: "Температура и заболеваемость", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Заболеваемость на 1000 чел.', data: [720, 750, 780, 760, 740, 730] },
          { name: 'Средняя температура, °C', data: [5.2, 5.8, 6.1, 5.5, 5.9, 6.2] }
        ]
      }
    },
    { 
      id: "temp-health-2", 
      title: "Влияние на сердечно-сосудистые заболевания", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Смертность от ССЗ на 1000 чел.', data: [45, 46, 47, 46, 45, 44] },
          { name: 'Средняя температура, °C', data: [5.2, 5.8, 6.1, 5.5, 5.9, 6.2] }
        ]
      }
    },
  ],
  "temperature-livingStandard": [
    { 
      id: "temp-living-1", 
      title: "Расходы на отопление", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Расходы на ЖКХ, %', data: [22, 23, 24, 25, 26, 27] },
          { name: 'Средняя температура, °C', data: [5.2, 5.8, 6.1, 5.5, 5.9, 6.2] }
        ]
      }
    },
  ],
  "precipitation-healthcare": [
    { 
      id: "prec-health-1", 
      title: "Осадки и респираторные заболевания", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Заболевания органов дыхания на 1000 чел.', data: [145, 158, 172, 165, 152, 148] },
          { name: 'Осадки, мм', data: [550, 580, 520, 490, 510, 530] }
        ]
      }
    },
  ],
  "precipitation-economy": [
    { 
      id: "prec-econ-1", 
      title: "Влияние осадков на сельское хозяйство", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Урожайность зерновых, ц/га', data: [28, 30, 25, 22, 26, 29] },
          { name: 'Осадки, мм', data: [550, 580, 520, 490, 510, 530] }
        ]
      }
    },
  ],
  "precipitation-infrastructure": [
    { 
      id: "prec-infra-1", 
      title: "Осадки и состояние дорог", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Дороги требующие ремонта, %', data: [35, 38, 42, 40, 38, 36] },
          { name: 'Осадки, мм', data: [550, 580, 520, 490, 510, 530] }
        ]
      }
    },
  ],
  "wind-healthcare": [
    { 
      id: "wind-health-1", 
      title: "Ветер и респираторные заболевания", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Заболевания органов дыхания на 1000 чел.', data: [145, 158, 172, 165, 152, 148] },
          { name: 'Скорость ветра, м/с', data: [3.2, 3.5, 3.8, 3.4, 3.1, 3.3] }
        ]
      }
    },
  ],
  "disasters-demography": [
    { 
      id: "dis-demo-1", 
      title: "Катаклизмы и демография", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Миграционный прирост', data: [-3000, -3000, -2400, -1600, -400, 600] },
          { name: 'Катаклизмы, случаев', data: [5, 7, 4, 3, 2, 1] }
        ]
      }
    },
  ],
  "disasters-healthcare": [
    { 
      id: "dis-health-1", 
      title: "Медицинская нагрузка при катаклизмах", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Обращения в скорую помощь', data: [125000, 138000, 132000, 128000, 122000, 118000] },
          { name: 'Катаклизмы, случаев', data: [5, 7, 4, 3, 2, 1] }
        ]
      }
    },
  ],
  "disasters-livingStandard": [
    { 
      id: "dis-living-1", 
      title: "Влияние на уровень жизни", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Процент населения за чертой бедности', data: [13.2, 13.5, 13.8, 13.1, 12.5, 11.9] },
          { name: 'Катаклизмы, случаев', data: [5, 7, 4, 3, 2, 1] }
        ]
      }
    },
  ],
  "disasters-economy": [
    { 
      id: "dis-econ-1", 
      title: "Экономический ущерб от катаклизмов", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Ущерб, млн руб.', data: [250, 380, 210, 150, 90, 45] },
          { name: 'Катаклизмы, случаев', data: [5, 7, 4, 3, 2, 1] }
        ]
      }
    },
  ],
  "disasters-infrastructure": [
    { 
      id: "dis-infra-1", 
      title: "Повреждения инфраструктуры", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Повреждения инфраструктуры, случаев', data: [45, 68, 42, 32, 18, 12] },
          { name: 'Катаклизмы, случаев', data: [5, 7, 4, 3, 2, 1] }
        ]
      }
    },
  ],
  "ecology-demography": [
    { 
      id: "eco-demo-1", 
      title: "Экология и миграция населения", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Миграционный прирост', data: [-3000, -3000, -2400, -1600, -400, 600] },
          { name: 'Индекс качества воздуха', data: [72, 68, 75, 78, 82, 85] }
        ]
      }
    },
  ],
  "ecology-healthcare": [
    { 
      id: "eco-health-1", 
      title: "Качество воздуха и заболеваемость", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Заболевания органов дыхания на 1000 чел.', data: [145, 158, 172, 165, 152, 148] },
          { name: 'Индекс качества воздуха', data: [72, 68, 75, 78, 82, 85] }
        ]
      }
    },
  ],
  "ecology-livingStandard": [
    { 
      id: "eco-living-1", 
      title: "Экология и качество жизни", 
      chartType: "line",
      chartData: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [
          { name: 'Индекс качества жизни', data: [65, 63, 68, 72, 75, 78] },
          { name: 'Индекс качества воздуха', data: [72, 68, 75, 78, 82, 85] }
        ]
      }
    },
  ],
};
