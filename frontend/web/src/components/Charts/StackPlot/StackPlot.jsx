import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  getTitleConfig,
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE,
  CHART_COLORS
} from '../chartConfig';
import styles from './StackPlot.module.scss';

const StackPlot = ({ 
  title, 
  timelineLabels = [], 
  legendItems = [],
  timelineData = []
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
          type: 'cross',
          label: {
            backgroundColor: CHART_COLORS.tooltip,
            fontFamily: TEXT_STYLES.tooltip.fontFamily
          }
        }
      },
      legend: {
        data: legendItems,
        top: 60,
        left: 'center',
        textStyle: TEXT_STYLES.legend
      },
      toolbox: {
        feature: {
          saveAsImage: {
            title: 'Сохранить'
          }
        },
        right: 20,
        top: 20
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: 80,
        top: 120,
        containLabel: true
      },
      xAxis: [{
        type: 'category',
        boundaryGap: false,
        axisLine: AXIS_LINE_STYLE,
        axisLabel: TEXT_STYLES.axis
      }],
      yAxis: [{
        type: 'value',
        axisLine: AXIS_LINE_STYLE,
        axisLabel: TEXT_STYLES.axis,
        splitLine: SPLIT_LINE_STYLE
      }],
      series: legendItems.map((name, index) => ({
        name: name,
        type: 'line',
        stack: 'Total',
        smooth: true,
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        label: index === legendItems.length - 1 ? {
          show: true,
          position: 'top',
          fontFamily: TEXT_STYLES.axis.fontFamily,
          fontSize: 11,
          color: CHART_COLORS.text
        } : { show: false }
      }))
    },
    options: timelineData
  };

  return (
    <div className={styles.stackPlot}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '500px' }} 
      />
    </div>
  );
};

StackPlot.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  legendItems: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.object)
};

export default StackPlot;
