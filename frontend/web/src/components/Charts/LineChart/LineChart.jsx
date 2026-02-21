import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  GRID_CONFIG,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE
} from '../chartConfig';
import styles from './LineChart.module.scss';

const LineChart = ({ title, labels = [], datasets = [] }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const option = {
    tooltip: {
      ...TOOLTIP_CONFIG,
      trigger: 'axis'
    },
    legend: {
      top: 20,
      left: 'center',
      textStyle: TEXT_STYLES.legend
    },
    grid: GRID_CONFIG,
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false,
      axisLine: AXIS_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis
    },
    yAxis: {
      type: 'value',
      axisLine: AXIS_LINE_STYLE,
      axisLabel: TEXT_STYLES.axis,
      splitLine: SPLIT_LINE_STYLE
    },
    series: datasets.map((dataset) => ({
      name: dataset.name,
      type: 'line',
      data: dataset.data,
      smooth: true,
      lineStyle: {
        width: 2.5
      },
      itemStyle: {
        borderWidth: 2
      },
      emphasis: {
        focus: 'series',
        lineStyle: {
          width: 3
        }
      }
    }))
  };

  return (
    <div className={styles.lineChart}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '400px' }} 
      />
    </div>
  );
};

LineChart.propTypes = {
  title: PropTypes.string.isRequired,
  labels: PropTypes.arrayOf(PropTypes.string),
  datasets: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      data: PropTypes.arrayOf(PropTypes.number).isRequired
    })
  )
};

export default LineChart;
