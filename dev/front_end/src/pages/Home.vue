<template>
  <div class="row" style="width: 85%;margin-left: auto;margin-right: auto">
    <div class="personal-menu-card">
      <q-avatar size="280px">
        <img :src="this.imgUrl" alt="用户头像">
      </q-avatar>
      <div class="q-py-sm" style="margin-left: auto;margin-right: auto">
        <span class="text-weight-bold text-h4">{{ name }}</span>
      </div>
      <div class="q-py-sm" style="margin-left: auto;margin-right: auto">
        <span class="text-grey text-h5">{{ id }}</span>
      </div>
      <q-card class="info q-pa-md">
        <div class="text-h4 q-pb-md">
          <span>课程信息</span>
        </div>
        <template v-for="course of courses">
          <course-info-item :course="course"/>
        </template>
        <template v-if="courses.length !== courseIds.length">
          <div class="text-center">
            <q-btn @click="getCourseInfo" rounded icon-right="read_more" flat class="text-blue-7 text-weight-bold text-subtitle2">展 示 更 多 课 程</q-btn>
          </div>
        </template>

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
        <q-btn @click="isUpload=true" rounded color="blue" icon="upload" style="margin-right: 20px">上传视频</q-btn>
        <q-btn rounded color="blue" icon="read_more" to="/videos">更多</q-btn>
      </div>
      <div class="flex">
        <template v-for="video in videos">
          <video-item
            :time="video.createdAt"
            :video_id="video._id"
            :uploader_name="name"
            :uploader_id="id"
            style="width: 48%"/>
        </template>
      </div>
    </div>
  </div>
  <q-dialog v-model="isUpload">
    <q-uploader
      label="上传视频"
      auto-upload
      accept="mp4"
      @rejected="onRejected"
      @finish="isUpload=false;"
      @uploaded="onSuccess"
      @failed="onFail"
      :form-fields="[{name: 'id', value: this.userId}]"
      field-name="video"
      :url="getUrl"
    />
  </q-dialog>
</template>

<script>
import {defineAsyncComponent} from 'vue';
import { useQuasar } from 'quasar';
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));
const videoItem = defineAsyncComponent(() => import("components/VideoItem"));
const courseInfoItem = defineAsyncComponent(() => import("../components/courseInfoItem"))

const $q = useQuasar()
export default {
  name: "PersonalUpload",
  components: {
    lineChart,
    videoItem,
    courseInfoItem
  },
  data() {
    return  {
      imgUrl: 'https://cdn.quasar.dev/img/boy-avatar.png',
      alert: false,
      id: 123123123,
      name: 'cynic',
      college: 23,
      isUpload: false,
      courseIds: [],
      courses: [],
      email: 'ca1312@163.com',
      userId: this.$route.params.id,
      videos: []
    }
  },
  methods : {
    getUserInfo() {
      this.$api.get('api/user/'+this.userId)
      .then(res => {
        console.log(res)

        this.name = res.data.name;
        this.email = res.data.mail;
        this.id = res.data.id;
        this.college = res.data.college;
        this.videos = res.data.videos;
        this.courseIds = res.data.courses;
        this.getCourseInfo()
      })
    },
    getCourseInfo() {
      const courseId = this.courseIds[this.courses.length]
      this.$api.get('api/courses/'+courseId)
        .then(res => {
          this.courses.push(res.data)
          // console.log(this.course)
        })
    },
    getUrl() {
      return "http://localhost:3000/api/videos/upload";
    },
    onRejected () {
      this.$q.notify({
        type: 'negative',
        message: "文件未通过属性验证"
      })
    },
    onSuccess() {
      this.isUpload = false;
      this.$q.notify({
        type: 'positive',
        message: "成功上传视频",
        position: 'center'
      })
      this.getUserInfo()
    },
    onFail() {
      this.isUpload = false;
      this.$q.notify({
        type: 'negative',
        message: "文件上传失败",
        position: 'center'
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
