<template>
  <q-card
    class="my-card text-white"
  >
    <q-card-section horizontal>
      <q-card-section>
        <video controls width="270" height="180" :src="'http://localhost:3000/api/videos/' + video_id" type="video/mp4"></video>
      </q-card-section>

      <q-card-section>
        <div class="text-subtitle2">学号：{{ uploader_id || "19231001"}}</div>
        <div class="text-subtitle2">上传者：{{ uploader_name || "jack" }}</div>
        <div class="text-subtitle2">授课老师：李红</div>
        <div class="text-subtitle2">上传时间：{{ time || "2021.7.6" }}</div>
        <div class="text-subtitle2">视频评分：80</div>
        <q-btn icon-right="arrow_forward" :to="'/analysis/' + video_id" style="margin-top: 20px">查看分析</q-btn>
      </q-card-section>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "VideoItem",
  props: {
    time: String,
    uploader_id: String,
    uploader_name: String,
    video_id: String
  },
}
</script>

<style scoped>
.my-card {
  background: radial-gradient(circle, #35a2ff 0%, #014a88 100%);
}
</style>
