<template>
  <q-card
    class="my-card text-white"
  >
    <q-card-section horizontal>
      <q-card-section>
        <video controls width="300" height="200" src="http://localhost:3000/api/video/get/61ff6f3e38c71eb3be910a51" type="video/mp4"></video>
      </q-card-section>

      <q-card-section>
        <div class="text-h6">学号：1234566</div>
        <div class="text-h6">上传者：jack</div>
        <div class="text-subtitle2">授课老师：李红</div>
        <div class="text-subtitle2">上传时间：2021.7.6</div>
        <div class="text-subtitle2">视频编号：123456789</div>
        <div class="text-subtitle2">视频评分：80</div>
      </q-card-section>

      <q-card-section>
        <q-btn size="lg" icon-right="arrow_forward" to="/analysis">查看分析</q-btn>
      </q-card-section>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "VideoItem"
}
</script>

<style scoped>
.my-card {
  background: radial-gradient(circle, #35a2ff 0%, #014a88 100%);
}
</style>
