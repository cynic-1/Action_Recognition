<template>
  <div style="margin-top: 30px">
    <div class="personal-menu-card">
      <q-card>
        <q-card-section horizontal>
        <q-card-section
          horizontal
        >
            <q-avatar size="120px">
              <img :src="this.imgUrl" alt="用户头像">
            </q-avatar>
          <q-card-section
            vertical
            style="padding-left: 100px"
          >
            <div class="q-py-sm">
              <span class="text-weight-bold text-h4">姓名--{{ name }}</span>
            </div>
            <div class="q-py-sm">
              <span class="text-grey text-h5">学号--{{ id }}</span>
            </div>
          </q-card-section>
        </q-card-section>
        <q-card-section vertical>
          <line-chart/>
        </q-card-section>
        </q-card-section>
      </q-card>
      <br><br>
    </div>
    <div class="row" style="width: 100%;">
      <div>
        <q-card v-if="!editing" class="info q-pa-md">
          <div class="text-h4">
            课程信息
            <q-btn rounded icon="more" flat class="text-right text-h5">更多</q-btn>
          </div>

<!--          <div class="text-h5 text-grey" style="margin: 20px">学号：{{id}}</div>-->
<!--          <div class="text-h5 text-grey" style="margin: 20px">姓名：{{name}}</div>-->
<!--          <div class="text-h5 text-grey" style="margin: 20px">邮箱：{{email}}</div>-->
          <div class="text-h5 text-grey">当前课程：{{course}}</div>
          <div class="text-h5 text-grey">任课老师：{{teacher}}</div>
        </q-card>
<!--        <q-card v-else class="info">-->
<!--          <div class="text-h3">个人信息</div>-->
<!--          <q-input label="学号" v-model="id"></q-input>-->
<!--          <q-input label="姓名" v-model="name"></q-input>-->
<!--          <q-input label="邮箱" v-model="email"></q-input>-->
<!--          <q-input label="课程" v-model="course"></q-input>-->
<!--          <q-input label="任课老师" v-model="teacher"></q-input>-->
<!--          <q-btn rounded style="margin-left: 35%;margin-top: 30px" size="lg" @click="save">保存</q-btn>-->
<!--        </q-card>-->
      </div>
      <div class="upload">
        <div class="text-h4 text-grey row" style="width: 80%; margin-left: auto; margin-right: auto;margin-bottom: 30px">
          <span style="margin-right: 60%">我的上传</span>
          <q-btn rounded color="blue" icon="upload">上传视频</q-btn>
        </div>
        <q-card
          class="my-card text-white"
          style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%); width: 80%; margin-left: auto; margin-right: auto;margin-bottom: 30px"
        >
          <q-card-section horizontal>
            <q-card-section>
              <q-video
                style="width: 200px;height: 150px;"
                src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
              />
            </q-card-section>

            <q-card-section style="margin-right: 150px">
              <div class="text-h6">学号：1234566</div>
              <div class="text-h6">上传者：jack</div>
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
    </div>
  </div>
</template>

<script>
import {defineAsyncComponent} from 'vue'
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));

export default {
  name: "PersonalUpload",
  components: {
    lineChart
  },
  data() {
    return  {
      imgUrl: 'https://cdn.quasar.dev/img/boy-avatar.png',
      alert: false,
      id: 12345678,
      name: 'jack london',
      teacher: '李红',
      course: '周三第四节',
      email: 'ca1312@163.com',
      editing : false
    }
  },
  methods : {
    edit(){
      this.editing = true
    },
    save(){
      this.editing = false
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
.info {
  width: 100%;
  margin-left: 20%;
  box-shadow: #1D1D1D;
}
.upload{
  width: 80%;
}
</style>
