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
import { fetchLineChart, fetchPieChart } from '../../services/api';

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

const hasLinePayload = (payload) => {
  return Boolean(
    payload
    && Array.isArray(payload.labels)
    && Array.isArray(payload.datasets)
    && payload.labels.length > 0
    && payload.datasets.length > 0
  );
};

const hasPiePayload = (payload) => {
  return Boolean(
    payload
    && Array.isArray(payload.timelineLabels)
    && Array.isArray(payload.timelineData)
    && payload.timelineLabels.length > 0
    && payload.timelineData.length > 0
  );
};

/**
 * Factory component for rendering different chart types
 * @param {Object} block - Content block configuration
 * @returns {React.Element|null} - Rendered chart component or null
 */
const ChartRenderer = ({ block }) => {
  const [lineData, setLineData] = useState(block.chartData);
  const [pieData, setPieData] = useState(block.pieData);
  const { chartType, title } = block;

  useEffect(() => {
    setLineData(block.chartData);
    setPieData(block.pieData);

    if (!block.indicators) {
      return;
    }

    const indicatorsCsv = Array.isArray(block.indicators)
      ? block.indicators.join(',')
      : block.indicators;

    if (!indicatorsCsv) {
      return;
    }

    const regionId = block.regionId ?? block.region_id;

    if (block.chartType === 'line') {
      fetchLineChart(indicatorsCsv, regionId).then((res) => {
        if (hasLinePayload(res)) {
          setLineData(res);
        }
      });
    }

    if (block.chartType === 'pie') {
      fetchPieChart(indicatorsCsv, regionId).then((res) => {
        if (hasPiePayload(res)) {
          setPieData(res);
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
      chartProps = { ...chartProps, ...(pieData || block.pieData) };
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
    indicators: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.arrayOf(PropTypes.string)
    ]),
    regionId: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    region_id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    chartData: PropTypes.object,
    stackPlotData: PropTypes.object,
    windPlotData: PropTypes.object,
    barBData: PropTypes.object,
    barData: PropTypes.object,
    pieData: PropTypes.object
  }).isRequired
};

export default ChartRenderer;
