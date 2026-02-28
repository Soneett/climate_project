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
import styles from './CombinedPlotC.module.scss';

const DAMAGE_COLORS = ['#ff7e8a', '#ff5757', '#fa2929', '#ff0400', '#F44336', '#E53935', '#D32F2F'];

const DEFAULT_MODES = [
  { key: 'relative', label: '% от ВРП' },
  { key: 'absolute', label: 'млрд руб.' }
];

const CombinedPlotC = ({
  title = 'Доля ущерба от катаклизмов в ВРП',
  data = [],
  yAxisLabel = 'Доля ущерба в ВРП (%)',
  legendLabel = 'Доля ущерба в ВРП',
  modes = DEFAULT_MODES,
  tooltipFormatter = null
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const [mode, setMode] = useState(() => modes[0]?.key ?? 'relative');

  const dataset = data.map(r => {
    const share = r.gdp && r.gdp !== 0 ? (r.damage / r.gdp * 100) : 0;
    return [r.year, +share.toFixed(2), +r.gdp.toFixed(2), +r.damage.toFixed(2)];
  });

  const isRelative = mode === (modes[0]?.key ?? 'relative');
  const yIndex = isRelative ? 1 : 3;
  const yName = isRelative ? yAxisLabel : (modes[1]?.label ?? 'Ущерб (млрд руб.)');
  const currentLegend = isRelative ? legendLabel : (modes[1]?.label ?? 'Ущерб (млрд руб.)');
  const currentModeLabel = isRelative ? (modes[0]?.label ?? '% от ВРП') : (modes[1]?.label ?? 'млрд руб.');
  const visualMapDimension = isRelative ? 1 : 3;

  const getVisualMapRange = () => {
    if (dataset.length === 0) return { min: 0, max: 100 };
    const values = dataset.map(r => r[yIndex]).filter(v => v != null);
    if (values.length === 0) return { min: 0, max: 100 };
    const dataMin = Math.min(...values);
    const dataMax = Math.max(...values);
    const range = dataMax - dataMin;
    const step = range > 10 ? 5 : (range > 1 ? 1 : 0.5);
    return {
      min: Math.floor(dataMin / step) * step,
      max: Math.ceil(dataMax / step) * step
    };
  };

  const option = {
    backgroundColor: '#ffffff',
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'item',
      formatter: tooltipFormatter || ((params) => {
        const v = params.value || [];
        const year = v[0] || params.name || '';
        const share = v[1] != null ? v[1] + ' %' : '—';
        const gdp = v[2] != null ? v[2] + ' млрд руб.' : '—';
        const damage = v[3] != null ? v[3] + ' млрд руб.' : '—';
        return `<b>${year}</b><br/>` +
          `Доля ущерба: ${share}<br/>` +
          `ВРП: ${gdp}<br/>` +
          `Ущерб: ${damage}`;
      })
    },
    legend: {
      show: false
    },
    grid: {
      left: 80,
      right: 80,
      top: 20,
      bottom: 100
    },
    dataZoom: [
      { type: 'slider', xAxisIndex: 0, start: 0, end: 100, bottom: 40, handleSize: '120%' },
      { type: 'inside', xAxisIndex: 0, start: 0, end: 100 }
    ],
    visualMap: {
      show: true,
      left: 'right',
      top: 'center',
      dimension: visualMapDimension,
      ...getVisualMapRange(),
      inRange: {
        color: DAMAGE_COLORS
      },
      text: [currentModeLabel, ''],
      calculable: true,
      textStyle: TEXT_STYLES.axis
    },
    xAxis: {
      type: 'category',
      data: dataset.map(r => r[0]),
      axisLine: AXIS_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis
    },
    yAxis: {
      type: 'value',
      name: yName,
      nameLocation: 'middle',
      nameGap: 50,
      axisLine: AXIS_LINE_STYLE,
      splitLine: SPLIT_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      nameTextStyle: TEXT_STYLES.axis
    },
    dataset: {
      source: dataset
    },
    series: [
      {
        name: currentLegend,
        type: 'bar',
        encode: { x: 0, y: yIndex },
        itemStyle: {
          opacity: 1,
          borderColor: '#fff',
          borderWidth: 1
        },
        label: {
          show: true,
          position: 'top',
          ...TEXT_STYLES.axis
        }
      }
    ]
  };

  return (
    <div className={styles.combinedPlotC}>
      <div className={styles.controls}>
        {modes.map(m => (
          <button
            key={m.key}
            className={`${styles.modeBtn} ${mode === m.key ? styles.modeBtnActive : ''}`}
            onClick={() => setMode(m.key)}
          >
            {m.label}
          </button>
        ))}
      </div>

      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '480px' }}
      />

      <div className={styles.legend}>
        <span className={styles.legendItem}>
          <span className={styles.legendSwatch} />
          {currentLegend}
        </span>
      </div>
    </div>
  );
};

CombinedPlotC.propTypes = {
  title: PropTypes.string,
  data: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.string.isRequired,
      gdp: PropTypes.number.isRequired,
      damage: PropTypes.number.isRequired
    })
  ),
  yAxisLabel: PropTypes.string,
  legendLabel: PropTypes.string,
  modes: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired
    })
  ),
  tooltipFormatter: PropTypes.func
};

export default CombinedPlotC;
