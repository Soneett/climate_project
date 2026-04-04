import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './PieChart.module.scss';

const PieChart = ({ title, timelineLabels = [], legendLeftItems = [], legendRightItems = [], timelineData = [] }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const option = {
    baseOption: {
      timeline: {
        ...TIMELINE_CONFIG,
        data: timelineLabels
      },
      tooltip: {
        ...TOOLTIP_CONFIG,
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: [
        {
          orient: 'vertical',
          left: '5%',
          top: 20,
          data: legendLeftItems,
          textStyle: TEXT_STYLES.legendSmall
        },
        {
          orient: 'vertical',
          right: '5%',
          top: 30,
          data: legendRightItems,
          textStyle: TEXT_STYLES.legendSmall
        }
      ],
      series: [{
        name: title,
        type: 'pie',
        radius: '50%',
        center: ['50%', '55%'],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0,0,0,0.5)'
          }
        },
        label: { show: false },
        labelLine: { show: false }
      }]
    },
    options: timelineData.map((o, i) => ({
      ...o,
      title: { text: timelineLabels[i] || '', left: 'center', top: 10, textStyle: TEXT_STYLES.axis }
    }))
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="pie-chart" className={styles.pieChart}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '500px' }}
      />
    </ChartWrapper>
  );
};

PieChart.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  legendLeftItems: PropTypes.arrayOf(PropTypes.string),
  legendRightItems: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.object)
};

export default PieChart;
