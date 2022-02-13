<template>
  <div style="margin-top: 30px">
    <div class="q-gutter-y-md" style="max-width: 600px;margin-left: auto;margin-right: auto">
        <q-tabs
          v-model="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="list" label="视频列表" />
          <q-tab name="analysis" label="学习分析" />
        </q-tabs>
    </div>
    <q-separator />
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="list">
        <q-card
          class="my-card text-white"
          style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%); width: 80%; margin-left: auto; margin-right: auto;margin-bottom: 30px"
          v-for="x in 8"
          :key="x"
        >
          <q-card-section horizontal>
            <q-card-section>
              <q-video
                style="width: 350px;height: 150px;margin-right: 60px"
                src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
              />
            </q-card-section>

            <q-card-section style="margin-right: 200px">
              <div class="text-h6">学号：1234566</div>
              <div class="text-h6" style="margin-bottom: 20px">上传者：张三</div>
              <div class="text-subtitle2">授课老师：李红</div>
              <div class="text-subtitle2">上传时间：2021.7.6</div>
              <div class="text-subtitle2">视频编号：123456789</div>
            </q-card-section>

            <q-card-section>
              <q-btn size="lg" icon-right="arrow_forward" style="margin-top: 80px" to="/rate">Go to check</q-btn>
            </q-card-section>
          </q-card-section>
        </q-card>
      </q-tab-panel>

      <q-tab-panel name="analysis">
        <line-chart/>
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script>
import {defineAsyncComponent} from "vue";
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));
export default {
  name: "StuVideoList",
  components: {
    lineChart
  },
  data(){
    return {
      tab: 'list',
    }
  }
}
</script>

<style scoped>

</style>
