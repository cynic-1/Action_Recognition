<template>
  <q-layout view="hHh lpR fFf">

    <q-header v-ripple class="text-white" :class="classes" height-hint="150">
      <q-toolbar>


        <q-toolbar-title class="q-px-xl" shrink>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          XAI
        </q-toolbar-title>

        <q-tabs align="center"
                inline-label
                mobile-arrows
                dense
                active-color="grey-1"
                class="text-white">
          <q-route-tab to="/" label="Get Started" />
          <q-route-tab to="/analysis" label="Analysis" />
          <q-route-tab to="/class" label="Class" />
          <q-route-tab to="/course" label="Course" />
          <q-route-tab to="/student" label="Student" />
          <q-route-tab to="/stuvideolist" label="List" />
          <q-route-tab to="/rate" label="Rate" />
          <q-route-tab to="/register" label="Register" />
          <q-route-tab to="/login" label="Login" />
        </q-tabs>

      </q-toolbar>


    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white text-italic text-h5 text-center">

          XAI:  Make AI Explainable

    </q-footer>

  </q-layout>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const colors = [
  'primary', 'amber', 'secondary', 'orange', 'accent',
  'lime', 'cyan', 'purple', 'brown', 'blue'
]

export default {
  data () {
    return {
      left: false
    }
  },
  setup () {
    const color = ref(colors[ 0 ])
    const index = ref(0)

    let timer

    onMounted(() => {
      timer = setInterval(() => {
        index.value = (index.value + 1) % colors.length
        color.value = colors[ index.value ]
      }, 2000)
    })

    onBeforeUnmount(() => {
      clearTimeout(timer)
    })

    return {
      color,
      index,
      classes: computed(() => `bg-${color.value}`)
    }
  }
}
</script>
