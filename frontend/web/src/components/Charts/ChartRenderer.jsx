import React, { useEffect, useState } from 'react';
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
  CombinedPlotB,
  CombinedPlotC,
  LineDotChart,
  MapChart,
  ColorMarkerMap
} from './index';
import { fetchLineChart, fetchPieChart, fetchWaffleChart, fetchStackPlot, fetchPopulationPyramid } from '../../services/api';

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
  combinedPlotB: CombinedPlotB,
  combinedPlotC: CombinedPlotC,
  lineDotChart: LineDotChart,
  mapChart: MapChart,
  colorMarkerMap: ColorMarkerMap
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

const hasWafflePayload = (payload) => {
  return Boolean(
    payload
    && Array.isArray(payload.timelineLabels)
    && Array.isArray(payload.timelineData)
    && payload.timelineLabels.length > 0
    && payload.timelineData.length > 0
  );
};

const hasStackPayload = (payload) => {
  return Boolean(
    payload
    && Array.isArray(payload.timelineLabels)
    && Array.isArray(payload.seriesData)
    && payload.timelineLabels.length > 0
    && payload.seriesData.length > 0
  );
};


const hasPyramidPayload = (payload) => {
  return Boolean(
    payload
    && Array.isArray(payload.categories)
    && Array.isArray(payload.timelineData)
    && payload.categories.length > 0
    && payload.timelineData.length > 0
  );
};

const deriveIndicatorsFromBlock = (block) => {
  if (block.indicators) {
    return (Array.isArray(block.indicators) ? block.indicators : String(block.indicators).split(','))
      .map((item) => String(item).trim())
      .filter(Boolean);
  }

  if (block.chartType === 'line' && block.chartData?.datasets) {
    return block.chartData.datasets
      .map((dataset) => dataset?.name)
      .filter(Boolean);
  }

  if (block.chartType === 'pie') {
    const legendItems = block.pieData?.legendLeftItems;
    if (Array.isArray(legendItems) && legendItems.length > 0) {
      return legendItems.filter(Boolean);
    }

    const timelinePoint = block.pieData?.timelineData?.[0];
    const seriesData = timelinePoint?.series?.[0]?.data;
    if (Array.isArray(seriesData)) {
      return seriesData.map((item) => item?.name).filter(Boolean);
    }
  }

  return [];
};

/**
 * Factory component for rendering different chart types
 * @param {Object} block - Content block configuration
 * @returns {React.Element|null} - Rendered chart component or null
 */
const ChartRenderer = ({ block }) => {
  const [lineData, setLineData] = useState(block.chartData);
  const [pieData, setPieData] = useState(block.pieData);
  const [waffleData, setWaffleData] = useState(block.waffleChartData || block.waffleData);
  const [stackData, setStackData] = useState(block.stackPlotData);
  const [pyramidData, setPyramidData] = useState(null);
  const { chartType, title } = block;

  useEffect(() => {
    setLineData(block.chartData);
    setPieData(block.pieData);
    setWaffleData(block.waffleChartData || block.waffleData);
    setStackData(block.stackPlotData);
    setPyramidData(null);

    const indicatorList = deriveIndicatorsFromBlock(block);
    const regionId = block.regionId ?? block.region_id;

    if (block.chartType === 'barB') {
      fetchPopulationPyramid(regionId).then((res) => {
        if (hasPyramidPayload(res)) {
          setPyramidData(res);
        }
      });
      return;
    }

    if (indicatorList.length === 0) {
      return;
    }

    if (block.chartType === 'line') {
      fetchLineChart(indicatorList, regionId).then((res) => {
        if (hasLinePayload(res)) {
          setLineData(res);
        }
      });
    }

    if (block.chartType === 'pie') {
      fetchPieChart(indicatorList, regionId).then((res) => {
        if (hasPiePayload(res)) {
          setPieData(res);
        }
      });
    }

    if (block.chartType === 'waffleChart' || block.chartType === 'waffle') {
      fetchWaffleChart(indicatorList, regionId).then((res) => {
        if (hasWafflePayload(res)) {
          setWaffleData(res);
        }
      });
    }

    if (block.chartType === 'stackPlot') {
      fetchStackPlot(indicatorList, regionId).then((res) => {
        if (hasStackPayload(res)) {
          setStackData(res);
        }
      });
    }
  }, [block]);

  // Determine which chart component to use
  const ChartComponent = CHART_COMPONENTS[chartType];

  if (!ChartComponent) {
    return null;
  }

  let chartProps = { title };

  switch (chartType) {
    case 'stackPlot':
      chartProps = { ...chartProps, ...(stackData || block.stackPlotData) };
      break;
    case 'windPlot':
      chartProps = { ...chartProps, ...block.windPlotData };
      break;
    case 'barB':
      chartProps = { ...chartProps, ...(pyramidData || { timelineLabels: [], categories: [], legendItems: ['Мужчины', 'Женщины'], timelineData: [] }) };
      break;
    case 'bar':
      chartProps = { ...chartProps, ...block.barData };
      break;
    case 'pie':
      chartProps = { ...chartProps, ...(pieData || block.pieData) };
      break;
    case 'programsPlot':
      chartProps = { ...chartProps, ...block.programsPlotData };
      break;
    case 'waffleChart':
      chartProps = { ...chartProps, ...(waffleData || block.waffleChartData) };
      break;
    case 'waffle':
      chartProps = { ...chartProps, ...(waffleData || block.waffleData) };
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
    case 'combinedPlotC':
      chartProps = { ...chartProps, ...block.combinedPlotCData };
      break;
    case 'lineDotChart':
      chartProps = { ...chartProps, ...block.lineDotChartData };
      break;
    case 'mapChart':
      chartProps = { ...chartProps, ...block.mapChartData };
      break;
    case 'colorMarkerMap':
      chartProps = { ...chartProps, ...block.colorMarkerMapData };
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
    pieData: PropTypes.object,
    programsPlotData: PropTypes.object,
    waffleChartData: PropTypes.object,
    waffleData: PropTypes.object,
    scatterPlotData: PropTypes.object,
    combinedPlotAData: PropTypes.object,
    combinedPlotBData: PropTypes.object,
    combinedPlotCData: PropTypes.object,
    lineDotChartData: PropTypes.object,
    mapChartData: PropTypes.object,
    colorMarkerMapData: PropTypes.object
  }).isRequired
};

export default ChartRenderer;
