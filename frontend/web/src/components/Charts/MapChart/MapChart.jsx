import React, { useRef, useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import { useChartResize } from '../../../hooks/useChartResize';
import { useWindowWidth } from '../../../hooks/useWindowWidth';
import styles from './MapChart.module.scss';

const MAP_NAME = 'AltaiRegion';

const MapChart = ({ geojsonPath, data = [], regionTitle = 'Республика Алтай', unit = 'чел.' }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const windowWidth = useWindowWidth();
  const isMobile = windowWidth < 576;

  const [view, setView] = useState('map');
  const [mapReady, setMapReady] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!geojsonPath) return;
    fetch(geojsonPath)
      .then((res) => res.json())
      .then((geoJson) => {
        echarts.registerMap(MAP_NAME, geoJson);
        setMapReady(true);
      })
      .catch((err) => {
        console.error('[MapChart] Failed to load GeoJSON:', err);
        setMapReady(false);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [geojsonPath]);

  const handleDownload = useCallback(() => {
    const instance = chartRef?.current?.getEchartsInstance?.();
    if (!instance) return;
    const url = instance.getDataURL({
      type: 'png',
      pixelRatio: 2,
      backgroundColor: '#fff'
    });
    const link = document.createElement('a');
    link.href = url;
    link.download = `${view === 'map' ? 'map' : 'bar'}-chart.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, [chartRef, view]);

  const values = data.map((d) => d.value);
  const minVal = values.length ? Math.min(...values) : 500;
  const maxVal = values.length ? Math.max(...values) : 65000;

  const animationCommon = {
    animationDurationUpdate: 1000,
    animationEasingUpdate: 'cubicOut'
  };

  const mapOption = {
    ...animationCommon,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: 'rgba(50, 50, 50, 0.9)',
      borderColor: '#777',
      textStyle: {
        color: '#f0f0f0',
        fontFamily: 'Raleway, sans-serif',
        fontSize: 13
      },
      formatter: (params) => {
        const val = params.value;
        return val != null
          ? `${params.name}: ${val.toLocaleString('ru-RU')} ${unit}`
          : params.name;
      }
    },
    visualMap: {
      min: minVal,
      max: maxVal,
      left: 'right',
      text: ['Высокая', 'Низкая'],
      calculable: true,
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      },
      textStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 12,
        color: '#374151'
      }
    },
    series: [
      {
        id: 'population',
        name: regionTitle,
        type: 'map',
        map: MAP_NAME,
        roam: true,
        label: {
          show: false,
          color: '#F3F4F6',
          textBorderColor: 'rgba(0,0,0,0.85)',
          textBorderWidth: 3,
          fontSize: 10
        },
        emphasis: {
          label: {
            show: true,
            color: '#F3F4F6',
            textBorderColor: 'rgba(0,0,0,0.85)',
            textBorderWidth: 3,
            fontWeight: 'bold',
            fontSize: 12
          },
          itemStyle: {
            areaColor: '#f46d43',
            borderColor: '#333',
            borderWidth: 2
          }
        },
        select: {
          itemStyle: {
            areaColor: '#f46d43'
          },
          label: {
            color: '#F3F4F6',
            textBorderColor: 'rgba(0,0,0,0.85)',
            textBorderWidth: 3,
            fontSize: 10,
          },
        },
        data: data,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  };

  const sorted = [...data].sort((a, b) => a.value - b.value);
  const barOption = {
    ...animationCommon,
    tooltip: {
      trigger: 'axis',
      confine: true,
      axisPointer: { type: 'shadow' },
      formatter: (params) =>
        `${params[0].name}: ${params[0].value.toLocaleString('ru-RU')} ${unit}`
    },

    grid: {
      left: '3%',
      right: isMobile ? '55%' : '5%',
      top: 20,
      bottom: 20,
      containLabel: true
    },

    xAxis: {
      type: 'value',
      axisLabel: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: isMobile ? 10 : 12,
        color: '#374151',
        rotate: isMobile ? 45 : 0
      }
    },

    yAxis: {
      type: 'category',
      data: sorted.map((d) => d.name),
      axisLabel: {
        show: !isMobile,
        margin: 12,
        rotate: 0,
        fontFamily: 'Raleway, sans-serif',
        fontSize: isMobile ? 9 : 11,
        color: '#374151',
        formatter: (value) => {
          if (!isMobile) {
            return value;
          }
          return '';
        }
      }
    },

    series: [
      {
        id: 'population',
        type: 'bar',
        barMaxWidth: 14,
        data: sorted.map((d) => d.value),
        itemStyle: { color: '#366164' },
        emphasis: { itemStyle: { color: '#9FB69F' } },

        label: {
          show: isMobile,
          position: 'right',
          distance: 8,
          formatter: function (params) {
            return params.name;
          },
          fontFamily: 'Raleway, sans-serif',
          fontSize: 11,
          color: '#374151',
          textBorderColor: 'rgba(255,255,255,0.9)',
          textBorderWidth: 2
        },
      }
    ]
  };

  return (
    <div className={styles.mapChart}>
      <div className={styles.header}>
        <span className={styles.regionTitle}>{regionTitle}</span>
        <div className={styles.headerActions}>
          <button
            className={styles.downloadBtn}
            onClick={handleDownload}
            title="Скачать PNG"
            aria-label="Скачать график в формате PNG"
          >
            ↓ PNG
          </button>
          <button
            className={styles.toggleBtn}
            onClick={() => setView((v) => (v === 'map' ? 'bar' : 'map'))}
            aria-pressed={view === 'bar'}
          >
            {view === 'map' ? 'Показать график' : 'Показать карту'}
          </button>
        </div>
      </div>

      {view === 'bar' && (
        <p className={styles.barLabel}>
          Численность районов {regionTitle}
        </p>
      )}

      {loading ? (
        <div className={styles.loadingState}>Загрузка карты…</div>
      ) : view === 'map' && !mapReady ? (
        <div className={styles.loadingState}>Не удалось загрузить карту</div>
      ) : (
        <ReactECharts
          ref={chartRef}
          echarts={echarts}
          option={view === 'map' ? mapOption : barOption}
          notMerge={true}
          lazyUpdate={false}
          style={{
            height: view === 'map' ? '500px' : `${Math.max(300, data.length * 20)}px`,
            width: '100%'
          }}
        />
      )}
    </div>
  );
};

MapChart.propTypes = {
  geojsonPath: PropTypes.string.isRequired,
  data: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      value: PropTypes.number.isRequired
    })
  ),
  regionTitle: PropTypes.string,
  unit: PropTypes.string
};

export default MapChart;
