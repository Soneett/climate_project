import React, { useRef, useEffect } from 'react'
import ReactECharts from 'echarts-for-react'
var option = {
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
        title: {
            text: 'Причины смертей (на 100 000 населения)',
            left: 'center',
            top: 20
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            top: 50
        },
        series: [
            {
                name: 'Причины смертей',
                type: 'pie',
                radius: '50%',
                emphasis: {
                    itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' }
                }
            }
        ]
    },
    options: [
        {
            title: { text: 'Причины смертей — 2021' },
            series: [{
                data: [
                    { value: 1000, name: 'Все причины' },
                    { value: 400, name: 'Болезни системы кровообращения' },
                    { value: 200, name: 'Новообразования' },
                    { value: 150, name: 'Внешние причины смерти' },
                    { value: 50, name: 'Транспортные травмы' },
                    { value: 30, name: 'ДТП' },
                    { value: 20, name: 'Случайные отравления алкоголем' },
                    { value: 25, name: 'Самоубийства' },
                    { value: 10, name: 'Убийства' },
                    { value: 80, name: 'Болезни органов дыхания' },
                    { value: 60, name: 'Болезни органов пищеварения' },
                    { value: 15, name: 'Инфекционные и паразитарные болезни' },
                    { value: 5, name: 'Туберкулез' }
                ]
            }]
        },
        {
            title: { text: 'Причины смертей — 2022' },
            series: [{
                data: [
                    { value: 1020, name: 'Все причины' },
                    { value: 410, name: 'Болезни системы кровообращения' },
                    { value: 205, name: 'Новообразования' },
                    { value: 155, name: 'Внешние причины смерти' },
                    { value: 52, name: 'Транспортные травмы' },
                    { value: 32, name: 'ДТП' },
                    { value: 22, name: 'Случайные отравления алкоголем' },
                    { value: 27, name: 'Самоубийства' },
                    { value: 12, name: 'Убийства' },
                    { value: 82, name: 'Болезни органов дыхания' },
                    { value: 62, name: 'Болезни органов пищеварения' },
                    { value: 16, name: 'Инфекционные и паразитарные болезни' },
                    { value: 5, name: 'Туберкулез' }
                ]
            }]
        },
        {
            title: { text: 'Причины смертей — 2023' },
            series: [{
                data: [
                    { value: 1015, name: 'Все причины' },
                    { value: 405, name: 'Болезни системы кровообращения' },
                    { value: 210, name: 'Новообразования' },
                    { value: 152, name: 'Внешние причины смерти' },
                    { value: 53, name: 'Транспортные травмы' },
                    { value: 33, name: 'ДТП' },
                    { value: 21, name: 'Случайные отравления алкоголем' },
                    { value: 26, name: 'Самоубийства' },
                    { value: 11, name: 'Убийства' },
                    { value: 81, name: 'Болезни органов дыхания' },
                    { value: 61, name: 'Болезни органов пищеварения' },
                    { value: 15, name: 'Инфекционные и паразитарные болезни' },
                    { value: 5, name: 'Туберкулез' }
                ]
            }]
        },
        {
            title: { text: 'Причины смертей — 2024' },
            series: [{
                data: [
                    { value: 1030, name: 'Все причины' },
                    { value: 420, name: 'Болезни системы кровообращения' },
                    { value: 215, name: 'Новообразования' },
                    { value: 158, name: 'Внешние причины смерти' },
                    { value: 55, name: 'Транспортные травмы' },
                    { value: 35, name: 'ДТП' },
                    { value: 23, name: 'Случайные отравления алкоголем' },
                    { value: 28, name: 'Самоубийства' },
                    { value: 12, name: 'Убийства' },
                    { value: 83, name: 'Болезни органов дыхания' },
                    { value: 63, name: 'Болезни органов пищеварения' },
                    { value: 16, name: 'Инфекционные и паразитарные болезни' },
                    { value: 5, name: 'Туберкулез' }
                ]
            }]
        },
        {
            title: { text: 'Причины смертей — 2025' },
            series: [{
                data: [
                    { value: 1040, name: 'Все причины' },
                    { value: 430, name: 'Болезни системы кровообращения' },
                    { value: 220, name: 'Новообразования' },
                    { value: 160, name: 'Внешние причины смерти' },
                    { value: 56, name: 'Транспортные травмы' },
                    { value: 36, name: 'ДТП' },
                    { value: 24, name: 'Случайные отравления алкоголем' },
                    { value: 29, name: 'Самоубийства' },
                    { value: 12, name: 'Убийства' },
                    { value: 85, name: 'Болезни органов дыхания' },
                    { value: 64, name: 'Болезни органов пищеварения' },
                    { value: 16, name: 'Инфекционные и паразитарные болезни' },
                    { value: 5, name: 'Туберкулез' }
                ]
            }]
        }
    ]
};

export default function MyChart() {
    const ref = useRef(null);

    useEffect(() => {
        const echartsInstance = ref.current?.getEchartsInstance?.();
        function handleResize() {
            echartsInstance?.resize();
        }
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div style={{ width: '100%', height: 600 }}>
            <ReactECharts
                ref={ref}
                option={option}
                style={{ height: '100%', width: '100%' }}
                notMerge={false}
                lazyUpdate={true}
            />
        </div>
    );
}