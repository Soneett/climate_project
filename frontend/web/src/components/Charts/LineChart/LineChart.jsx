import React, { useRef, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import styles from './LineChart.module.scss';

const LineChart = ({ title, labels = [], datasets = [] }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const handleResize = () => {
      chartRef.current?.getEchartsInstance()?.resize();
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const option = {
    title: {
      text: title,
      left: 'center',
      top: 20,
      textStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 18,
        fontWeight: 600,
        color: '#2C3E38'
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E5E7EB',
      borderWidth: 1,
      textStyle: {
        color: '#2C3E38',
        fontFamily: 'Raleway, sans-serif'
      }
    },
    legend: {
      top: 60,
      left: 'center',
      textStyle: {
        fontFamily: 'Raleway, sans-serif',
        fontSize: 13,
        color: '#2C3E38'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: 100,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#D1D5DB'
        }
      },
      axisLabel: {
        color: '#6B7280',
        fontFamily: 'Raleway, sans-serif'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#D1D5DB'
        }
      },
      axisLabel: {
        color: '#6B7280',
        fontFamily: 'Raleway, sans-serif'
      },
      splitLine: {
        lineStyle: {
          color: '#F3F4F6'
        }
      }
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

export default LineChart;
