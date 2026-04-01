import React, { useCallback } from 'react';
import PropTypes from 'prop-types';
import styles from './ChartWrapper.module.scss';

const ChartWrapper = ({ children, chartRef, filename = 'chart', className = '' }) => {
  const handleDownload = useCallback(() => {
    const instance = chartRef?.current?.getEchartsInstance?.();
    if (!instance) return;
    const url = instance.getDataURL({
      type: 'png',
      pixelRatio: 2,
      backgroundColor: '#fff'
    });
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, [chartRef, filename]);

  return (
    <div className={`${styles.chartWrapper} ${className}`}>
      <button
        className={styles.downloadBtn}
        onClick={handleDownload}
        title="Скачать PNG"
        aria-label="Скачать график в формате PNG"
      >
        ↓ PNG
      </button>
      {children}
    </div>
  );
};

ChartWrapper.propTypes = {
  children: PropTypes.node.isRequired,
  chartRef: PropTypes.object.isRequired,
  filename: PropTypes.string,
  className: PropTypes.string
};

export default ChartWrapper;
