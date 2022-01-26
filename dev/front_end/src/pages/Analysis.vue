<template xmlns="http://www.w3.org/1999/html">
  <div class="row" style="width: 95%;margin:20px auto 20px auto">
    <div class="q-pa-md" style="width: 40%">
      <q-video
        :ratio="16/9"
        src="https://www.youtube.com/embed/6x73pRYlJ8Y?rel=0"
      />

      <q-card
        class="my-card text-white"
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%);margin-top: 30px"
      >
        <q-card-section>
          <div class="text-h4" style="text-align: center">动作评估</div>
          <q-separator dark inset />
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="margin-left: 20%;margin-right: 20%">稳定性: 19</span>
            <span>准确度：23</span>
          </div>
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="margin-left: 20%;margin-right: 20%">出界率: 19</span>
            <span>接球率：23</span>
          </div>
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="margin-left: 20%;margin-right: 20%">出界率: 19</span>
            <span>接球率：23</span>
          </div>
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="margin-left: 20%;margin-right: 20%">出界率: 19</span>
            <span>接球率：23</span>
          </div>
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="margin-left: 20%;margin-right: 20%">出界率: 19</span>
            <span>接球率：23</span>
          </div>
          <div class="text-h5 row"  style="width: 90%;margin-left: auto;margin-right: auto">
            <span style="margin-left: 20%;margin-right: 20%">稳定性: 19</span>
            <span>准确度：23</span>
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
          <div class="text-h4" style="text-align: center">上肢动作</div>
          <q-separator dark inset />
          <div class="text-h6 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="width: 20%">
              击球部位<br>
              1.0/3<br>
              <span style="font-size: small;color: orange">击球部位靠后</span>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              接球角度<br>
              60.3/180<br>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              击球角度<br>
              50.1/180<br>
              <span style="font-size: small;color: orange">接球角度偏小</span>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              手臂与躯干角度<br>
              72.1/180<br>
              <span style="font-size: small;color: orange">正常</span>
            </span>
          </div>
        </q-card-section>

        <q-card-section>
          <div class="text-h4" style="text-align: center">下肢动作</div>
          <q-separator dark inset />
          <div class="text-h6 row"  style="width: 90%;margin-left: auto;margin-right: auto;margin-bottom: 20px">
            <span style="width: 20%">
              接球姿势<br>
              1.0/3<br>
              <span style="font-size: small;color: orange">下蹲角度太小</span>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              击球姿势<br>
              <br>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              击球时起跳高度<br>
              0.7<br>
              <span style="font-size: small;color: orange">尝试更早起跳</span>
            </span>
            <q-separator dark inset vertical style="margin-left: 5px;margin-right: 5px"/>
            <span style="width: 20%">
              大腿与小腿弯曲角度<br>
              72.1/180<br>
              <span style="font-size: small;color: orange">正常</span>
            </span>
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
name: "Analysis"
}
</script>

<style scoped>

</style>
