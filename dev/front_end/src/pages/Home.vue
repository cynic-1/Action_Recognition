<template>
  <div class="row" style="width: 85%;margin-left: auto;margin-right: auto">
    <div class="personal-menu-card">
      <q-avatar size="280px">
        <img :src="this.imgUrl" alt="用户头像">
      </q-avatar>
      <div class="q-py-sm" style="margin-left: auto;margin-right: auto">
        <span class="text-weight-bold text-h4">姓名--{{ name }}</span>
      </div>
      <div class="q-py-sm" style="margin-left: auto;margin-right: auto">
        <span class="text-grey text-h5">学号--{{ id }}</span>
      </div>
      <q-card class="info q-pa-md">
        <div class="text-h4 row">
          <span>课程信息</span>
          <q-btn rounded icon-right="read_more" flat class="text-right text-subtitle2">查看更多</q-btn>
        </div>
        <div class="text-h5 text-grey" style="margin: 20px">当前课程：{{courseTime}}</div>
        <div class="text-h5 text-grey" style="margin: 20px">任课老师：{{teachers}}</div>
      </q-card>
    </div>

    <div class="upload">
      <q-card>
        <q-card-section vertical>
          <line-chart/>
        </q-card-section>
      </q-card>
      <div class="text-h5 text-grey row q-mb-lg" style="margin-top: 20px">
        <span style="margin-right: 60%">我的上传</span>
        <q-btn rounded color="blue" icon="upload" style="margin-right: 20px">上传视频</q-btn>
        <q-btn rounded color="blue" icon="read_more" to="/videos">更多</q-btn>
      </div>
      <div class="row">
        <video-item style="width: 48%;margin-right: 2%"/>
        <video-item style="width: 48%"/>
      </div>
    </div>
  </div>
</template>

<script>
import {defineAsyncComponent} from 'vue'
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));
const videoItem = defineAsyncComponent(() => import("components/VideoItem"));

const dayMap = ['零', '一', '二', '三', '四', '五', '六', '日']
const numberMap = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
const semMap = ['', '秋季学期', '春季学期']
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
      course: {
        year: 2022,
        semester: 1,
        day: 3,
        classNo: 4,
        teachers: [{
          _id: "62020090fc4badc851a96a99",
          name: "梁秀英"
        }
        ]
      },
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
        this.$api.get('api/courses/'+courseId)
        .then(res => {
          this.course = res.data;
          console.log(this.course)
        })
      })
    },
  },
  computed: {
    courseTime() {
      return this.course.year + '年 ' + semMap[this.course.semester] + ' 周 ' + dayMap[this.course.day] + ' 第 ' + numberMap[this.course.classNo] + '节';
    },
    teachers() {
      return this.course.teachers.reduce((sum, current) => sum + current.name, "")
    }
  },
  created() {
    this.getUserInfo()

  }


}
</script>

<style scoped>
.personal-menu-card {
  width: 25%;
  padding: 30px;
}
.info {
  margin-top: 30px;
  width: 100%;
  box-shadow: #1D1D1D;
}
.upload{
  width: 75%;
  margin-top: 30px;
}
/*.width-80-center {*/
/*  width: 80%; margin-left: auto; margin-right: auto;*/
/*}*/
</style>
