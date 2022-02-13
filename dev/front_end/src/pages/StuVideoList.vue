<template>
  <div class="q-pt-md">
  <div class="q-gutter-y-md" style="max-width: 600px;margin-left: auto;margin-right: auto;">
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
    <q-separator/>
  </div>
  <div>
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="list">
        <left-drawer>
          <template #leftDrawer>
            此处应有一个列表进行筛选
          </template>
          <template #main>
            <template
              v-for="x in 3"
              :key="x">
              <div style="margin-left: auto;margin-right: auto">
                <video-item/>
              </div>
            </template>
          </template>
        </left-drawer>
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
const videoItem = defineAsyncComponent(() => import("components/VideoItem"));
const leftDrawer = defineAsyncComponent(() => import("../layouts/LeftDrawer"))
export default {
  name: "StuVideoList",
  components: {
    videoItem,
    lineChart,
    leftDrawer
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
