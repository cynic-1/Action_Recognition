<template>
  <div
    id="researchLineChart"
    style="min-height: 300px; min-width: 800px"
  />
</template>

<script>
import * as echarts from "echarts/core";
import {
  GridComponent,
  LegendComponent,
  TitleComponent,
  ToolboxComponent,
  TooltipComponent
} from "echarts/components";
import { LineChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import { onMounted, onUnmounted, watch } from "vue";

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

export default {
  "name": "LineChart",
  setup () {

    let option; let chart;
    option = {
      "tooltip": {
        "trigger": "axis"
      },
      "legend": {
        "textStyle": {
          "fontSize": "20"
        },
        "data": ["动作质量得分", "动作稳定性得分"]
      },
      "grid": {
        "left": "3%",
        "right": "4%",
        "bottom": "3%",
        "containLabel": true
      },
      "xAxis": {
        "type": "category",
        "boundaryGap": false,
        "data": [1,2,3,4,5,6,7,8,9]
      },
      "yAxis": {
        "type": "value"
      },
      "series": [
        {
          "name": "动作质量得分",
          "type": "line",
          "data": [65, 74, 70, 82, 86, 92, 98, 97, 98]
        },
        {
          name: "动作稳定性得分",
          type: "line",
          stack: "Total",
          data: [33, 42, 46, 24, 56, 88, 79, 92, 96]
        }
      ]
    };
    function initChart () {

      chart = echarts.init(document.getElementById("researchLineChart"));
      // 把配置和数据放这里
      // 在 setup 中你应该避免使用 this，因为它不会找到组件实例。setup 的调用发生在 data property、computed property 或 methods 被解析之前，所以它们无法在 setup 中被获取。
      chart.setOption(option);
      window.onresize = function () {

        // 自适应大小
        chart.resize();

      };

    }

    onMounted(() => {

      initChart();

    });

    onUnmounted(() => {

      echarts.dispose(chart);

    });

    watch(
      option,
      (newOptions) => {

        chart.value.setOption(newOptions);

      },
      { "deep": true }
    );

    return {
      option
    };

  }
};
</script>

<style scoped>

</style>
