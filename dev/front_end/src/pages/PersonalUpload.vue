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
        </q-card-section>f
      </q-card>
    </div>
    <div class="row">
      <div>
        <q-card class="info q-pa-md">
          <div class="text-h4">
            课程信息
            <q-btn rounded icon="more" flat class="text-right text-h5">更多</q-btn>
          </div>
          <div class="text-h5 text-grey">当前课程：{{course}}</div>
          <div class="text-h5 text-grey">任课老师：{{teacher}}</div>
        </q-card>
      </div>
      <div class="upload">
        <div class="text-h4 text-grey row width-80-center q-mb-lg">
          <span style="margin-right: 60%">我的上传</span>
          <q-btn rounded color="blue" icon="upload">上传视频</q-btn>
        </div>
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
      id: 123123123,
      name: 'cynic',
      college: 23,
      course: "",
      email: 'ca1312@163.com',
      userId: this.$route.params.id
    }
  },
  methods : {
    getUserInfo() {
      let courseId;
      this.$api.get('api/user/'+this.userId)
      .then(res => {
        this.name = res.data.name;
        this.email = res.data.mail;
        this.id = res.data.id;
        this.college = res.data.college;
        courseId = res.data.courses[res.data.courses.length-1]
        console.log(courseId)
        this.$api.get('api/course/'+courseId)
        .then(res => {
          this.course = res.data;
          console.log(this.course)
        })
      })
    }
  },
  created() {
    this.getUserInfo()
  }


}
</script>

<style scoped>
.personal-menu-card {
  width: 100%;
  padding-bottom: 40px;
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
