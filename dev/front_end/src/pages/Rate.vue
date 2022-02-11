<template>
  <div class="q-pa-md row" style="width: 100%">
    <div style="width: 10%;">
      <q-btn round icon="arrow_back" color="blue" size="lg" to="/stuvideolist"></q-btn>
    </div>
    <div style="width: 80%">
      <q-video
        :ratio="16/9"
        src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
      />
      <div>
        <span style="margin-right: 30px">学号：1234456</span>
        <span style="margin-right: 30px">姓名：张三</span>
        <span style="margin-right: 30px">上传时间：2020.08.06</span>
        <span>视频编号：123456789</span>
      </div>
      <div style="margin-top: 20px">
        <q-card bordered style="padding: 30px">
          <q-input rounded outlined v-model="rate" label="评分" style="width: 20%;margin-bottom: 30px"/>
          <q-input rounded outlined type="textarea" v-model="comment" label="评价"/>
          <q-btn rounded color="blue" size="lg" align="center" style="margin-top: 30px;margin-left: 40%">提交评价</q-btn>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Rate",
  data () {
    return {
      rate: '',
      comment: ''
    }
  }
}
</script>

<style scoped>

</style>
