import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE
} from '../chartConfig';
import styles from './ScatterPlot.module.scss';

const CATEGORY_COLORS = ['#26af55', '#769a76', '#e54e1b', '#2684d7'];

const ScatterPlot = ({
  title = 'Взаимосвязь температуры и демографии',
  categories = [],
  years = [],
  data = [],
  xAxisOptions = [],
  yAxisLabel = 'Значение'
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const [xType, setXType] = useState(() => xAxisOptions[0]?.key || 'annual');
  const [selectedYear, setSelectedYear] = useState(null);
  const [hiddenCategories, setHiddenCategories] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const currentXLabel = xAxisOptions.find(t => t.key === xType)?.label || xType;

  const toggleCategory = (cat) => {
    setHiddenCategories(prev =>
      prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]
    );
  };

  const buildSeries = () =>
    categories.map((cat, idx) => ({
      name: cat,
      type: 'scatter',
      symbolSize: (val) => {
        const year = Array.isArray(val) ? val[2] : val.value[2];
        if (selectedYear !== null && year === selectedYear) return 14;
        if (selectedYear !== null) return 7;
        return 10;
      },
      itemStyle: {
        color: CATEGORY_COLORS[idx % CATEGORY_COLORS.length]
      },
      data: data
        .filter(d => d.category === cat)
        .map(d => ({
          value: [d[xType], d.value, d.year],
          itemStyle: {
            opacity: selectedYear !== null && d.year !== selectedYear ? 0.35 : 1
          }
        })),
      emphasis: { focus: 'series' }
    }));

  const option = {
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'item',
      formatter: (params) => {
        const [xVal, value, year] = params.data.value;
        return `
          <b>${params.seriesName}</b><br/>
          Год: ${year}<br/>
          ${currentXLabel}: ${xVal}<br/>
          ${yAxisLabel}: ${value.toLocaleString('ru-RU')}
        `;
      }
    },
    legend: {
      show: false,
      selectedMode: 'multiple',
      selected: Object.fromEntries(categories.map(cat => [cat, !hiddenCategories.includes(cat)]))
    },
    grid: {
      left: 60,
      right: 60,
      bottom: 20,
      top: 25,
      containLabel: true
    },
    xAxis: {
      type: 'value',
      scale: true,
      name: `${currentXLabel}`,
      nameLocation: 'middle',
      nameGap: 25,
      axisLine: AXIS_LINE_STYLE,
      splitLine: SPLIT_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      nameTextStyle: TEXT_STYLES.axis
    },
    yAxis: {
      type: 'value',
      name: yAxisLabel,
      nameLocation: 'middle',
      nameGap: 60,
      axisLine: AXIS_LINE_STYLE,
      splitLine: SPLIT_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      nameTextStyle: TEXT_STYLES.axis
    },
    series: buildSeries()
  };

  return (
    <div className={styles.scatterPlot}>
      <div className={styles.controls}>
        <div className={styles.yearFilter}>
          <span className={styles.filterLabel}>Год:</span>
          <button
            className={`${styles.yearBtn} ${selectedYear === null ? styles.yearBtnActive : ''}`}
            onClick={() => setSelectedYear(null)}
          >
            Все
          </button>
          {years.map(y => (
            <button
              key={y}
              className={`${styles.yearBtn} ${selectedYear === y ? styles.yearBtnActive : ''}`}
              onClick={() => setSelectedYear(selectedYear === y ? null : y)}
            >
              {y}
            </button>
          ))}
        </div>

        <div className={styles.tempSelector}>
          <button
            className={styles.tempBtn}
            onClick={() => setMenuOpen(o => !o)}
          >
            {currentXLabel} ▾
          </button>
          {menuOpen && (
            <ul className={styles.tempMenu}>
              {xAxisOptions.map(t => (
                <li
                  key={t.key}
                  className={`${styles.tempMenuItem} ${xType === t.key ? styles.tempMenuItemActive : ''}`}
                  onClick={() => { setXType(t.key); setMenuOpen(false); }}
                >
                  {t.label}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '500px' }}
      />

      <div className={styles.legend}>
        {categories.map((cat, idx) => (
          <button
            key={cat}
            className={`${styles.legendItem} ${hiddenCategories.includes(cat) ? styles.legendItemHidden : ''}`}
            onClick={() => toggleCategory(cat)}
          >
            <span
              className={styles.legendDot}
              style={{ backgroundColor: CATEGORY_COLORS[idx % CATEGORY_COLORS.length] }}
            />
            {cat}
          </button>
        ))}
      </div>
    </div>
  );
};

ScatterPlot.propTypes = {
  title: PropTypes.string,
  categories: PropTypes.arrayOf(PropTypes.string),
  years: PropTypes.arrayOf(PropTypes.number),
  data: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number.isRequired,
      category: PropTypes.string.isRequired,
      value: PropTypes.number.isRequired
    })
  ),
  xAxisOptions: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired
    })
  ),
  yAxisLabel: PropTypes.string
};

export default ScatterPlot;
