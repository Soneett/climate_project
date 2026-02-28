import React, { useRef, useState, useCallback, useMemo, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  TIMELINE_CONFIG,
} from '../chartConfig';
import styles from './WaffleChart.module.scss';

const NICE_COLORS = [
  '#5470c6', '#91cc75', '#fac858', '#ee6666',
  '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
];

const WaffleChart = ({ title, timelineLabels = [], timelineData = [] }) => {
  const chartRef = useRef(null);
  const [selectedCategories, setSelectedCategories] = useState({});
  useChartResize(chartRef);

  const GRID_WIDTH = 16;
  const GRID_HEIGHT = 10;
  const TOTAL_CELLS = GRID_WIDTH * GRID_HEIGHT;

  const allCategories = useMemo(() => {
    return [...new Set(timelineData.flatMap(y => y.data.map(i => i.name)))];
  }, [timelineData]);

  const splitCategories = useMemo(() => {
    const half = Math.ceil(allCategories.length / 2);
    return {
      left: allCategories.slice(0, half),
      right: allCategories.slice(half)
    };
  }, [allCategories]);

  useEffect(() => {
    const initial = {};
    allCategories.forEach(cat => { initial[cat] = true; });
    setSelectedCategories(initial);
  }, [allCategories]);

  const calculateCellDistribution = useCallback((visibleData) => {
    const totalValue = visibleData.reduce((sum, item) => sum + item.value, 0);
    if (totalValue === 0) return [];

    const distribution = visibleData.map(item => ({
      ...item,
      cells: Math.floor((item.value / totalValue) * TOTAL_CELLS)
    }));

    let allocatedCells = distribution.reduce((sum, item) => sum + item.cells, 0);
    let i = 0;
    while (allocatedCells < TOTAL_CELLS && distribution.length > 0) {
      distribution[i % distribution.length].cells++;
      allocatedCells++;
      i++;
    }
    return distribution;
  }, [TOTAL_CELLS]);

  const options = useMemo(() => {
    return timelineData.map((yearData, yearIdx) => {
      const year = timelineLabels[yearIdx];
      const visibleItems = yearData.data.filter(item => selectedCategories[item.name] !== false);
      const distributed = calculateCellDistribution(visibleItems);

      const series = allCategories.map((catName, catIdx) => {
        const distItem = distributed.find(d => d.name === catName);
        const cellCount = distItem ? distItem.cells : 0;

        const previousCellsSum = distributed
          .slice(0, distributed.findIndex(d => d.name === catName))
          .reduce((sum, d) => sum + d.cells, 0);

        const categoryPoints = [];
        for (let i = 0; i < cellCount; i++) {
          const globalIdx = previousCellsSum + i;
          categoryPoints.push({
            value: [globalIdx % GRID_WIDTH, Math.floor(globalIdx / GRID_WIDTH)],
            name: catName,
            year: year,
            percentage: distItem ? (distItem.value / (visibleItems.reduce((s, d) => s + d.value, 0) || 1)) * 100 : 0,
            absoluteValue: distItem?.absoluteValue || 0
          });
        }

        return {
          name: catName,
          type: 'scatter',
          symbol: 'roundRect',
          symbolSize: 30,
          data: categoryPoints,
          emphasis: {
            focus: 'series',
            itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' }
          },
          blur: { itemStyle: { opacity: 0.15 } },
          itemStyle: {
            color: NICE_COLORS[catIdx % NICE_COLORS.length],
            borderColor: '#fff',
            borderWidth: 2,
            borderRadius: 4
          },
          animationDuration: 500,
          animationEasingUpdate: 'cubicInOut'
        };
      });

      return {
        title: {
          text: year,
          left: 'center',
          top: 20,
          textStyle: { ...TEXT_STYLES.axis }
        },
        legend: [
          {
            data: splitCategories.left,
            orient: 'vertical',
            left: '7%',
            top: 'center',
            selected: selectedCategories,
            textStyle: TEXT_STYLES.legend
          },
          {
            data: splitCategories.right,
            orient: 'vertical',
            right: '7%',
            top: 'center',
            selected: selectedCategories,
            textStyle: TEXT_STYLES.legend
          }
        ],
        series
      };
    });
  }, [timelineData, timelineLabels, selectedCategories, allCategories, splitCategories, calculateCellDistribution, GRID_WIDTH]);

  const option = {
    backgroundColor: '#ffffff',
    baseOption: {
      timeline: { ...TIMELINE_CONFIG, data: timelineLabels, bottom: 0 },
      tooltip: {
        ...TOOLTIP_CONFIG,
        trigger: 'item',
        formatter: (params) => {
          const marker = `<span style="display:inline-block;margin-right:8px;border-radius:2px;width:10px;height:10px;background-color:${params.color};"></span>`;
          // ДОБАВЛЕН жирный текст <b> для числовых значений
          return `
            <div style="font-family: ${TEXT_STYLES.tooltip.fontFamily}; min-width: 160px; padding: 5px;">
              ${marker}<b>${params.data.name}</b><br/>
              <div style="margin-top: 8px; border-top: 1px solid #eee; padding-top: 5px; line-height: 1.6;">
                Доля: <b>${params.data.percentage.toFixed(1)}%</b><br/>
                Значение: <b>${params.data.absoluteValue.toLocaleString()}</b>
              </div>
            </div>
          `;
        }
      },
      grid: {
        top: 'center',
        left: 'center',
        width: 550,
        height: 350,
        containLabel: false
      },
      xAxis: {
        type: 'value',
        min: -0.5,
        max: GRID_WIDTH - 0.5,
        splitLine: { show: false }, axisLine: { show: false },
        axisTick: { show: false }, axisLabel: { show: false }
      },
      yAxis: {
        type: 'value',
        min: -0.5,
        max: GRID_HEIGHT - 0.5,
        inverse: true,
        splitLine: { show: false }, axisLine: { show: false },
        axisTick: { show: false }, axisLabel: { show: false }
      }
    },
    options: options
  };

  return (
    <div className={styles.waffleChartWrapper} style={{ width: '100%', height: '550px', background: '#fff' }}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%' }}
        onEvents={{
          legendselectchanged: (params) => setSelectedCategories(params.selected)
        }}
      />
    </div>
  );
};

WaffleChart.propTypes = {
  title: PropTypes.string,
  timelineLabels: PropTypes.arrayOf(PropTypes.string),
  timelineData: PropTypes.arrayOf(PropTypes.shape({
    data: PropTypes.arrayOf(PropTypes.shape({
      name: PropTypes.string.isRequired,
      value: PropTypes.number.isRequired,
      absoluteValue: PropTypes.number
    }))
  }))
};

export default WaffleChart;