<template>
  <div class="row" style="width: 85%;margin-left: auto;margin-right: auto">
    <div class="personal-menu-card">
      <div class="my-father cursor-pointer">
        <q-avatar size="280px" @click="toggleIsUploadAvatar" class="my-avatar">
          <img :src="this.imgUrl" alt="用户头像">
        </q-avatar>
        <div class="my-element text-center text-h6 text-weight-medium text-white">更 换 头 像</div>
      </div>
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
        <q-btn @click="toggleIsUpload" rounded color="blue" icon="upload" style="margin-right: 20px">上传视频</q-btn>
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
      @finish="toggleIsUpload"
      @uploaded="onSuccess"
      @failed="onFail"
      :form-fields="[{name: 'id', value: this.userId}]"
      field-name="video"
      :url="getUrl"
    />
  </q-dialog>
    <my-upload field="img"
               @crop-success="cropSuccess"
               @crop-upload-success="cropUploadSuccess"
               @crop-upload-fail="cropUploadFail"
               v-model="isUploadAvatar"
               :width="300"
               :height="300"
               :url="`http://localhost:3000/api/user/${userId}/avatar/upload`"
               :params="params"
               :headers="headers"
               img-format="png">

    </my-upload>
</template>

<script>
import {defineAsyncComponent} from 'vue';
import { useQuasar } from 'quasar';
import myUpload from 'vue-image-crop-upload/upload-3'
const lineChart = defineAsyncComponent(() => import("../components/LineChart"));
const videoItem = defineAsyncComponent(() => import("components/VideoItem"));
const courseInfoItem = defineAsyncComponent(() => import("../components/courseInfoItem"))

const $q = useQuasar()
export default {
  name: "PersonalUpload",
  components: {
    lineChart,
    videoItem,
    courseInfoItem,
    myUpload
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
      videos: [],
      isUploadAvatar: false,
      params: {
        token: '123456798',
        name: 'avatar'
      },
      headers: {
        smail: '*_~'
      },
      imgDataUrl: ''
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
    },
    cropSuccess(imgDataUrl, field){
      console.log('-------- crop success --------');
      this.imgDataUrl = imgDataUrl;
    },
    /**
     * upload success
     *
     * [param] jsonData   服务器返回数据，已进行json转码
     * [param] field
     */
    cropUploadSuccess(jsonData, field){
      console.log('-------- upload success --------');
      console.log(jsonData);
      console.log('field: ' + field);
    },
    /**
     * upload fail
     *
     * [param] status    server api return error status, like 500
     * [param] field
     */
    cropUploadFail(status, field){
      console.log('-------- upload fail --------');
      console.log(status);
      console.log('field: ' + field);
    },
    toggleIsUpload() {
      this.isUpload = !this.isUpload
    },
    toggleIsUploadAvatar() {
      this.isUploadAvatar = !this.isUploadAvatar
    },
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
.my-element {
  display: none;
  width: 160px;
  height: 2em;
  border-radius: 10px;
  background-color: black;
  position: relative;
  margin-left: 60px;
}
.my-element::before {
  position: absolute;
  top: -20px;
  left: 70px;
  content: '';
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-bottom: 10px solid black;
  border-left: 10px solid transparent;
  border-top: 10px solid transparent;
}
.my-father:hover .my-element {
  display: block;
}

</style>
