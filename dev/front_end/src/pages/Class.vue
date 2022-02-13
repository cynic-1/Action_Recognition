<template>
  <div class="q-pa-md row items-start q-gutter-md" style="width: 80%;margin-left: auto;margin-right: auto;margin-top: 30px">
      <q-card class="my-card" v-for="item in course" :key="item">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">{{item.name}}</div>
          <div class="text-subtitle2">教师:{{item.teacher}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;总人数:{{item.num}}</div>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat to="/course"><span style="font-weight: bold">查看课程</span></q-btn>
          <q-btn flat to="/student"><span style="font-weight: bold">学生详情</span></q-btn>
        </q-card-actions>
      </q-card>
  </div>
</template>

<script>
export default {
  name: "Class",
  data(){
    return {
      course : [
        {name: "周三第四节", teacher: "李红", num: 45 },
        {name: "周三第五节", teacher: "李红", num: 43 },
        {name: "周三第六节", teacher: "李红", num: 42 },
        {name: "周三第七节", teacher: "李红", num: 43 },
        {name: "周四第四节", teacher: "李红", num: 45 },
        {name: "周四第五节", teacher: "李红", num: 44 },
        {name: "周四第六节", teacher: "李红", num: 47 },
        {name: "周四第七节", teacher: "李红", num: 40 },
        {name: "周四第八节", teacher: "李红", num: 43 },
      ]
    }
  }
}
</script>

<style scoped>
.my-card {
  width: 100%;
  max-width: 370px;
}
</style>
