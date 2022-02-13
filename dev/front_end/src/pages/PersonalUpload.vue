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
    </div>
    <div class="row">
      <div>
        <q-card class="info q-pa-md">
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
        <div class="text-h4 text-grey row width-80-center q-mb-lg">
          <span style="margin-right: 60%">我的上传</span>
          <q-btn rounded color="blue" icon="upload">上传视频</q-btn>
        </div>
<!--        <q-card-->
<!--          class="my-card text-white"-->
<!--          style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%); width: 80%; margin-left: auto; margin-right: auto;margin-bottom: 30px"-->
<!--        >-->
<!--          <q-card-section horizontal>-->
<!--            <q-card-section>-->
<!--              <video controls width="500" height="300" src="http://localhost:3000/api/video/get/61ff6f3e38c71eb3be910a51" type="video/mp4"></video>-->

<!--            </q-card-section>-->

<!--            <q-card-section style="margin-right: 10%">-->
<!--              <div class="text-h6">学号：1234566</div>-->
<!--              <div class="text-h6">上传者：jack</div>-->
<!--              <div class="text-subtitle2">授课老师：李红</div>-->
<!--              <div class="text-subtitle2">上传时间：2021.7.6</div>-->
<!--              <div class="text-subtitle2">视频编号：123456789</div>-->
<!--              <div class="text-subtitle2">视频评分：80</div>-->
<!--            </q-card-section>-->

<!--            <q-card-section>-->
<!--              <q-btn size="lg" icon-right="arrow_forward" style="margin-top: 80px" to="/analysis">查看分析</q-btn>-->
<!--            </q-card-section>-->
<!--          </q-card-section>-->
<!--        </q-card>-->
        <div class="width-80-center">
          <video-item/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {defineAsyncComponent} from 'vue'
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));
const videoItem = defineAsyncComponent(() => import("components/VideoItem"));
export default {
  name: "PersonalUpload",
  components: {
    lineChart,
    videoItem
  },
  data() {
    return  {
      imgUrl: 'https://cdn.quasar.dev/img/boy-avatar.png',
      alert: false,
      id: 19231061,
      name: '宋永欣',
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
  width: 75%;
}
.width-80-center {
  width: 80%; margin-left: auto; margin-right: auto;
}
</style>
