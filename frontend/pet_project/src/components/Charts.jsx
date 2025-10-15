import React, { useRef, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';

const lineOption = {
    title: {
        text: 'Демографические показатели региона',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['Население', 'Родившиеся', 'Умершие', 'Миграция'],
        top: 30
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        name: 'Год',
        nameLocation: 'middle',
        nameGap: 25,
        data: ['2021', '2022', '2023', '2024', '2025']
    },
    yAxis: {
        type: 'value',
        name: 'Количество людей'
    },
    series: [
        { name: 'Население', type: 'line', data: [120000, 121500, 123000, 124500, 126000], smooth: true },
        { name: 'Родившиеся', type: 'line', data: [15000, 14800, 14700, 14500, 14400], smooth: true },
        { name: 'Умершие', type: 'line', data: [8000, 8200, 8300, 8400, 8500], smooth: true },
        { name: 'Миграция', type: 'line', data: [2000, 1800, 2200, 2100, 2300], smooth: true }
    ]
};

// Круговой график причин смертей с динамикой
const pieOption = {
    baseOption: {
        timeline: {
            axisType: 'category',
            data: ['2021', '2022', '2023', '2024', '2025'],
            autoPlay: false,
            playInterval: 2000,
            left: 'center',
            bottom: 0,
            width: '70%',
            label: { formatter: '{value}' }
        },
        title: { text: 'Причины смертей (на 100 000 населения)', left: 'center', top: 20 },
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        legend: [
            { orient: 'vertical', left: '5%', top: 50, data: ['Болезни системы кровообращения','Новообразования','Внешние причины смерти','Транспортные травмы','ДТП','Случайные отравления алкоголем'] },
            { orient: 'vertical', right: '5%', top: 50, data: ['Самоубийства','Убийства','Болезни органов дыхания','Болезни органов пищеварения','Инфекционные и паразитарные болезни','Туберкулез'] }
        ],
        series: [{
            name: 'Причины смертей',
            type: 'pie',
            radius: '50%',
            center: ['50%', '55%'],
            emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } }
        }]
    },
    options: [
        { title: { text: 'Причины смертей — 2021' }, series: [{ data: [ { value: 400, name: 'Болезни системы кровообращения' }, { value: 220, name: 'Новообразования' }, { value: 160, name: 'Внешние причины смерти' }, { value: 60, name: 'Транспортные травмы' }, { value: 35, name: 'ДТП' }, { value: 25, name: 'Случайные отравления алкоголем' }, { value: 30, name: 'Самоубийства' }, { value: 12, name: 'Убийства' }, { value: 90, name: 'Болезни органов дыхания' }, { value: 70, name: 'Болезни органов пищеварения' }, { value: 18, name: 'Инфекционные и паразитарные болезни' }, { value: 6, name: 'Туберкулез' } ] }] },
        { title: { text: 'Причины смертей — 2022' }, series: [{ data: [ { value: 480, name: 'Болезни системы кровообращения' }, { value: 260, name: 'Новообразования' }, { value: 200, name: 'Внешние причины смерти' }, { value: 75, name: 'Транспортные травмы' }, { value: 42, name: 'ДТП' }, { value: 32, name: 'Случайные отравления алкоголем' }, { value: 38, name: 'Самоубийства' }, { value: 15, name: 'Убийства' }, { value: 105, name: 'Болезни органов дыхания' }, { value: 78, name: 'Болезни органов пищеварения' }, { value: 20, name: 'Инфекционные и паразитарные болезни' }, { value: 8, name: 'Туберкулез' } ] }] },
        { title: { text: 'Причины смертей — 2023' }, series: [{ data: [ { value: 420, name: 'Болезни системы кровообращения' }, { value: 290, name: 'Новообразования' }, { value: 220, name: 'Внешние причины смерти' }, { value: 85, name: 'Транспортные травмы' }, { value: 50, name: 'ДТП' }, { value: 36, name: 'Случайные отравления алкоголем' }, { value: 42, name: 'Самоубийства' }, { value: 18, name: 'Убийства' }, { value: 110, name: 'Болезни органов дыхания' }, { value: 88, name: 'Болезни органов пищеварения' }, { value: 22, name: 'Инфекционные и паразитарные болезни' }, { value: 10, name: 'Туберкулез' } ] }] },
        { title: { text: 'Причины смертей — 2024' }, series: [{ data: [ { value: 500, name: 'Болезни системы кровообращения' }, { value: 270, name: 'Новообразования' }, { value: 240, name: 'Внешние причины смерти' }, { value: 95, name: 'Транспортные травмы' }, { value: 55, name: 'ДТП' }, { value: 38, name: 'Случайные отравления алкоголем' }, { value: 48, name: 'Самоубийства' }, { value: 20, name: 'Убийства' }, { value: 115, name: 'Болезни органов дыхания' }, { value: 92, name: 'Болезни органов пищеварения' }, { value: 25, name: 'Инфекционные и паразитарные болезни' }, { value: 12, name: 'Туберкулез' } ] }] },
        { title: { text: 'Причины смертей — 2025' }, series: [{ data: [ { value: 530, name: 'Болезни системы кровообращения' }, { value: 320, name: 'Новообразования' }, { value: 260, name: 'Внешние причины смерти' }, { value: 110, name: 'Транспортные травмы' }, { value: 60, name: 'ДТП' }, { value: 42, name: 'Случайные отравления алкоголем' }, { value: 52, name: 'Самоубийства' }, { value: 22, name: 'Убийства' }, { value: 120, name: 'Болезни органов дыхания' }, { value: 95, name: 'Болезни органов пищеварения' }, { value: 28, name: 'Инфекционные и паразитарные болезни' }, { value: 15, name: 'Туберкулез' } ] }] }
    ]
};

export default function Dashboard() {
    const lineRef = useRef(null);
    const pieRef = useRef(null);

    useEffect(() => {
        const handleResize = () => {
            lineRef.current?.getEchartsInstance()?.resize();
            pieRef.current?.getEchartsInstance()?.resize();
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div>
            <div style={{ width: '100%', height: 400, marginBottom: 50 }}>
                <ReactECharts ref={lineRef} option={lineOption} style={{ height: '100%', width: '100%' }} />
            </div>
            <div style={{ width: '100%', height: 600 }}>
                <ReactECharts ref={pieRef} option={pieOption} style={{ height: '100%', width: '100%' }} />
            </div>
        </div>
    );
}
