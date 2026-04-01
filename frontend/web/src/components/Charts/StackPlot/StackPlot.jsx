import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  AXIS_LINE_STYLE,
  SPLIT_LINE_STYLE,
  CHART_COLORS
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './StackPlot.module.scss';

const StackPlot = ({
  title,
  timelineLabels = [],
  legendItems = [],
  timelineData = [],
  seriesData = []
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const getSeriesConfig = (name, index, totalSeriesCount, data = []) => ({
    name,
    type: 'line',
    stack: 'Total',
    smooth: true,
    areaStyle: {},
    data,
    emphasis: {
      focus: 'series'
    },
    label: index === totalSeriesCount - 1 ? {
      show: true,
      position: 'top',
      fontFamily: TEXT_STYLES.axis.fontFamily,
      fontSize: 11,
      color: CHART_COLORS.text
    } : { show: false }
  });

  const getTimelineBasedSeriesData = () => legendItems.map((name, index) => (
    getSeriesConfig(
      name,
      index,
      legendItems.length,
      timelineData.map((item) => {
        const values = item?.series?.[index]?.data;
        if (Array.isArray(values)) {
          return values[values.length - 1] ?? null;
        }
        return values ?? null;
      })
    )
  ));

  const option = {
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
      top: 35,
      left: 'center',
      textStyle: TEXT_STYLES.legend
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: 50,
      top: 135,
      containLabel: true
    },
    xAxis: [{
      type: 'category',
      data: timelineLabels,
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
    series: seriesData.length > 0
      ? seriesData.map((series, index) => getSeriesConfig(
        series.name,
        index,
        seriesData.length,
        series.data
      ))
      : getTimelineBasedSeriesData()
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="stack-plot" className={styles.stackPlot}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '500px' }}
      />
    </ChartWrapper>
  );
};

StackPlot.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  legendItems: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.object),
  seriesData: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      data: PropTypes.arrayOf(PropTypes.number).isRequired
    })
  )
};

export default StackPlot;
