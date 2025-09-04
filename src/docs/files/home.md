# FutureFoods Food Systems Data Model

Aim is to create a harmonised data model.

<div id="indicators-sunburst-chart" style="width: 100; height: 600px;"></div>

<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
<script type="text/javascript">
  var chartDom = document.getElementById('indicators-sunburst-chart');
  var myChart = echarts.init(chartDom);

  fetch("../data/indicators_chart_data.json")
    .then(r => r.json())
    .then(data => {
      var option = {
        radius: [0, '95%'],
        emphasis: {
          focus: 'ancestor'
        },
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
          label: {
            overflow: 'break'
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
              r: '65%',
              label: {
                rotate: 'tangential',
                overflow: 'break',
                formatter: function(params) {
                  const name = params.name;
                  return name.length > 12 ? name.slice(0,12) + '…' : name;
                }
              }
            },
            {
              r0: '65%',
              r: '90%',
              label: {
                rotate: 'tangential',
                overflow: 'break',
                padding: 3,
                silent: false,
                formatter: function(params) {
                  const name = params.name;
                  return name.length > 12 ? name.slice(0,12) + '…' : name;
                }
              },
              tooltip: {
                show: true,
                formatter: function(params) {
                  return params.name + ': ' + (params.value || '');
                }
              }
            }
          ]
        }
      };
      myChart.setOption(option);
    });

  window.addEventListener('resize', function() {
    myChart.resize();
  });
</script>
