import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import { useWindowWidth } from '../../../hooks/useWindowWidth';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  AXIS_LINE_STYLE
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './CombinedPlotA.module.scss';

const DEFAULT_Y2_OPTIONS = [
  { key: 'annual', label: 'Среднегодовая температура' },
  { key: 'summer', label: 'Средняя температура лета' },
  { key: 'winter', label: 'Средняя температура зимы' },
  { key: 'tmax', label: 'Максимальная зарегистрированная температура' },
  { key: 'tmin', label: 'Минимальная зарегистрированная температура' }
];

const DEFAULT_Y1_SERIES = [
  { key: 'income', name: 'Доходы', color: '#26af55' },
  { key: 'expense', name: 'Расходы', color: '#e54e1b' }
];

const TEMP_COLOR = '#5470C6';

const CombinedPlotA = ({
  data = [],
  yAxis1Series = DEFAULT_Y1_SERIES,
  yAxis1Label = 'Финансовые показатели (млн)',
  yAxis2Options = DEFAULT_Y2_OPTIONS
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const windowWidth = useWindowWidth();
  const isMobile = windowWidth < 576;

  const [tempType, setTempType] = useState(() => yAxis2Options[0]?.key || 'annual');
  const [hiddenSeries, setHiddenSeries] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const currentTempLabel = yAxis2Options.find(t => t.key === tempType)?.label || tempType;

  const toggleSeries = (name) => {
    setHiddenSeries(prev =>
      prev.includes(name) ? prev.filter(s => s !== name) : [...prev, name]
    );
  };

  const seriesDefs = [
    ...yAxis1Series.map(s => ({ name: s.name, color: s.color })),
    { name: 'Температура', label: currentTempLabel, color: TEMP_COLOR }
  ];

  const option = {
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const year = params[0]?.axisValue;
        let html = `<b>${year}</b><br/>`;
        params.forEach(p => {
          html += `${p.marker} ${p.seriesName}: ${p.value}<br/>`;
        });
        return html;
      }
    },
    legend: {
      show: false,
      selectedMode: 'multiple',
      selected: Object.fromEntries(seriesDefs.map(s => [s.name, !hiddenSeries.includes(s.name)]))
    },
    grid: {
      left: '5%',
      right: '5%',
      top: 80,
      bottom: 100
    },
    dataZoom: [
      { type: 'slider', xAxisIndex: 0, start: 0, end: 100, bottom: 40, handleSize: '120%' },
      { type: 'inside', xAxisIndex: 0, start: 0, end: 100 }
    ],
    xAxis: {
      type: 'category',
      data: data.map(d => d.year),
      axisLine: AXIS_LINE_STYLE,
      axisLabel: { ...TEXT_STYLES.axis, fontSize: isMobile ? 10 : 12, rotate: isMobile ? 45 : 0 }
    },
    yAxis: [
      {
        type: 'value',
        name: yAxis1Label,
        nameLocation: 'middle',
        nameGap: 50,
        position: 'left',
        axisLine: { show: true, lineStyle: { color: yAxis1Series[0]?.color || '#26af55' } },
        splitLine: { lineStyle: { type: 'dashed' } },
        axisLabel: TEXT_STYLES.axis,
        nameTextStyle: TEXT_STYLES.axis
      },
      {
        type: 'value',
        name: `${currentTempLabel} (°C)`,
        nameLocation: 'middle',
        nameGap: 60,
        position: 'right',
        axisLine: { show: true, lineStyle: { color: TEMP_COLOR } },
        splitLine: { show: false },
        axisLabel: { ...TEXT_STYLES.axis, color: TEMP_COLOR },
        nameTextStyle: { ...TEXT_STYLES.axis, color: TEMP_COLOR }
      }
    ],
    series: [
      ...yAxis1Series.map((s) => ({
        name: s.name,
        type: 'bar',
        yAxisIndex: 0,
        barGap: 0,
        barWidth: `${Math.floor(30 / Math.max(1, yAxis1Series.length))}%`,
        itemStyle: { color: s.color },
        emphasis: { itemStyle: { borderWidth: 1.5 } },
        data: data.map(d => d[s.key])
      })),
      {
        name: 'Температура',
        type: 'line',
        yAxisIndex: 1,
        smooth: true,
        lineStyle: { color: TEMP_COLOR, width: 3 },
        itemStyle: { color: TEMP_COLOR },
        symbol: 'circle',
        symbolSize: 10,
        emphasis: { focus: 'series' },
        data: data.map(d => d[tempType])
      }
    ]
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="combined-plot-a" className={styles.combinedPlotA}>
      <div className={styles.controls}>
        <div className={styles.tempSelector}>
          <button
            className={styles.tempBtn}
            onClick={() => setMenuOpen(o => !o)}
          >
            {currentTempLabel} ▾
          </button>
          {menuOpen && (
            <ul className={styles.tempMenu}>
              {yAxis2Options.map(t => (
                <li
                  key={t.key}
                  className={`${styles.tempMenuItem} ${tempType === t.key ? styles.tempMenuItemActive : ''}`}
                  onClick={() => { setTempType(t.key); setMenuOpen(false); }}
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
        style={{ height: '100%', width: '100%', minHeight: '480px' }}
      />

      <div className={styles.legend}>
        {seriesDefs.map(s => (
          <button
            key={s.name}
            className={`${styles.legendItem} ${hiddenSeries.includes(s.name) ? styles.legendItemHidden : ''}`}
            onClick={() => toggleSeries(s.name)}
          >
            <span className={styles.legendSwatch} style={{ backgroundColor: s.color }} />
            {s.label || s.name}
          </button>
        ))}
      </div>
    </ChartWrapper>
  );
};

CombinedPlotA.propTypes = {
  title: PropTypes.string,
  data: PropTypes.arrayOf(PropTypes.object),
  yAxis1Series: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      color: PropTypes.string.isRequired
    })
  ),
  yAxis1Label: PropTypes.string,
  yAxis2Options: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired
    })
  )
};

export default CombinedPlotA;
