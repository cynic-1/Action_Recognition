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
            <q-tree
              :nodes="props"
              node-key="label"
              v-model:selected="selected"
              default-expand-all
            />
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
import { ref } from 'vue'
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
    const selected = ref(null)
    return {
      tab: 'list',
      selected,
      props: [
        {
          label: '我的上传',
          children: [
            {
              label: '2019年春季学期',
              children: [
                { label: '2019.03.12' },
                { label: '2019.03.19' },
                { label: '2019.03.26' },
                { label: '2019.04.05' },
              ]
            },
            {
              label: '2019年秋季学期',
              children: [
                { label: '2019.09.03' },
                { label: '2019.09.10' },
                { label: '2019.09.17' },
                { label: '2019.09.24' },
              ]
            },
            {
              label: '2020年春季学期',
              children: [
                { label: '2020.03.17' },
                { label: '2019.04.12' },
                { label: '2019.05.16' },
                { label: '2019.06.02' },
              ]
            }
          ]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
