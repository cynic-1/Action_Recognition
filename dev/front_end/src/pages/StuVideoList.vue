<template>
  <div style="margin-top: 30px">
    <q-card
      class="my-card text-white"
      style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%); width: 80%; margin-left: auto; margin-right: auto;margin-bottom: 30px"
      v-for="x in 8"
      :key="x"
    >
      <q-card-section horizontal>
        <q-card-section>
          <q-video
            style="width: 70%;height: 150px;margin-right: 200px"
            src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
          />
        </q-card-section>

        <q-card-section style="margin-right: 200px">
          <div class="text-h6">学号：1234566</div>
          <div class="text-h6" style="margin-bottom: 20px">上传者：jack</div>
          <div class="text-subtitle2">授课老师：李红</div>
          <div class="text-subtitle2">上传时间：2021.7.6</div>
          <div class="text-subtitle2">视频编号：123456789</div>
        </q-card-section>

        <q-card-section>
          <q-btn size="lg" icon-right="arrow_forward" style="margin-top: 80px" to="/rate">Go to check</q-btn>
        </q-card-section>
      </q-card-section>
    </q-card>

  </div>
</template>

<script>
export default {
  name: "StuVideoList"
}
</script>

<style scoped>

</style>
