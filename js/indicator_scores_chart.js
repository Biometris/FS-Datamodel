var chartDom = document.getElementById('indicator-scores-heatmap');
var heatmapChart = echarts.init(chartDom);

fetch("../data/indicator_scores_chart_data.json")
    .then(r => r.json())
    .then(data => {
        var option = {
        tooltip: {
            position: 'top'
        },
        grid: {
            height: '50%',
            top: '10%'
        },
        xAxis: {
            type: 'category',
            position: 'top',
            axisLabel: {
                show: true,
                rotate: 45
            },
            splitArea: {
                show: true
            }
        },
        yAxis: {
            type: 'category',            
            splitArea: {
                show: true
            }
        },
        visualMap: {
            show: false,
            min: 0,
            max: 2,
            calculable: true,
            orient: 'horizontal',
            bottom: '5%',
            inRange: {
                color: ['#e74c3c', '#f39c12', '#2ecc71']
            }
        },   
        series: [
            {
                type: 'heatmap',
                data: data,
                label: {
                    show: false
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]        
        };
        heatmapChart.setOption(option);
    });

window.addEventListener('resize', function() {
    heatmapChart.resize();
});
