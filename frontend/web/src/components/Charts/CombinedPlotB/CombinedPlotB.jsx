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
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './CombinedPlotB.module.scss';

const CAUSE_COLORS = ['#5470C6', '#91CC75', '#EE6666', '#FAC858'];

const CombinedPlotB = ({
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
  const [hiddenCauses, setHiddenCauses] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const currentXLabel = xAxisOptions.find(t => t.key === xType)?.label || xType;

  const toggleCause = (cause) => {
    setHiddenCauses(prev =>
      prev.includes(cause) ? prev.filter(c => c !== cause) : [...prev, cause]
    );
  };

  const buildSeries = () =>
    categories.map((cause, idx) => ({
      name: cause,
      type: 'scatter',
      symbolSize: (val) => {
        const cases = Array.isArray(val) ? val[1] : val.value[1];
        return Math.max(6, Math.sqrt(cases) * 0.5);
      },
      itemStyle: {
        color: CAUSE_COLORS[idx % CAUSE_COLORS.length]
      },
      data: hiddenCauses.includes(cause) ? [] : data
        .filter(d => d.category === cause)
        .map(d => ({
          value: [d[xType], d.cases, d.year],
          itemStyle: {
            opacity: selectedYear !== null && d.year !== selectedYear ? 0.3 : 1
          }
        })),
      emphasis: { focus: 'series' }
    }));

  const option = {
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'item',
      formatter: (params) => {
        const [xVal, cases, year] = params.data.value;
        return `
          <b>${params.seriesName}</b><br/>
          Год: ${year}<br/>
          ${currentXLabel}: ${xVal}<br/>
          ${yAxisLabel}: ${cases.toLocaleString('ru-RU')}
        `;
      }
    },
    legend: {
      show: false,
      selectedMode: 'multiple'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: 100,
      top: 20,
      containLabel: true
    },
    xAxis: {
      type: 'value',
      scale: true,
      name: `${currentXLabel}`,
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
      axisLine: AXIS_LINE_STYLE,
      splitLine: SPLIT_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      nameTextStyle: TEXT_STYLES.axis
    },
    series: buildSeries()
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="combined-plot-b" className={styles.combinedPlotB}>
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
        style={{ height: '100%', width: '100%', minHeight: '480px' }}
      />

      <div className={styles.legend}>
        {categories.map((cause, idx) => (
          <button
            key={cause}
            className={`${styles.legendItem} ${hiddenCauses.includes(cause) ? styles.legendItemHidden : ''}`}
            onClick={() => toggleCause(cause)}
          >
            <span
              className={styles.legendDot}
              style={{ backgroundColor: CAUSE_COLORS[idx % CAUSE_COLORS.length] }}
            />
            {cause}
          </button>
        ))}
      </div>
    </ChartWrapper>
  );
};

CombinedPlotB.propTypes = {
  categories: PropTypes.arrayOf(PropTypes.string),
  years: PropTypes.arrayOf(PropTypes.number),
  data: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number.isRequired,
      category: PropTypes.string.isRequired,
      cases: PropTypes.number.isRequired
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

export default CombinedPlotB;
