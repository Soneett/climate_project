export const MOCK_USERS = [
  {
    id: 1,
    name: "Андрей Администратов",
    email: "admin",
    role: "admin",
    password: "123",
  },
  {
    id: 2,
    name: "Мария Редакторова",
    email: "editor",
    role: "editor",
    password: "123",
  },
];

export const INFO_STATS = {
  totalIndicators: 63,
  socialAspects: 20,
  regionalData: 8,
  climate: 31,
  governanceAndPolitics: 4,
  periodStart: "2020 год",
  periodEnd: "2024 год",
  lastUpdate: "01.01.2026",
};

export const DB_TABLES = [
  {
    key: "regions",
    labelEn: "Regions",
    labelRu: "регионы",
    columns: ["id", "name", "code", "type", "parent_id"],
    description:
      "Хранит информацию о регионах России. Используется во всех таблицах, где данные привязаны к региону.",
  },
  {
    key: "units",
    labelEn: "Units",
    labelRu: "единицы измерения",
    columns: ["id", "code", "name"],
    description: "Справочник единиц измерения. Используется в indicators для указания единицы измерения.",
  },
  {
    key: "indicator_subtypes",
    labelEn: "Indicator subtypes",
    labelRu: "подтипы показателей",
    columns: ["id", "name"],
    description:
      "Справочник для уточняющей классификации показателей. Используется в indicators для детализации.",
  },
  {
    key: "indicators",
    labelEn: "Indicators",
    labelRu: "показатели",
    columns: ["id", "name", "unit_id", "type", "theme", "subtype_id"],
    description: "Справочник всех показателей. Используется в indicator_values.",
  },
  {
    key: "data_sources",
    labelEn: "Data sources",
    labelRu: "источники данных",
    columns: ["id", "name", "url", "organization", "date_collected"],
    description:
      "Справочник источников. Используется в indicator_values и population_age_sex.",
  },
  {
    key: "indicator_values",
    labelEn: "Indicators values",
    labelRu: "значения показателей",
    columns: ["id", "indicator_id", "region_id", "year", "value", "source_id"],
    description:
      "Хранит числовые значения показателей по регионам и годам. Привязывает показатель к региону, году и источнику.",
  },
  {
    key: "population_age_sex",
    labelEn: "Population, age, sex",
    labelRu: "население по возрасту и полу",
    columns: ["id", "region_id", "year", "age_code", "sex_code", "value", "source_id"],
    description:
      "Хранит демографическую пирамиду. Содержит возрастно-половую структуру населения.",
  },
  {
    key: "regional_programs",
    labelEn: "Regional programs",
    labelRu: "региональные программы",
    columns: ["id", "name", "level", "start_year", "end_year", "description", "status", "budget_total"],
    description:
      "Содержит сведения о программах. Через program_regions можно связать с регионами.",
  },
  {
    key: "program_regions",
    labelEn: "Program regions",
    labelRu: "связь программ и регионов",
    columns: ["id", "program_id", "region_id"],
    description:
      "Реализует связь многие-ко-многим между программами и регионами.",
  },
  {
    key: "events",
    labelEn: "Events",
    labelRu: "события",
    columns: ["id", "region_id", "date", "type", "severity", "description", "economic_loss"],
    description:
      "Хранит информацию о природных и чрезвычайных происшествиях.",
  },
];

export const TABLE_PREVIEW_ROWS = {
  regions: [
    { id: 1, name: "Москва", code: "77", type: "город федерального значения", parent_id: null },
    { id: 2, name: "Санкт-Петербург", code: "78", type: "город федерального значения", parent_id: null },
    { id: 3, name: "Московская область", code: "50", type: "область", parent_id: null },
  ],
  units: [
    { id: 1, code: "чел.", name: "человек" },
    { id: 2, code: "руб.", name: "рубль" },
    { id: 3, code: "%", name: "процент" },
  ],
  indicator_subtypes: [
    { id: 1, name: "демографический" },
    { id: 2, name: "экономический" },
    { id: 3, name: "социальный" },
  ],
  indicators: [
    { id: 1, name: "Численность населения", unit_id: 1, type: "социальный", theme: "демография", subtype_id: 1 },
    { id: 2, name: "ВРП на душу населения", unit_id: 2, type: "экономический", theme: "экономика", subtype_id: 2 },
    { id: 3, name: "Уровень безработицы", unit_id: 3, type: "социальный", theme: "труд", subtype_id: 3 },
  ],
  data_sources: [
    { id: 1, name: "Росстат", url: "https://rosstat.gov.ru", organization: "Росстат", date_collected: "2024-01-01" },
    { id: 2, name: "МЧС России", url: "https://mchs.gov.ru", organization: "МЧС", date_collected: "2024-01-01" },
    { id: 3, name: "Минэкономразвития", url: "https://economy.gov.ru", organization: "МЭР", date_collected: "2024-01-01" },
  ],
  indicator_values: [
    { id: 1, indicator_id: 1, region_id: 1, year: 2023, value: 12692466, source_id: 1 },
    { id: 2, indicator_id: 1, region_id: 2, year: 2023, value: 5597763, source_id: 1 },
    { id: 3, indicator_id: 2, region_id: 1, year: 2022, value: 1850000, source_id: 1 },
  ],
  population_age_sex: [
    { id: 1, region_id: 1, year: 2023, age_code: "0-4", sex_code: "M", value: 380000, source_id: 1 },
    { id: 2, region_id: 1, year: 2023, age_code: "0-4", sex_code: "F", value: 360000, source_id: 1 },
    { id: 3, region_id: 1, year: 2023, age_code: "5-9", sex_code: "M", value: 395000, source_id: 1 },
  ],
  regional_programs: [
    { id: 1, name: "Безопасные и качественные дороги", level: "федеральный", start_year: 2019, end_year: 2030, description: "Программа развития дорог", status: "активная", budget_total: 4700000000 },
    { id: 2, name: "Демография", level: "национальный", start_year: 2019, end_year: 2030, description: "Нацпроект демография", status: "активная", budget_total: 3560000000 },
    { id: 3, name: "Образование", level: "национальный", start_year: 2019, end_year: 2030, description: "Нацпроект образование", status: "активная", budget_total: 784500000 },
  ],
  program_regions: [
    { id: 1, program_id: 1, region_id: 1 },
    { id: 2, program_id: 1, region_id: 2 },
    { id: 3, program_id: 2, region_id: 1 },
  ],
  events: [
    { id: 1, region_id: 1, date: "2023-07-15", type: "наводнение", severity: "средняя", description: "Подтопление жилых домов", economic_loss: 15000000 },
    { id: 2, region_id: 3, date: "2023-08-03", type: "лесной пожар", severity: "высокая", description: "Пожар в Подмосковье", economic_loss: 45000000 },
    { id: 3, region_id: 2, date: "2023-11-20", type: "снегопад", severity: "низкая", description: "Обильные снегопады", economic_loss: 5000000 },
  ],
};

export const MOCK_HISTORY = [
  {
    id: 1,
    target: "regions",
    targetRu: "регионы",
    userEmail: "admin@example.com",
    date: "19.03.2026",
    action: "Добавлена новая запись",
  },
  {
    id: 2,
    target: "indicator_values",
    targetRu: "значения показателей",
    userEmail: "editor@example.com",
    date: "18.03.2026",
    action: "Загружены данные",
  },
  {
    id: 3,
    target: "График: Численность населения",
    targetRu: "График: Численность населения",
    userEmail: "editor@example.com",
    date: "17.03.2026",
    action: "Обновлён файл данных",
  },
  {
    id: 4,
    target: "units",
    targetRu: "единицы измерения",
    userEmail: "admin@example.com",
    date: "15.03.2026",
    action: "Изменена запись",
  },
];
