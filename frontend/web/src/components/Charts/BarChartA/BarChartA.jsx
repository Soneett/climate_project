import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG,
  GRID_CONFIG,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './BarChartA.module.scss';

const BarChartA = ({ title, timelineLabels = [], dataSource = [], seriesCount = 3 }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const series = Array(seriesCount).fill(null).map(() => ({ type: 'bar' }));

  const option = {
    baseOption: {
      timeline: {
        ...TIMELINE_CONFIG,
        data: timelineLabels
      },
      title: {},
      tooltip: {
        ...TOOLTIP_CONFIG,
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        top: 35,
        left: 'center',
        textStyle: TEXT_STYLES.legend
      },
      grid: {
        ...GRID_CONFIG,
        bottom: 80
      },
      xAxis: {
        type: 'category',
        axisLine: AXIS_LINE_STYLE,
        axisLabel: TEXT_STYLES.axis
      },
      yAxis: {
        type: 'value',
        axisLine: AXIS_LINE_STYLE,
        axisLabel: TEXT_STYLES.axis,
        splitLine: SPLIT_LINE_STYLE
      },
      series: series
    },
    options: dataSource.map((o, i) => ({
      ...o,
      title: { text: timelineLabels[i] || '', left: 'center', top: 10, textStyle: TEXT_STYLES.axis }
    }))
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="bar-chart" className={styles.barChart}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '500px' }}
      />
    </ChartWrapper>
  );
};

BarChartA.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  dataSource: PropTypes.arrayOf(PropTypes.object),
  seriesCount: PropTypes.number
};

export default BarChartA;
