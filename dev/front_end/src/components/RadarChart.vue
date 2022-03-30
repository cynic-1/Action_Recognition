<template>
  <div id="radarChart" style="width: 500px; height: 300px;"/>
</template>

<script>
import * as echarts from 'echarts/core';
import { TitleComponent, LegendComponent } from 'echarts/components';
import { RadarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([TitleComponent, LegendComponent, RadarChart, CanvasRenderer]);
export default {
  name: "RadarChart",
  mounted() {
    this.showChart()
  },
  methods: {
    showChart() {
      let myChart = echarts.init(document.getElementById('radarChart'))

      let option = {
        color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C'],
        title: {
          text: '能力评价'
        },
        legend: {},
        radar: [
          {
            indicator: [
              { text: '协调性', max: 100, color: '#FFFFFF' },
              { text: '准确性', max: 100, color: '#FFFFFF' },
              { text: '完整性', max: 100, color: '#FFFFFF' },
              { text: '灵活性', max: 100, color: '#FFFFFF' },
              { text: '连续性', max: 100, color: '#FFFFFF' },
            ],
            center: ['60%', '50%'],
            radius: 120,
            startAngle: 90,
            splitNumber: 4,
            shape: 'circle',
            axisName: {
              formatter: '【{value}】',
              color: '#428BD4'
            },
            splitArea: {
              areaStyle: {
                color: ['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
                shadowColor: 'rgba(0, 0, 0, 0.2)',
                shadowBlur: 10
              }
            },
            axisLine: {
              lineStyle: {
                color: 'rgba(211, 253, 250, 0.8)'
              }
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(211, 253, 250, 0.8)'
              }
            }
          },
        ],
        series: [
          {
            type: 'radar',
            emphasis: {
              lineStyle: {
                width: 4
              }
            },
            data: [
              {
                value: [72, 80, 83, 72, 77],
                name: '年级平均'
              },
              {
                value: [80, 77, 84, 76, 82],
                name: '班级平均',
                areaStyle: {
                  color: 'rgba(255, 228, 52, 0.6)'
                }
              },
              {
                value: [84, 91, 89, 92, 95],
                name: '你的表现',
                areaStyle: {
                  color: 'rgba(231, 22, 52, 0.3)'
                }
              }
            ]
          },
        ]
      };
      myChart.setOption(option)
    }
  }
}
</script>

<style scoped>

</style>
