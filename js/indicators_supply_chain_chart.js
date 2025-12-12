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
