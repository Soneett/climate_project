import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG,
  CHART_COLORS
} from '../chartConfig';
import styles from './WaffleChart.module.scss';

// Default color palette for categories
const DEFAULT_COLORS = [
  '#64B5F6',  // blue
  '#81C784',  // green
  '#FFD54F',  // yellow
  '#E57373',  // red
  '#9575CD',  // purple
  '#4DB6AC',  // teal
  '#FF8A65',  // orange
  '#A1887F'   // brown
];

// Name for empty cells in waffle grid
const EMPTY_CELL_NAME = 'Прочее';

const WaffleChart = ({ title, timelineLabels = [], timelineData = [] }) => {
  const chartRef = useRef(null);
  const [selectedCategories, setSelectedCategories] = useState({});
  useChartResize(chartRef);

  // Waffle chart configuration - 10x10 grid for 100 cells
  const GRID_COLS = 10;
  const GRID_ROWS = 10;
  const TOTAL_CELLS = GRID_COLS * GRID_ROWS; // 100 cells
  const CELL_SIZE = 12; // Larger circles with minimal spacing
  const CELL_BORDER_WIDTH = 0.5; // Minimal border for denser packing

  // Convert percentage data to waffle grid data
  // Takes into account hidden categories for proper redistribution
  const convertToWaffleData = React.useCallback((data, year, hiddenCategories = []) => {
    const waffleData = [];
    let currentIndex = 0;
    
    // Filter out hidden categories
    const visibleData = data.filter(item => !hiddenCategories.includes(item.name));
    
    // Calculate total of visible categories for redistribution
    const totalVisible = visibleData.reduce((sum, item) => sum + item.value, 0);
    
    // If all categories are hidden, show empty grid
    if (totalVisible === 0 || visibleData.length === 0) {
      for (let i = 0; i < TOTAL_CELLS; i++) {
        const row = Math.floor(i / GRID_COLS);
        const col = i % GRID_COLS;
        waffleData.push({
          value: [col, row],
          name: EMPTY_CELL_NAME,
          percentage: 0,
          absoluteValue: 0,
          year: year
        });
      }
      return waffleData;
    }
    
    // Calculate total absolute values if provided
    const hasAbsoluteValues = data.some(item => item.absoluteValue);
    const totalAbsolute = hasAbsoluteValues 
      ? data.reduce((sum, item) => sum + (item.absoluteValue || 0), 0)
      : 1000;
    
    visibleData.forEach((item) => {
      // Recalculate percentage based on visible categories only
      const recalculatedPercentage = (item.value / totalVisible) * 100;
      
      // Calculate number of cells based on recalculated percentage
      const cells = Math.round((recalculatedPercentage / 100) * TOTAL_CELLS);
      const absoluteValue = item.absoluteValue || Math.round((item.value / 100) * totalAbsolute);
      
      for (let i = 0; i < cells && currentIndex < TOTAL_CELLS; i++) {
        const row = Math.floor(currentIndex / GRID_COLS);
        const col = currentIndex % GRID_COLS;
        waffleData.push({
          value: [col, row],
          name: item.name,
          percentage: recalculatedPercentage,
          absoluteValue: absoluteValue,
          year: year
        });
        currentIndex++;
      }
    });
    
    // Fill remaining cells with empty color if needed
    while (currentIndex < TOTAL_CELLS) {
      const row = Math.floor(currentIndex / GRID_COLS);
      const col = currentIndex % GRID_COLS;
      waffleData.push({
        value: [col, row],
        name: EMPTY_CELL_NAME,
        percentage: 0,
        absoluteValue: 0,
        year: year
      });
      currentIndex++;
    }
    
    return waffleData;
  }, [GRID_COLS, TOTAL_CELLS]);

  // Get all unique categories across all years
  const allCategories = [...new Set(
    timelineData.flatMap(yearData => 
      yearData.data.map(item => item.name)
    )
  )].filter(name => name !== EMPTY_CELL_NAME);
  
  // Initialize selected categories on mount
  React.useEffect(() => {
    if (allCategories.length > 0 && Object.keys(selectedCategories).length === 0) {
      const initialSelected = {};
      allCategories.forEach(category => {
        initialSelected[category] = true;
      });
      setSelectedCategories(initialSelected);
    }
  }, [allCategories.length]); // eslint-disable-line react-hooks/exhaustive-deps
  
  // Prepare options for timeline - recalculate when selectedCategories changes
  const options = React.useMemo(() => {
    return timelineData.map((yearData, index) => {
      const year = timelineLabels[index];
      
      // Get hidden categories from selectedCategories state
      const hiddenCategories = Object.keys(selectedCategories).filter(
        key => selectedCategories[key] === false
      );
      
      const waffleData = convertToWaffleData(yearData.data, year, hiddenCategories);
      
      // Group data by category for separate series
      const categoriesInYear = yearData.data.map(item => item.name);
      const series = categoriesInYear.map((category) => ({
        type: 'scatter',
        name: category,
        data: waffleData.filter(d => d.name === category),
        symbolSize: CELL_SIZE,
        itemStyle: {
          color: DEFAULT_COLORS[allCategories.indexOf(category) % DEFAULT_COLORS.length],
          borderColor: '#fff',
          borderWidth: CELL_BORDER_WIDTH
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 5,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0,0,0,0.3)'
          }
        },
        animation: true,
        animationDuration: 800,
        animationEasing: 'cubicOut',
        animationDurationUpdate: 500
      }));
      
      // Add empty cells as a separate series (not in legend)
      series.push({
        type: 'scatter',
        name: EMPTY_CELL_NAME,
        data: waffleData.filter(d => d.name === EMPTY_CELL_NAME),
        symbolSize: CELL_SIZE,
        itemStyle: {
          color: '#f0f0f0',
          borderColor: '#fff',
          borderWidth: CELL_BORDER_WIDTH
        },
        animation: true,
        animationDuration: 800,
        animationEasing: 'cubicOut',
        animationDurationUpdate: 500
      });
      
      return {
        title: {
          text: timelineLabels[index] || '',
          left: 'center',
          top: 10,
          textStyle: TEXT_STYLES.axis
        },
        legend: {
          data: categoriesInYear,
          top: 30,
          left: 'center',
          type: 'scroll',
          orient: 'horizontal',
          textStyle: TEXT_STYLES.legend,
          itemWidth: 20,
          itemHeight: 14,
          selected: selectedCategories,
          pageIconSize: 12,
          pageTextStyle: TEXT_STYLES.legendSmall
        },
        series: series
      };
    });
  }, [timelineData, timelineLabels, selectedCategories, allCategories, convertToWaffleData]);

  const option = {
    baseOption: {
      timeline: {
        ...TIMELINE_CONFIG,
        data: timelineLabels
      },
      title: {},
      tooltip: {
        ...TOOLTIP_CONFIG,
        formatter: (params) => {
          // Don't show tooltip for empty cells
          if (params.data.name === EMPTY_CELL_NAME || params.data.percentage === 0) {
            return null;
          }
          
          return `
            <div style="font-family: ${TEXT_STYLES.tooltip.fontFamily};">
              <strong>Год:</strong> ${params.data.year}<br/>
              <strong>Вид:</strong> ${params.data.name}<br/>
              <strong>Процент:</strong> ${params.data.percentage.toFixed(1)}%<br/>
              <strong>Абсолютное значение:</strong> ${params.data.absoluteValue}
            </div>
          `;
        }
      },
      grid: {
        left: '5%',
        right: '5%',
        top: 140,
        bottom: 80,
        containLabel: true
      },
      xAxis: {
        type: 'value',
        min: -0.5,
        max: GRID_COLS - 0.5,
        interval: 1,
        splitLine: {
          show: false
        },
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          show: false
        }
      },
      yAxis: {
        type: 'value',
        min: -0.5,
        max: GRID_ROWS - 0.5,
        interval: 1,
        splitLine: {
          show: false
        },
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          show: false
        },
        inverse: true
      },
      series: []
    },
    options: options
  };

  const onLegendSelectChanged = (params) => {
    setSelectedCategories(params.selected);
  };

  return (
    <div className={styles.waffleChart}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '500px' }} 
        onEvents={{
          legendselectchanged: onLegendSelectChanged
        }}
      />
    </div>
  );
};

WaffleChart.propTypes = {
  title: PropTypes.string.isRequired,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.shape({
    title: PropTypes.shape({
      text: PropTypes.string.isRequired
    }).isRequired,
    data: PropTypes.arrayOf(PropTypes.shape({
      name: PropTypes.string.isRequired,
      value: PropTypes.number.isRequired,
      absoluteValue: PropTypes.number
    })).isRequired
  }))
};

export default WaffleChart;
