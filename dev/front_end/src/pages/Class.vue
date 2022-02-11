<template>
  <div class="q-pa-md row items-start q-gutter-md" style="width: 80%;margin-left: auto;margin-right: auto;margin-top: 30px">
      <q-card class="my-card" v-for="x in 9" :key="x">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">周三第四节</div>
          <div class="text-subtitle2">教师:李红&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;总人数:45</div>
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
  name: "Class"
}
</script>

<style scoped>
.my-card {
  width: 100%;
  max-width: 370px;
}
</style>
