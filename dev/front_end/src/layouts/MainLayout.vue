<template>
  <q-layout view="hHh lpR fFf">

    <q-header v-ripple class="text-white bg-blue-8" height-hint="150">
      <q-toolbar>


        <q-toolbar-title class="q-px-xl" shrink>
          <q-avatar>
            <img src="http://www.buaa.edu.cn/__local/B/CD/A6/968D8F6600C0B8195CD59008BF5_9249A080_12AB7.jpg?e=.jpg" alt="北京航空航天大学">
          </q-avatar>
          北航智慧排球教学系统
        </q-toolbar-title>

        <q-tabs align="center"
                inline-label
                mobile-arrows
                dense
                active-color="grey-1"
                class="text-white">
<!--          <q-route-tab to="/" label="Get Started" />-->
          <q-route-tab :to="'/home/'+userId" label="个人中心" />
          <q-route-tab to="/analysis" label="动作分析" />
<!--          <q-route-tab to="/class" label="课程" />-->
          <q-route-tab to="/class" label="班级详情" />
          <q-route-tab to="/course" label="课程详情" />
          <q-route-tab to="/student" label="学生管理" />
          <q-route-tab to="/videos" label="视频列表" />
<!--          <q-route-tab to="/rate" label="Rate" />-->
<!--          <q-route-tab to="/register" label="Register" />-->
          <q-route-tab to="/login" label="登录/注册" />
        </q-tabs>

      </q-toolbar>


    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white text-italic text-h5 text-center">

            智慧排球: 见所未见

    </q-footer>

  </q-layout>
</template>

<script>
import { computed } from 'vue'


export default {
  data () {
    return {
      left: false
    }
  },
  setup () {

    return {
      userId: computed(() => sessionStorage.getItem('userId'))
    }
  }
}
</script>
