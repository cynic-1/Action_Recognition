<template>
  <div>
    <div class="text-h6 text-grey">{{ semester }} <q-separator/></div>
    <div class="text-h5  q-pa-sm">课程时间：{{courseTime}}</div>
    <div class="text-h5  q-pa-sm">任课老师：{{teachers}}</div>
  </div>
</template>

<script>
const dayMap = ['零', '一', '二', '三', '四', '五', '六', '日']
const numberMap = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
const semMap = ['', '秋季学期', '春季学期']

export default {
  name: "courseInfoItem",
  props: {
    course: Object
  },
  computed: {
    semester() {
      return this.course.year + '年 ' + semMap[this.course.semester]
    },
    courseTime() {
      return ' 周' + dayMap[this.course.day] + '第' + numberMap[this.course.classNo] + '节';
    },
    teachers() {
      return this.course.teachers.reduce((sum, current) => sum + " " + current.name, "")
    }
  },
}
</script>

<style scoped>

</style>
