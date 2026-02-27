import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import ReactECharts from 'echarts-for-react';
import { useChartResize } from '../../../hooks/useChartResize';
import {
  TOOLTIP_CONFIG,
  TEXT_STYLES,
  CHART_COLORS
} from '../chartConfig';
import styles from './ProgramsPlot.module.scss';

// Status colors matching project palette
const STATUS_COLORS = {
  'завершена': '#81C784',      // green
  'в процессе': '#64B5F6',     // blue
  'приостановлена': '#FFD54F',  // yellow
  'не реализована': '#E57373'   // red
};

const VALID_STATUSES = Object.keys(STATUS_COLORS);

const ProgramsPlot = ({ title, programs = [] }) => {
  const chartRef = useRef(null);
  const [modalData, setModalData] = useState(null);
  const [selectedStatuses, setSelectedStatuses] = useState({});
  useChartResize(chartRef);

  // Parse date string "YYYY-MM" to timestamp
  const parseDate = (dateStr) => {
    if (!dateStr) return null;
    const [year, month] = dateStr.split('-').map(Number);
    return new Date(year, month - 1, 1).getTime();
  };

  // Define timeline range
  const minDate = parseDate('2020-01');
  const maxDate = parseDate('2024-12');

  // Get unique statuses for legend
  const statuses = [...new Set(programs.map(p => p.status))];
  
  // Initialize selected statuses on mount
  React.useEffect(() => {
    if (statuses.length > 0 && Object.keys(selectedStatuses).length === 0) {
      const initialSelected = {};
      statuses.forEach(status => {
        initialSelected[status] = true;
      });
      setSelectedStatuses(initialSelected);
    }
  }, [statuses.length]); // eslint-disable-line react-hooks/exhaustive-deps

  // Prepare data for custom series
  const seriesData = programs.map((program, index) => {
    const startTime = parseDate(program.startDate);
    const endTime = program.endDate ? parseDate(program.endDate) : maxDate;
    const budget = program.budget || 0;
    
    return {
      name: program.name,
      value: [
        index,           // y position (program index)
        startTime,       // start time
        endTime,         // end time
        budget,          // budget for height calculation
        program.status   // status for color
      ],
      itemStyle: {
        color: STATUS_COLORS[program.status] || '#999'
      },
      program: program  // store full program data
    };
  });

  // Calculate bar height based on budget
  const maxBudget = Math.max(...programs.map(p => p.budget || 0));
  const minHeight = 15;
  const maxHeight = 40;

  const renderItem = (params, api) => {
    const yIndex = api.value(0);
    const start = api.coord([api.value(1), yIndex]);
    const end = api.coord([api.value(2), yIndex]);
    const budget = api.value(3);
    
    // Get grid boundaries from params.coordSys
    const gridLeft = params.coordSys.x;
    const gridRight = params.coordSys.x + params.coordSys.width;
    
    // Clamp coordinates to grid boundaries
    const clampedStartX = Math.max(start[0], gridLeft);
    const clampedEndX = Math.min(end[0], gridRight);
    
    // Don't render if completely outside boundaries
    if (clampedStartX >= clampedEndX) {
      return null;
    }
    
    // Calculate height based on budget
    const height = budget > 0 
      ? minHeight + (budget / maxBudget) * (maxHeight - minHeight)
      : minHeight;
    
    const rectWidth = clampedEndX - clampedStartX;
    
    return {
      type: 'rect',
      shape: {
        x: clampedStartX,
        y: start[1] - height / 2,
        width: rectWidth,
        height: height
      },
      style: api.style(),
      // Left-to-right appearance animation
      enterFrom: {
        x: clampedStartX,
        y: start[1] - height / 2,
        width: 0,
        opacity: 0
      },
      leaveTo: {
        x: clampedEndX,
        width: 0,
        opacity: 0
      },
      transition: ['shape', 'style']
    };
  };

  const option = {
    tooltip: {
      ...TOOLTIP_CONFIG,
      formatter: (params) => {
        const program = params.data.program;
        const startDate = program.startDate;
        const endDate = program.endDate || 'н.в.';
        const budget = program.budget ? `${program.budget} млн руб.` : 'не указан';
        
        return `
          <div style="font-family: ${TEXT_STYLES.tooltip.fontFamily};">
            <strong>${program.name}</strong><br/>
            Статус: ${program.status}<br/>
            Бюджет: ${budget}<br/>
            Период: ${startDate} — ${endDate}
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
      left: '15%',
      right: '8%',
      top: 70,
      bottom: 90,
      containLabel: true
    },
    xAxis: {
      type: 'time',
      min: minDate,
      max: maxDate,
      axisLine: {
        lineStyle: {
          color: CHART_COLORS.border
        }
      },
      axisLabel: {
        ...TEXT_STYLES.axis,
        formatter: (value) => {
          const date = new Date(value);
          const year = date.getFullYear();
          const month = date.getMonth() + 1;
          
          // Get current dataZoom range to determine zoom level
          const chartInstance = chartRef.current?.getEchartsInstance();
          if (chartInstance) {
            const option = chartInstance.getOption();
            const dataZoom = option.dataZoom?.[0];
            if (dataZoom) {
              const zoomRange = dataZoom.end - dataZoom.start;
              // Show months if zoomed in (less than 50% of timeline visible)
              if (zoomRange < 50) {
                return `${year}-${month.toString().padStart(2, '0')}`;
              }
            }
          }
          
          // Default to showing only years
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
      axisLine: {
        lineStyle: {
          color: CHART_COLORS.border
        }
      },
      axisLabel: {
        ...TEXT_STYLES.axis,
        width: 150,
        overflow: 'truncate',
        ellipsis: '...'
      },
      splitLine: {
        show: false
      }
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
        handleStyle: {
          color: CHART_COLORS.secondary
        },
        textStyle: TEXT_STYLES.axis,
        borderColor: CHART_COLORS.border,
        fillerColor: CHART_COLORS.secondary,
        moveHandleStyle: {
          color: CHART_COLORS.primary
        }
      }
    ],
    series: statuses.map(status => ({
      type: 'custom',
      name: status,
      renderItem: renderItem,
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
  };

  const onChartClick = (params) => {
    if (params.componentType === 'series') {
      setModalData(params.data.program);
    }
  };

  const onLegendSelectChanged = (params) => {
    setSelectedStatuses(params.selected);
  };
  
  const onEvents = {
    click: onChartClick,
    legendselectchanged: onLegendSelectChanged
  };

  const closeModal = () => {
    setModalData(null);
  };

  return (
    <div className={styles.programsPlot}>
      <ReactECharts 
        ref={chartRef} 
        option={option} 
        style={{ height: '100%', width: '100%', minHeight: '600px' }}
        onEvents={onEvents}
      />
      {modalData && (
        <div className={styles.modal} onClick={closeModal}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <button className={styles.closeButton} onClick={closeModal}>×</button>
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
    </div>
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
