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
<!--      <q-video-->
<!--        :ratio="16/9"-->
<!--        src="http://localhost:8080/api/video/get"-->
<!--      />-->
      <div style="width: 90%;margin-bottom: 20px">
        <q-carousel
          swipeable
          animated
          arrows
          v-model="slide"
          :fullscreen.sync="fullscreen"
          infinite
          height="300px"
        >
          <q-carousel-slide :name="1" img-src="../assets/1.webp" />
          <q-carousel-slide :name="2" img-src="../assets/2.webp" />
          <q-carousel-slide :name="3" img-src="../assets/3.webp" />
          <q-carousel-slide :name="4" img-src="../assets/4.webp" />
          <q-carousel-slide :name="5" img-src="../assets/1.jpg" />

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
      <video controls width="500" height="300" src="http://localhost:3000/api/videos/61ff6f3e38c71eb3be910a51" type="video/mp4"></video>
<!--      <q-uploader-->
<!--        url="http://localhost:8080/api/video/upload"-->
<!--        label="video"-->
<!--        field-name="video"-->
<!--        style="max-width: 300px"-->
<!--      />-->
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
                  上臂 {{evaluate.position[slide-1]}}<br>
                  <span class="text-warning">击球部位靠后</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  接/击球手臂角度<br>
                  {{evaluate.hitAngle[slide-1]}}/180<br>
                  <span class="text-warning">角度合适</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  手臂弯曲角度<br>
                  {{evaluate.armBendAngle[slide-1]}}/180<br>
                  <span class="text-warning">角度偏小</span>
                </div>
                <q-separator dark inset vertical/>
                <div class="col">
                  手臂与躯干角度<br>
                  {{evaluate.armAngle[slide-1][0]}},{{evaluate.armAngle[slide-1][1]}}/180<br>
                  <span class="text-warning">正常</span>
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="text-h4 q-pa-sm">下肢动作</div>
              <q-separator dark inset />
              <div class="text-h6 row text-center">
                <div class="col">
                  小腿与地面角度<br>
                  {{evaluate.legAngle[slide-1]}}/90<br>
                  <span class="text-warning">角度太小</span>
                </div>

                <q-separator dark inset vertical/>
                <div class="col">
                  大小腿弯曲角度<br>
                  {{evaluate.legBendAngle[slide-1]}}/180<br>
                  <span class="text-warning">正常</span>
                </div>

                <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
                <div class="col">
                  人跳起高度<br>
                  {{evaluate.height[slide-1]}}m<br>
                  <span class="text-warning">接球不应起跳</span>
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="fas fa-volleyball-ball" class="q-pa-sm"/>排球参数</div>
              <q-separator dark inset />
              <div class="row q-pa-md">
                <div class="text-h6 col text-center">
                  球的高度<br>{{evaluate.ballHeight[slide-1]}}m
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  球的运动方向<br>{{evaluate.ballAngle[slide-1]}}/90
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  球的运行速度<br>{{evaluate.speed[slide-1]}}m/s
                </div>
              </div>
            </q-card-section>

    <!--        <q-card-section>-->
    <!--          <div class="text-h4" style="text-align: center">老师评价</div>-->
    <!--          <q-separator dark inset />-->
    <!--          <div class="text-h5" style="margin-top: 20px;margin-bottom: 20px">评分： 85</div>-->
    <!--&lt;!&ndash;          <q-video&ndash;&gt;-->
    <!--&lt;!&ndash;            style="width: 60%;height: 300px;margin: 20px auto 10px auto"&ndash;&gt;-->
    <!--&lt;!&ndash;            src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"&ndash;&gt;-->
    <!--&lt;!&ndash;          />&ndash;&gt;-->
    <!--&lt;!&ndash;            <video controls width="500" height="400" src="http://localhost:8080/api/video/get/61ff6f3e38c71eb3be910a51" type="video/mp4"></video>&ndash;&gt;-->
    <!--        <div class="text-subtitle1">达拉克斯基的离开洒家的打开拉萨机立刻大家阿斯利康决定了空间啊滤镜老咔叽陈卡雷就拉开差距萨洛克插卡就是v出来的洒家扩大除了卡v就立刻数据来看v可垃圾啊v地理空间率考虑到了恐惧绿蜡卡拉居留卡v空间的v离开v拉开点距离看见立刻除了卡具v考虑阿娇v安洁丽卡v扩大距离v离开的v了恐惧v点卡v率的卡距离打开v就卡了大局来看v的恐惧啦v将来肯定是v建立打开吃撒吃撒从建立凯撒距离喀什滤镜啊v老咔叽定律v快乐大居留卡就 离开数据利空打击了v利空打击率及的角色v离开家</div>-->
    <!--        </q-card-section>-->
          </q-card>
        </q-tab-panel>
        <q-tab-panel name="summary">
          <q-card
            class="my-card text-white"
            style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
          >
            <q-card-section>
              <div class="text-h4 q-pa-sm"><q-icon name="fas fa-volleyball-ball" class="q-pa-sm"/>
                动作评估
                <q-btn label="发布评价" color="blue" @click="commentShow = true" align="right" rounded size="lg" style="margin-left: 400px"/>
              </div>
              <q-separator dark inset />
              <div class="row q-pa-md">
                <div class="text-h6 col text-center">
                  动作质量评估<br>{{quality[slide-1]}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作稳定性<br>{{stability[slide-1]}}
                </div>
                <q-separator dark inset vertical/>
                <div class="text-h6 col text-center">
                  动作准确性<br>{{accuracy[slide-1]}}
                </div>
              </div>
            </q-card-section>
          </q-card>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<script>
export default {
name: "Analysis",
  data() {
  return {
    evaluate: {
      stability: [48,45,68,56,64],
      accuracy: [80,78,79,81,92],
      quality: [70,56,67,73,63],
      position: [0.3,0.2,0.4,0.1,0.3],
      hitAngle: [60.3,65.4,100.8,123.1,119.2],
      armBendAngle: [50.1,90.8,67.8,98.2,123.1],
      armAngle: [[72.1,72.1],[67.5,66.5],[56.3,67.8],[78.9,89.7], [66.2,56.4]],
      legAngle: [78,64,67,75,51],
      legBendAngle: [155,164,145,111,145],
      height: [0.7,0.56,1.1,0.98,0.98],
      ballHeight:[3.6,2.4,2.3,2.1,2.8],
      ballAngle: [28,37,45,12,56],
      speed: [1.23,2.34,2.11,1.45,2.53]
    },
    slide: 1,
    fullscreen: false,
    commentShow: false,
    comment:'',
    rate: 0,
    tab: 'evaluate'
  }
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
    }
  }
}
</script>

<style scoped>

</style>
