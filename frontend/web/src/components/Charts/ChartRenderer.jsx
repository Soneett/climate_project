import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {
  LineChart,
  PieChart,
  BarChartA,
  BarChartB,
  StackPlot,
  WindPlot
} from './index';
import { fetchLineChart } from '../../services/api';

/**
 * Chart type to component mapping
 */
const CHART_COMPONENTS = {
  line: LineChart,
  pie: PieChart,
  bar: BarChartA,
  barB: BarChartB,
  stackPlot: StackPlot,
  windPlot: WindPlot
};

/**
 * Factory component for rendering different chart types
 * @param {Object} block - Content block configuration
 * @returns {React.Element|null} - Rendered chart component or null
 */
const ChartRenderer = ({ block }) => {

  const [lineData, setLineData] = useState(block.chartData);
  const { chartType, title } = block;

  useEffect(() => {
    if (block.chartType === "line" && block.indicators) {
      fetchLineChart(block.indicators).then((res) => {
        if (res) {
          setLineData(res);
        }
      });
    }
  }, [block]);

  // Determine which chart component to use
  const ChartComponent = CHART_COMPONENTS[chartType];

  if (!ChartComponent) {
    return null;
  }

  // Prepare props based on chart type
  let chartProps = { title };

  switch (chartType) {
    case 'stackPlot':
      chartProps = { ...chartProps, ...block.stackPlotData };
      break;
    case 'windPlot':
      chartProps = { ...chartProps, ...block.windPlotData };
      break;
    case 'barB':
      chartProps = { ...chartProps, ...block.barBData };
      break;
    case 'bar':
      chartProps = { ...chartProps, ...block.barData };
      break;
    case 'pie':
      chartProps = { ...chartProps, ...block.pieData };
      break;
    case 'line':
    default:
      if (lineData) {
        chartProps = {
          title,
          labels: lineData.labels,
          datasets: lineData.datasets
        };
      }
      break;
      }

  return <ChartComponent {...chartProps} />;
};

ChartRenderer.propTypes = {
  block: PropTypes.shape({
    chartType: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    indicators: PropTypes.string,
    chartData: PropTypes.object,
    stackPlotData: PropTypes.object,
    windPlotData: PropTypes.object,
    barBData: PropTypes.object,
    barData: PropTypes.object,
    pieData: PropTypes.object
  }).isRequired
};

export default ChartRenderer;
