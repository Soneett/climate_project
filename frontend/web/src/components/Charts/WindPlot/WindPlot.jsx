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
import styles from './WindPlot.module.scss';

const WindPlot = ({ 
  title = "Скорость и преобладающее направление ветра",
  timelineLabels = [], 
  timelineData = [] // массив объектов { dir, avg, max } для каждого года
}) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ'];

  const option = {
    baseOption: {
      timeline: {
        ...TIMELINE_CONFIG,
        data: timelineLabels
      },
      animation: true,
      animationDurationUpdate: 1500,
      title: getTitleConfig(title),
      tooltip: {
        ...TOOLTIP_CONFIG,
        trigger: 'item',
        formatter: function(params) {
          if (params.seriesType === 'gauge') {
            const index = Math.round(params.value / 45) % 8;
            return `Преобладающее направление: ${directions[index]}`;
          }
          if (params.seriesType === 'bar') {
            return `${params.seriesName}: ${params.value} м/с`;
          }
          return params.name || '';
        }
      },
      grid: { 
        left: '10%', 
        right: '10%', 
        top: '55%', 
        height: '25%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        min: 0,
        splitLine: SPLIT_LINE_STYLE,
        axisLabel: { 
          formatter: '{value} м/с',
          ...TEXT_STYLES.axis
        },
        axisLine: AXIS_LINE_STYLE
      },
      yAxis: {
        type: 'category',
        data: ['Скорость'],
        axisTick: { show: false },
        axisLine: { show: false },
        axisLabel: TEXT_STYLES.axis
      },
      series: [
        {
          name: 'Преобладающее направление',
          type: 'gauge',
          center: ['50%', '32%'],
          radius: '38%',
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 360,
          splitNumber: 8,
          axisLine: { 
            lineStyle: { 
              width: 18, 
              color: [[1, CHART_COLORS.compass]]
            } 
          },
          axisLabel: {
            distance: -40,
            color: CHART_COLORS.text,
            fontSize: 14,
            fontFamily: TEXT_STYLES.axis.fontFamily,
            formatter: function(v) {
              return directions[Math.round(v / 45) % 8];
            }
          },
          axisTick: {
            lineStyle: {
              color: '#B7CCAD'
            }
          },
          splitLine: {
            lineStyle: {
              color: '#B7CCAD'
            }
          },
          pointer: { 
            length: '65%', 
            width: 12, 
            itemStyle: { 
              color: CHART_COLORS.primary
            } 
          },
          detail: { show: false },
          animation: true,
          animationDurationUpdate: 1500,
          data: [{ value: timelineData[0]?.dir || 0 }]
        },
        {
          name: 'Макс. скорость',
          type: 'bar',
          stack: 's',
          barWidth: 28,
          itemStyle: { 
            color: '#E57373'
          },
          label: { 
            show: true, 
            position: 'insideRight',
            formatter: '{c} м/с',
            distance: 5,
            color: CHART_COLORS.text,
            fontWeight: 'bold',
            fontFamily: TEXT_STYLES.legend.fontFamily
          },
          emphasis: { focus: 'series' },
          animation: true,
          animationDurationUpdate: 1500,
          data: [timelineData[0]?.max || 0]
        },
        {
          name: 'Средняя скорость',
          type: 'bar',
          stack: 's',
          barGap: '-100%',
          barWidth: 28,
          itemStyle: { 
            color: '#81C784'
          },
          label: { 
            show: true, 
            position: 'insideRight', 
            formatter: '{c} м/с', 
            color: '#fff',
            fontFamily: TEXT_STYLES.legend.fontFamily
          },
          emphasis: { focus: 'series' },
          animation: true,
          animationDurationUpdate: 1500,
          data: [timelineData[0]?.avg || 0]
        }
      ]
    },
    options: timelineData.map((data, index) => ({
      title: { text: `${title} — ${timelineLabels[index]}` },
      xAxis: { max: Math.ceil(data.max * 1.2) },
      series: [
        { data: [{ value: data.dir }] },
        { data: [data.max] },
        { data: [data.avg] }
      ]
    }))
  };

  return (
    <div className={styles.windPlot}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '550px' }} 
      />
    </div>
  );
};

WindPlot.propTypes = {
  title: PropTypes.string,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(
    PropTypes.shape({
      dir: PropTypes.number,
      avg: PropTypes.number,
      max: PropTypes.number
    })
  )
};

export default WindPlot;
