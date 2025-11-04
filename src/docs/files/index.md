# FutureFoods Food Systems Data Model

The aim is to establish a harmonised data model for structured collection of metadata on Food Systems indicators.

## Supply chain component hierarchy tree

<div id="indicators-tree-chart" style="width: 100; height: 600px;"></div>

## Dimension sunburst diagram

<div id="indicators-sunburst-chart" style="width: 100; height: 600px;"></div>

<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>

<script type="text/javascript">
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
</script>

<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>

<script type="text/javascript">
  var chartDom = document.getElementById('indicators-tree-chart');
  var treeChart = echarts.init(chartDom);

  fetch("data/indicators_supply_chain_chart_data.json")
    .then(r => r.json())
    .then(data => {
      var option = {
        tooltip: {
            show: true,
            trigger: 'item',
            triggerOn: 'mousemove',
            formatter: function(params) {
                return params.name;
            }
        },
        series: {
          type: 'tree',
          data: [data],
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            position: 'left',
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 9,
            formatter: function(params) {
                return params.name;
              }
          },
          leaves: {
            label: {
              position: 'right',
              verticalAlign: 'middle',
              align: 'left',
              overflow: 'break',
              formatter: function(params) {
                return params.name;
              }
            }
          },
          emphasis: {
            focus: 'descendant'
          },          
          expandAndCollapse: true,
          animationDuration: 550,
          animationDurationUpdate: 750,
          initialTreeDepth: 3
        }
      };
      treeChart.setOption(option);
    });

  window.addEventListener('resize', function() {
    treeChart.resize();
  });
</script>