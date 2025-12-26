import React, { useRef, useEffect } from "react";
import ReactECharts from "echarts-for-react";
import styles from "./LineChart.module.scss";

/* корректное объявление опций */
const lineOption = {
  title: { text: "Демографические показатели региона", left: "center" },
  tooltip: { trigger: "axis" },
  legend: { data: ["Население", "Родившиеся", "Умершие", "Миграция"], top: 40 },
  grid: { left: "3%", right: "4%", bottom: "6%", containLabel: true },
  toolbox: { feature: { saveAsImage: {} } },
  xAxis: { type: "category", name: "Год", nameLocation: "middle", nameGap: 25, data: ["2021", "2022", "2023", "2024", "2025"] },
  yAxis: { type: "value", name: "Количество людей" },
  series: [
    { name: "Население", type: "line", data: [120000, 130500, 115000, 100500, 126000], smooth: true },
    { name: "Родившиеся", type: "line", data: [15000, 20800, 14700, 14500, 14400], smooth: true },
    { name: "Умершие", type: "line", data: [8000, 8200, 8300, 8400, 18500], smooth: true },
    { name: "Миграция", type: "line", data: [2000, 1800, 2200, 2100, 2300], smooth: true }
  ]
};

const LineChart = ({ type = "line" }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const handleResize = () => chartRef.current?.getEchartsInstance?.()?.resize?.();
    window.addEventListener("resize", handleResize);
    // один вызов при монтировании
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className={styles.chart}>
      <ReactECharts
        ref={chartRef}
        className={styles.echarts}
        option={lineOption}
        style={{ width: "100%", height: "100%" }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
};

export default LineChart;