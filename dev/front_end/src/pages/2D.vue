<template>
  <div>
<!--    <canvas id="myCanvas" width="200" height="200"></canvas>-->
    <div id="draw-shapes">
    </div>
  </div>
</template>

<script>
import Two from "two.js";
export default {
  name: "2D",
  mounted() {
    // this.drawLine()
    this.two()
  },
  methods : {
    // drawLine() {
    //   /*获取元素*/
    //   let myCanvas = document.querySelector('#myCanvas');
    //   /*获取绘图工具*/
    //   let ctx = myCanvas.getContext('2d');
    //   ctx.beginPath();
    //   ctx.moveTo(75, 50);
    //   ctx.lineTo(100, 75);
    //   ctx.lineTo(100, 25);
    //   ctx.closePath()
    //   ctx.stroke()
    // },
    two(){
      let elem = document.getElementById('draw-shapes');/*原生的JS代码 取到你所创建的Div*/
      let params = { width: 400, height: 400}; //设置二维空间的宽高
      let two = new Two(params).appendTo(elem); //新建一个在div中的二维空间
      let left_leg_up = two.makeLine(20,20,20,60);
      let left_leg_down = two.makeLine(20,60,40,75);
      let circle = two.makeCircle(-70, 0, 50);

      left_leg_up.fill = '#FFD31C';//填充色
      left_leg_down.fill = '#FFD31C';//填充色
      let left_leg = two.makeGroup(left_leg_up, left_leg_down);
      left_leg.position.set(two.width / 2, two.height / 2);
      two.update();
    }
  }
}
</script>

<style scoped>

</style>
