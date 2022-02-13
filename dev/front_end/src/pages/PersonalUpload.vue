<template>
  <div style="margin-top: 30px">
    <div class="personal-menu-card">
      <q-card class="personal">
        <q-card-section
          horizontal
          style="padding-top: 30px;padding-bottom: 30px"
        >
          <q-btn
            round
            @click="alert = true"
          >
            <q-avatar size="120px" >
              <img :src="this.imgUrl" alt="用户头像">
            </q-avatar>
          </q-btn>

          <q-card-actions
            vertical
            class="justify-around"
            style="padding-left: 100px"
          >
            <div class="q-py-sm">
              <span class="text-weight-bold text-h4">姓名--{{ name }}</span>
            </div>
            <div class="q-py-sm">
              <span class="text-grey text-h5">学号--{{ id }}</span>
            </div>
          </q-card-actions>
        </q-card-section>
      </q-card>
      <br><br>
    </div>

    <div class="text-h4 row" style="margin-left: 100px;margin-bottom: 30px">
      <span>我的上传：</span>
      <q-btn color="blue" rounded style="margin-left: 70%">上传视频</q-btn>
    </div>
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
          <div class="text-subtitle2">视频评分：80</div>
        </q-card-section>

        <q-card-section>
          <q-btn size="lg" icon-right="arrow_forward" style="margin-top: 80px" to="/analysis">查看分析</q-btn>
        </q-card-section>
      </q-card-section>
    </q-card>

  </div>
</template>

<script>
export default {
  name: "PersonalUpload",
  data() {
    return  {
      imgUrl: '',
      alert: false,
      id: 12345678,
      name: 'jack london'
    }
  }

}
</script>

<style scoped>
.personal-menu-card {
  width: 100%;
  padding-bottom: 40px;
}
.personal{
  padding-left: 30%;
}
</style>
