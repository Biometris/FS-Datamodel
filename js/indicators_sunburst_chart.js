var chartDom = document.getElementById('indicators-sunburst-chart');
var sunburstChart = echarts.init(chartDom);

fetch("data/indicators_sunburst_chart_data.json")
  .then(r => r.json())
  .then(data => {
    var option = {
      tooltip: {
          show: true,
          trigger: 'item',
          formatter: function(params) {
              return params.name;
          }
      },
      series: {
        type: 'sunburst',
        data: data,
        radius: [0, '95%'],
        emphasis: {
          focus: 'ancestor'
        },
        levels: [
          {},
          {
            r0: '15%',
            r: '35%',
            label: {
              rotate: 'tangential',
              overflow: 'break'
            }
          },
          {
            r0: '35%',
            r: '92%',
            label: {
              overflow: 'break',
              formatter: function(params) {
                const name = params.name;
                return name.length > 20 ? name.slice(0,20) + '…' : name;
              }
            }
          },
          {
            r0: '92%',
            r: '98%',
            label:  {
              overflow: 'break',
              formatter: function(params) {
                const name = params.name;
                return ' ';
              }
            },
            tooltip: {
              show: true,
              formatter: function(params) {
                return params.name + ': ' + (params.value || '');
              }
            },
            itemStyle: {
              borderWidth: 3
            }
          }
        ]
      }
    };
    sunburstChart.setOption(option);
  });

window.addEventListener('resize', function() {
  sunburstChart.resize();
});
