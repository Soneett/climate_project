import React from 'react';
import PropTypes from 'prop-types';
import {
  LineChart,
  PieChart,
  BarChartA,
  BarChartB,
  StackPlot,
  WindPlot,
  ProgramsPlot,
  WaffleChart,
  ScatterPlot,
  CombinedPlotA,
  CombinedPlotB
} from './index';

/**
 * Chart type to component mapping
 */
const CHART_COMPONENTS = {
  line: LineChart,
  pie: PieChart,
  bar: BarChartA,
  barB: BarChartB,
  stackPlot: StackPlot,
  windPlot: WindPlot,
  programsPlot: ProgramsPlot,
  waffleChart: WaffleChart,
  waffle: WaffleChart,
  scatterPlot: ScatterPlot,
  combinedPlotA: CombinedPlotA,
  combinedPlotB: CombinedPlotB
};

/**
 * Factory component for rendering different chart types
 * @param {Object} block - Content block configuration
 * @returns {React.Element|null} - Rendered chart component or null
 */
const ChartRenderer = ({ block }) => {
  const { chartType, title } = block;

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
    case 'programsPlot':
      chartProps = { ...chartProps, ...block.programsPlotData };
      break;
    case 'waffleChart':
      chartProps = { ...chartProps, ...block.waffleChartData };
      break;
    case 'waffle':
      chartProps = { ...chartProps, ...block.waffleData };
      break;
    case 'scatterPlot':
      chartProps = { ...chartProps, ...block.scatterPlotData };
      break;
    case 'combinedPlotA':
      chartProps = { ...chartProps, ...block.combinedPlotAData };
      break;
    case 'combinedPlotB':
      chartProps = { ...chartProps, ...block.combinedPlotBData };
      break;
    case 'line':
    default:
      if (block.chartData) {
        chartProps = {
          title,
          labels: block.chartData.labels,
          datasets: block.chartData.datasets
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
    chartData: PropTypes.object,
    stackPlotData: PropTypes.object,
    windPlotData: PropTypes.object,
    barBData: PropTypes.object,
    barData: PropTypes.object,
    pieData: PropTypes.object,
    programsPlotData: PropTypes.object,
    waffleChartData: PropTypes.object,
    waffleData: PropTypes.object,
    scatterPlotData: PropTypes.object,
    combinedPlotAData: PropTypes.object,
    combinedPlotBData: PropTypes.object
  }).isRequired
};

export default ChartRenderer;
