import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  AXIS_LINE_STYLE
} from '../chartConfig';
import styles from './CombinedPlotA.module.scss';

const TEMP_TYPES = [
  { key: 'annual', label: 'Среднегодовая' },
  { key: 'summer', label: 'Средняя температура лета' },
  { key: 'winter', label: 'Средняя температура зимы' },
  { key: 'tmax', label: 'Максимальная' },
  { key: 'tmin', label: 'Минимальная' }
];

const INCOME_COLOR = '#26af55';
const EXPENSE_COLOR = '#e54e1b';
const TEMP_COLOR = '#5470C6';

const CombinedPlotA = ({
  title = 'Взаимосвязь температуры и уровня жизни',
  data = []
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const [tempType, setTempType] = useState('annual');
  const [hiddenSeries, setHiddenSeries] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const currentTempLabel = TEMP_TYPES.find(t => t.key === tempType)?.label || tempType;

  const toggleSeries = (name) => {
    setHiddenSeries(prev =>
      prev.includes(name) ? prev.filter(s => s !== name) : [...prev, name]
    );
  };

  const seriesDefs = [
    { name: 'Доходы', color: INCOME_COLOR },
    { name: 'Расходы', color: EXPENSE_COLOR },
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
      left: 80,
      right: 80,
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
      axisLabel: TEXT_STYLES.axis
    },
    yAxis: [
      {
        type: 'value',
        name: 'Финансовые показатели (млн)',
        nameLocation: 'middle',
        nameGap: 50,
        position: 'left',
        axisLine: { show: true, lineStyle: { color: INCOME_COLOR } },
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
      {
        name: 'Доходы',
        type: 'bar',
        yAxisIndex: 0,
        barGap: 0,
        barWidth: '30%',
        itemStyle: { color: INCOME_COLOR },
        emphasis: { itemStyle: { borderColor: '#145c32', borderWidth: 1.5 } },
        data: data.map(d => d.income)
      },
      {
        name: 'Расходы',
        type: 'bar',
        yAxisIndex: 0,
        barWidth: '30%',
        itemStyle: { color: EXPENSE_COLOR },
        emphasis: { itemStyle: { borderColor: '#7a1f1f', borderWidth: 1.5 } },
        data: data.map(d => d.expense)
      },
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
    <div className={styles.combinedPlotA}>
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
              {TEMP_TYPES.map(t => (
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
    </div>
  );
};

CombinedPlotA.propTypes = {
  title: PropTypes.string,
  data: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.string.isRequired,
      income: PropTypes.number.isRequired,
      expense: PropTypes.number.isRequired,
      annual: PropTypes.number,
      summer: PropTypes.number,
      winter: PropTypes.number,
      tmax: PropTypes.number,
      tmin: PropTypes.number
    })
  )
};

export default CombinedPlotA;
