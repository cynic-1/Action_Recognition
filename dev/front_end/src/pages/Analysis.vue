<template xmlns="http://www.w3.org/1999/html" class="bg-blue-6">
  <div class="row" style="width: 95%;margin:20px auto 20px auto">
    <div class="q-pa-md" style="width: 40%">
<!--      <q-video-->
<!--        :ratio="16/9"-->
<!--        src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"-->
<!--      />-->
      <q-uploader
        url="http://localhost:8080/api/video/upload"
        label="video"
        field-name="video"
        style="max-width: 300px"
      />

      <q-card
        class="my-card text-white"
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%);margin-top: 30px"
      >
        <q-card-section>
          <div class="text-h4 q-pa-sm"><q-icon name="fas fa-volleyball-ball" class="q-pa-sm"/>动作评估</div>
          <q-separator dark inset />
          <div class="row q-pa-md">
            <div class="text-h5 col text-center">
              动作质量评估<br>{{quality}}
            </div>
          </div>
          <div class="row q-pa-md">
            <div class="text-h5 col text-center">
              动作稳定性<br>{{stability}}
            </div>
            <div class="text-h5 col text-center">
              动作准确性<br>{{accuracy}}
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <div class="q-pa-md" style="width: 60%">
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
              1.0/3<br>
              <span class="text-warning">击球部位靠后</span>
            </div>
            <q-separator dark inset vertical/>
            <div class="col">
              接球角度<br>
              60.3/180<br>
            </div>
            <q-separator dark inset vertical/>
            <div class="col">
              击球角度<br>
              50.1/180<br>
              <span class="text-warning">接球角度偏小</span>
            </div>
            <q-separator dark inset vertical/>
            <div class="col">
              手臂与躯干角度<br>
              72.1/180<br>
              <span class="text-warning">正常</span>
            </div>
          </div>
        </q-card-section>

        <q-card-section>
          <div class="text-h4 q-pa-sm">下肢动作</div>
          <q-separator dark inset />
          <div class="text-h6 row text-center">
            <div class="col">
              接球姿势<br>
              1.0/3<br>
              <span class="text-warning">下蹲角度太小</span>
            </div>

            <q-separator dark inset vertical/>
            <div class="col">
              击球姿势<br>
              1.5/3.0<br>
            </div>

            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <div class="col">
              击球时起跳高度<br>
              0.7<br>
              <span class="text-warning">尝试更早起跳</span>
            </div>

            <q-separator dark inset vertical/>
            <div class="col">
              大腿与小腿弯曲角度<br>
              72.1/180<br>
              <span class="text-warning">正常</span>
            </div>

          </div>
        </q-card-section>

        <q-card-section>
          <div class="text-h4" style="text-align: center">正确示范</div>
          <q-separator dark inset />
          <q-video
            style="width: 60%;height: 300px;margin: 20px auto 10px auto"
            src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
export default {
name: "Analysis",
  data() {
  return {
    evaluate: {
      stability: 48,
      accuracy: 80,
      quality: 70
    },
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
