import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  getTitleConfig,
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG,
  GRID_CONFIG,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE,
  CHART_COLORS
} from '../chartConfig';
import styles from './BarChartB.module.scss';

const BarChartB = ({ 
  title, 
  timelineLabels = [], 
  categories = [], // возрастные группы: ['0–4', '5–9', '10–14', ...]
  legendItems = ['Мужчины', 'Женщины'],
  timelineData = [] // массив данных для каждого года
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const option = {
    baseOption: {
      timeline: {
        ...TIMELINE_CONFIG,
        data: timelineLabels
      },
      title: getTitleConfig(title),
      tooltip: {
        ...TOOLTIP_CONFIG,
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function (params) {
          return params
            .map(p => `${p.seriesName}: ${Math.abs(p.value)}`)
            .join('<br/>');
        }
      },
      legend: {
        data: legendItems,
        top: 60,
        left: 'center',
        textStyle: TEXT_STYLES.legend
      },
      grid: {
        ...GRID_CONFIG,
        bottom: 80
      },
      xAxis: [{
        type: 'value',
        axisLine: AXIS_LINE_STYLE,
        axisLabel: {
          ...TEXT_STYLES.axis,
          formatter: value => Math.abs(value)
        },
        splitLine: SPLIT_LINE_STYLE
      }],
      yAxis: [{
        type: 'category',
        axisTick: { show: false },
        data: categories,
        axisLine: AXIS_LINE_STYLE,
        axisLabel: TEXT_STYLES.axis
      }],
      series: [
        {
          name: legendItems[0] || 'Мужчины',
          type: 'bar',
          stack: 'Total',
          label: {
            show: true,
            position: 'left',
            formatter: ({ value }) => Math.abs(value),
            fontFamily: TEXT_STYLES.legend.fontFamily,
            fontSize: 11,
            color: CHART_COLORS.text
          },
          emphasis: {
            focus: 'series'
          },
          itemStyle: {
            color: '#5B8DEF'
          }
        },
        {
          name: legendItems[1] || 'Женщины',
          type: 'bar',
          stack: 'Total',
          label: {
            show: true,
            position: 'right',
            fontFamily: TEXT_STYLES.legend.fontFamily,
            fontSize: 11,
            color: CHART_COLORS.text
          },
          emphasis: {
            focus: 'series'
          },
          itemStyle: {
            color: '#F472B6'
          }
        }
      ]
    },
    options: timelineData
  };

  return (
    <div className={styles.barChartB}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '600px' }} 
      />
    </div>
  );
};

BarChartB.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  categories: PropTypes.arrayOf(PropTypes.string),
  legendItems: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.object)
};

export default BarChartB;
