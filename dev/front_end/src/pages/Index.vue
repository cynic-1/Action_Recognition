<template>
  <q-page>
    <div class="q-px-xl" style="">
      <q-carousel
        animated
        v-model="slide"
        infinite
        :autoplay="autoplay"
        thumbnails
        transition-prev="slide-right"
        transition-next="slide-left"
        v-model:fullscreen="fullscreen"
        @mouseenter="autoplay = false"
        @mouseleave="autoplay = true"
      >
        <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
        <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg" />
        <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/parallax2.jpg" />
        <q-carousel-slide :name="4" img-src="https://cdn.quasar.dev/img/quasar.jpg" />
        <template v-slot:control>
          <q-carousel-control
            position="bottom-right"
            :offset="[18, 18]"
          >
            <q-btn
              push round dense color="white" text-color="primary"
              :icon="fullscreen ? 'fullscreen_exit' : 'fullscreen'"
              @click="fullscreen = !fullscreen"
            />
          </q-carousel-control>
        </template>
      </q-carousel>
    </div>
    <div class="q-pa-xl">
      <div class="row q-px-xl">
        <div class="col">
          <q-card flat bordered="false" class="row">
            <q-icon name="android" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
        <div class="col">
          <q-card flat bordered="false" class="row">
            <q-icon name="psychology" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
        <div class="col">
          <q-card flat bordered="false" class="row">
            <q-icon name="rocket" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
      </div>
    </div>
    <div class="q-pa-lg">
      <span class="text-h4 text-blue-grey-6 row">
        Framework
      </span>
      <div class="row q-pa-md">
        <q-img src="~assets/summary.png"/>
      </div>
    </div>
    <div class="q-pa-lg">
      <span class="text-h4 text-blue-grey-6 row">
        Framework
      </span>
      <div class="row q-pa-md">
        <div class="col q-pa-md">
          <q-card class="row shadow-6">
            <q-icon name="android" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
        <div class="col q-pa-md">
          <q-card class="row shadow-6">
            <q-icon name="psychology" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
        <div class="col q-pa-md">
          <q-card class="row shadow-6">
            <q-icon name="rocket" size="7em" class="q-mx-auto text-blue-5"/>
            <span class="text-h5 text-primary text-center">
              Comprehensive Datasets and Unified Data Structures
            </span>
            <span class="text-h6 text-center">
              LibCity provides 35 spatio-temporal datasets
              and introduces unified data structures to format representations of datas and the input of algorithms.
            </span>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  "name": 'PageIndex',
  data () {

    return {
      "slide": 1,
      "autoplay": true,
      "fullscreen": false
    };

}
});
</script>
