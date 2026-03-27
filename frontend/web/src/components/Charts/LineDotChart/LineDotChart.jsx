import React, { useRef, useState, useMemo } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './LineDotChart.module.scss';

const LINE_COLORS = ['#5470C6', '#91CC75', '#FAC858', '#EE6666'];
const VISUAL_MAP_COLORS = ['#EE6666', '#FAC858', '#91CC75', '#3BA272'];

const LineDotChart = ({
                        years = [],
                        primaryCategories = [],
                        secondaryOptions = [],
                        data = [],
                        yAxisLabel = 'Значение',
                        xAxisLabel = ''
                      }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const [secondaryKey, setSecondaryKey] = useState(() => secondaryOptions[0]?.key ?? '');
  const [menuOpen, setMenuOpen] = useState(false);
  const [hiddenCategories, setHiddenCategories] = useState([]);

  const toggleCategory = (cat) => {
    setHiddenCategories(prev =>
      prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]
    );
  };

  const currentSecondaryLabel =
    secondaryOptions.find(o => o.key === secondaryKey)?.label ?? secondaryKey;

  const allSecondaryValues = useMemo(
    () => (secondaryKey ? data.map(d => d[secondaryKey]).filter(v => v != null) : []),
    [data, secondaryKey]
  );

  const minSecondary = allSecondaryValues.length ? Math.min(...allSecondaryValues) : 0;
  const maxSecondary = allSecondaryValues.length ? Math.max(...allSecondaryValues) : 100;

  const getYAxisRange = () => {
    const visibleData = data.filter(d => !hiddenCategories.includes(d.category));
    if (!visibleData.length) return { min: 0, max: 100 };

    const values = visibleData.map(d => d.value).filter(v => v != null);
    if (!values.length) return { min: 0, max: 100 };

    const min = Math.min(...values);
    const max = Math.max(...values);
    const padding = (max - min) * 0.1 || Math.max(1, max * 0.05);

    return {
      min: Math.floor(min - padding),
      max: Math.ceil(max + padding)
    };
  };

  const series = primaryCategories.map((cat, idx) => ({
    name: cat,
    type: 'line',
    smooth: false,
    symbol: 'circle',
    symbolSize: 8,
    lineStyle: {
      color: LINE_COLORS[idx % LINE_COLORS.length],
      width: 2,
      opacity: hiddenCategories.includes(cat) ? 0 : 1
    },
    emphasis: { focus: 'series' },
    silent: hiddenCategories.includes(cat),
    data: years
      .map(year => {
        const entry = data.find(d => d.year === year && d.category === cat);
        if (!entry) return null;

        return {
          value: [year, entry.value, entry[secondaryKey] ?? null],
          itemStyle: { opacity: hiddenCategories.includes(cat) ? 0 : 1 }
        };
      })
      .filter(Boolean)
  }));

  const option = {
    backgroundColor: '#ffffff',
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'item',
      formatter: (params) => {
        const [year, value, secondaryVal] = params.data.value;
        return `<b>${params.seriesName}</b><br/>` +
          `Год: ${year}<br/>` +
          `${yAxisLabel}: ${value != null ? value.toLocaleString('ru-RU') : '—'}<br/>` +
          `${currentSecondaryLabel}: ${secondaryVal != null ? secondaryVal : '—'}`;
      }
    },
    legend: { show: false },
    grid: {
      left: '5%',
      right: 70,
      top: 20,
      bottom: 86,
      containLabel: true
    },
    dataZoom: [
      { type: 'slider', xAxisIndex: 0, start: 0, end: 100, bottom: 46, handleSize: '120%' },
      { type: 'inside', xAxisIndex: 0, start: 0, end: 100 }
    ],
    visualMap: {
      show: true,
      dimension: 2,
      min: minSecondary,
      max: maxSecondary,
      orient: 'vertical',
      left: 'right',
      top: 'center',
      height: 220,
      inRange: {
        color: VISUAL_MAP_COLORS,
        symbolSize: [8, 12]
      },
      outOfRange: {
        color: 'transparent',
        symbolSize: 0
      },
      text: [currentSecondaryLabel, ''],
      calculable: true,
      textStyle: {
        ...TEXT_STYLES.axis,
        overflow: 'break',
        width: 120
      }
    },
    xAxis: {
      type: 'category',
      data: years,
      name: xAxisLabel,
      nameLocation: 'middle',
      nameGap: 30,
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
      scale: true,
      ...getYAxisRange(),
      axisLine: AXIS_LINE_STYLE,
      splitLine: SPLIT_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      nameTextStyle: TEXT_STYLES.axis
    },
    series
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="line-dot-chart" className={styles.lineDotChart}>
      <div className={styles.controls}>
        <div className={styles.selector}>
          <button
            className={styles.selectorBtn}
            onClick={() => setMenuOpen(o => !o)}
            aria-haspopup="menu"
            aria-expanded={menuOpen}
            type="button"
          >
            {currentSecondaryLabel} ▾
          </button>

          {menuOpen && (
            <ul className={styles.selectorMenu} role="menu">
              {secondaryOptions.map(o => (
                <li
                  key={o.key}
                  className={`${styles.selectorMenuItem} ${secondaryKey === o.key ? styles.selectorMenuItemActive : ''}`}
                  onClick={() => { setSecondaryKey(o.key); setMenuOpen(false); }}
                  role="menuitem"
                >
                  {o.label}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <ReactECharts
        ref={chartRef}
        option={option}
        notMerge
        lazyUpdate={false}
        style={{ height: '100%', width: '100%', minHeight: '420px' }}
      />

      <div className={styles.legend}>
        {primaryCategories.map((cat, idx) => (
          <button
            key={cat}
            className={`${styles.legendItem} ${hiddenCategories.includes(cat) ? styles.legendItemHidden : ''}`}
            onClick={() => toggleCategory(cat)}
            type="button"
          >
            <span
              className={styles.legendDot}
              style={{ backgroundColor: LINE_COLORS[idx % LINE_COLORS.length] }}
            />
            {cat}
          </button>
        ))}
      </div>
    </ChartWrapper>
  );
};

LineDotChart.propTypes = {
  title: PropTypes.string,
  years: PropTypes.arrayOf(PropTypes.string),
  primaryCategories: PropTypes.arrayOf(PropTypes.string),
  secondaryOptions: PropTypes.arrayOf(PropTypes.shape({
    key: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired
  })),
  data: PropTypes.arrayOf(PropTypes.shape({
    year: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    value: PropTypes.number.isRequired
  })),
  yAxisLabel: PropTypes.string,
  xAxisLabel: PropTypes.string
};

export default LineDotChart;