import React, { useRef, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import styles from './PieChart.module.scss';

const PieChart = ({ title, timelineLabels = [], legendLeftItems = [], legendRightItems = [], timelineData = [] }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const handleResize = () => {
      chartRef.current?.getEchartsInstance()?.resize();
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const option = {
    baseOption: {
      timeline: {
        axisType: 'category',
        data: timelineLabels,
        autoPlay: false,
        playInterval: 2000,
        left: 'center',
        bottom: 0,
        width: '70%',
        label: { 
          formatter: '{value}',
          color: '#2C3E38',
          fontFamily: 'Raleway, sans-serif'
        },
        lineStyle: {
          color: '#9FB69F'
        },
        itemStyle: {
          color: '#9FB69F',
          borderColor: '#9FB69F'
        },
        checkpointStyle: {
          color: '#366164',
          borderColor: '#366164'
        },
        controlStyle: {
          color: '#9FB69F',
          borderColor: '#9FB69F'
        }
      },
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
        trigger: 'item', 
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#E5E7EB',
        borderWidth: 1,
        textStyle: {
          color: '#2C3E38',
          fontFamily: 'Raleway, sans-serif'
        }
      },
      legend: [
        { 
          orient: 'vertical', 
          left: '5%', 
          top: 60, 
          data: legendLeftItems,
          textStyle: {
            fontFamily: 'Raleway, sans-serif',
            fontSize: 12,
            color: '#2C3E38'
          }
        },
        { 
          orient: 'vertical', 
          right: '5%', 
          top: 60, 
          data: legendRightItems,
          textStyle: {
            fontFamily: 'Raleway, sans-serif',
            fontSize: 12,
            color: '#2C3E38'
          }
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
        label: {
          fontFamily: 'Raleway, sans-serif',
          fontSize: 12,
          color: '#2C3E38'
        }
      }]
    },
    options: timelineData
  };

  return (
    <div className={styles.pieChart}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '500px' }} 
      />
    </div>
  );
};

export default PieChart;
