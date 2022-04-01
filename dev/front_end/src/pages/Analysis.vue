<template xmlns="http://www.w3.org/1999/html" class="bg-blue-6">
  <q-dialog v-model="commentShow" >
    <q-card bordered style="padding: 30px;width: 700px; max-width: 80vw;">
      <q-input rounded outlined v-model="rate" label="评分" style="width: 50%;margin-bottom: 30px"/>
      <q-input rounded outlined type="textarea" v-model="comment" label="评价"/>
      <q-btn rounded color="blue" size="lg" align="center" style="margin-top: 30px;margin-left: 40%">提交评价</q-btn>
    </q-card>
  </q-dialog>
  <div class="row" style="width: 95%;margin:20px auto 20px auto">
    <div class="q-pa-md" style="width: 40%">
      <div style="margin-bottom: 20px">
        <q-carousel
          swipeable
          animated
          arrows
          v-model="slide"
          :fullscreen.sync="fullscreen"
          infinite
          style="height: 300px; width: 533px;"
          class="no-padding"
        >
          <template v-for="(keyPoint,index) of keyPoints">
            <q-carousel-slide :name="index+1" class="no-padding">
              <q-img :ratio="16/9" style="height: 300px" :src="`http://localhost:3000/api/keyPoints/${keyPoint._id}/image`"/>
            </q-carousel-slide>
          </template>

          <template v-slot:control>
            <q-carousel-control
              position="top-right"
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
      <video controls width="533" height="300" :src="'http://localhost:3000/api/videos/'+videoId" type="video/mp4"></video>
    </div>

    <div class="q-pa-md" style="width: 60%">
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="blue"
        indicator-color="blue"
        align="justify"
        narrow-indicator
      >
        <q-tab name="evaluate" label="技术分析" />
        <q-tab name="summary" label="总体分析" />
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="evaluate">
          <q-card
            class="my-card text-white"
            style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
          >
            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="fas fa-hands" class="q-pa-sm"/>上肢动作</div>
              <q-separator dark inset />
              <div class="text-h6 row text-center">
                <div class="col">
                  击球部位<br>
                  上臂 {{currentKeyPoint.upper.hitPosition || "-"}}<br>
                  <span class="text-warning">击球部位靠后</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  接/击球手臂角度<br>
                  {{currentKeyPoint.upper.hitAngle}} / 180<br>
                  <span class="text-warning">角度合适</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  手臂弯曲角度<br>
                  {{currentKeyPoint.upper.angleForearmArm || "-"}} / 180<br>
                  <span class="text-warning">角度偏小</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  手臂与躯干角度<br>
                  {{currentKeyPoint.upper.angleArmTrunk || "-"}} / 180<br>
                  <span class="text-warning">正常</span>
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="directions_walk" size="xl" class="q-pa-sm"/>下肢动作</div>
              <q-separator dark inset />
              <div class="text-h6 row text-center">
                <div class="col">
                  小腿与大腿角度<br>
                  {{currentKeyPoint.lower.angleCalfThigh || "-"}} / 90<br>
                  <span class="text-warning">角度太小</span>
                </div>

                <q-separator dark inset vertical/>
                <div class="col">
                  大腿与躯干角度<br>
                  {{currentKeyPoint.lower.angleThighTrunk || "-"}} / 180<br>
                  <span class="text-warning">正常</span>
                </div>

                <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
                <div class="col">
                  人跳起高度<br>
                  {{currentKeyPoint.lower.jumpHeight || 0}} m<br>
                  <span class="text-warning">接球不应起跳</span>
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="fas fa-volleyball-ball" class="q-pa-sm"/>排球参数</div>
              <q-separator dark inset />
              <div class="row q-pa-md">
                <div class="text-h6 col text-center">
                  球的高度<br>{{currentKeyPoint.ball.lastHeight || "-"}} cm
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  球的初始角度<br>{{currentKeyPoint.ball.initialAngle || "-"}} / 90
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  球的运行速度<br>{{currentKeyPoint.ball.initialVelocity || "-"}} m/s
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="star_rate" size="xl" class="q-pa-sm"/>
                动作评估
              </div>
              <q-separator dark inset />
              <div class="row q-pa-md">
                <div class="text-h6 col text-center">
                  动作质量评估<br>{{currentKeyPoint.rate}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作协调性<br>{{currentKeyPoint.coordination}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作准确性<br>{{currentKeyPoint.accuracy}}
                </div>
              </div>
            </q-card-section>
          </q-card>
        </q-tab-panel>
        <q-tab-panel name="summary">
          <q-card
            class="my-card text-white"
            style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
          >
            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="star_rate" size="xl" class="q-pa-sm"/>
                动作评估
                <q-btn label="发布评价" color="blue" @click="commentShow = true" align="right" rounded size="lg" style="margin-left: 400px"/>
              </div>
              <q-separator dark inset />
              <div class="row q-pa-md">
                <div class="text-h6 col text-center">
                  动作质量评估<br>{{currentKeyPoint.rate}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作协调性<br>{{currentKeyPoint.coordination}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作准确性<br>{{currentKeyPoint.accuracy}}
                </div>
              </div>
            </q-card-section>
            <q-card-section>
              <polar-bar-chart v-if="flag"/>
              <radar-chart/>
            </q-card-section>
          </q-card>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<script>
import polarBarChart from "components/polarBarChart";
// import radarChart from "components/RadarChart";
export default {
  name: "Analysis",
  components: {
    polarBarChart,
    // radarChart,
  },
  data() {
    return {
      keyPoints: [{
        "imgLoc": "1.jpg",
        "data": {
          "upper": {
            "hitPosition": "\u672a\u63a5\u7403",
            "hitAngle": 116.45272702462493,
            "angleForearmArm": null,
            "angleArmTrunk": 0
          },
          "lower": {
            "angleCalfThigh": 173.41078210585206,
            "angleThighTrunk": 173.73855214289523,
            "jumpHeight": 0
          },
          "ball": {
            "lastHeight": 313.3058668814066,
            "initialAngle": null,
            "initialVelocity": null
          },
          "coordination": 90,
          "accuracy": 80,
          "rate": 85
        }
      },],
      videoId: "",
      slide: 1,
      fullscreen: false,
      commentShow: false,
      comment:'',
      rate: 0,
      tab: 'evaluate',
      angles: [158.2 , 81.5, 127.8, 135.7, 102.85],
      flag: true,
    }
  },
  methods: {
    getKeyPoints() {
      this.$api.get("/api/videos/"+this.videoId+"/keyPoints")
      .then(res => {
        this.keyPoints = res.data.keyPoints
        console.log(res.data)
      })
      .catch(err => {
        console.log(err)
      })
    },
    getVideoId() {
      this.videoId = this.$route.params.id
    },
  },
  computed: {
    quality() {
      return this.evaluate.quality > 100 ? 100 : this.evaluate.quality < 0 ? 0 : this.evaluate.quality;
    },
    stability() {
      return this.evaluate.stability > 100 ? 100 : this.evaluate.stability < 0 ? 0 : this.evaluate.stability;
    },
    accuracy() {
      return this.evaluate.accuracy > 100 ? 100 : this.evaluate.accuracy < 0 ? 0 : this.evaluate.accuracy;
    },
    currentKeyPoint() {
      return this.keyPoints[this.slide-1].data
    },
  },
  created() {
    this.getVideoId()
    this.getKeyPoints()
  }
}
</script>

