<template>
  <div id="anglesPolarBarChart" style="width: 300px; height: 300px;"/>
</template>

<script>
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  PolarComponent,
  TooltipComponent
} from 'echarts/components';
import { BarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  PolarComponent,
  TooltipComponent,
  BarChart,
  CanvasRenderer
]);

export default {
  name: "polarBarChart",
  mounted() {
    this.showChart()
  },
  methods: {
    showChart() {
      let myChart = echarts.init(document.getElementById('anglesPolarBarChart'))
      let option = {
        title: [
          {
            text: '视频中各类夹角的均值'
          }
        ],
        polar: {
          radius: [30, '80%'],
          tooltip: {
            show: true,
            borderColor: 'rgba(211, 253, 250, 0.8)'
          }
        },
        textStyle: {
          color: '#FFFFFF'
        },
        angleAxis: {
          max: 360,
          startAngle: 105
        },
        radiusAxis: {
          type: 'category',
          data: ['小臂大臂夹角', '大臂躯干夹角', '小腿大腿夹角', '大腿躯干夹角', '球初速度水平夹角'],
          // axisLine: {
          //   show: true,
          //   lineStyle: {
          //     color: 'rgba(211, 253, 250, 0.8)'
          //   }
          // }
        },
        tooltip: {},
        series: {
          type: 'bar',
          data: [158.2 , 81.5, 127.8, 135.7, 102.85],
          coordinateSystem: 'polar',
          label: {
            show: true,
            position: 'middle',
            formatter: '{b}'
          }
        }
      }
      myChart.setOption(option)
    }
  }
}
</script>

<style scoped>

</style>
