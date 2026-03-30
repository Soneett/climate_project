import React, { useRef, useState, useMemo, useCallback } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import { useWindowWidth } from '../../../hooks/useWindowWidth';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  CHART_COLORS
} from '../chartConfig';
import ChartWrapper from '../ChartWrapper/ChartWrapper';
import styles from './ProgramsPlot.module.scss';

const STATUS_COLORS = {
  'завершена': '#81C784',
  'в процессе': '#64B5F6',
  'приостановлена': '#FFD54F',
  'не реализована': '#E57373'
};

const VALID_STATUSES = Object.keys(STATUS_COLORS);

const parseDate = (dateStr) => {
  if (!dateStr) return null;
  const [year, month] = dateStr.split('-').map(Number);
  return new Date(year, month - 1, 1).getTime();
};

const ProgramsPlot = ({ title, programs = [] }) => {
  const chartRef = useRef(null);
  useChartResize(chartRef);

  const [modalData, setModalData] = useState(null);
  const [selectedStatuses, setSelectedStatuses] = useState({});

  const windowWidth = useWindowWidth();
  const isMobile = windowWidth < 768;

  const minDate = parseDate('2020-01');
  const maxDate = parseDate('2024-12');

  const statuses = useMemo(
    () => [...new Set(programs.map(p => p.status))],
    [programs]
  );

  React.useEffect(() => {
    if (statuses.length > 0 && Object.keys(selectedStatuses).length === 0) {
      const initialSelected = {};
      statuses.forEach((status) => {
        initialSelected[status] = true;
      });
      setSelectedStatuses(initialSelected);
    }
  }, [statuses, selectedStatuses]);

  const maxBudget = useMemo(
    () => Math.max(0, ...programs.map(p => p.budget || 0)),
    [programs]
  );

  const seriesData = useMemo(
    () =>
      programs.map((program, index) => ({
        name: program.name,
        value: [
          index,
          parseDate(program.startDate),
          program.endDate ? parseDate(program.endDate) : maxDate,
          program.budget || 0,
          program.status,
          program.name
        ],
        itemStyle: {
          color: STATUS_COLORS[program.status] || '#999'
        },
        program
      })),
    [programs, maxDate]
  );

  const renderItem = useCallback(
    (params, api) => {
      const yIndex = api.value(0);
      const start = api.coord([api.value(1), yIndex]);
      const end = api.coord([api.value(2), yIndex]);
      const budget = api.value(3);
      const programName = api.value(5);

      const gridLeft = params.coordSys.x;
      const gridRight = params.coordSys.x + params.coordSys.width;

      const clampedStartX = Math.max(start[0], gridLeft);
      const clampedEndX = Math.min(end[0], gridRight);

      if (clampedStartX >= clampedEndX) return null;

      const minHeight = isMobile ? 20 : 15;
      const maxHeight = isMobile ? 44 : 40;
      const height = budget > 0
        ? minHeight + (budget / (maxBudget || 1)) * (maxHeight - minHeight)
        : minHeight;

      const rectY = start[1] - height / 2;
      const rectWidth = clampedEndX - clampedStartX;
      const color = api.visual('color');
      const borderRadius = Math.max(4, Math.round(height * 0.22));

      return {
        type: 'group',
        children: [
          {
            type: 'rect',
            shape: {
              x: clampedStartX,
              y: rectY,
              width: rectWidth,
              height,
              r: [borderRadius, borderRadius, borderRadius, borderRadius]
            },
            style: {
              fill: color
            }
          },
          {
            type: 'text',
            style: {
              x: clampedStartX + 8,
              y: rectY + height / 2,
              text: programName || '',
              verticalAlign: 'middle',
              align: 'left',
              fill: '#1f2937',
              font: isMobile
                ? '500 10px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,sans-serif'
                : '500 11px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,sans-serif',
              width: Math.max(rectWidth - 16, 0),
              overflow: 'truncate'
            },
            z2: 10
          }
        ],
        enterFrom: { x: clampedStartX, y: rectY, scaleX: 0.01, originX: clampedStartX },
        transition: ['shape', 'style']
      };
    },
    [isMobile, maxBudget]
  );

  const option = useMemo(() => ({
    tooltip: isMobile
      ? { show: false }
      : {
        ...TOOLTIP_CONFIG,
        trigger: 'item',
        formatter: (params) => {
          const program = params.data.program;
          const endDate = program.endDate || 'н.в.';
          const budget = program.budget ? `${program.budget} млн руб.` : 'не указан';

          return `
              <div style="font-family: ${TEXT_STYLES.tooltip.fontFamily};">
                <strong>${program.name}</strong><br/>
                Статус: ${program.status}<br/>
                Бюджет: ${budget}<br/>
                Период: ${program.startDate} — ${endDate}
              </div>
            `;
        }
      },
    legend: {
      data: statuses,
      top: 20,
      left: 'center',
      textStyle: TEXT_STYLES.legend,
      itemWidth: 20,
      itemHeight: 14,
      selected: selectedStatuses
    },
    grid: {
      left: '4%',
      right: '5%',
      top: 60,
      bottom: 90,
      containLabel: false
    },
    xAxis: {
      type: 'time',
      min: minDate,
      max: maxDate,
      axisLine: {
        lineStyle: { color: CHART_COLORS.border }
      },
      axisLabel: {
        ...TEXT_STYLES.axis,
        rotate: isMobile ? 35 : 0,
        margin: isMobile ? 12 : 8,
        formatter: (value) => {
          const date = new Date(value);
          const year = date.getFullYear();
          const month = date.getMonth() + 1;

          const chartInstance = chartRef.current?.getEchartsInstance();
          if (chartInstance) {
            const currentOption = chartInstance.getOption();
            const dataZoom = currentOption.dataZoom?.[0];
            if (dataZoom) {
              const zoomRange = dataZoom.end - dataZoom.start;
              if (zoomRange < 50) {
                return `${year}-${month.toString().padStart(2, '0')}`;
              }
            }
          }
          return year.toString();
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: CHART_COLORS.borderLight,
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: programs.map(p => p.name),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { show: false },
      splitLine: { show: false }
    },
    dataZoom: [
      {
        type: 'slider',
        xAxisIndex: 0,
        filterMode: 'weakFilter',
        height: 20,
        bottom: 20,
        start: 0,
        end: 100,
        handleIcon: 'path://M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z',
        handleSize: '80%',
        handleStyle: { color: CHART_COLORS.secondary },
        textStyle: TEXT_STYLES.axis,
        borderColor: CHART_COLORS.border,
        fillerColor: CHART_COLORS.secondary,
        moveHandleStyle: { color: CHART_COLORS.primary }
      }
    ],
    series: statuses.map((status) => ({
      type: 'custom',
      name: status,
      renderItem,
      encode: {
        x: [1, 2],
        y: 0
      },
      data: seriesData.filter(d => d.program.status === status),
      clip: true,
      itemStyle: {
        color: STATUS_COLORS[status] || '#999'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0,0,0,0.5)'
        },
        scale: true,
        scaleSize: 5
      },
      animation: true,
      animationDuration: 1000,
      animationEasing: 'cubicInOut',
      animationDurationUpdate: 500
    }))
  }), [
    statuses,
    selectedStatuses,
    isMobile,
    minDate,
    maxDate,
    programs,
    renderItem,
    seriesData
  ]);

  const onEvents = {
    click: (params) => {
      if (params.componentType === 'series') {
        setModalData(params.data.program);
      }
    },
    legendselectchanged: (params) => {
      setSelectedStatuses(params.selected);
    }
  };

  return (
    <ChartWrapper chartRef={chartRef} filename="programs-plot" className={styles.programsPlot}>
      <ReactECharts
        ref={chartRef}
        option={option}
        style={{ height: '100%', width: '100%', minHeight: '600px' }}
        onEvents={onEvents}
      />

      {modalData && (
        <div className={styles.modal} onClick={() => setModalData(null)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <button className={styles.closeButton} onClick={() => setModalData(null)}>×</button>
            <h3>{modalData.name}</h3>
            <div className={styles.modalBody}>
              <p><strong>Статус:</strong> {modalData.status}</p>
              <p><strong>Бюджет:</strong> {modalData.budget ? `${modalData.budget} млн руб.` : 'не указан'}</p>
              <p><strong>Период:</strong> {modalData.startDate} — {modalData.endDate || 'настоящее время'}</p>
              <p><strong>Описание:</strong></p>
              <p>{modalData.description}</p>
            </div>
          </div>
        </div>
      )}
    </ChartWrapper>
  );
};

ProgramsPlot.propTypes = {
  title: PropTypes.string.isRequired,
  programs: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    status: PropTypes.oneOf(VALID_STATUSES).isRequired,
    budget: PropTypes.number,
    startDate: PropTypes.string.isRequired,
    endDate: PropTypes.string,
    description: PropTypes.string.isRequired
  }))
};

export default ProgramsPlot;
