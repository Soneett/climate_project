import React, { useState, useRef, useEffect, useCallback } from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import PropTypes from 'prop-types';
import styles from './ColorMarkerMap.module.scss';

const DISASTER_SYMBOLS = {
  fire: { symbol: 'circle', color: '#d73027', name: 'Пожар' },
  frost: { symbol: 'rect', color: '#74add1', name: 'Заморозки' },
};

const YEARS = [2020, 2021, 2022, 2023, 2024];

function computeCentroid(feature) {
  const geometry = feature?.geometry;
  if (!geometry) return null;

  let allCoords = [];
  if (geometry.type === 'Polygon') {
    allCoords = geometry.coordinates[0] || [];
  } else if (geometry.type === 'MultiPolygon') {
    geometry.coordinates.forEach((poly) => {
      allCoords = allCoords.concat(poly[0] || []);
    });
  }

  if (!allCoords.length) return null;

  const lng = allCoords.reduce((s, c) => s + c[0], 0) / allCoords.length;
  const lat = allCoords.reduce((s, c) => s + c[1], 0) / allCoords.length;
  return [lng, lat];
}

const MAP_REGISTER_PREFIX = 'ColorMarkerMap_';

const ColorMarkerMap = ({
                          geojson: geojsonProp,
                          geojsonPath,
                          indicatorOptions,
                          dataByYear,
                          regionTitle = 'Регион',
                        }) => {
  const chartRef = useRef(null);
  const mapName = `${MAP_REGISTER_PREFIX}${regionTitle}`;

  const [geojson, setGeojson] = useState(geojsonProp || null);
  const [mapReady, setMapReady] = useState(false);
  const [loading, setLoading] = useState(!geojsonProp && !!geojsonPath);

  const [selectedYear, setSelectedYear] = useState(YEARS[YEARS.length - 1]);
  const [selectedIndicator, setSelectedIndicator] = useState(
    indicatorOptions?.[0]?.key || ''
  );
  const [visibleDisasters, setVisibleDisasters] = useState({
    fire: true,
    frost: true,
  });
  const [selectedDisaster, setSelectedDisaster] = useState(null);

  useEffect(() => {
    if (geojsonProp) {
      setGeojson(geojsonProp);
    } else if (geojsonPath) {
      setLoading(true);
      fetch(geojsonPath)
        .then((res) => res.json())
        .then((data) => {
          setGeojson(data);
        })
        .catch((err) => {
          console.error('[ColorMarkerMap] Failed to load GeoJSON:', err);
        })
        .finally(() => setLoading(false));
    }
  }, [geojsonProp, geojsonPath]);

  useEffect(() => {
    if (geojson && !mapReady) {
      echarts.registerMap(mapName, geojson);
      setMapReady(true);
    }
  }, [geojson, mapName, mapReady]);

  const toggleDisaster = useCallback((type) => {
    setVisibleDisasters((prev) => ({ ...prev, [type]: !prev[type] }));
  }, []);

  const currentData = dataByYear[selectedYear] || [];

  const mapData = currentData.map((item) => ({
    name: item.name,
    value: item[selectedIndicator] ?? null,
    ...item,
  }));

  const markerData = currentData
    .filter((item) => item.marker && visibleDisasters[item.marker.type])
    .map((item) => {
      const feature = geojson?.features?.find(
        (f) =>
          f.properties?.name === item.name ||
          f.properties?.NAME === item.name ||
          f.properties?.NAME_1 === item.name
      );
      const coords = feature?.properties?.center || computeCentroid(feature) || [0, 0];

      const disasterInfo = DISASTER_SYMBOLS[item.marker.type] || DISASTER_SYMBOLS.fire;
      return {
        name: item.name,
        value: coords,
        marker: item.marker,
        itemStyle: { color: disasterInfo.color },
        symbol: disasterInfo.symbol,
        symbolSize: 15,
      };
    });

  const values = mapData
    .map((d) => d.value)
    .filter((v) => v != null && Number.isFinite(Number(v)));
  const minValue = values.length ? Math.min(...values) : 0;
  const maxValue = values.length ? Math.max(...values) : 100;

  const indicatorLabel =
    indicatorOptions?.find((o) => o.key === selectedIndicator)?.label || selectedIndicator;

  const option = {
    title: {
      subtext: `${regionTitle} — ${selectedYear}`,
      left: 'center',
      textStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 16,
        color: '#111827',
      },
      subtextStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 12,
        color: '#374151',
      },
    },
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(50, 50, 50, 0.9)',
      borderColor: '#777',
      textStyle: {
        color: '#f0f0f0',
        fontFamily: 'Raleway, sans-serif',
        fontSize: 13,
      },
      formatter: (params) => {
        if (params.seriesType === 'map') {
          const val = params.value;
          return val != null
            ? `<b>${params.name}</b><br/>Год: ${selectedYear}<br/>${indicatorLabel}: ${Number(val).toLocaleString('ru-RU')}`
            : `<b>${params.name}</b><br/>Год: ${selectedYear}<br/>${indicatorLabel}: Н/Д`;
        }
        return '';
      },
    },
    visualMap: {
      left: 'right',
      min: minValue,
      max: maxValue,
      inRange: {
        color: [
          '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8',
          '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026',
        ],
      },
      text: ['Высокий', 'Низкий'],
      calculable: true,
      textStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 12,
        color: '#374151',
      },
    },
    geo: {
      map: mapName,
      roam: true,
      silent: false,
      itemStyle: {
        borderColor: '#333',
        borderWidth: 0.5,
        areaColor: '#eee',
      },
    },
    series: [
      {
        name: indicatorLabel,
        type: 'map',
        map: mapName,
        roam: true,
        geoIndex: 0,
        tooltip: { show: true },
        label: {
          show: false,
          color: '#ffffff',
          textBorderColor: 'rgba(0,0,0,0.9)',
          textBorderWidth: 3,
          fontSize: 10,
        },
        itemStyle: {
          borderColor: '#333',
          borderWidth: 0.8,
        },
        emphasis: {
          label: {
            show: true,
            color: '#ffffff',
            textBorderColor: 'rgba(0,0,0,0.9)',
            textBorderWidth: 3,
            fontWeight: 'bold',
            fontSize: 12,
          },
          itemStyle: {
            areaColor: '#f46d43',
            borderColor: '#333',
            borderWidth: 2,
          },
        },
        select: {
          disabled: true,
          itemStyle: {
            areaColor: '#f46d43',
          },
          label: {
            color: '#ffffff',
            textBorderColor: 'rgba(0,0,0,0.9)',
            textBorderWidth: 3,
            fontSize: 10,
          },
        },
        data: mapData,
      },
      {
        name: 'Катаклизмы',
        type: 'scatter',
        coordinateSystem: 'geo',
        data: markerData,
        symbolSize: 15,
        label: { show: false },
        zlevel: 5,
        tooltip: { show: false },
      },
    ],
  };

  const onEvents = {
    click: (params) => {
      if (params.seriesType === 'scatter' && params.data?.marker) {
        setSelectedDisaster({
          district: params.name,
          ...params.data.marker,
        });
      }
    },
  };

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <div className={styles.indicatorSelector}>
          <label htmlFor="indicator-select">Показатель:</label>
          <select
            id="indicator-select"
            value={selectedIndicator}
            onChange={(e) => setSelectedIndicator(e.target.value)}
          >
            {indicatorOptions?.map((opt) => (
              <option key={opt.key} value={opt.key}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.disasterFilter}>
          <span className={styles.filterLabel}>Катаклизмы:</span>
          {Object.entries(DISASTER_SYMBOLS).map(([type, info]) => (
            <label key={type} className={styles.checkbox}>
              <input
                type="checkbox"
                checked={visibleDisasters[type]}
                onChange={() => toggleDisaster(type)}
              />
              <span style={{ color: info.color }}>{info.name}</span>
            </label>
          ))}
        </div>
      </div>

      {loading && <div className={styles.loadingState}>Загрузка карты…</div>}
      {!loading && !mapReady && <div className={styles.loadingState}>Не удалось загрузить карту</div>}

      {mapReady && (
        <ReactECharts
          ref={chartRef}
          echarts={echarts}
          option={option}
          notMerge
          style={{ height: '500px', width: '100%' }}
          opts={{ renderer: 'canvas' }}
          onEvents={onEvents}
        />
      )}

      <div className={styles.timeline}>
        <label htmlFor="year-slider">
          Год: <strong>{selectedYear}</strong>
        </label>
        <input
          id="year-slider"
          type="range"
          min={YEARS[0]}
          max={YEARS[YEARS.length - 1]}
          value={selectedYear}
          onChange={(e) => setSelectedYear(Number(e.target.value))}
          className={styles.slider}
        />
        <div className={styles.yearLabels}>
          {YEARS.map((year) => (
            <span
              key={year}
              className={year === selectedYear ? styles.active : ''}
              onClick={() => setSelectedYear(year)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') setSelectedYear(year);
              }}
            >
              {year}
            </span>
          ))}
        </div>
      </div>

      {selectedDisaster && (
        <div className={styles.modal} onClick={() => setSelectedDisaster(null)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <button
              className={styles.closeBtn}
              onClick={() => setSelectedDisaster(null)}
              type="button"
              aria-label="Закрыть"
            >
              ×
            </button>
            <h3>Информация о катаклизме</h3>
            <p><strong>Район:</strong> {selectedDisaster.district}</p>
            <p>
              <strong>Тип:</strong>{' '}
              {selectedDisaster.type === 'fire' ? 'Пожар' : 'Заморозки'}
            </p>
            {selectedDisaster.date && <p><strong>Дата:</strong> {selectedDisaster.date}</p>}
            {selectedDisaster.description && (
              <p><strong>Описание:</strong> {selectedDisaster.description}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

ColorMarkerMap.propTypes = {
  geojson: PropTypes.object,
  geojsonPath: PropTypes.string,
  indicatorOptions: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
    })
  ).isRequired,
  dataByYear: PropTypes.shape({
    2020: PropTypes.array,
    2021: PropTypes.array,
    2022: PropTypes.array,
    2023: PropTypes.array,
    2024: PropTypes.array,
  }).isRequired,
  regionTitle: PropTypes.string,
  title: PropTypes.string,
};

export default ColorMarkerMap;
