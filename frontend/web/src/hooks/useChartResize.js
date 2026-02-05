import { useEffect } from 'react';

/**
 * Custom hook to handle chart resize on window resize events
 * @param {Object} chartRef - React ref object pointing to the chart instance
 */
export const useChartResize = (chartRef) => {
  useEffect(() => {
    const handleResize = () => {
      chartRef.current?.getEchartsInstance()?.resize();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [chartRef]);
};
